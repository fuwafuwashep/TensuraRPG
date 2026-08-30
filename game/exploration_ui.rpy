# ============================================================
# EXPLORATION UI
# ============================================================


# ============================================================
# STORAGE
# ============================================================

screen storage_menu():

    modal True

    add "#00000070"


    frame:

        xalign 0.5
        yalign 0.5

        xsize 800
        ysize 760

        background "#D6D6D6F2"

        padding (30, 30)


        vbox:

            spacing 20


            hbox:

                xfill True


                text "STORAGE":

                    size 38
                    color "#202020"


                textbutton "X":

                    xalign 1.0

                    text_size 28
                    text_color "#202020"

                    background None

                    action Hide("storage_menu")



            null height 5


            # ------------------------------------------------
            # ONE LARGE STORAGE LIST.
            # NO CATEGORIES.
            # ------------------------------------------------

            viewport:

                xfill True
                ysize 610

                mousewheel True
                draggable True

                scrollbars "vertical"


                vbox:

                    xfill True
                    spacing 10


                    use storage_entry(
                        "Hipokute Herbs",
                        hipokute_herb_clusters
                    )


                    use storage_entry(
                        "Magic Ore",
                        magic_ore_clusters
                    )


                    # Add future items here.
                    #
                    # Example:
                    #
                    # use storage_entry(
                    #     "Healing Potion",
                    #     healing_potions
                    # )



screen storage_entry(item_name, amount):


    frame:

        xfill True
        yminimum 75

        background "#EEEEEE"

        padding (20, 14)


        hbox:

            xfill True


            # Placeholder item icon.

            frame:

                xsize 48
                ysize 48

                background "#B8B8B8"

                text "?":

                    size 24
                    color "#202020"

                    xalign 0.5
                    yalign 0.5


            null width 18


            text item_name:

                size 26
                color "#202020"

                yalign 0.5


            text "x[amount]":

                size 26
                color "#202020"

                xalign 1.0
                yalign 0.5



# ============================================================
# SKILLS
# ============================================================

screen skills_menu():

    modal True

    add "#00000070"


    frame:

        xalign 0.5
        yalign 0.5

        xsize 800
        ysize 760

        background "#D6D6D6F2"

        padding (30, 30)


        vbox:

            spacing 18


            hbox:

                xfill True


                text "SKILLS":

                    size 38
                    color "#202020"


                textbutton "X":

                    xalign 1.0

                    background None

                    text_size 28
                    text_color "#202020"

                    action Hide("skills_menu")



            viewport:

                xfill True
                ysize 620

                mousewheel True
                draggable True

                scrollbars "vertical"


                vbox:

                    xfill True
                    spacing 10


                    if mana_perception:

                        use skill_entry(
                            "Mana Perception",
                            "Allows perception of magicules and the surrounding world."
                        )


                    if telepathy:

                        use skill_entry(
                            "Telepathy",
                            "Allows direct mental communication."
                        )


                    if water_manipulation:

                        use skill_entry(
                            "Water Manipulation",
                            "Allows the use of Spirit Water Magic. Currently available: Water Blade."
                        )


                    if heat_resistance:

                        use skill_entry(
                            "Heat Resistance",
                            "Reduces the effects of extreme heat."
                        )


                    if cold_resistance:

                        use skill_entry(
                            "Cold Resistance",
                            "Reduces the effects of extreme cold."
                        )


                    if electricity_resistance:

                        use skill_entry(
                            "Electricity Resistance",
                            "Reduces damage from electricity."
                        )


                    if paralysis_resistance:

                        use skill_entry(
                            "Paralysis Resistance",
                            "Increases resistance to paralysis."
                        )



screen skill_entry(skill_name, description):


    frame:

        xfill True

        background "#EEEEEE"

        padding (18, 15)


        vbox:

            spacing 5


            text skill_name:

                size 27
                color "#202020"


            text description:

                size 20
                color "#555555"



# ============================================================
# MOVE / LOADOUT MENU
# ============================================================

screen loadout_menu():

    modal True

    add "#00000070"


    frame:

        xalign 0.5
        yalign 0.5

        xsize 950
        ysize 760

        background "#D6D6D6F2"

        padding (30, 30)


        vbox:

            spacing 20


            hbox:

                xfill True


                text "MOVE LOADOUT":

                    size 38
                    color "#202020"


                textbutton "X":

                    xalign 1.0

                    background None

                    text_size 28
                    text_color "#202020"

                    action Hide("loadout_menu")



            hbox:

                spacing 20


                # ============================================
                # AVAILABLE MOVES
                # ============================================

                frame:

                    xsize 425
                    ysize 610

                    background "#EEEEEE"

                    padding (20, 20)


                    vbox:

                        spacing 12


                        text "AVAILABLE":

                            size 27
                            color "#202020"


                        use move_display(
                            "Basic Attack",
                            "Physical"
                        )


                        if water_manipulation:

                            use move_display(
                                "Water Blade",
                                "Spirit Water Magic"
                            )


                        # Later, when you add more techniques:
                        #
                        # if water_manipulation:
                        #
                        #     use move_display(
                        #         "Water Bullet",
                        #         "Spirit Water Magic"
                        #     )



                # ============================================
                # EQUIPPED / SELECTED
                # ============================================

                frame:

                    xsize 425
                    ysize 610

                    background "#EEEEEE"

                    padding (20, 20)


                    vbox:

                        spacing 12


                        text "SELECTED":

                            size 27
                            color "#202020"


                        use move_display(
                            "Basic Attack",
                            "Physical"
                        )


                        if water_manipulation:

                            use move_display(
                                "Water Blade",
                                "Magic"
                            )


                        else:

                            use move_display(
                                "EMPTY",
                                ""
                            )


                        use move_display(
                            "EMPTY",
                            ""
                        )


                        use move_display(
                            "EMPTY",
                            ""
                        )



screen move_display(move_name, move_type):


    frame:

        xfill True
        yminimum 72

        background "#D0D0D0"

        padding (14, 10)


        hbox:

            spacing 12


            # Placeholder move icon.

            frame:

                xsize 45
                ysize 45

                background "#B3B3B3"

                text "?":

                    size 22
                    color "#202020"

                    xalign 0.5
                    yalign 0.5


            vbox:

                yalign 0.5


                text move_name:

                    size 23
                    color "#202020"


                if move_type:

                    text move_type:

                        size 16
                        color "#626262"