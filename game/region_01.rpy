# ============================================================
# REGION 01
# VELDORA'S CAVE
# PART 1
# ============================================================


# ============================================================
# BACKGROUNDS
# ============================================================

# Completely blind.
image cave_blind = Solid("#000000")


# ------------------------------------------------------------
# NORMAL CAVE BACKGROUNDS
# ------------------------------------------------------------

# Dead End
image cave_branch_d = "images/backgrounds/VeldoracaveBranchD.png"

# Left / Right
image cave_branch_lr = "images/backgrounds/VeldoracaveBranchLR.png"

# Left / Straight / Right
image cave_branch_lsr = "images/backgrounds/VeldoracaveBranchLSR.png"

# Straight
image cave_branch_s = "images/backgrounds/VeldoracaveBranchS.png"

# Straight while blind / gray
image cave_branch_sg = "images/backgrounds/VeldoracaveBranchSG.png"


# ------------------------------------------------------------
# LAKE BACKGROUNDS
# ------------------------------------------------------------

# With herbs
image cave_lake_1 = "images/backgrounds/VeldoracaveLake1.png"
image cave_lake_2 = "images/backgrounds/VeldoracaveLake2.png"

# After herbs have been absorbed
image cave_lake_empty_1 = "images/backgrounds/VeldoracaveLakeEmpty1.png"
image cave_lake_empty_2 = "images/backgrounds/VeldoracaveLakeEmpty2.png"


# ------------------------------------------------------------
# COMPATIBILITY
#
# Your Veldora cutscene currently uses "scene cave_visible".
# Keep this so that cutscene does not break.
# ------------------------------------------------------------

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
# CREATURE FLAGS
# ============================================================

default heat_lizard_absorbed = False
default cold_lizard_absorbed = False
default electric_lizard_absorbed = False

default thunder_frog_defeated = False


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
# COMBAT VARIABLES
# ============================================================

default player_max_hp = 30
default player_hp = 30


# ============================================================
# BACKGROUND HELPER
# ============================================================

label update_cave_view(view_type="D"):


    # --------------------------------------------------------
    # BEFORE MANA PERCEPTION
    # --------------------------------------------------------

    if not mana_perception:

        # The straight route toward Veldora is visible only as
        # the gray/blind version.

        if view_type == "S":

            scene cave_branch_sg

        else:

            scene cave_blind

        return


    # --------------------------------------------------------
    # AFTER MANA PERCEPTION
    # --------------------------------------------------------

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


# ============================================================
# LAKE BACKGROUND HELPERS
# ============================================================

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
# REGION START
# ============================================================

label region_01_start:


    scene cave_blind
    with fade


    centered "Veldora's Cave"


    pause 1.0


    n "I can't see anything."

    n "I can only feel my immediate surroundings."

    n "There seems to be more than one direction I can travel."


    jump cave_start


# ============================================================
# START
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


            n "The chamber is empty."


            menu:

                "Go back":

                    jump cave_branch_1


# ============================================================
# BRANCH 2
#
# LEFT DOES NOT EXIST TO THE PLAYER UNTIL VELDORA IS MET.
# ============================================================

label cave_branch_2:


    call update_cave_view("LSR")


    menu:

        "Go left" if met_veldora:

            jump cave_part_2_locked


        "Go forward":

            jump cave_branch_3


        "Go right":

            jump cave_branch_4


        "Go back":

            jump cave_branch_1


# ============================================================
# PART 2
# ============================================================

label cave_part_2_locked:

    call update_cave_view("S")


    n "This pathway leads deeper into the cave."

    jump cave_part_2_start


# ============================================================
# VELDORA ROUTE
#
# THREE STRAIGHT PANELS BEFORE VELDORA
# ============================================================


# ------------------------------------------------------------
# STRAIGHT 1
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# STRAIGHT 2
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# STRAIGHT 3
# ------------------------------------------------------------

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


    # --------------------------------------------------------
    # MAGIC ORE
    #
    # Originally 3 here and 3 near the lake.
    # Lake ore was removed, so all 6 are now here.
    # --------------------------------------------------------

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
# BRANCH 4
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
# UNDERGROUND LAKE
#
# ONLY TWO PANELS NOW.
# ============================================================


# ------------------------------------------------------------
# LAKE PANEL 1
# ------------------------------------------------------------

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
# WATER MANIPULATION - LAKE 1
# ============================================================

label acquire_water_manipulation:


    n "I approach the underground lake."

    n "I absorb some of the water."


    pause 1.0


    n "Something changes."


    $ water_manipulation = True


    n "Acquired: Water Manipulation."


    jump underground_lake_1


# ------------------------------------------------------------
# LAKE PANEL 2
# RIGHT SIDE OF LAKE
# ------------------------------------------------------------

label underground_lake_2:


    call update_lake_2_view


    # --------------------------------------------------------
    # GECKO HINT
    #
    # Now happens here instead of in a separate lake cave.
    # --------------------------------------------------------

    if mana_perception and not gecko_hint_seen:


        $ gecko_hint_seen = True


        n "Something suddenly moves across the cave wall."

        n "A small gecko."

        n "It notices me and immediately disappears into a crack."

        n "Its body seemed strangely adapted to this cave."

        n "Maybe other lizards like it have developed unusual resistances."


    # --------------------------------------------------------
    # HERBS
    # --------------------------------------------------------

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


# ============================================================
# WATER MANIPULATION - LAKE 2
# ============================================================

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
# THUNDER FROG AREA
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


# ============================================================
# THUNDER FROG BATTLE
# ============================================================

label thunder_frog_battle:


    call battle_thunder_frog


    # --------------------------------------------------------
    # WIN
    # --------------------------------------------------------

    if _return == "won":


        n "The Thunder Frog has been defeated!"


        $ thunder_frog_defeated = True
        $ paralysis_resistance = True


        n "Acquired: Paralysis Resistance."


        jump thunder_frog_area


    # --------------------------------------------------------
    # RAN
    # --------------------------------------------------------

    elif _return == "ran":


        jump cave_branch_6


    # --------------------------------------------------------
    # LOST
    # --------------------------------------------------------

    else:


        n "I can't continue..."


        menu:

            "Try the battle again":

                jump thunder_frog_battle


            "Retreat to Branch 6":

                $ player_hp = player_max_hp

                jump cave_branch_6