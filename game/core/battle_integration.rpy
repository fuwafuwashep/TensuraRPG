default player_mp = 100
default player_max_mp = 100
default player_attack = 0
default player_defense = 0
default player_speed = 10
default player_level = 1
default player_experience = 0
default player_resistances = {}
default player_immunities = []
default active_encounter = None
default last_battle_outcome = None
default battle_turn = 0
default enemy_acted_this_round = False

init 2 python:
    # Encounters may override the same enemy's story/defeat/escape behaviour.
    ENCOUNTERS = {
        "forest_rabbit": {"enemy": "horn_rabbit", "defeat": "retreat", "retreat": "crossroads"},
        "direwolf_defence": {"enemy": "direwolf_leader", "predator": False, "can_run": False, "defeat": "rescue"},
        "orc_lord": {"enemy": "orc_lord", "can_run": True, "run_chance": 0.8, "defeat": "retreat", "retreat": "ravine", "boss": True},
    }
    ENEMY_DATA["orc_lord"] = {
        "name": "Orc Lord (prototype)", "max_hp": 1400, "run_chance": 0.8,
        "sprite": None, "background": "west_jura_battle", "perception": True,
        "physical_resistance": True, "grants": [], "speed": 13, "boss": True,
        "moves": [{"name": "Cleaving Strike", "type": "physical", "min": 70, "max": 95, "accuracy": 0.95},
                  {"name": "Ravenous Blow", "type": "physical", "min": 65, "max": 85, "accuracy": 0.9, "drain": True}],
    }
    for enemy_id, definition in ENEMY_DATA.items():
        definition.setdefault("speed", 9)
        definition.setdefault("drops", {"hipokute": 1})
        definition.setdefault("xp", 25)
    ENEMY_DATA["horn_rabbit"]["drops"] = {"berries": 1}
    ENEMY_DATA["orc_lord"]["xp"] = 200
    ENEMY_DATA["orc_lord"]["drops"] = {"magicule_tonic": 2}
    for move_name, definition in MOVE_DATA.items():
        definition["mp_cost"] = 0 if move_name in ("Basic Attack", "Predate") else 5 if definition["damage"] == 0 else 8
    SKILL_DATA = {}
    for skill_id, display_name in dict(SKILL_NAMES, mana_perception="Mana Perception", telepathy="Telepathy", water_manipulation="Water Manipulation", heat_resistance="Heat Resistance", cold_resistance="Cold Resistance", electricity_resistance="Electricity Resistance", paralysis_resistance="Paralysis Resistance").items():
        category = "Unique" if skill_id in ("great_sage", "predator") else "Resistance" if skill_id.endswith("resistance") else "Extra" if skill_id in ("mana_perception", "thought_communication", "keen_smell", "danger_sense") else "Intrinsic"
        SKILL_DATA[skill_id] = {"name": display_name, "category": category}
    SKILL_CATEGORIES = ("Intrinsic", "Common", "Extra", "Unique", "Magic", "Physical", "Aura", "Resistance", "Nullification")

    def learn_skill(skill_id, source="event"):
        if skill_id not in SKILL_DATA:
            return False
        gained = not has_skill(skill_id)
        if gained:
            if hasattr(store, skill_id):
                grant_skill(skill_id)
            else:
                store.learned_skills.append(skill_id)
            for immunity in SKILL_DATA[skill_id].get("immunities", []):
                if immunity not in store.player_immunities:
                    store.player_immunities.append(immunity)
            for move in SKILL_DATA[skill_id].get("moves", []):
                unlock_move(move)
            store.world_state["skill_sources"][skill_id] = source
        return gained

    def battle_resolution(policy):
        for rule in policy.get("end_conditions", []):
            if conditions_met(rule["when"]):
                return rule["result"]
        return None

    def restore_player():
        store.player_hp = store.player_max_hp
        store.player_mp = store.player_max_mp
        reset_move_uses()

    def effective_player_speed():
        return store.player_speed + (5 if store.battle_turn == 1 and (store.danger_sense or store.shadow_motion) else 0)

    def enemy_goes_first():
        speed = store.enemy_data.get("speed", 9)
        if store.enemy_speed_reduced:
            speed = max(1, speed // 2)
        return speed > effective_player_speed()

    def battle_status_text(side):
        labels = {"poisoned": "Poison", "burned": "Burn", "skip_turn": "Held", "restrained": "Restrained"}
        result = [label for key, label in labels.items() if getattr(store, side + "_" + key, False)]
        if side == "enemy" and getattr(store, "enemy_speed_reduced", False):
            result.append("Slowed")
        return " / ".join(result) or "Ready"

    def available_battle_allies():
        if not store.thought_communication:
            return []
        return [c for c, data in CHARACTER_DATA.items() if data.get("assist") and character_state(c).get("met") and character_state(c).get("alive", True) and not world_flag("goblins_destroyed") and relationship_value(c, "trust") >= data["assist"]["trust"] and world_flag("goblin_arc_complete")]

    def battle_assistance():
        allies = available_battle_allies()[:3]
        store.battle_allies = [CHARACTER_DATA[c]["name"] for c in allies]
        healing = sum(CHARACTER_DATA[c]["assist"].get("heal", 0) for c in allies)
        actual = min(healing, store.player_max_hp - store.player_hp)
        store.player_hp += actual
        return actual

    def record_battle_result(enemy_id, result, policy):
        outcome = {"won": "victory", "lost": "defeat", "ran": "escape"}.get(result, result)
        if outcome == "victory" and store.last_battle_predated and store.last_predation_efficiency == 1.0:
            outcome = "special_victory"
        # Data hooks can recognize nonstandard resolutions without changing callers.
        for alternate in policy.get("outcomes", []):
            if result in alternate.get("results", ["won"]) and conditions_met(alternate["when"]):
                outcome = alternate["outcome"]
                break
        won = outcome in ("victory", "special_victory", "alternate_victory")
        details = {"enemy": enemy_id, "outcome": outcome, "location": store.current_location,
                   "turns": store.battle_turn, "kijin_recruited": world_flag("kijin_recruited"),
                   "met_shizue": world_flag("met_shizue"), "power": store.player_max_hp}
        store.world_state["battles"].append(details)
        store.last_battle_outcome = outcome
        if won:
            set_world_flag(enemy_id + "_defeated")
            if hasattr(store, enemy_id + "_defeated"):
                setattr(store, enemy_id + "_defeated", True)
            variant = "canon"
            if enemy_id == "orc_lord" and not has_event("orc_lord_defeated"):
                early = not world_flag("kijin_recruited")
                set_world_flag("orc_lord_early", early)
                set_world_flag("orc_lord_before_shizue", not world_flag("met_shizue"))
                variant = "before_kijin" if early else "before_shizue" if not world_flag("met_shizue") else "canon"
                if store.player_max_hp >= 700:
                    variant = "overleveled"
                if early and not world_flag("met_shizue"):
                    details["missing_allies"] = True
            record_event(enemy_id + "_defeated", variant, details)
            for item_id, count in ENEMY_DATA[enemy_id].get("drops", {}).items():
                add_item(item_id, count)
            store.player_experience += ENEMY_DATA[enemy_id].get("xp", 25)
            while store.player_experience >= store.player_level * 75:
                store.player_experience -= store.player_level * 75
                store.player_level += 1
                store.player_max_hp += 20
                store.player_hp += 20
                store.player_max_mp += 5
                store.player_mp = min(store.player_max_mp, store.player_mp + 5)
                store.player_attack += 2
        apply_effects(policy.get("effects", {}).get(outcome, {}))
        return "won" if won else "lost" if outcome == "defeat" else "ran"

label battle_enemy(enemy_key, predator_allowed=True, encounter_id=None):
    $ migrate_game_state()
    $ active_encounter = encounter_id
    $ encounter_policy = dict(ENCOUNTERS.get(encounter_id, {}))
    $ battle_predator_allowed = encounter_policy.get("predator", predator_allowed)
    $ in_battle = True
    $ battle_turn = 0
    $ battle_allies = [CHARACTER_DATA[c]["name"] for c in available_battle_allies()[:3]]
    call battle_enemy_turns(enemy_key, battle_predator_allowed)
    $ battle_final_result = record_battle_result(enemy_key, _return, encounter_policy)
    hide screen battle_stage
    hide screen battle_stomach_menu
    hide screen battle_allies_menu
    $ in_battle = False
    $ active_encounter = None
    if battle_final_result == "lost":
        $ defeat_behavior = encounter_policy.get("defeat", "retreat")
        if defeat_behavior == "game_over":
            n "Rimuru cannot recover from this battle."
            $ renpy.full_restart()
        elif defeat_behavior == "capture":
            $ set_world_flag("captured")
            n "Rimuru is captured. The outcome has been recorded."
        elif defeat_behavior == "rescue":
            n "Your allies pull you to safety."
        else:
            n "Rimuru retreats to recover."
        $ player_hp = max(1, player_max_hp // 2)
        if encounter_policy.get("retreat"):
            $ enter_location(encounter_policy["retreat"])
        if encounter_policy.get("defeat_label"):
            call expression encounter_policy["defeat_label"]
    return battle_final_result
