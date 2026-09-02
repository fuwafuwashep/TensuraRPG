# ============================================================
# WEST JURA FOREST
# ============================================================

# The art for this region has not been added yet, so these are
# placeholder backgrounds. Replace the Solid() lines with real
# PNG paths later without changing the navigation labels.


# ============================================================
# PLACEHOLDER BACKGROUNDS
# ============================================================

image west_jura_forest = Solid("#1F3826")
image west_jura_crossroads = Solid("#294A31")
image west_jura_clearing = Solid("#36583A")
image west_jura_orchard = Solid("#3F5934")
image west_jura_village = Solid("#514B36")
image west_jura_command_tent_injured = Solid("#4A4035")
image west_jura_command_tent_healed = Solid("#5A4C3D")
image west_jura_wolf_den = Solid("#2F312D")
image west_jura_battle = Solid("#243528")


# ============================================================
# INVENTORY / STORAGE
# ============================================================

# One Healing Blob is supplied as a temporary test amount so the
# command-tent healing sequence can currently be played.
default healing_blobs = 1

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
# WEST JURA MONSTER FLAGS
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
# REGION ENTRY
# ============================================================

label west_jura_start:

    $ current_region = "West_Jura"
    $ sync_skill_moves()

    if not west_jura_intro_seen:

        $ west_jura_intro_seen = True

        call west_jura_adventurer_trio_cutscene

    scene west_jura_forest
    with dissolve

    n "I'm outside Veldora's Cave now."

    menu:

        "Go back into Veldora's Cave":

            $ current_region = "Veldoras_Cave"
            jump veldora_cave_exit

        "Go forward into the forest":
            jump west_jura_crossroads


# ============================================================
# ADVENTURER TRIO CUTSCENE
# ============================================================

label west_jura_adventurer_trio_cutscene:

    scene west_jura_forest
    with fade

    n "Three adventurers pass near the cave entrance."

    n "None of them notice me."

    n "They continue on through the forest without realizing I was there."

    return


# ============================================================
# MAIN CROSSROADS
# ============================================================

label west_jura_crossroads:

    $ current_region = "West_Jura"

    scene west_jura_crossroads

    menu:

        "Go forward":
            jump west_jura_goblin_route

        "Go right":
            jump west_jura_right_warning

        "Go left":
            jump west_jura_left_warning

        "Go back toward Veldora's Cave":
            jump west_jura_start

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# DEEP-FOREST WARNING
# ============================================================

label west_jura_right_warning:

    if deep_forest_warning_seen:
        jump west_jura_horn_rabbit_area

    $ deep_forest_warning_seen = True

    n "Are you sure you want to go deeper into the forest?"

    n "It is recommended to go forward first."

    $ renpy.pause(3.0, hard=True)

    menu:

        "Yes, let's go.":
            jump west_jura_horn_rabbit_area

        "Maybe not.":
            jump west_jura_crossroads


label west_jura_left_warning:

    if deep_forest_warning_seen:
        jump west_jura_left_deep_placeholder

    $ deep_forest_warning_seen = True

    n "Are you sure you want to go deeper into the forest?"

    n "It is recommended to go forward first."

    $ renpy.pause(3.0, hard=True)

    menu:

        "Yes, let's go.":
            jump west_jura_left_deep_placeholder

        "Maybe not.":
            jump west_jura_crossroads


# The supplied map does not define what is beyond the LEFT side
# of the first crossroads yet.
label west_jura_left_deep_placeholder:

    scene west_jura_forest

    n "This deeper western route has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_crossroads


# ============================================================
# GOBLIN MEETING
# ============================================================

label west_jura_goblin_route:

    if not goblin_meeting_seen:

        call west_jura_goblin_meeting_cutscene

        $ goblin_meeting_seen = True
        $ goblin_village_unlocked = True

    scene west_jura_forest

    menu:

        "Go to Goblin Village":
            jump west_jura_goblin_village

        "Go back to the crossroads":
            jump west_jura_crossroads


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

    if goblins_destroyed:
        jump west_jura_wolf_den

    scene west_jura_village

    menu:

        "Enter the Command Tent":
            jump west_jura_command_tent

        "Go to the Berry Grove":
            jump west_jura_village_berry_grove

        "Explore other village areas":

            n "The rest of Goblin Village has not been implemented yet."

            jump west_jura_goblin_village

        "Return to the forest":
            jump west_jura_goblin_route


