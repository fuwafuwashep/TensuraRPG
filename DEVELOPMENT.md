# Playing and extending Tensura RPG

Open this existing project in the Ren'Py 8.5.3 launcher and choose **Launch
Project**. **Start** plays the original opening/cave. In development mode,
**Test West Jura** starts at the forest edge with Mana Perception and Water
Manipulation. It is a new game and does not overwrite a manual save slot.

## Quick playable route

1. From the forest edge, go forward and gather roadside berries.
2. Go right and challenge the Horn Rabbit. Water Blade costs MP; Items consume
   a turn. Predate can consume a living enemy below 100 HP. Basic Attack remains
   available when other resources are exhausted. Rest at the cave entrance or
   village to restore HP, MP and move uses.
3. Return to the crossroads, then take the goblin trail. Meeting the patrol
   before or after the rabbit gives a different event variant/reward.
4. Enter the village, talk to Haruna, and give the berries. Relationships shows
   Trust and Romance independently. Gifting stays friendly unless Rimuru
   explicitly expresses romantic interest during a local conversation.
5. Heal the injured goblins in the command tent with a Healing Blob. Help or
   refuse Rigurd to follow the original village branches. Naming evolves
   Telepathy into Thought Communication. Trusted villagers can then help in battle.

For sequence testing, the crossroads' western ravine can be surveyed with Mana
Perception and crossed using Steel Thread or Water Manipulation. The prototype
Orc Lord is deliberately dangerous. The ogre settlement on the outer forest loop
offers optional meeting/recruitment events before or after the boss. **Status**
shows ordered history and any unlocked prototype epilogues; viewing one does not
end exploration. **Debug** can teleport, give items, learn skills, adjust
relationships, set flags, record events, test battles, and restore resources.

Debug entry points and mutation helpers require `config.developer`. Ren'Py's
normal distribution build disables developer mode; do not force it on for a
release. Tests/development artifacts are excluded from distributions.

## Where content belongs

| Content | Authority |
| --- | --- |
| World progression, conditions, history, migration | `game/core/state.rpy` |
| Item definitions / owned quantities and use | `game/data/items.rpy` / `game/core/inventory.rpy` |
| Character presence, stages and gates | `game/data/character_data.rpy` |
| Gift preferences / relationship changes | `game/data/gifts.rpy` / `game/core/relationships.rpy` |
| Region nodes / navigation loop | `game/data/locations.rpy` / `game/core/navigation.rpy` |
| Events, variants, endings / event execution | `game/data/story_events.rpy` / `game/core/story_events.rpy` |
| Dialogue | Existing cave/West Jura labels and `game/story/` |
| Enemies / moves and loadouts | Existing `game/battle_system.rpy` / `game/skills.rpy` |
| Encounter policies, progression, skill metadata | `game/core/battle_integration.rpy` |
| Optional panels / development tools | `game/ui/rpg_screens.rpy` / `game/ui/debug.rpy` |
| Engine tests and catalog validation | `game/tests/engine_tests.rpy` / `game/core/validation.rpy` |

The original cave labels remain usable and keep their authored backgrounds.
West Jura's original movement label names are compatibility entrances to the new
navigation loop. New regions should use location definitions, not duplicate that
loop. The existing `ENEMY_DATA` and `MOVE_DATA` remain the single enemy/move
catalogs; there is no competing battle system or inventory.

## Catalog contracts

Define catalogs during init and treat them as read-only during play. Keep mutable
run state in Ren'Py `default` variables. Use the helpers from labels or explicit
screen actions; screen rendering/prediction must not grant rewards or sync skills.
Use `renpy.random` for gameplay randomness so rollback remains consistent.

A location has `title`, `background`, `description`, and `actions`. An action has
a stable `id`, `text`, and `kind`. Supported kinds are `exit`, `label`, `gather`,
`battle`, `npc`, `event`, `rest`, and `discover`. The catalog includes constructors
`path`, `scene_action`, `resource`, `fight`, and `forest_node` for common cases.
`visible_when` hides an action; `when` leaves it visible but disables it. A
location's first matching `variants` entry supplies a complete replacement view.
Add a registered background or use an existing explicitly marked placeholder.

Conditions are an AND of their keys; nest `all`, `any`, and `not` for alternatives.
Supported keys are `events`, `no_events`, `flags`, `phase_min`, `phase_max`,
`locations`, `items`, `skills`, `met`, `alive`, `present`, `recruited`, `bosses`,
`relationships`, `choices`, `before`, `power_min`, `power_max`, and `discovered`.
Battle rules additionally support `battle_turn_min`, `enemy_hp_max`, and
`player_hp_max`. `power_min/max` currently measures maximum HP. For example:

