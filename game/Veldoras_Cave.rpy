# ============================================================
# VELDORA'S CAVE
# ============================================================


# ============================================================
# BACKGROUNDS
# ============================================================

image cave_blind = Solid("#000000")

image cave_branch_d = "images/backgrounds/VeldoracaveBranchD.png"
image cave_branch_lr = "images/backgrounds/VeldoracaveBranchLR.png"
image cave_branch_lsr = "images/backgrounds/VeldoracaveBranchLSR.png"
image cave_branch_s = "images/backgrounds/VeldoracaveBranchS.png"
image cave_branch_sg = "images/backgrounds/VeldoracaveBranchSG.png"

image cave_lake_1 = "images/backgrounds/VeldoracaveLake1.png"
image cave_lake_2 = "images/backgrounds/VeldoracaveLake2.png"

image cave_lake_empty_1 = "images/backgrounds/VeldoracaveLakeEmpty1.png"
image cave_lake_empty_2 = "images/backgrounds/VeldoracaveLakeEmpty2.png"


# ============================================================
# CHASM BACKGROUNDS
#
# L = Giant Bat side
# M = Middle
# S = Spider
# R = Rightmost
# ============================================================

image cave_chasm_l = "images/backgrounds/VeldoracaveChasmL.png"
image cave_chasm_m = "images/backgrounds/VeldoracaveChasmM.png"
image cave_chasm_s = "images/backgrounds/VeldoracaveChasmS.png"
image cave_chasm_r = "images/backgrounds/VeldoracaveChasmR.png"


# ============================================================
# PLACEHOLDER EXIT
# ============================================================

image cave_exit_placeholder = Solid("#555555")


# Compatibility.
image cave_visible = "images/backgrounds/VeldoracaveBranchD.png"


# ============================================================
# PLAYER ABILITIES
# ============================================================

default mana_perception = False
default telepathy = False

default water_manipulation = False

default heat_resistance = False
default cold_resistance = False
default electricity_resistance = False
default paralysis_resistance = False


# ============================================================
# STORY FLAGS
# ============================================================

default met_veldora = False
default veldora_in_stomach = False
default gecko_hint_seen = False


# ============================================================
# PART 1 CREATURE FLAGS
# ============================================================

default heat_lizard_absorbed = False
default cold_lizard_absorbed = False
default electric_lizard_absorbed = False
default thunder_frog_defeated = False


# ============================================================
# PART 2 CREATURE FLAGS
# ============================================================

default tempest_serpent_defeated = False
default black_spider_defeated = False
default giant_bat_defeated = False
default evil_centipede_defeated = False
default armorsaurus_defeated = False


# ============================================================
# CHASM FLAGS
# ============================================================

default chasm_thread_unlocked = False

# Where the player came from when entering the Spider area.
default spider_return_location = "right"


# ============================================================
# RESOURCE FLAGS
# ============================================================

default branch3_ore_absorbed = False
default branch5_ore_absorbed = False
default veldora_ore_absorbed = False

default branch4_herbs_absorbed = False
default lake1_herbs_absorbed = False
default lake2_herbs_absorbed = False
default frog_herbs_absorbed = False


# ============================================================
# RESOURCE COUNTERS
# ============================================================

default magic_ore_clusters = 0
default hipokute_herb_clusters = 0


# ============================================================
# COMBAT
# ============================================================

default player_max_hp = 300
default player_hp = 300


# ============================================================
# BACKGROUND HELPERS
# ============================================================

label update_cave_view(view_type="D"):

    if not mana_perception:

        if view_type == "S":
            scene cave_branch_sg

        else:
            scene cave_blind

        return


    if view_type == "D":
        scene cave_branch_d

    elif view_type == "LR":
        scene cave_branch_lr

    elif view_type == "LSR":
        scene cave_branch_lsr

    elif view_type == "S":
        scene cave_branch_s

    else:
        scene cave_branch_d

    return


label update_lake_1_view:

    if not mana_perception:
        scene cave_blind

    elif lake1_herbs_absorbed:
        scene cave_lake_empty_1

    else:
        scene cave_lake_1

    return


label update_lake_2_view:

    if not mana_perception:
        scene cave_blind

    elif lake2_herbs_absorbed:
        scene cave_lake_empty_2

    else:
        scene cave_lake_2

    return


