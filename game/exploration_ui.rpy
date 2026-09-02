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

            viewport:

                xfill True
                ysize 610

                mousewheel True
                draggable True
                scrollbars "vertical"

                vbox:

                    xfill True
                    spacing 10

                    use storage_entry("Healing Blobs", healing_blobs)
                    use storage_entry("Berry Bundles", berry_bundles)
                    use storage_entry("Cattle Deer", cattle_deer_stored)
                    use storage_entry("Hipokute Herbs", hipokute_herb_clusters)
                    use storage_entry("Magic Ore", magic_ore_clusters)


screen storage_entry(item_name, amount):

    frame:

        xfill True
        yminimum 75

        background "#EEEEEE"
        padding (20, 14)

        hbox:

            xfill True

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

    $ sync_skill_moves()
    $ owned_skills = get_owned_skills()

    add "#00000070"

    frame:

        xalign 0.5
        yalign 0.5

        xsize 850
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

                    for skill_name, description in owned_skills:

                        if skill_name == "Keen Smell" and current_region == "West_Jura":

                            use skill_entry(
                                skill_name,
                                description,
                                [
                                    Hide("skills_menu"),
                                    Jump("west_jura_keen_smell_menu")
                                ],
                                "USE"
                            )

                        else:

                            use skill_entry(
                                skill_name,
                                description
                            )


screen skill_entry(
    skill_name,
    description,
    skill_action=None,
    action_text=""
):

    frame:

        xfill True
        background "#EEEEEE"
        padding (18, 15)

        hbox:

            xfill True
            spacing 15

            vbox:

                xsize 650
                spacing 5

                text skill_name:
                    size 27
                    color "#202020"

                text description:
                    size 20
                    color "#555555"

            if skill_action is not None:

                textbutton action_text:

                    yalign 0.5
                    xsize 100
                    ysize 48

                    background "#D0D0D0"
                    hover_background "#E4E4E4"

                    text_color "#202020"
                    text_hover_color "#000000"
                    text_xalign 0.5
                    text_yalign 0.5

                    action skill_action


# ============================================================
# MOVE LOADOUT
# ============================================================

screen loadout_menu():

    modal True

    $ sync_skill_moves()

    add "#00000070"

    frame:

        xalign 0.5
        yalign 0.5

        xsize 1120
        ysize 800

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

                    xsize 520
                    ysize 660
                    background "#EEEEEE"
                    padding (20, 20)

                    vbox:

                        spacing 12

                        text "AVAILABLE MOVES":
                            size 27
                            color "#202020"

                        viewport:

                            xfill True
                            ysize 585

                            mousewheel True
                            draggable True
                            scrollbars "vertical"

                            vbox:

                                xfill True
                                spacing 8

                                for move_name in unlocked_moves:
                                    use available_move_row(move_name)


                # ============================================
                # EQUIPPED MOVES
                # ============================================

                frame:

                    xsize 520
                    ysize 660
                    background "#EEEEEE"
                    padding (20, 20)

                    viewport:

                        xfill True
                        ysize 620

                        mousewheel True
                        draggable True
                        scrollbars "vertical"

                        vbox:

                            xfill True
                            spacing 12

                            use equipped_category_block("PHYSICAL", "physical", 3)
                            use equipped_category_block("AURA", "aura", 5)
                            use equipped_category_block("MAGIC", "magic", 5)
                            use equipped_category_block("SKILLS", "skills", 5)


screen available_move_row(move_name):

    $ move_data = MOVE_DATA[move_name]
    $ category_name = move_data["category"].upper()
    $ equipped = move_is_equipped(move_name)

    frame:

        xfill True
        yminimum 70
        background "#D0D0D0"
        padding (12, 10)

        hbox:

            xfill True
            spacing 10

            vbox:

                xsize 300

                text move_name:
                    size 22
                    color "#202020"

                text category_name:
                    size 15
                    color "#666666"

            if equipped:

                text "EQUIPPED":
                    size 17
                    color "#555555"
                    yalign 0.5

            else:

                textbutton "EQUIP":

                    xsize 100
                    ysize 42
                    yalign 0.5

                    background "#BEBEBE"
                    hover_background "#DADADA"

                    text_color "#202020"
                    text_xalign 0.5
                    text_yalign 0.5

                    action Function(equip_move, move_name)


screen equipped_category_block(title, category, limit):

    $ equipped_moves = get_equipped_moves(category, True)

    vbox:

        xfill True
        spacing 6

        text "[title]  [len(equipped_moves)] / [limit]":
            size 23
            color "#202020"

        if equipped_moves:

            for move_name in equipped_moves:
                use equipped_move_row(move_name)

        else:

            frame:
                xfill True
                ysize 48
                background "#D8D8D8"

                text "EMPTY":
                    size 19
                    color "#888888"
                    xalign 0.5
                    yalign 0.5


screen equipped_move_row(move_name):

    frame:

        xfill True
        yminimum 58
        background "#D0D0D0"
        padding (12, 8)

        hbox:

            xfill True

            text move_name:
                size 20
                color "#202020"
                yalign 0.5

            textbutton "REMOVE":

                xalign 1.0
                xsize 105
                ysize 40

                background "#BEBEBE"
                hover_background "#DADADA"

                text_size 15
                text_color "#202020"
                text_xalign 0.5
                text_yalign 0.5

                action Function(unequip_move, move_name)
