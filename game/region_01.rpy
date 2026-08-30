# ============================================================
# REGION 01
# VELDORA'S CAVE
# PART 1
# ============================================================


# ------------------------------------------------------------
# PLACEHOLDER BACKGROUNDS
# ------------------------------------------------------------

# Completely blind before Mana Perception.
image cave_blind = Solid("#000000")

# Placeholder for being able to see.
# Replace this with actual cave artwork later.
image cave_visible = Solid("#555555")


# ------------------------------------------------------------
# PLAYER ABILITIES
# ------------------------------------------------------------

default mana_perception = False
default telepathy = False

default water_manipulation = False

default heat_resistance = False
default cold_resistance = False
default electricity_resistance = False
default paralysis_resistance = False


# ------------------------------------------------------------
# STORY FLAGS
# ------------------------------------------------------------

default met_veldora = False
default veldora_in_stomach = False

default gecko_hint_seen = False


# ------------------------------------------------------------
# CREATURE FLAGS
# ------------------------------------------------------------

default heat_lizard_absorbed = False
default cold_lizard_absorbed = False
default electric_lizard_absorbed = False

default thunder_frog_defeated = False


# ------------------------------------------------------------
# RESOURCE FLAGS
# ------------------------------------------------------------

default branch3_ore_absorbed = False
default branch5_ore_absorbed = False

default veldora_ore_absorbed = False
default lake_cave_ore_absorbed = False

default branch4_herbs_absorbed = False
default lake1_herbs_absorbed = False
default lake2_herbs_absorbed = False
default lake3_herbs_absorbed = False
default frog_herbs_absorbed = False


# How many clusters you've absorbed.
default magic_ore_clusters = 0
default hipokute_herb_clusters = 0


# ------------------------------------------------------------
# BASIC COMBAT VARIABLES
# ------------------------------------------------------------

default player_max_hp = 30
default player_hp = 30

label update_cave_view:

    if mana_perception:
        scene cave_visible
    else:
        scene cave_blind

    return

label region_01_start:

    scene cave_blind
    with fade

    centered "Veldora's Cave"

    pause 1.0

    n "I can't see anything."

    n "I can only feel my immediate surroundings."

    n "There seems to be more than one direction I can travel."

    jump cave_start

label cave_start:

    call update_cave_view

    menu:

        "Go left":
            jump cave_branch_1

        "Go right":
            jump heat_lizard_cave

label heat_lizard_cave:

    call update_cave_view

    if not mana_perception:

        n "I enter a small chamber."

        if not heat_lizard_absorbed:
            n "Something small scurries across the stone."

        menu:

            "Go back":
                jump cave_start

    else:

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

label cave_branch_1:

    call update_cave_view

    menu:

        "Go left":
            jump cold_lizard_cave

        "Go right":
            jump cave_branch_2

        "Go back":
            jump cave_start

label cold_lizard_cave:

    call update_cave_view

    if not mana_perception:

        n "The air becomes noticeably colder."

        if not cold_lizard_absorbed:
            n "I hear something moving nearby."

        menu:

            "Go back":
                jump cave_branch_1

    else:

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

            menu:

                "Go back":
                    jump cave_branch_1

label cave_branch_2:

    call update_cave_view

    menu:

        "Go left" if met_veldora:
            jump cave_part_2_locked

        "Go forward":
            jump cave_branch_3

        "Go right":
            jump cave_branch_4

        "Go back":
            jump cave_branch_1

label cave_part_2_locked:

    n "This pathway leads deeper into the cave."

    n "Part 2 has not been implemented yet."

    jump cave_branch_2

label cave_branch_3:

    call update_cave_view

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

        "Go forward":
            jump cave_branch_5

        "Go back":
            jump cave_branch_2

label cave_branch_5:

    call update_cave_view

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

        "Go forward":
            jump veldora_chamber

        "Go back":
            jump cave_branch_3

label veldora_chamber:

    call update_cave_view

    if not met_veldora:

        call veldora_first_meeting

        jump veldora_chamber


    # --------------------------------------------------------
    # THREE MAGIC ORE CLUSTERS BEHIND VELDORA
    # --------------------------------------------------------

    if not veldora_ore_absorbed:

        n "Behind where Veldora was resting are three enormous clusters of magic ore."

        menu:

            "Absorb the three clusters":
                $ veldora_ore_absorbed = True
                $ magic_ore_clusters += 3

                n "All three clusters are absorbed."

                jump veldora_chamber

            "Leave them alone":
                pass


    menu:

        "Go back":
            jump cave_branch_5

label cave_branch_4:

    call update_cave_view

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

label underground_lake_1:

    call update_cave_view

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

label acquire_water_manipulation:

    n "I approach the underground lake."

    n "I absorb some of the water."

    pause 1.0

    n "Something changes."

    $ water_manipulation = True

    n "Acquired: Water Manipulation."

    jump underground_lake_1

label underground_lake_2:

    call update_cave_view

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
            jump acquire_water_manipulation_middle

        "Continue farther along the lake":
            jump underground_lake_3

        "Go back":
            jump underground_lake_1

label acquire_water_manipulation_middle:

    n "I absorb some of the underground water."

    $ water_manipulation = True

    n "Acquired: Water Manipulation."

    jump underground_lake_2

label underground_lake_3:

    call update_cave_view

    if not lake3_herbs_absorbed:

        n "Another patch of Hipokute Herbs grows nearby."

        menu:

            "Absorb the herbs":
                $ lake3_herbs_absorbed = True
                $ hipokute_herb_clusters += 1

                jump underground_lake_3

            "Leave them":
                pass


    menu:

        "Enter the cave on the left":
            jump lake_side_cave

        "Go back":
            jump underground_lake_2

label lake_side_cave:

    call update_cave_view


    # Gecko clue only happens when the player can actually see.

    if mana_perception and not gecko_hint_seen:

        $ gecko_hint_seen = True

        n "Something suddenly moves across the cave wall."

        n "A small gecko."

        n "It notices me and immediately disappears into a crack."

        n "Its body seemed strangely adapted to this cave."

        n "Maybe other lizards like it have developed unusual resistances."


    if not lake_cave_ore_absorbed:

        n "Three large magic ore clusters are embedded in the cave."

        menu:

            "Absorb all three clusters":
                $ lake_cave_ore_absorbed = True
                $ magic_ore_clusters += 3

                n "The three clusters are absorbed."

                jump lake_side_cave

            "Leave them":
                pass


    menu:

        "Return to the lake":
            jump underground_lake_3

label cave_branch_6:

    call update_cave_view

    menu:

        "Go right":
            jump electric_lizard_cave

        "Go left":
            jump thunder_frog_area

        "Go back":
            jump cave_branch_4

label electric_lizard_cave:

    call update_cave_view

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

label thunder_frog_area:

    call update_cave_view


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


    # ========================================================
    # PLAYER WON
    # ========================================================

    if _return == "won":

        n "The Thunder Frog has been defeated!"

        $ thunder_frog_defeated = True
        $ paralysis_resistance = True

        n "Acquired: Paralysis Resistance."

        jump thunder_frog_area


    # ========================================================
    # PLAYER RAN AWAY
    # ========================================================

    elif _return == "ran":

        jump cave_branch_6


    # ========================================================
    # PLAYER LOST
    # ========================================================

    else:

        n "I can't continue..."

        menu:

            "Try the battle again":

                jump thunder_frog_battle


            "Retreat to Branch 6":

                $ player_hp = player_max_hp

                jump cave_branch_6