# ============================================================
# VILLAGE BERRY GROVE
# ============================================================

label west_jura_village_berry_grove:

    scene west_jura_orchard

    if not village_berry_grove_harvested:

        menu:

            "Gather berries":

                $ village_berry_grove_harvested = True
                $ berry_bundles += 1

                n "You store a bundle of berries in your Stomach."

                jump west_jura_village_berry_grove

            "Go back":
                jump west_jura_goblin_village

    else:

        n "You've already gathered the ripe berries here."

        menu:

            "Go back":
                jump west_jura_goblin_village


# ============================================================
# COMMAND TENT
# ============================================================

label west_jura_command_tent:

    if injured_goblins_healed:
        scene west_jura_command_tent_healed

    else:
        scene west_jura_command_tent_injured


    if not injured_goblins_healed:

        n "Several injured goblins are lying inside the tent."

        menu:

            "Use one Healing Blob" if healing_blobs > 0:

                $ healing_blobs -= 1

                call west_jura_heal_goblins_cutscene

                $ injured_goblins_healed = True

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

        "Talk to Rigurd":
            jump west_jura_talk_rigurd

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

            jump west_jura_wolf_den

        "Go back and help them":

            $ goblin_help_choice_made = True
            $ helped_goblins = True

            jump west_jura_help_goblins_arc


# ============================================================
# HELPING THE GOBLINS
# ============================================================

label west_jura_help_goblins_arc:

    call west_jura_fortification_cutscene
    call west_jura_direwolf_arrival_cutscene

    n "Talking the Direwolves down fails."

    n "Their leader steps forward."

    # Predator is intentionally disabled in this story fight.
    call battle_enemy("direwolf_leader", predator_allowed=False)

    if _return == "won":

        $ direwolf_leader_defeated = True

        call west_jura_naming_cutscene

        $ goblin_arc_complete = True

        # Sleeping after the naming restores move uses.
        $ reset_move_uses()
        $ player_hp = player_max_hp

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

    n "Then I begin naming the villagers and the Direwolves."

    n "The naming consumes so much energy that I eventually fall asleep."

    return


# ============================================================
# WOLF DEN - BAD GOBLIN OUTCOME
# ============================================================

label west_jura_wolf_den:

    scene west_jura_wolf_den

    n "The former Goblin Village has become a Direwolf den."

    if not direwolf_leader_defeated:

        menu:

            "Challenge the leader of the pack":

                # This is no longer the protected story fight,
                # so Predator is allowed here.
                call battle_enemy("direwolf_leader", predator_allowed=True)

                if _return == "won":

                    $ direwolf_leader_defeated = True
                    n "The Direwolf Leader has been defeated."

                    jump west_jura_wolf_den

                else:

                    jump west_jura_wolf_den

            "Return to the forest":
                jump west_jura_goblin_route

    else:

        menu:

            "Return to the forest":
                jump west_jura_goblin_route


# ============================================================
# RIGHT DEEP-FOREST ROUTE
# MAIN BRANCH 1 - HORN RABBIT
# ============================================================

label west_jura_horn_rabbit_area:

    scene west_jura_forest

    if not horn_rabbit_defeated:

        n "A Horn Rabbit blocks the path."

        menu:

            "Fight the Horn Rabbit":

                call battle_enemy("horn_rabbit")

                if _return == "won":

                    $ horn_rabbit_defeated = True

                    jump west_jura_horn_rabbit_area

                elif _return == "ran":
                    jump west_jura_crossroads

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_crossroads

            "Retreat":
                jump west_jura_crossroads


    else:

        menu:

            "Take the left-side path toward Blumund":
                jump west_jura_blumund_path

            "Continue along the main forest path":
                jump west_jura_main_branch_2

            "Fight another Horn Rabbit":

                call battle_enemy("horn_rabbit")
                jump west_jura_horn_rabbit_area

            "Go back to the crossroads":
                jump west_jura_crossroads

            "Use Keen Smell" if keen_smell:
                jump west_jura_keen_smell_menu