# ============================================================
# VELDORA'S CAVE START
# ============================================================

label veldoras_cave_start:

    scene cave_blind
    with fade

    centered "Veldora's Cave"

    pause 1.0

    n "I can't see anything."

    n "I can only feel my immediate surroundings."

    n "There seems to be more than one direction I can travel."

    jump cave_start


# ============================================================
# STARTING BRANCH
# ============================================================

label cave_start:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump cave_branch_1

        "Go right":
            jump heat_lizard_cave


# ============================================================
# HEAT LIZARD
# ============================================================

label heat_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "I enter a small chamber."

        if not heat_lizard_absorbed:
            n "Something small scurries across the stone."

        menu:

            "Go back":
                jump cave_start


    if not heat_lizard_absorbed:

        n "A small lizard is clinging to the cave wall."

        menu:

            "Absorb the lizard":

                $ heat_lizard_absorbed = True
                $ heat_resistance = True

                n "The lizard is absorbed."

                n "Acquired: Heat Resistance."

                jump heat_lizard_cave


            "Leave it alone":
                jump cave_start


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_start


# ============================================================
# BRANCH 1
# ============================================================

label cave_branch_1:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump cold_lizard_cave

        "Go right":
            jump cave_branch_2

        "Go back":
            jump cave_start


# ============================================================
# COLD LIZARD
# ============================================================

label cold_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "The air becomes noticeably colder."

        if not cold_lizard_absorbed:
            n "I hear something moving nearby."

        menu:

            "Go back":
                jump cave_branch_1


    if not cold_lizard_absorbed:

        n "A pale lizard rests against the cold stone."

        menu:

            "Absorb the lizard":

                $ cold_lizard_absorbed = True
                $ cold_resistance = True

                n "The lizard is absorbed."

                n "Acquired: Cold Resistance."

                jump cold_lizard_cave


            "Leave it alone":
                jump cave_branch_1


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_branch_1


# ============================================================
# MAIN THREE-WAY BRANCH
#
# The left route only becomes available after meeting Veldora.
# ============================================================

label cave_branch_2:

    call update_cave_view("LSR")

    menu:

        "Go left" if met_veldora:
            jump cave_part_2_start

        "Go forward":
            jump cave_branch_3

        "Go right":
            jump cave_branch_4

        "Go back":
            jump cave_branch_1


# ============================================================
# VELDORA ROUTE
# STRAIGHT 1
# ============================================================

label cave_branch_3:

    call update_cave_view("S")

    if not branch3_ore_absorbed:

        n "I come across a strange mineral cluster."

        menu:

            "Absorb the mineral":

                $ branch3_ore_absorbed = True
                $ magic_ore_clusters += 1

                n "The mineral cluster is absorbed."

                jump cave_branch_3


            "Leave it alone":
                pass


    menu:

        "Move forward":
            jump cave_branch_5

        "Go back":
            jump cave_branch_2


# ============================================================
# VELDORA ROUTE
# STRAIGHT 2
# ============================================================

label cave_branch_5:

    call update_cave_view("S")

    if not branch5_ore_absorbed:

        n "Another mineral cluster is nearby."

        menu:

            "Absorb the mineral":

                $ branch5_ore_absorbed = True
                $ magic_ore_clusters += 1

                n "The mineral cluster is absorbed."

                jump cave_branch_5


            "Leave it alone":
                pass


    menu:

        "Move forward":
            jump veldora_approach

        "Go back":
            jump cave_branch_3


# ============================================================
# VELDORA ROUTE
# STRAIGHT 3
# ============================================================

label veldora_approach:

    call update_cave_view("S")

    menu:

        "Move forward":
            jump veldora_chamber

        "Go back":
            jump cave_branch_5


# ============================================================
# VELDORA CHAMBER
# ============================================================

label veldora_chamber:

    call update_cave_view("D")

    if not met_veldora:

        call veldora_first_meeting

        jump veldora_chamber


    if not veldora_ore_absorbed:

        n "Behind where Veldora was resting are six enormous clusters of magic ore."

        menu:

            "Absorb the six clusters":

                $ veldora_ore_absorbed = True
                $ magic_ore_clusters += 6

                n "All six clusters are absorbed."

                jump veldora_chamber


            "Leave them alone":
                pass


    menu:

        "Go back":
            jump veldora_approach


