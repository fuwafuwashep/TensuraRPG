# ============================================================
# FOREST OF DESIRE
# ============================================================
# The file was renamed from West_Jura.rpy to West_Forest.rpy.
# Existing west_jura_* label names remain internally for save and map-data
# compatibility. Player-facing text calls the region the Forest of Desire.


# ============================================================
# FOREST BACKGROUNDS
# ============================================================
# D   = dead end / monster / boss
# LRS = left / right / straight crossroads
# LS  = left / straight main path
# S   = straight path from the cave

image desire_forest_d = "images/forest_backgrounds/DesireForestBranchD.png"
image desire_forest_lrs = "images/forest_backgrounds/DesireForestBranchLRS.png"
image desire_forest_ls = "images/forest_backgrounds/DesireForestBranchLS.png"
image desire_forest_s = "images/forest_backgrounds/DesireForestBranchS.png"
image desire_forest_clearing = "images/forest_backgrounds/DesireForestClearing.png"
image desire_forest_clearing_empty = "images/forest_backgrounds/DesireForestClearingEmpty.png"
image desire_forest_goblin_village = "images/forest_backgrounds/DesireForestGoblinVillage.png"
image desire_forest_goblin_command = "images/forest_backgrounds/DesireForestGoblinCommand.png"


# Keep the old image aliases because data/locations.rpy already points at them.
image west_jura_forest = "images/forest_backgrounds/DesireForestBranchS.png"
image west_jura_crossroads = "images/forest_backgrounds/DesireForestBranchLRS.png"
image west_jura_clearing = "images/forest_backgrounds/DesireForestClearing.png"
image west_jura_orchard = "images/forest_backgrounds/DesireForestBranchLS.png"
image west_jura_village = "images/forest_backgrounds/DesireForestGoblinVillage.png"
image west_jura_command_tent_injured = "images/forest_backgrounds/DesireForestGoblinCommand.png"
image west_jura_command_tent_healed = "images/forest_backgrounds/DesireForestGoblinCommand.png"
image west_jura_wolf_den = "images/forest_backgrounds/DesireForestBranchD.png"
image west_jura_battle = "images/forest_backgrounds/DesireForestBranchD.png"


# ============================================================
# INVENTORY / STORAGE LEGACY COUNTERS
# ============================================================

# Healing Blobs are now crafted from Hipoutke Herbs.
default healing_blobs = 0

default berry_bundles = 0
default cattle_deer_stored = 0


# ============================================================
# REGION FLAGS
# ============================================================

default west_jura_intro_seen = False
default deep_forest_warning_seen = False

default goblin_meeting_seen = False
default goblin_village_unlocked = False

default village_berry_grove_harvested = False
default injured_goblins_healed = False
default rigurd_wolf_request_seen = False
default goblin_help_choice_made = False
default helped_goblins = False
default romance_route_available = True
default goblins_destroyed = False
default wolves_control_village = False
default direwolf_leader_defeated = False
default goblin_arc_complete = False


# ============================================================
# FOREST MONSTER FLAGS
# ============================================================

default horn_rabbit_defeated = False
default giant_bear_defeated = False
default barghest_defeated = False
default knight_spider_defeated = False
default blood_boar_defeated = False
default blade_tiger_defeated = False


default cattle_deer_captured = False


# ============================================================
# BERRY ORCHARDS
# ============================================================

default berry_orchard_1_harvested = False
default berry_orchard_2_harvested = False
default berry_orchard_3_harvested = False


# ============================================================
# SIDE-PATH RETURN TRACKING
# ============================================================

default side_path_3_from = "side1"


# ============================================================
# FOREST OF DESIRE MAP ART / TEXT PATCH
# ============================================================
# LOCATIONS is authored in data/locations.rpy. This runs after that file is
# initialized, so we can keep the existing navigation system and only replace
# the player-facing region name, art, and Bull Deer clearing behavior.

