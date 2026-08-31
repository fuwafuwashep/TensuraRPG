# ============================================================
# REGION 01
# VELDORA'S CAVE
# PART 2
# ============================================================


# ============================================================
# TEMPORARY BACKGROUNDS
#
# Replace these when the Chasm and Exit artwork is finished.
# ============================================================

image cave_chasm_placeholder = Solid("#242424")
image cave_exit_placeholder = Solid("#555555")


# ============================================================
# PART 2 FLAGS
# ============================================================

default tempest_serpent_defeated = False
default black_spider_defeated = False
default giant_bat_defeated = False
default evil_centipede_defeated = False
default armorsaurus_defeated = False


# The spider leaves usable thread across the chasm after defeat.
default chasm_thread_unlocked = False


# Remembers which side the player approached the spider from.
default spider_entry_side = "right"


# ============================================================
# PART 2 START
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

                call battle_part2_enemy("tempest_serpent")


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

                jump part2_chasm_left


            "Go back":

                jump cave_part_2_start


# ============================================================
# CHASM - RIGHT SIDE
#
# Reached by taking the right path from the Part 2 entrance.
# ============================================================

label part2_chasm_right:


    scene cave_chasm_placeholder


    n "The path opens onto a massive underground chasm."


    menu:

        "Go left":

            $ spider_entry_side = "right"

            jump black_spider_area


        "Go back":

            jump cave_part_2_start


# ============================================================
# BLACK SPIDER
# ============================================================

label black_spider_area:


    call update_cave_view("D")


    if not black_spider_defeated:


        n "A large black spider crawls into my path."

        n "Black Spider"

        n "It produces two different kinds of thread."

        n "Sticky Thread and Steel Thread."


        menu:

            "Fight the Black Spider":

                call battle_part2_enemy("black_spider")


                if _return == "won":

                    $ black_spider_defeated = True
                    $ chasm_thread_unlocked = True


                    n "The Black Spider has been defeated."

                    n "Some of its thread remains anchored around the chasm."

                    n "It looks strong enough to swing from."


                    jump black_spider_area


                elif _return == "ran":


                    if spider_entry_side == "left":

                        jump part2_chasm_left

                    else:

                        jump part2_chasm_right


                else:


                    n "I can't continue..."


                    menu:

                        "Try again":

                            jump black_spider_area


                        "Retreat":

                            $ player_hp = player_max_hp


                            if spider_entry_side == "left":

                                jump part2_chasm_left

                            else:

                                jump part2_chasm_right


            "Retreat":


                if spider_entry_side == "left":

                    jump part2_chasm_left

                else:

                    jump part2_chasm_right


    else:


        menu:

            "Swing across the chasm" if chasm_thread_unlocked:

                jump part2_across_chasm


            "Go left":

                jump part2_chasm_left


            "Go right":

                jump part2_chasm_right


# ============================================================
# CHASM - LEFT SIDE OF SPIDER
#
# Serpent path and spider path connect here.
# ============================================================

label part2_chasm_left:


    scene cave_chasm_placeholder


    n "I stand along another section of the chasm."


    menu:

        "Go left":

            jump giant_bat_area


        "Go right":

            $ spider_entry_side = "left"

            jump black_spider_area


        "Go back through the serpent passage" if tempest_serpent_defeated:

            jump tempest_serpent_area


# ============================================================
# GIANT BAT
#
# Optional dead-end encounter.
# ============================================================

label giant_bat_area:


    call update_cave_view("D")


    if not giant_bat_defeated:


        n "Something large moves across the ceiling."

        n "A Giant Bat drops down in front of me."

        n "Giant Bat"

        n "Intrinsic Skills: Drain and Ultrasonic Waves."


        menu:

            "Fight the Giant Bat":

                call battle_part2_enemy("giant_bat")


                if _return == "won":

                    $ giant_bat_defeated = True

                    n "The Giant Bat has been defeated."

                    jump giant_bat_area


                elif _return == "ran":

                    jump part2_chasm_left


                else:

                    n "I can't continue..."


                    menu:

                        "Try again":

                            jump giant_bat_area


                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_chasm_left


            "Retreat":

                jump part2_chasm_left


    else:


        n "The chamber is quiet."


        menu:

            "Go back":

                jump part2_chasm_left


# ============================================================
# ACROSS THE CHASM
# ============================================================

label part2_across_chasm:


    scene cave_chasm_placeholder


    n "I swing across the chasm using the spider's thread."


    menu:

        "Move forward":

            jump part2_final_branch


        "Swing back across":

            $ spider_entry_side = "left"

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

                call battle_part2_enemy("evil_centipede")


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

                call battle_part2_enemy("armorsaurus")


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
# CAVE EXIT
#
# PLACEHOLDER UNTIL EXIT ART IS FINISHED.
# ============================================================

label veldora_cave_exit:


    scene cave_exit_placeholder
    with dissolve


    n "The tunnel begins to open up."

    n "Light is coming from somewhere ahead."

    n "The exit of Veldora's Cave is just beyond this point."


    menu:

        "Go back":

            jump part2_final_branch


        "Continue":

            n "The area beyond Veldora's Cave has not been implemented yet."

            jump veldora_cave_exit