# ============================================================
# VELDORA FIRST MEETING
# ============================================================

label veldora_first_meeting:

    scene cave_blind
    with fade

    n "Something feels different."

    n "There is an overwhelming presence directly ahead of me."

    pause 1.0

    v "KUHAHAHAHAHA!"

    v "You finally found me!"

    n "A voice suddenly echoes throughout the cavern."

    v "Very well! I shall grant you the ability to perceive your surroundings!"

    n "Something changes inside me."

    $ mana_perception = True
    $ telepathy = True

    n "Acquired: Mana Perception."

    n "Acquired: Telepathy."

    n "Veldora is stored within my Stomach."

    $ veldora_in_stomach = True
    $ met_veldora = True

    pause 1.0

    n "For the first time, the darkness disappears."

    scene cave_branch_d
    with dissolve

    show veldora dragon at veldora_large
    with dissolve

    n "I can see."

    pause 1.0

    n "A pathway I couldn't perceive before has also become visible."

    n "A new path has been unlocked."

    return


# ============================================================
# HERB BRANCH
# ============================================================

label cave_branch_4:

    call update_cave_view("LR")

    if not branch4_herbs_absorbed:

        n "Several strange medicinal plants grow along the cave floor."

        menu:

            "Absorb the Hipokute Herbs":

                $ branch4_herbs_absorbed = True
                $ hipokute_herb_clusters += 1

                n "The herbs are absorbed."

                jump cave_branch_4


            "Leave them":
                pass


    menu:

        "Go left":
            jump underground_lake_1

        "Go right":
            jump cave_branch_6

        "Go back":
            jump cave_branch_2


# ============================================================
# UNDERGROUND LAKE - LEFT
# ============================================================

label underground_lake_1:

    call update_lake_1_view

    if not lake1_herbs_absorbed:

        n "Hipokute Herbs grow near the water."

        menu:

            "Absorb the herbs":

                $ lake1_herbs_absorbed = True
                $ hipokute_herb_clusters += 1

                jump underground_lake_1


            "Leave them":
                pass


    menu:

        "Drink the water" if not water_manipulation:
            jump acquire_water_manipulation

        "Continue along the lake":
            jump underground_lake_2

        "Return to Branch 4":
            jump cave_branch_4


# ============================================================
# WATER MANIPULATION
# ============================================================

label acquire_water_manipulation:

    n "I approach the underground lake."

    n "I absorb some of the water."

    pause 1.0

    n "Something changes."

    $ water_manipulation = True

    n "Acquired: Water Manipulation."

    jump underground_lake_1


# ============================================================
# UNDERGROUND LAKE - RIGHT
# ============================================================

label underground_lake_2:

    call update_lake_2_view

    if mana_perception and not gecko_hint_seen:

        $ gecko_hint_seen = True

        n "Something suddenly moves across the cave wall."

        n "A small gecko."

        n "It notices me and immediately disappears into a crack."

        n "Its body seemed strangely adapted to this cave."

        n "Maybe other lizards like it have developed unusual resistances."


    if not lake2_herbs_absorbed:

        n "More Hipokute Herbs grow along the shore."

        menu:

            "Absorb the herbs":

                $ lake2_herbs_absorbed = True
                $ hipokute_herb_clusters += 1

                jump underground_lake_2


            "Leave them":
                pass


    menu:

        "Drink the water" if not water_manipulation:
            jump acquire_water_manipulation_right

        "Go back along the lake":
            jump underground_lake_1


label acquire_water_manipulation_right:

    n "I absorb some of the underground water."

    $ water_manipulation = True

    n "Acquired: Water Manipulation."

    jump underground_lake_2


# ============================================================
# BRANCH 6
# ============================================================

label cave_branch_6:

    call update_cave_view("LR")

    menu:

        "Go right":
            jump electric_lizard_cave

        "Go left":
            jump thunder_frog_area

        "Go back":
            jump cave_branch_4


# ============================================================
# ELECTRIC LIZARD
# ============================================================

