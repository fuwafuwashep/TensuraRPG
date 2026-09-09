# Engine integration tests. Distribution exclusions are at the end of this file.

testsuite slice:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False, save=False)
        assert screen "main_menu" timeout 5.0

    testcase navigation_gift:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        click id "forward"
        assert eval current_location == "crossroads"
        click id "crossroads_berries"
        advance until screen "location_choices"
        assert eval item_count("berries") == 1
        click "Inventory"
        assert screen "storage_menu"
        screenshot "inventory.png"
        click "Close"
        click id "forward"
        advance until screen "location_choices"
        assert eval has_event("met_goblins")
        assert eval world_state["event_details"]["met_goblins"]["variant"] == "cave_arrival"
        click id "village"
        assert eval current_location == "village"
        screenshot "village.png"
        click id "npc_haruna"
        advance until screen "npc_choices"
        click "Talk"
        advance until screen "npc_choices"
        click "Give Gift"
        click "Berry Bundle"
        advance until screen "npc_choices"
        assert eval item_count("berries") == 0
        assert eval relationship_value("haruna", "trust") == 7
        assert eval relationship_value("haruna", "romance") == 0
        click "Leave"
        advance until screen "location_choices"
        click "Relationships"
        screenshot "relationships.png"
        click "Close"
        click "Debug"
        screenshot "debug.png"
        click "Close"
        run Function(renpy.save, "slice-roundtrip")
        run Function(add_item, "berries", 9)
        run Function(change_relationship, "haruna", 20)
        run Function(set_world_flag, "save_probe", True)
        run Function(renpy.load, "slice-roundtrip")
        assert eval current_location == "village" timeout 5.0
        assert eval item_count("berries") == 0
        assert eval relationship_value("haruna", "trust") == 7
        assert eval not world_flag("save_probe")
        assert eval world_state["history"].count("first_gift_haruna") == 1

    testcase cave_start:
        run Start()
        advance until screen "choice"
        assert eval current_region == "Veldoras_Cave"
        screenshot "cave.png"

    testcase battle_items_and_variant:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        click id "forward"
        click id "right"
        click id "fight_horn_rabbit"
        advance until screen "battle_command_menu"
        assert eval in_battle
        assert eval not renpy.get_screen("rpg_toolbar")
        screenshot "battle.png"
        click "FIGHT"
        click "MAGIC"
        click "Water Blade"
        advance until screen "battle_command_menu"
        assert eval player_mp == 92
        assert eval enemy_hp == 100
        assert eval player_hp < player_max_hp
        click "ITEMS"
        screenshot "battle_items.png"
        click "Use"
        advance until screen "battle_command_menu"
        assert eval item_count("healing_blob") == 0
        click "FIGHT"
        click "MAGIC"
        click "Water Blade"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "SKILLS"
        click "Predate"
        advance until screen "location_choices"
        assert eval not in_battle
        assert eval not renpy.get_screen("battle_stage")
        assert eval last_battle_outcome == "special_victory"
        assert eval has_skill("danger_sense")
        assert eval item_count("berries") == 1
        click id "back"
        click id "forward"
        advance until screen "location_choices"
        assert eval world_state["event_details"]["met_goblins"]["variant"] == "forest_hunter"
        assert eval event_before("horn_rabbit_defeated", "met_goblins")
        assert eval item_count("healing_blob") == 1

    testcase state_contracts:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        python:
            assert validate_game_catalogs() == []
            assert set(relationships) == set()
            add_item("trail_note", 5)
            assert item_count("trail_note") == 1
            assert not remove_item("berries", 1)
            assert not use_item("healing_blob")
            assert not apply_effects({"items": {"berries": -1, "stuffed_animal": 1}})
            assert item_count("stuffed_animal") == 0
            before = item_count("healing_blob")
            migrate_game_state()
            migrate_game_state()
            assert item_count("healing_blob") == before
            unequip_move("Water Blade")
            sync_skill_moves()
            get_equipped_moves("magic")
            assert not move_is_equipped("Water Blade")
            unequip_move("Basic Attack")
            assert move_is_equipped("Basic Attack")
            old_physical = list(battle_physical_moves)
            battle_physical_moves.clear()
            assert "Basic Attack" in get_equipped_moves("physical")
            battle_physical_moves.extend(old_physical)
            assert not event_before("missing", "also_missing")
            record_event("test_first")
            record_event("test_second")
            assert event_before("test_first", "test_second")
            assert not record_event("test_first")
            set_world_flag("village_access")
            enter_location("village")
            meet_character("haruna")
            change_relationship("haruna", romance=100)
            assert relationship_value("haruna", "romance") == 0
            change_relationship("haruna", trust=60, romance=100)
            assert relationship_value("haruna", "romance") == 20
            record_event("haruna_personal")
            change_relationship("haruna", romance=100)
            assert relationship_value("haruna", "romance") == 55
            record_event("haruna_courtship")
            change_relationship("haruna", trust=25, romance=100)
            assert relationship_value("haruna", "romance") == 100
            change_relationship("veldora", trust=4, romance=20)
            assert set(relationships["veldora"]) == {"trust"}
            assert gift_preview("benimaru", "strategy_book")["trust"] > gift_preview("benimaru", "stuffed_animal")["trust"]
            assert conditions_met({"all": [{"events": ["test_first"]}, {"any": [{"skills": ["water_manipulation"]}, {"items": {"berries": 9}}]}], "locations": ["village"], "alive": ["haruna"], "present": ["haruna"], "met": ["haruna"], "relationships": {"haruna": {"trust": 60}}, "phase_min": 0, "phase_max": 1, "power_min": 300, "power_max": 500})
            set_world_flag("goblins_destroyed")
            assert not character_present("haruna")
            assert location_view("village")["background"] == "west_jura_wolf_den"
            player_immunities.append("electric")
            assert reduce_player_damage_for_resistance(50, "electric") == 0
            player_resistances["heat"] = 1.0
            assert reduce_player_damage_for_resistance(50, "heat") == 0
            enter_location("ravine")
            assert not any(a["id"] == "cross" for a in location_actions("ravine"))
            set_world_flag("ravine_surveyed")
            assert resolve_location_action("cross") is not None

    testcase rollback_gather:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        click id "forward"
        click id "crossroads_berries"
        assert eval item_count("berries") == 1
        run Rollback()
        assert screen "location_choices" timeout 5.0
        assert eval item_count("berries") == 0
        assert eval not world_flag("crossroads_berries")
        assert eval not has_event("gathered_berries")
        click id "crossroads_berries"
        advance until screen "location_choices"
        assert eval item_count("berries") == 1

    testcase early_boss:
        run Start("test_early_boss_setup")
        advance until screen "location_choices"
        click id "perception"
        advance until screen "location_choices"
        click id "cross"
        click id "fight_orc_lord"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "choice"
        click "Leave the monster"
        advance until screen "location_choices"
        assert eval world_flag("orc_lord_defeated")
        assert eval world_flag("orc_lord_early")
        assert eval not world_flag("kijin_recruited")
        assert eval not world_flag("met_shizue")
        click id "event_orc_aftermath"
        advance until screen "location_choices"
        assert eval "independent_forest" in eligible_endings()
        run Function(enter_location, "ogre_border")
        run Jump("explore_location")
        click id "event_ogres_met"
        advance until screen "location_choices"
        assert eval world_state["choices"]["ogre_alliance"] == "reconstruction"
        click id "event_kijin_recruited"
        advance until screen "location_choices"
        assert eval event_before("orc_lord_defeated", "kijin_recruited")
        assert eval world_flag("orc_lord_early")

    testcase defeat_and_escape:
        run Start("test_defeat_setup")
        advance until screen "location_choices"
        assert eval last_battle_outcome == "defeat"
        assert eval current_location == "crossroads"
        assert eval player_hp == player_max_hp // 2
        assert eval not world_flag("horn_rabbit_defeated")
        assert eval not in_battle
        run Jump("test_escape_setup")
        advance until screen "battle_command_menu"
        click "RUN"
        advance until screen "location_choices"
        assert eval last_battle_outcome == "escape"
        assert eval not world_flag("horn_rabbit_defeated")
        assert eval not renpy.get_screen("battle_stage")

    testcase battle_save_load:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        click id "forward"
        click id "right"
        click id "fight_horn_rabbit"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "MAGIC"
        click "Water Blade"
        advance until screen "battle_command_menu"
        run Function(renpy.save, "battle-roundtrip")
        run SetVariable("player_mp", 0)
        run SetVariable("enemy_hp", 1)
        run Function(renpy.load, "battle-roundtrip")
        assert screen "battle_command_menu" timeout 5.0
        assert eval enemy_hp == 100
        assert eval player_mp == 92
        assert eval battle_turn == 2
        assert eval in_battle
        click "FIGHT"
        click "MAGIC"
        click "Water Blade"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "SKILLS"
        click "Predate"
        advance until screen "location_choices"
        assert eval len(world_state["battles"]) == 1
        assert eval world_state["history"].count("horn_rabbit_defeated") == 1

    testcase legacy_migration:
        run Start("test_legacy_setup")
        advance until screen "location_choices"
        assert eval item_count("berries") == 4
        assert eval item_count("healing_blob") == 6
        assert eval has_event("met_veldora")
        assert eval has_event("horn_rabbit_defeated")
        assert eval event_index("met_veldora") is None
        assert eval not event_before("met_veldora", "met_goblins")
        run Function(remove_item, "berries", 2)
        run Function(migrate_game_state)
        assert eval item_count("berries") == 2

    testcase cave_to_forest:
        run Start()
        advance until screen "choice"
        run SetVariable("player_attack", 1000)
        click "Go left"
        click "Go right"
        click "Go forward"
        advance until screen "choice"
        click "Absorb the mineral"
        advance until screen "choice"
        click "Move forward"
        advance until screen "choice"
        click "Absorb the mineral"
        advance until screen "choice"
        click "Move forward"
        click "Move forward"
        advance until screen "choice"
        assert eval met_veldora and mana_perception and telepathy
        click "Absorb the six clusters"
        advance until screen "choice"
        assert eval item_count("magic_ore") == 8
        screenshot "cave_veldora.png"
        click "Go back"
        click "Go back"
        click "Go back"
        click "Go back"
        click "Go left"
        click "Go right"
        click "Go left"
        advance until screen "choice"
        click "Fight the Black Spider"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "choice"
        click "Predate the defeated monster"
        advance until screen "choice"
        assert eval chasm_thread_unlocked and has_skill("steel_thread")
        click "Swing across the chasm"
        advance until screen "choice"
        click "Move forward"
        click "Go right"
        advance until screen "choice"
        click "Fight the Armorsaurus"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "choice"
        click "Predate the defeated monster"
        advance until screen "choice"
        click "Move forward"
        advance until screen "choice"
        click "Step outside"
        advance until screen "location_choices"
        assert eval current_location == "cave_mouth"
        assert eval has_event("left_cave") and has_event("met_veldora")
        assert eval armorsaurus_defeated

    testcase goblin_story_preserved:
        run Start("test_goblin_setup")
        advance until screen "location_choices"
        click id "forward"
        click id "forward"
        advance until screen "location_choices"
        click id "village"
        click id "tent"
        advance until screen "choice"
        click "Use one Healing Blob"
        advance until screen "choice"
        assert eval injured_goblins_healed
        click "Talk to Rigurd about the Direwolves"
        advance until screen "choice"
        click "Help the goblins"
        advance until screen "battle_command_menu"
        assert eval enemy_run_chance == 0
        assert eval not battle_predator_allowed
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "choice"
        assert eval goblin_arc_complete and thought_communication and not telepathy
        assert eval character_state("ranga").get("recruited")
        click "Go outside into Goblin Village"
        assert eval current_location == "village"
        assert eval character_present("rigurd")

    testcase alternate_battle_condition:
        run Start("test_survival_setup")
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "location_choices"
        assert eval last_battle_outcome == "alternate_victory"
        assert eval has_event("giant_bear_defeated")

    testcase debug_panels:
        run Start("debug_slice_start")
        advance until screen "location_choices"
        click "Debug"
        click "Items"
        click "Give Stuffed Animal"
        assert eval item_count("stuffed_animal") == 5
        click "People"
        screenshot "debug_people.png"
        click "Skills"
        click "Learn Thought Communication"
        assert eval has_skill("thought_communication")
        click "Story"
        screenshot "debug_story.png"
        click "Battle"
        screenshot "debug_battle.png"
        click "Close"
        click "Status"
        screenshot "status.png"
        click "Close"
        click "Skills"
        screenshot "skills.png"
        click "X"
        click "Loadout"
        screenshot "loadout.png"
        click "X"

    testcase existing_legacy_save:
        if eval renpy.can_load("legacy-import"):
            run Start("debug_slice_start")
            advance until screen "location_choices"
            run Function(renpy.load, "legacy-import")
            advance until eval (renpy.get_screen("location_choices") or renpy.get_screen("choice"))
            assert eval world_state["schema"] == 1
            assert eval not in_battle
            assert eval item_count("berries") == berry_bundles
            assert eval item_count("magic_ore") == magic_ore_clusters
            screenshot "legacy_recovery.png"

    testcase village_refusal:
        run Start("test_goblin_setup")
        advance until screen "location_choices"
        click id "forward"
        click id "forward"
        advance until screen "location_choices"
        click id "village"
        click id "tent"
        advance until screen "choice"
        click "Use one Healing Blob"
        advance until screen "choice"
        click "Talk to Rigurd about the Direwolves"
        advance until screen "choice"
        click "Do not help"
        advance until screen "choice"
        click "I still won't help"
        advance until screen "location_choices"
        assert eval world_flag("goblins_destroyed")
        assert eval not character_state("haruna").get("alive", True)
        assert eval not character_present("rigurd", "command_tent")
        assert eval "lost_village" in eligible_endings()
        click id "back"
        click id "village"
        assert eval location_view(current_location)["background"] == "west_jura_wolf_den"
        assert eval not any(a["kind"] == "npc" for a in location_actions(current_location))

    testcase allied_boss_order:
        run Start("test_early_boss_setup")
        advance until screen "location_choices"
        run Function(enter_location, "ogre_border")
        run Jump("explore_location")
        click id "event_ogres_met"
        advance until screen "location_choices"
        assert eval world_state["choices"]["ogre_alliance"] == "defence"
        click id "event_kijin_recruited"
        advance until screen "location_choices"
        run Function(enter_location, "orc_approach")
        run Jump("explore_location")
        click id "fight_orc_lord"
        advance until screen "battle_command_menu"
        click "FIGHT"
        click "PHYSICAL"
        click "Basic Attack"
        advance until screen "choice"
        click "Leave the monster"
        advance until screen "location_choices"
        assert eval not world_flag("orc_lord_early")
        assert eval event_before("kijin_recruited", "orc_lord_defeated")
        click id "event_orc_aftermath"
        advance until screen "location_choices"
        assert eval "allied_forest" in eligible_endings()
        assert eval "independent_forest" not in eligible_endings()

    testcase rollback_gift:
        run Start("test_gift_setup")
        advance until screen "location_choices"
        click id "npc_haruna"
        advance until screen "npc_choices"
        click "Give Gift"
        click "Berry Bundle"
        assert eval item_count("berries") == 0
        assert eval relationship_value("haruna", "trust") == 5
        run Rollback()
        assert screen "gift_selection" timeout 5.0
        assert eval item_count("berries") == 1
        assert eval relationship_value("haruna", "trust") == 0
        assert eval not has_event("first_gift_haruna")
        assert eval gift_history == {}