```python
{"events": ["ogres_met"],
 "any": [{"skills": ["steel_thread"]}, {"skills": ["water_manipulation"]}],
 "relationships": {"haruna": {"trust": 20}},
 "before": [("kijin_recruited", "orc_lord_defeated")]}
```

Events specify `title`, optional `location`, `when`, a scene `label`, optional
`priority`, optional `automatic`, `variants`, and `effects`. Variants are ordered;
the first eligible one wins. Scene labels accept `(variant)` and return `True`
to complete or `False` to cancel. Effects support `flags`, item quantity deltas,
`skills`, `met`, `recruited`, relationship deltas, `choices`, and monotonically
increasing `phase`. Negative item costs are checked together before applying
effects. Base and variant item/relationship deltas add; other dictionaries merge.
Keep rewards in effects so a scene cannot accidentally grant them twice.

`record_event(id, variant, details)` records only the first occurrence. The full
battle log records every battle. `has_event`, `event_index`, and `event_before`
query progression; an old save's unknown sequence is never invented. `ENDINGS`
entries use the same conditions and a title/summary. Current ending scenes are
short optional epilogues, leaving room for full authored endings later.

Items declare name, description, category, stackability, optional `gift`, and
optional `use` HP/MP restoration. Quantities live only in `inventory`. Call
`add_item`, `remove_item`, `item_count`, or `use_item`; five old counters are
migration mirrors, never an independent inventory. Predator can refine Hipokute
into a Healing Blob from Inventory outside battle.

Characters use ordered conditional `locations` placements, optional sprite,
individual `stages`, and `romance_gates` tuples `(cap, required_trust, event_id)`.
An explicit per-run character `location` overrides placements; `alive=False`
removes the character from local interactions. Romanceable characters have only
Trust and Romance. Story-only characters have Trust alone. Romantic intent and
gift history are separate flags/history, not additional relationship scores.
Gift preferences select `early`, `middle`, `late`, or `default` reactions, with
individual Trust/Romance deltas and optional text. Positive repeated-gift gains
diminish. Unwritten personal-event gates deliberately prevent completing routes
whose scenes have not been authored.

An encounter references an existing enemy and may override `can_run`,
`run_chance`, `predator`, `defeat`, `retreat`, and `defeat_label`. Defeat supports
retreat, rescue, capture, or game over. `end_conditions` is an ordered list of
`when`/`result` rules checked after a completed turn. Normalized outcomes are
`victory`, `defeat`, `escape`, `special_victory`, and `alternate_victory`; outcome
`effects` connect them to story state. Original callers still receive
`won`/`lost`/`ran`. Enemy metadata supplies speed, drops and XP. Skill metadata
can grant new moves/immunities through `learn_skill(id, source)`; original skill
flags and move-effect implementations remain supported.

## Repeatable validation and save handling

From this project in PowerShell:

```powershell
& 'C:\Users\Fuwa\Downloads\renpy-8.5.3-sdk\lib\py3-windows-x86_64\python.exe' tools\run_checks.py 'C:\Users\Fuwa\Downloads\renpy-8.5.3-sdk'
```

The runner copies scripts/assets into `.checkpoints/test-project`, preserving
compiled statement IDs when available. It runs lint with dynamic reference
checks and the actual Ren'Py `slice` UI tests, then saves reports/screenshots in
`test-results`. Its test windows exit automatically. A second positional argument
can specify an older `.save` file to copy for the optional legacy recovery test.
Without that fixture the legacy-file case does no work; the synthetic migration
test still runs. Never run the suite directly in a player's working project:
Ren'Py also writes `game/saves` even when `--savedir` points elsewhere.

Schema 0 saves import legacy quantities/flags once, preserve unknown event order,
and resume at a safe cave landmark or forest crossroads. This resets obsolete
mid-scene/battle contexts. Current schema saves preserve the current battle turn,
HP/MP, inventory, loadout, relationships and event history. Rollback is blocked
across the load/migration boundary and works during subsequent play.

The verified run passed all 17 cases and 121 test-language assertions, including
an actual September 2 pre-upgrade save, plus Python invariants. Original save
backups and pre-refactor source are in the ignored `.checkpoints` folder. The
work has not been committed; the initial user edits remain part of the working
tree. New art, permanent dialogue, additional towns, complete romance routes,
and final balance are future content work.