# ============================================================
# BLUMUND SIDE ROUTE
# ============================================================

label west_jura_blumund_path:

    scene west_jura_forest

    menu:

        "Continue toward Blumund":
            jump west_jura_blumund_placeholder

        "Go toward the clearing":
            jump west_jura_cattle_deer_clearing

        "Go back":
            jump west_jura_horn_rabbit_area


label west_jura_blumund_placeholder:

    scene west_jura_clearing

    n "The route toward Blumund has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_blumund_path


label west_jura_cattle_deer_clearing:

    scene west_jura_clearing

    if not cattle_deer_captured:

        n "Several Cattle Deer are grazing in the clearing."

        menu:

            "Capture a Cattle Deer in your Stomach":

                $ cattle_deer_captured = True
                $ cattle_deer_stored += 1

                n "A Cattle Deer is stored in your Stomach."

                n "It does not grant a skill, but keeping Cattle Deer can unlock breeding-related content later."

                jump west_jura_cattle_deer_clearing

            "Leave them alone":
                jump west_jura_blumund_path

    else:

        n "The remaining Cattle Deer keep their distance."

        menu:

            "Go back":
                jump west_jura_blumund_path


# ============================================================
# MAIN BRANCH 2
# ============================================================

label west_jura_main_branch_2:

    scene west_jura_forest

    menu:

        "Take the path into the berry orchard":
            jump west_jura_berry_orchard_1

        "Continue along the main path":
            jump west_jura_main_branch_3

        "Go back toward the Horn Rabbit area":
            jump west_jura_horn_rabbit_area

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# BERRY ORCHARD 1
# ============================================================

label west_jura_berry_orchard_1:

    scene west_jura_orchard

    if not berry_orchard_1_harvested:

        n "Berries grow throughout this section of the orchard."

    menu:

        "Gather the berries" if not berry_orchard_1_harvested:

            $ berry_orchard_1_harvested = True
            $ berry_bundles += 1

            n "You store a bundle of berries."

            jump west_jura_berry_orchard_1

        "Go deeper into the orchard":
            jump west_jura_berry_orchard_2

        "Return to the main path":
            jump west_jura_main_branch_2


# ============================================================
# BERRY ORCHARD 2 - GIANT BEAR
# ============================================================

label west_jura_berry_orchard_2:

    scene west_jura_orchard

    if not giant_bear_defeated:

        n "A Giant Bear has claimed the deeper orchard."

        menu:

            "Fight the Giant Bear":

                call battle_enemy("giant_bear")

                if _return == "won":

                    $ giant_bear_defeated = True

                    jump west_jura_berry_orchard_2

                elif _return == "ran":
                    jump west_jura_berry_orchard_1

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_berry_orchard_1

            "Go back":
                jump west_jura_berry_orchard_1


    if not berry_orchard_2_harvested:

        n "The berries are safe to gather now."

    menu:

        "Gather the berries" if not berry_orchard_2_harvested:

            $ berry_orchard_2_harvested = True
            $ berry_bundles += 1

            n "You store a bundle of berries."

            jump west_jura_berry_orchard_2

        "Go left to the first orchard":
            jump west_jura_berry_orchard_1

        "Go right to another orchard":
            jump west_jura_berry_orchard_3

        "Fight another Giant Bear":

            call battle_enemy("giant_bear")
            jump west_jura_berry_orchard_2


# ============================================================
# BERRY ORCHARD 3
# ============================================================

label west_jura_berry_orchard_3:

    scene west_jura_orchard

    menu:

        "Gather the berries" if not berry_orchard_3_harvested:

            $ berry_orchard_3_harvested = True
            $ berry_bundles += 1

            n "You store a bundle of berries."

            jump west_jura_berry_orchard_3

        "Go left into the deeper orchard":
            jump west_jura_berry_orchard_2

        "Return to the main forest path":
            jump west_jura_main_branch_3