label electric_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "I hear something moving quickly nearby."

        menu:

            "Go back":
                jump cave_branch_6


    if not electric_lizard_absorbed:

        n "A strange lizard crawls across the cave wall."

        n "Tiny sparks occasionally jump across its skin."

        menu:

            "Absorb it":

                $ electric_lizard_absorbed = True
                $ electricity_resistance = True

                n "The lizard is absorbed."

                n "Acquired: Electricity Resistance."

                jump electric_lizard_cave


            "Leave it alone":
                jump cave_branch_6


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_branch_6


# ============================================================
# THUNDER FROG
# ============================================================

label thunder_frog_area:

    call update_cave_view("D")

    if not thunder_frog_defeated:

        n "A large creature blocks the path."

        n "Electricity crackles across its body."

        n "Thunder Frog"

        n "It appears highly resistant to paralysis."

        menu:

            "Fight the Thunder Frog":
                jump thunder_frog_battle

            "Retreat":
                jump cave_branch_6


    else:

        n "The defeated Thunder Frog is gone."

        if not frog_herbs_absorbed:

            n "Three clusters of Hipokute Herbs surround the chamber."

            menu:

                "Absorb all three herb clusters":

                    $ frog_herbs_absorbed = True
                    $ hipokute_herb_clusters += 3

                    n "The herbs are absorbed."

                    jump thunder_frog_area


                "Leave them":
                    pass


        menu:

            "Return to Branch 6":
                jump cave_branch_6


label thunder_frog_battle:

    call battle_thunder_frog

    if _return == "won":

        n "The Thunder Frog has been defeated!"

        $ thunder_frog_defeated = True
        $ paralysis_resistance = True

        n "Acquired: Paralysis Resistance."

        jump thunder_frog_area


    elif _return == "ran":

        jump cave_branch_6


    else:

        n "I can't continue..."

        menu:

            "Try the battle again":
                jump thunder_frog_battle

            "Retreat to Branch 6":

                $ player_hp = player_max_hp

                jump cave_branch_6


# ============================================================
# PART 2
# ============================================================


# ============================================================
# PART 2 ENTRANCE
# ============================================================

label cave_part_2_start:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump tempest_serpent_area

        "Go right":
            jump part2_chasm_right

        "Go back":
            jump cave_branch_2


# ============================================================
# TEMPEST SERPENT
# ============================================================

label tempest_serpent_area:

    call update_cave_view("D")

    if not tempest_serpent_defeated:

        n "A massive serpent blocks the path."

        n "Its body shifts as it notices my presence."

        n "Tempest Serpent"

        n "Intrinsic Skill: Heat Source Perception."

        n "It appears capable of using Poison Breath."

        menu:

            "Fight the Tempest Serpent":

                call battle_enemy("tempest_serpent")

                if _return == "won":

                    $ tempest_serpent_defeated = True

                    n "The Tempest Serpent has been defeated."

                    jump tempest_serpent_area


                elif _return == "ran":
                    jump cave_part_2_start


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump tempest_serpent_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump cave_part_2_start


            "Retreat":
                jump cave_part_2_start


    else:

        n "The Tempest Serpent no longer blocks the passage."

        menu:

            "Go forward":
                jump part2_chasm_middle

            "Go back":
                jump cave_part_2_start


# ============================================================
# CHASM R
# RIGHTMOST CHASM
# ============================================================

label part2_chasm_right:

    scene cave_chasm_r

    menu:

        "Go left":

            $ spider_return_location = "right"

            jump black_spider_area


        "Go back":
            jump cave_part_2_start


# ============================================================
# CHASM S
# BLACK SPIDER
# ============================================================

label black_spider_area:

    scene cave_chasm_s

    if not black_spider_defeated:

        n "A large black spider crawls into my path."

        n "Black Spider"

        n "It produces two different kinds of thread."

        n "Sticky Thread and Steel Thread."

        menu:

            "Fight the Black Spider":

                call battle_enemy("black_spider")

                if _return == "won":

                    $ black_spider_defeated = True
                    $ chasm_thread_unlocked = True

                    n "The Black Spider has been defeated."

                    n "Some of its thread remains anchored across the chasm."

                    n "It looks strong enough to swing from."

                    jump black_spider_area


                elif _return == "ran":

                    if spider_return_location == "middle":
                        jump part2_chasm_middle

                    else:
                        jump part2_chasm_right


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump black_spider_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            if spider_return_location == "middle":
                                jump part2_chasm_middle

                            else:
                                jump part2_chasm_right


            "Retreat":

                if spider_return_location == "middle":
                    jump part2_chasm_middle

                else:
                    jump part2_chasm_right


    else:

        menu:

            "Swing across the chasm" if chasm_thread_unlocked:
                jump part2_across_chasm

            "Go left":
                jump part2_chasm_middle

            "Go right":
                jump part2_chasm_right