init 10 python:

    for _location in LOCATIONS.values():

        if "title" in _location:
            _location["title"] = (
                _location["title"]
                .replace("West Jura", "Forest of Desire")
                .replace("Veldora's Cave", "Storm Dragon's Cave")
            )

        if "description" in _location:
            _location["description"] = (
                _location["description"]
                .replace("Jura Forest", "Forest of Desire")
                .replace("West Jura", "Forest of Desire")
                .replace("Veldora's Cave", "Storm Dragon's Cave")
            )

            if _location["description"].startswith("Placeholder artwork"):
                _location["description"] = ""

        for _action in _location.get("actions", []):

            if "text" in _action:
                _action["text"] = (
                    _action["text"]
                    .replace("West Jura", "Forest of Desire")
                    .replace("Veldora's Cave", "Storm Dragon's Cave")
                )

    # Background mapping based on the Forest of Desire image names.
    _background_map = {
        "cave_mouth": "desire_forest_s",
        "crossroads": "desire_forest_lrs",
        "goblin_route": "desire_forest_ls",
        "village": "desire_forest_goblin_village",
        "command_tent": "desire_forest_goblin_command",
        "village_grove": "desire_forest_ls",
        "wolf_den": "desire_forest_d",
        "rabbit_trail": "desire_forest_d",
        "blumund_path": "desire_forest_ls",
        "deer_clearing": "desire_forest_clearing",
        "main2": "desire_forest_ls",
        "orchard1": "desire_forest_ls",
        "orchard2": "desire_forest_d",
        "orchard3": "desire_forest_ls",
        "main3": "desire_forest_ls",
        "main4": "desire_forest_lrs",
        "barghest_trail": "desire_forest_d",
        "spider_trail": "desire_forest_d",
        "main6": "desire_forest_lrs",
        "boar_trail": "desire_forest_d",
        "side1": "desire_forest_ls",
        "side2": "desire_forest_lrs",
        "charybdis_border": "desire_forest_d",
        "main7": "desire_forest_lrs",
        "tiger_trail": "desire_forest_d",
        "tiger_clearing": "desire_forest_clearing",
        "main8": "desire_forest_lrs",
        "main9": "desire_forest_lrs",
        "ogre_border": "desire_forest_d",
        "ravine": "desire_forest_d",
        "hidden_grove": "desire_forest_ls",
        "orc_approach": "desire_forest_d",
        "blumund_border": "desire_forest_d",
        "falmuth_border": "desire_forest_d",
        "canaat_border": "desire_forest_d",
        "dwargon_border": "desire_forest_d",
    }

    for _key, _background in _background_map.items():

        if _key in LOCATIONS:
            LOCATIONS[_key]["background"] = _background

    # Replace the original one-deer resource action with the whole clearing:
    # four male Bull Deer and four female Bull Deer.
    if "deer_clearing" in LOCATIONS:

        LOCATIONS["deer_clearing"]["title"] = (
            "Forest of Desire • Bull Deer Clearing"
        )

        LOCATIONS["deer_clearing"]["actions"] = [
            {
                "id": "capture_bull_deer_herd",
                "text": "Use Predator • Shelter the Bull Deer herd",
                "kind": "label",
                "label": "forest_desire_capture_bull_deer",
                "when": {"skills": ["predator"]},
                "visible_when": {
                    "flags": {"cattle_deer_captured": False}
                },
            },
            path(
                "back",
                "Go back",
                "blumund_path"
            ),
        ]

        LOCATIONS["deer_clearing"]["variants"] = [
            {
                "title": "Forest of Desire • Empty Bull Deer Clearing",
                "background": "desire_forest_clearing_empty",
                "description": (
                    "The clearing is quiet after the herd was sheltered "
                    "inside Predator."
                ),
                "actions": [
                    path(
                        "back",
                        "Go back",
                        "blumund_path"
                    )
                ],
                "when": {
                    "flags": {"cattle_deer_captured": True}
                },
            }
        ]


# ============================================================
# REGION ENTRY
# ============================================================