# ============================================================
# MAIN BRANCH 3
# ============================================================

label west_jura_main_branch_3:

    scene west_jura_clearing

    menu:

        "Take the left path into the berry orchard":
            jump west_jura_berry_orchard_3

        "Continue down the main path":
            jump west_jura_main_branch_4

        "Go back toward Main Branch 2":
            jump west_jura_main_branch_2

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# MAIN BRANCH 4
# ============================================================

label west_jura_main_branch_4:

    scene west_jura_forest

    menu:

        "Take the left-side path":
            jump west_jura_barghest_area

        "Continue along the main path":
            jump west_jura_knight_spider_area

        "Go back toward Main Branch 3":
            jump west_jura_main_branch_3

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# BARGHEST / FALMUTH ROUTE
# ============================================================

label west_jura_barghest_area:

    scene west_jura_clearing

    if not barghest_defeated:

        n "A Barghest waits in the clearing."

        menu:

            "Fight the Barghest":

                call battle_enemy("barghest")

                if _return == "won":

                    $ barghest_defeated = True

                    jump west_jura_barghest_area

                elif _return == "ran":
                    jump west_jura_main_branch_4

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_main_branch_4

            "Retreat":
                jump west_jura_main_branch_4


    menu:

        "Continue toward Falmuth":
            jump west_jura_falmuth_placeholder

        "Fight another Barghest":

            call battle_enemy("barghest")
            jump west_jura_barghest_area

        "Go back":
            jump west_jura_main_branch_4


label west_jura_falmuth_placeholder:

    scene west_jura_forest

    n "The path to Falmuth has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_barghest_area


# ============================================================
# MAIN BRANCH 5 - KNIGHT SPIDER
# ============================================================

label west_jura_knight_spider_area:

    scene west_jura_forest

    if not knight_spider_defeated:

        n "A Knight Spider blocks the main trail."

        menu:

            "Fight the Knight Spider":

                call battle_enemy("knight_spider")

                if _return == "won":

                    $ knight_spider_defeated = True

                    n "You already possess the Knight Spider's useful skills."
                    n "A large magicule gain will be added here when the magicule-capacity system is implemented."

                    jump west_jura_knight_spider_area

                elif _return == "ran":
                    jump west_jura_main_branch_4

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_main_branch_4

            "Retreat":
                jump west_jura_main_branch_4


    menu:

        "Continue toward the Canaat Mountains":
            jump west_jura_canaat_placeholder

        "Take the route toward the outer forest loop":
            jump west_jura_main_branch_6

        "Go back toward Main Branch 4":
            jump west_jura_main_branch_4

        "Fight another Knight Spider":

            call battle_enemy("knight_spider")
            jump west_jura_knight_spider_area

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


label west_jura_canaat_placeholder:

    scene west_jura_forest

    n "The route to the Canaat Mountains has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_knight_spider_area


# ============================================================
# MAIN BRANCH 6
# ============================================================

label west_jura_main_branch_6:

    scene west_jura_forest

    menu:

        "Head toward the Knight Spider trail":
            jump west_jura_knight_spider_area

        "Continue around the outer forest loop":
            jump west_jura_main_branch_7

        "Take the side path":
            jump west_jura_blood_boar_area

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# BLOOD BOAR
# ============================================================

label west_jura_blood_boar_area:

    scene west_jura_clearing

    if not blood_boar_defeated:

        n "A Blood Boar blocks the side path."

        menu:

            "Fight the Blood Boar":

                call battle_enemy("blood_boar")

                if _return == "won":

                    $ blood_boar_defeated = True

                    jump west_jura_blood_boar_area

                elif _return == "ran":
                    jump west_jura_main_branch_6

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_main_branch_6

            "Retreat":
                jump west_jura_main_branch_6


    menu:

        "Take the right path":
            jump west_jura_side_path_1

        "Take the left path":
            jump west_jura_side_path_2

        "Fight another Blood Boar":

            call battle_enemy("blood_boar")
            jump west_jura_blood_boar_area

        "Return to Main Branch 6":
            jump west_jura_main_branch_6


