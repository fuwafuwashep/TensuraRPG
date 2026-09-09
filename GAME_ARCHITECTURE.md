# Tensura RPG architecture

## Phase 0: repository audit (2026-09-07)

The local working tree is the implementation baseline. It already contained user
edits in Veldoras_Cave.rpy, West_Jura.rpy, battle_system.rpy, battle_menu.rpy and
skills.rpy. Those changes include the Armorsaurus exit, explicit battle returns,
Steel Strength acquisition, and Telepathy evolving during naming; preserve them.

Inspected all twelve gameplay/UI/config .rpy files, the generated common
translation, asset inventory, SVG command button, Git changes, and crash logs.
The supplied novel collection is reference material, not project instructions.

### Existing reusable systems

- `script.rpy` / `cutscenes.rpy`: Rimuru's opening and cave entry.
- `Veldoras_Cave.rpy`: complete branching cave, perception-dependent images,
  one-time herbs/ore, Veldora encounter, resistance acquisition, six monsters,
  chasm traversal and exit. Keep the labels and images.
- `West_Jura.rpy`: mapped forest loop, orchards, side trails, six ordinary
  monsters, goblin healing/defence/naming, refusal destroying the village, and
  several explicitly unfinished region boundaries. Keep routes and scenes.
- `battle_system.rpy`: central ENEMY_DATA, shared single-enemy turn loop,
  Predator, damage/status/resistance effects, legacy won/lost/ran returns.
- `skills.rpy`: MOVE_DATA, categorized loadout, limited uses, skill grants and
  evolution. Retain these authorities instead of introducing another move model.
- `battle_menu.rpy`: original SVG command layout, sprite positions and categories.
- `exploration_ui.rpy`: storage, skills and equipment screens.
- `screens.rpy`, `gui.rpy`, `options.rpy`: 1920x1080 VN interface and standard
  Ren'Py save/load/preferences. Keep the save directory unchanged.
- Assets: 16 cave backgrounds, Veldora, Rimuru battle sprite, Thunder Frog,
  original command SVG and stock GUI. West Jura already uses Solid placeholders.

### Confirmed debt / baseline validation

Ren'Py 8.5.3 SDK is installed locally. Baseline lint identifies two percent-format
errors in battle dialogue; logs also show a Predator percent-format crash.
HP resets on every battle; Stomach cannot use items; status lacks bars/resources;
battle artwork disappears during attack narration. Screen evaluation mutates
skill/loadout state, which can re-equip moves removed by the player. Speed flags
currently have no combat effect. Region logic repeats movement/encounter handling.
Five counters act as inventory. There is no relationship/event/ending engine,
ordered story history, schema migration, or development panel.

Existing branches are present in source and compile, but full playability must
be established with runtime checks, not inferred from lint alone.

## Implementation architecture

- `core/state.rpy`: save-owned structured state, compatibility aliases,
  idempotent migration, ordered history (unknown legacy order stays unknown),
  character presence and a shared declarative condition evaluator.
- `data/items.rpy` / `core/inventory.rpy`: one item catalog and one quantity
  store, migrate the existing counters once; all gameplay uses the same helpers.
- `data/character_data.rpy`, `data/gifts.rpy`, `core/relationships.rpy`: exactly
  Trust and Romance, per-character stages/preferences, opt-in romantic intent,
  local NPC interactions and reusable reactions. Future character entries are
  content-disabled, not globally available NPCs.
- `core/story_events.rpy` / `data/story_events.rpy`: eligibility, prioritized
  variants, completion effects, choices/history and ending evaluation.
- `core/navigation.rpy` / `data/locations.rpy`: full-screen VN backgrounds,
  conditional/hidden exits, resources, enemies, NPCs and story actions. West Jura
  label names remain compatibility entries; existing story labels are reused.
- `core/battle_integration.rpy`: encounter policies, persistent HP/MP, rewards,
  speed, ally assistance and normalized outcome history around the existing loop.
  Existing callers still receive won/lost/ran.