label west_jura_start:

    $ migrate_game_state()
    $ record_event("left_cave")

    # Keep the old internal region key for save compatibility.
    $ current_region = "West_Jura"
    $ sync_skill_moves()

    if not west_jura_intro_seen:

        $ west_jura_intro_seen = True

        call west_jura_adventurer_trio_cutscene

    $ enter_location("cave_mouth")
    jump explore_location


# Optional clearer alias for new code.
label west_forest_start:
    jump west_jura_start


label west_jura_adventurer_trio_cutscene:

    scene west_jura_forest
    with fade

    n "Three adventurers pass near the cave entrance."

    n "None of them notice me."

    n "They continue on through the Forest of Desire without realizing I was there."

    return


# ============================================================
# MAIN CROSSROADS
# ============================================================

label west_jura_crossroads:
    $ enter_location("crossroads")
    jump explore_location


label west_jura_right_warning:
    $ enter_location("rabbit_trail")
    jump explore_location


label west_jura_left_warning:
    $ enter_location("ravine")
    jump explore_location


label west_jura_left_deep_placeholder:
    $ enter_location("ravine")
    jump explore_location


label west_jura_goblin_route:
    $ enter_location("goblin_route")
    jump explore_location


label west_jura_goblin_meeting_cutscene:

    scene west_jura_forest
    with dissolve

    n "A group of goblins approaches me in the forest."

    n "After speaking with them, I learn that their settlement is nearby."

    n "They invite me to their village."

    return


# ============================================================
# GOBLIN VILLAGE
# ============================================================

label west_jura_goblin_village:
    $ enter_location("village")
    jump explore_location


label west_jura_village_berry_grove:
    $ enter_location("village_grove")
    jump explore_location


label west_jura_command_tent:

    $ enter_location("command_tent")
    $ navigation_active = False

    if goblins_destroyed:
        jump west_jura_wolf_den

    if injured_goblins_healed:
        scene west_jura_command_tent_healed

    else:
        scene west_jura_command_tent_injured


    if not injured_goblins_healed:

        n "Several injured goblins are lying inside the tent."

        menu:

            "Use one Healing Blob" if item_count("healing_blob") > 0:

                $ remove_item("healing_blob")

                call west_jura_heal_goblins_cutscene

                $ injured_goblins_healed = True
                $ record_event("injured_goblins_healed")

                jump west_jura_command_tent


            "Leave the tent":
                jump west_jura_goblin_village


    if goblin_arc_complete:

        n "The immediate Goblin Village story is complete."

        n "The next part of the village story will be implemented later."

        menu:

            "Explore more of the forest":
                jump west_jura_crossroads

            "Go outside into Goblin Village":
                jump west_jura_goblin_village


    n "Rigurd remains inside the command tent."

    menu:

        "Talk to Rigurd about the Direwolves":
            jump west_jura_talk_rigurd

        "Visit Rigurd / Give Gift":
            call npc_interaction("rigurd")
            jump west_jura_command_tent

        "Leave the tent":
            jump west_jura_goblin_village


label west_jura_heal_goblins_cutscene:

    n "The Healing Blob spreads over the injured goblins."

    n "Their wounds begin to close."

    n "After some time, they are healthy enough to leave the tent."

    n "Only Rigurd remains inside."

    return


# ============================================================
# RIGURD / DIREWOLF DECISION
# ============================================================

label west_jura_talk_rigurd:

    if goblin_help_choice_made:

        if helped_goblins:

            n "The village is preparing for the Direwolves."

            jump west_jura_help_goblins_arc

        else:

            n "There is nothing more to discuss."

            jump west_jura_command_tent


    $ rigurd_wolf_request_seen = True

    n "Rigurd explains that Direwolves have been attacking the settlement."

    n "He asks if I will help protect the goblins."

    menu:

        "Help the goblins":

            $ goblin_help_choice_made = True
            $ helped_goblins = True

            jump west_jura_help_goblins_arc

        "Do not help":
            jump west_jura_refuse_goblins_warning