# ============================================================
# SIDE PATH 1
# ============================================================

label west_jura_side_path_1:

    scene west_jura_forest

    menu:

        "Continue":

            $ side_path_3_from = "side1"
            jump west_jura_side_path_3

        "Go back":
            jump west_jura_blood_boar_area


# ============================================================
# SIDE PATH 2
# ============================================================

label west_jura_side_path_2:

    scene west_jura_forest

    menu:

        "Continue forward":

            $ side_path_3_from = "side2"
            jump west_jura_side_path_3

        "Take the path toward Dwargon":
            jump west_jura_dwargon_placeholder

        "Go back":
            jump west_jura_blood_boar_area


label west_jura_dwargon_placeholder:

    scene west_jura_clearing

    n "The route to Dwargon has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_side_path_2


# ============================================================
# SIDE PATH 3 / CHARYBDIS CAVE
# ============================================================

label west_jura_side_path_3:

    scene west_jura_forest

    n "Charybdis Cave has not been implemented yet."

    menu:

        "Go back":

            if side_path_3_from == "side2":
                jump west_jura_side_path_2

            else:
                jump west_jura_side_path_1


# ============================================================
# MAIN BRANCH 7
# ============================================================

label west_jura_main_branch_7:

    scene west_jura_forest

    menu:

        "Continue toward Main Branch 6":
            jump west_jura_main_branch_6

        "Continue around the loop toward Main Branch 8":
            jump west_jura_main_branch_8

        "Take the one-way side trail":
            jump west_jura_blade_tiger_area

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# BLADE TIGER
# ============================================================

label west_jura_blade_tiger_area:

    scene west_jura_clearing

    if not blade_tiger_defeated:

        n "A Blade Tiger waits ahead."

        menu:

            "Fight the Blade Tiger":

                call battle_enemy("blade_tiger")

                if _return == "won":

                    $ blade_tiger_defeated = True

                    jump west_jura_blade_tiger_area

                elif _return == "ran":
                    jump west_jura_blade_tiger_clearing

                else:

                    $ player_hp = player_max_hp
                    jump west_jura_blade_tiger_clearing

            "Retreat":
                jump west_jura_blade_tiger_clearing


    menu:

        "Fight another Blade Tiger":

            call battle_enemy("blade_tiger")
            jump west_jura_blade_tiger_area

        "Go back":
            jump west_jura_blade_tiger_clearing


# ============================================================
# CLEARING CONNECTED TO MAIN BRANCH 8
# ============================================================

label west_jura_blade_tiger_clearing:

    scene west_jura_clearing

    menu:

        "Go toward the Blade Tiger":
            jump west_jura_blade_tiger_area

        "Return to Main Branch 8":
            jump west_jura_main_branch_8


# ============================================================
# MAIN BRANCH 8
# ============================================================

label west_jura_main_branch_8:

    scene west_jura_forest

    menu:

        "Continue toward Main Branch 7":
            jump west_jura_main_branch_7

        "Continue around the loop toward Main Branch 9":
            jump west_jura_main_branch_9

        "Take the path to the Blade Tiger clearing":
            jump west_jura_blade_tiger_clearing

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


# ============================================================
# MAIN BRANCH 9
# ============================================================

label west_jura_main_branch_9:

    scene west_jura_forest

    menu:

        "Continue toward Main Branch 8":
            jump west_jura_main_branch_8

        "Return to the original crossroads":
            jump west_jura_crossroads

        "Take the path toward the Ogre Village":
            jump west_jura_ogre_village_placeholder

        "Use Keen Smell" if keen_smell:
            jump west_jura_keen_smell_menu


label west_jura_ogre_village_placeholder:

    scene west_jura_clearing

    n "The Ogre Village has not been implemented yet."

    menu:

        "Go back":
            jump west_jura_main_branch_9


# ============================================================
# KEEN SMELL
# ============================================================

label west_jura_keen_smell_menu:

    $ current_region = "West_Jura"

    scene west_jura_forest

    n "Keen Smell lets me locate monsters throughout West Jura."

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