- `ui/rpg_screens.rpy`, `ui/debug.rpy`: optional inventory/relationships/status,
  local interaction menus and developer-only tools. Battle HUD is separate.
- `story/slice_events.rpy`: short, explicitly provisional dialogue demonstrating
  sequence changes, personal-event gates and an early boss. No new chapters.

State is declared with `default`; init catalogs are read-only during play.
All interactions remain Ren'Py labels/screens, not Python dialogue loops.
No persistent data holds run-specific progression. Screens only read state;
actions/labels perform mutations. New-game and after-load migration share one
idempotent path. Older saves resume at an exploration landmark after migration:
the forest crossroads or the nearest supported cave milestone. They retain
inventory, original skill flags, loadout and quest progression, but deliberately
discard an obsolete mid-scene/mid-battle call stack. Newly created saves retain
their exact exploration or battle position. Unknown legacy event order remains
unknown. This recovery was tested with an actual pre-upgrade save; compatibility
with every historical script version is not guaranteed.

## Implementation and validation order

1. Repair known crashes; establish state, inventory, migration and conditions.
2. Add relationships, gifts, story variants and ending definitions.
3. Connect West Jura navigation and original cave/quest entry points.
4. Integrate battle resources, items, outcomes, progression and presentation.
5. Add optional menus, developer tools and minimal demonstration scenes.
6. Run lint, catalog/reference checks and actual Ren'Py integration tests for
   cave entry, navigation, battle, gifts, sequence breaking, save/load and rollback.

Each phase is checked before proceeding. No existing image is deleted or renamed.
Balance values and new dialogue are provisional. Future towns and romance routes
remain data extension points, not claims of completed content.

## Delivered slice and verification

Implemented the layers above while retaining the original cave scenes, forest
story scenes, enemy/move catalogs, command-button asset and every existing image.
West Jura movement labels now delegate to 36 location definitions, including the
original forest loop, unfinished region boundaries, and three prototype western
locations. The normal route supports gathering, combat, local talk/gifting,
village defence or refusal, optional relationship/status menus, and save/load.

The prototype Orc Lord is accessible using perception and traversal skills,
without meeting Shizue or recruiting the kijin. The first victory records who
was recruited at the time; later recruitment cannot rewrite that history.
Ogre dialogue/alliance choices, aftermath state and optional epilogues differ
with that order. New dialogue, missing sprites/backgrounds and boss balance are
explicitly provisional. Haruna/Rigurd have local interactions; the other V1
characters have data support, while complete character routes are still unwritten.

Validated on Windows with Ren'Py 8.5.3:

- Lint and dynamic catalog/reference checks passed with no warnings.
- 17 engine test cases and 121 test-language assertions passed, plus the Python
  invariant assertions inside `state_contracts`.
- Runtime coverage: cave opening and exit via Veldora/chasm/Armorsaurus; original
  goblin healing, defence, naming and refusal; forest gather and rematches;
  MP/item consumption; defeat, escape and alternate victory; before/after-alliance
  boss branches; gift/relationship persistence; actual gather and gift rollback;
  mid-battle save/load; an actual older save; developer and optional menus.
- Screenshots were reviewed at 1920×1080. Existing cave art and Rimuru are reused;
  missing art displays named placeholders. No mobile packaging/performance or
  comprehensive combat/romance balancing pass has been performed.

Tests run in `.checkpoints/test-project` through `tools/run_checks.py`, isolating
both Ren'Py save locations. The first direct test run exposed Ren'Py's mirroring
into `game/saves` despite `--savedir`; local original saves were restored from the
untouched roaming save directory. Both copies were backed up in
`.checkpoints/save-recovery`, and an original slot's SHA256 was verified.
Subsequent tests never run against the playable project's save directories.

The pre-refactor source checkpoint is `.checkpoints/phase0/game`. Existing user
edits are preserved and the work remains uncommitted for review. See
`DEVELOPMENT.md` for play routes, catalog contracts and the repeatable check command.