# ============================================================
# CHASM M
# MIDDLE CHASM
#
# Serpent route connects here.
# ============================================================

label part2_chasm_middle:

    scene cave_chasm_m

    menu:

        "Go left":
            jump giant_bat_area

        "Go right":

            $ spider_return_location = "middle"

            jump black_spider_area

        "Return through the serpent passage" if tempest_serpent_defeated:
            jump tempest_serpent_area


# ============================================================
# CHASM L
# GIANT BAT
# ============================================================

label giant_bat_area:

    scene cave_chasm_l

    if not giant_bat_defeated:

        n "Something large moves across the ceiling."

        n "A Giant Bat drops down in front of me."

        n "Giant Bat"

        n "Intrinsic Skills: Drain and Ultrasonic Waves."

        menu:

            "Fight the Giant Bat":

                call battle_enemy("giant_bat")

                if _return == "won":

                    $ giant_bat_defeated = True

                    n "The Giant Bat has been defeated."

                    jump giant_bat_area


                elif _return == "ran":
                    jump part2_chasm_middle


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump giant_bat_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_chasm_middle


            "Retreat":
                jump part2_chasm_middle


    else:

        n "The Giant Bat is gone."

        menu:

            "Go right":
                jump part2_chasm_middle


# ============================================================
# ACROSS THE CHASM
#
# For now this uses the Spider chasm artwork from the
# opposite side until you make a separate far-side image.
# ============================================================

label part2_across_chasm:

    scene cave_chasm_s

    n "I swing across the chasm using the spider's thread."

    menu:

        "Move forward":
            jump part2_final_branch

        "Swing back across":
            jump black_spider_area


# ============================================================
# FINAL BRANCH
# ============================================================

label part2_final_branch:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump evil_centipede_area

        "Go right":
            jump armorsaurus_area

        "Go back":
            jump part2_across_chasm


# ============================================================
# EVIL CENTIPEDE
# ============================================================

label evil_centipede_area:

    call update_cave_view("D")

    if not evil_centipede_defeated:

        n "A long armored creature crawls across the stone."

        n "Evil Centipede"

        n "Intrinsic Skill: Paralyzing Breath."

        menu:

            "Fight the Evil Centipede":

                call battle_enemy("evil_centipede")

                if _return == "won":

                    $ evil_centipede_defeated = True

                    n "The Evil Centipede has been defeated."

                    jump evil_centipede_area


                elif _return == "ran":
                    jump part2_final_branch


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump evil_centipede_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_final_branch


            "Retreat":
                jump part2_final_branch


    else:

        menu:

            "Move forward":
                jump veldora_cave_exit

            "Go back":
                jump part2_final_branch


# ============================================================
# ARMORSAURUS
# ============================================================

label armorsaurus_area:

    call update_cave_view("D")

    if not armorsaurus_defeated:

        n "A heavily armored monster blocks the tunnel."

        n "Armorsaurus"

        n "Intrinsic Skill: Body Armor."

        menu:

            "Fight the Armorsaurus":

                call battle_enemy("armorsaurus")

                if _return == "won":

                    $ armorsaurus_defeated = True

                    n "The Armorsaurus has been defeated."

                    jump armorsaurus_area


                elif _return == "ran":
                    jump part2_final_branch


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump armorsaurus_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_final_branch


            "Retreat":
                jump part2_final_branch


    else:

        menu:

            "Move forward":
                jump veldora_cave_exit

            "Go back":
                jump part2_final_branch


# ============================================================
# VELDORA CAVE EXIT
# ============================================================

label veldora_cave_exit:

    scene cave_exit_placeholder
    with dissolve

    $ current_region = "Veldoras_Cave"

    n "The tunnel begins to open up."

    n "Light is coming from somewhere ahead."

    n "The exit of Veldora's Cave is just beyond this point."

    menu:

        "Go back into Veldora's Cave":

            jump part2_final_branch


        "Step outside":

            $ current_region = "West_Jura"

            jump west_jura_start