label test_gift_setup:
    $ migrate_game_state()
    $ set_world_flag("village_access")
    $ add_item("berries")
    $ enter_location("village")
    jump explore_location

label test_early_boss_setup:
    $ migrate_game_state()
    $ learn_skill("mana_perception", "test")
    $ learn_skill("water_manipulation", "test")
    $ player_attack = 3000
    $ enter_location("ravine")
    jump explore_location

label test_defeat_setup:
    $ migrate_game_state()
    $ enter_location("rabbit_trail")
    $ player_hp = 1
    $ player_speed = 0
    call battle_enemy("horn_rabbit", encounter_id="forest_rabbit")
    jump explore_location

label test_escape_setup:
    $ restore_player()
    call battle_enemy("horn_rabbit", encounter_id="test_escape")
    jump explore_location

label test_legacy_setup:
    $ berry_bundles = 4
    $ healing_blobs = 6
    $ met_veldora = True
    $ goblin_meeting_seen = True
    $ horn_rabbit_defeated = True
    $ migrate_game_state()
    $ enter_location("crossroads")
    jump explore_location

label test_goblin_setup:
    $ player_attack = 1000
    $ telepathy = True
    jump debug_slice_start

label test_survival_setup:
    $ migrate_game_state()
    $ enter_location("crossroads")
    call battle_enemy("giant_bear", encounter_id="test_survival")
    jump explore_location

init 20 python:
    if renpy.game.args.command == "test":
        ENCOUNTERS["test_escape"] = {"enemy": "horn_rabbit", "can_run": True, "run_chance": 1.0}
        ENCOUNTERS["test_survival"] = {"enemy": "giant_bear", "end_conditions": [{"when": {"battle_turn_min": 1}, "result": "alternate_victory"}]}

init python:
    build.classify("game/tests/**", None)
    build.classify("tools/**", None)
    build.classify("test-results/**", None)
    build.classify("tests/**", None)
    build.classify("GAME_ARCHITECTURE.md", None)
    build.classify("DEVELOPMENT.md", None)
