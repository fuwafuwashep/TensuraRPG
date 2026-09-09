# Run-specific state only. Catalogs live in data/ and are never mutated in play.
default world_state = {"schema": 0, "flags": {}, "history": [], "event_details": {}, "legacy_events": [], "phase": 0, "characters": {}, "discoveries": [], "visits": {}, "choices": {}, "battles": [], "skill_sources": {}, "endings": []}
default current_location = None
default navigation_active = False
default in_battle = False
default learned_skills = []
define config.load_failed_label = "recover_legacy_save"

init -20 python:
    import renpy.store as store

    # Compatibility with original cave/quest labels and old saves.
    LEGACY_FLAGS = {
        "met_veldora": "met_veldora", "veldora_in_stomach": "veldora_in_stomach",
        "met_goblins": "goblin_meeting_seen", "village_access": "goblin_village_unlocked",
        "injured_goblins_healed": "injured_goblins_healed",
        "helped_goblins": "helped_goblins", "goblins_destroyed": "goblins_destroyed",
        "wolves_control_village": "wolves_control_village",
        "direwolf_leader_defeated": "direwolf_leader_defeated",
        "goblin_arc_complete": "goblin_arc_complete",
    }
    LEGACY_EVENTS = ("met_veldora", "veldora_in_stomach", "met_goblins",
                     "injured_goblins_healed", "direwolf_leader_defeated", "goblin_arc_complete")

    def world_flag(key):
        if key in LEGACY_FLAGS:
            return bool(getattr(store, LEGACY_FLAGS[key], False))
        return bool(store.world_state["flags"].get(key, False))

    def set_world_flag(key, value=True):
        store.world_state["flags"][key] = bool(value)
        if key in LEGACY_FLAGS:
            setattr(store, LEGACY_FLAGS[key], bool(value))

    def has_event(event_id):
        return event_id in store.world_state["history"] or event_id in store.world_state["legacy_events"]

    def event_index(event_id):
        # None deliberately means unknown, including pre-migration history.
        history = store.world_state["history"]
        return history.index(event_id) if event_id in history else None

    def event_before(first, second):
        a, b = event_index(first), event_index(second)
        return a is not None and b is not None and a < b

    def record_event(event_id, variant="default", details=None):
        if has_event(event_id):
            return False
        store.world_state["history"].append(event_id)
        entry = {"variant": variant, "location": store.current_location, "phase": store.world_state["phase"]}
        entry.update(details or {})
        store.world_state["event_details"][event_id] = entry
        set_world_flag(event_id)
        return True

    def character_state(character_id):
        return store.world_state["characters"].get(character_id, {})

    def meet_character(character_id, recruited=False):
        data = dict(character_state(character_id))
        data.update({"met": True, "alive": data.get("alive", True)})
        if recruited:
            data["recruited"] = True
        store.world_state["characters"][character_id] = data

    def character_location(character_id):
        data = character_state(character_id)
        if not data.get("alive", True):
            return None
        if "location" in data:
            return data["location"]
        for placement in CHARACTER_DATA.get(character_id, {}).get("locations", []):
            if conditions_met(placement.get("when", {})):
                return placement["location"]
        return None

    def character_present(character_id, location=None):
        location = store.current_location if location is None else location
        return location is not None and character_location(character_id) == location

    def has_skill(skill_id):
        return bool(getattr(store, skill_id, skill_id in store.learned_skills))

    def conditions_met(rule):
        """Declarative AND; nest any/all/not for alternatives. No eval or lambdas."""
        for key, value in rule.items():
            if key == "all":
                ok = all(conditions_met(part) for part in value)
            elif key == "any":
                ok = any(conditions_met(part) for part in value)
            elif key == "not":
                ok = not conditions_met(value)
            elif key == "events":
                ok = all(has_event(e) for e in value)
            elif key == "no_events":
                ok = all(not has_event(e) for e in value)
            elif key == "flags":
                ok = all(world_flag(k) == v for k, v in value.items())
            elif key == "phase_min":
                ok = store.world_state["phase"] >= value
            elif key == "phase_max":
                ok = store.world_state["phase"] <= value
            elif key == "locations":
                ok = store.current_location in value
            elif key == "items":
                ok = all(item_count(k) >= v for k, v in value.items())
            elif key == "skills":
                ok = all(has_skill(k) for k in value)
            elif key == "met":
                ok = all(character_state(k).get("met", False) for k in value)
            elif key == "alive":
                ok = all(character_state(k).get("alive", True) for k in value)
            elif key == "present":
                ok = all(character_present(k) for k in value)
            elif key == "recruited":
                ok = all(character_state(k).get("recruited", False) for k in value)
            elif key == "bosses":
                ok = all(world_flag(k + "_defeated") for k in value)
            elif key == "relationships":
                ok = all(relationship_value(c, stat) >= minimum for c, stats in value.items() for stat, minimum in stats.items())
            elif key == "choices":
                ok = all(store.world_state["choices"].get(k) == v for k, v in value.items())
            elif key == "before":
                ok = all(event_before(a, b) for a, b in value)
            elif key == "power_min":
                ok = store.player_max_hp >= value
            elif key == "power_max":
                ok = store.player_max_hp <= value
            elif key == "discovered":
                ok = all(k in store.world_state["discoveries"] for k in value)
            elif key == "battle_turn_min":
                ok = store.in_battle and store.battle_turn >= value
            elif key == "enemy_hp_max":
                ok = store.in_battle and store.enemy_hp <= value
            elif key == "player_hp_max":
                ok = store.in_battle and store.player_hp <= value
            else:
                raise ValueError("Unknown condition: " + key)
            if not ok:
                return False
        return True

    def apply_effects(effects):
        # Validate all costs before making any mutation.
        if any(item_count(key) < -amount for key, amount in effects.get("items", {}).items() if amount < 0):
            return False
        for key, value in effects.get("flags", {}).items():
            set_world_flag(key, value)
        for key, value in effects.get("items", {}).items():
            add_item(key, value) if value > 0 else remove_item(key, -value)
        for skill in effects.get("skills", []):
            learn_skill(skill, "event")
        for character in effects.get("met", []):
            meet_character(character)
        for character in effects.get("recruited", []):
            meet_character(character, True)
        for character, delta in effects.get("relationships", {}).items():
            change_relationship(character, **delta)
        store.world_state["choices"].update(effects.get("choices", {}))
        if "phase" in effects:
            store.world_state["phase"] = max(store.world_state["phase"], effects["phase"])
        return True

    def migrate_game_state():
        if store.world_state["schema"] < 1:
            # Import quantities exactly once. Legacy counters become mirrors.
            for item_id, variable in LEGACY_ITEMS.items():
                store.inventory[item_id] = max(0, int(getattr(store, variable, 0)))
            old_events = list(LEGACY_EVENTS) + [key + "_defeated" for key in ENEMY_DATA if getattr(store, key + "_defeated", False)]
            for event_id in old_events:
                if getattr(store, event_id, False):
                    set_world_flag(event_id)
                if world_flag(event_id) and not has_event(event_id):
                    store.world_state["legacy_events"].append(event_id)
            if world_flag("met_veldora"):
                meet_character("veldora")
            if world_flag("met_goblins"):
                meet_character("rigurd")
            if world_flag("goblins_destroyed"):
                for key in ("haruna", "rigurd"):
                    store.world_state["characters"][key] = dict(character_state(key), alive=False)
                store.world_state["choices"]["goblin_defence"] = "refused"
            if world_flag("goblin_arc_complete"):
                meet_character("ranga", True)
                store.world_state["phase"] = max(1, store.world_state["phase"])
            store.world_state["schema"] = 1
        sync_skill_moves()

label after_load:
    $ migrating_legacy_save = world_state["schema"] < 1
    $ migrate_game_state()
    $ renpy.block_rollback()
    if migrating_legacy_save:
        jump recover_legacy_save
    return

label recover_legacy_save:
    $ migrate_game_state()
    $ renpy.reset_all_contexts()
    python:
        # reset_all_contexts also clears Ren'Py's per-context menu markers.
        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
    $ in_battle = False
    $ navigation_active = False
    $ player_hp = max(1, player_hp)
    scene black
    n "This older save resumes at a nearby exploration landmark. Rimuru's progression and inventory have been kept."
    $ renpy.block_rollback()
    if current_region == "West_Jura":
        $ enter_location(current_location if current_location in LOCATIONS else "crossroads")
        jump explore_location
    elif armorsaurus_defeated:
        jump veldora_cave_exit
    elif chasm_thread_unlocked:
        jump part2_final_branch
    elif met_veldora:
        jump cave_branch_2
    else:
        jump cave_start