label west_jura_refuse_goblins_warning:

    n "It is strongly recommended that you help the goblins."

    n "Refusing removes a romanceable option, and many characters from the story will die."

    n "By the next day, the Goblin Village will be destroyed and the Direwolves will take it as a den."

    menu:

        "I still won't help":

            $ goblin_help_choice_made = True
            $ helped_goblins = False
            $ romance_route_available = False

            n "The next day..."

            $ goblins_destroyed = True
            $ wolves_control_village = True

            $ world_state["choices"]["goblin_defence"] = "refused"
            $ record_event("goblins_destroyed")

            $ world_state["characters"]["haruna"] = dict(character_state("haruna"), alive=False)

            $ world_state["characters"]["rigurd"] = dict(character_state("rigurd"), alive=False)

            jump west_jura_wolf_den


        "Go back and help them":

            $ goblin_help_choice_made = True
            $ helped_goblins = True

            jump west_jura_help_goblins_arc


# ============================================================
# HELPING THE GOBLINS
# ============================================================

label west_jura_help_goblins_arc:

    $ world_state["choices"]["goblin_defence"] = "helped"

    call west_jura_fortification_cutscene
    call west_jura_direwolf_arrival_cutscene

    n "Talking the Direwolves down fails."

    n "Their leader steps forward."

    # Predator is intentionally disabled in this story fight.
    call battle_enemy(
        "direwolf_leader",
        predator_allowed=False,
        encounter_id="direwolf_defence"
    )

    if _return == "won":

        $ direwolf_leader_defeated = True

        call west_jura_naming_cutscene

        $ goblin_arc_complete = True
        $ record_event("goblin_arc_complete")
        $ meet_character("ranga", True)
        $ change_relationship("haruna", trust=10)
        $ change_relationship("rigurd", trust=8)
        $ world_state["phase"] = max(1, world_state["phase"])

        # Sleeping after the naming restores move uses.
        $ restore_player()

        scene west_jura_command_tent_healed
        with fade

        n "I wake up inside the Command Tent."

        n "The next part of this story will be implemented later."

        menu:

            "Explore more of the forest":
                jump west_jura_crossroads

            "Go outside into Goblin Village":
                jump west_jura_goblin_village


    else:

        n "I can't continue..."

        menu:

            "Try the Direwolf battle again":
                jump west_jura_help_goblins_arc

            "Return to the Command Tent":

                $ player_hp = player_max_hp

                jump west_jura_command_tent


label west_jura_fortification_cutscene:

    scene west_jura_village

    n "I spend time helping the goblins fortify the settlement."

    n "Barricades are reinforced and everyone prepares for the attack."

    return


label west_jura_direwolf_arrival_cutscene:

    scene west_jura_village

    n "Night falls."

    n "The Direwolf pack finally arrives outside the settlement."

    n "I try to talk them down before anyone has to die."

    return


label west_jura_naming_cutscene:

    scene west_jura_village

    n "After defeating their leader, I gather the goblins and Direwolves together."

    n "Standing on a tree trunk, I give them three rules to follow."

    n "Then I begin naming the villagers."

    n "After that, I begin naming the Direwolves."

    if telepathy and not thought_communication:

        n "As I continue naming the Direwolves, something changes."

        n "Telepathy begins evolving."

        $ telepathy = False
        $ thought_communication = True

        $ sync_skill_moves()

        n "Telepathy evolved into Thought Communication."

        n "Acquired: Thought Communication."

        n "The Allies battle function has been unlocked."

    n "The naming consumes so much energy that I eventually fall asleep."

    return


# ============================================================
# BULL DEER CLEARING
# ============================================================

label forest_desire_capture_bull_deer:

    $ navigation_active = False

    scene desire_forest_clearing

    n "The clearing contains four male Bull Deer and four female Bull Deer."

    n "Predator can shelter the entire herd safely inside Stomach."

    $ bull_deer_stored = add_item_group([("bull_deer_male", 4), ("bull_deer_female", 4)])

    if bull_deer_stored:

        $ cattle_deer_captured = True
        $ set_world_flag("cattle_deer_captured")

        scene desire_forest_clearing_empty
        with dissolve

        n "Stored: Bull Deer (Male) ×4."
        n "Stored: Bull Deer (Female) ×4."

        n "Each herd stack occupies two inventory spaces."

    else:

        n "There is not enough contiguous space in Stomach for the herd."

    $ enter_location("deer_clearing")
    jump explore_location


# ============================================================
# FOREST LOCATION WRAPPERS
# ============================================================

label west_jura_wolf_den:
    $ enter_location("wolf_den")
    jump explore_location


label west_jura_horn_rabbit_area:
    $ enter_location("rabbit_trail")
    jump explore_location


label west_jura_blumund_path:
    $ enter_location("blumund_path")
    jump explore_location


label west_jura_blumund_placeholder:
    $ enter_location("blumund_border")
    jump explore_location


label west_jura_cattle_deer_clearing:
    $ enter_location("deer_clearing")
    jump explore_location


label west_jura_main_branch_2:
    $ enter_location("main2")
    jump explore_location


label west_jura_berry_orchard_1:
    $ enter_location("orchard1")
    jump explore_location


label west_jura_berry_orchard_2:
    $ enter_location("orchard2")
    jump explore_location


label west_jura_berry_orchard_3:
    $ enter_location("orchard3")
    jump explore_location


label west_jura_main_branch_3:
    $ enter_location("main3")
    jump explore_location


label west_jura_main_branch_4:
    $ enter_location("main4")
    jump explore_location


label west_jura_barghest_area:
    $ enter_location("barghest_trail")
    jump explore_location


label west_jura_falmuth_placeholder:
    $ enter_location("falmuth_border")
    jump explore_location


label west_jura_knight_spider_area:
    $ enter_location("spider_trail")
    jump explore_location


label west_jura_canaat_placeholder:
    $ enter_location("canaat_border")
    jump explore_location


label west_jura_main_branch_6:
    $ enter_location("main6")
    jump explore_location


label west_jura_blood_boar_area:
    $ enter_location("boar_trail")
    jump explore_location


label west_jura_side_path_1:
    $ enter_location("side1")
    jump explore_location


label west_jura_side_path_2:
    $ enter_location("side2")
    jump explore_location


label west_jura_dwargon_placeholder:
    $ enter_location("dwargon_border")
    jump explore_location


label west_jura_side_path_3:
    $ enter_location("charybdis_border")
    jump explore_location


label west_jura_main_branch_7:
    $ enter_location("main7")
    jump explore_location


label west_jura_blade_tiger_area:
    $ enter_location("tiger_trail")
    jump explore_location


label west_jura_blade_tiger_clearing:
    $ enter_location("tiger_clearing")
    jump explore_location


label west_jura_main_branch_8:
    $ enter_location("main8")
    jump explore_location


label west_jura_main_branch_9:
    $ enter_location("main9")
    jump explore_location


label west_jura_ogre_village_placeholder:
    $ enter_location("ogre_border")
    jump explore_location


# ============================================================
# KEEN SMELL
# ============================================================

label west_jura_keen_smell_menu:

    $ current_region = "West_Jura"

    scene west_jura_forest

    n "Keen Smell lets me locate monsters throughout the Forest of Desire."

    menu:

        "Track a Horn Rabbit":
            jump west_jura_horn_rabbit_area

        "Track a Giant Bear":
            jump west_jura_berry_orchard_2

        "Track a Barghest":
            jump west_jura_barghest_area

        "Track a Knight Spider":
            jump west_jura_knight_spider_area

        "Track a Blood Boar":
            jump west_jura_blood_boar_area

        "Track a Blade Tiger":
            jump west_jura_blade_tiger_area

        "Cancel":
            jump west_jura_crossroads
