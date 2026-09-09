# ============================================================
# EXPLORATION UI
# ============================================================


# ============================================================
# STORAGE
# ============================================================

screen storage_menu():
    tag rpg_panel
    modal True
    zorder 200
    on "show" action Function(migrate_inventory_grid)
    on "hide" action Function(inventory_close_cleanup)
    key "game_menu" action [Function(inventory_close_cleanup), Hide("storage_menu")]
    use inventory_grid_screen([Function(inventory_close_cleanup), Hide("storage_menu")])


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

    tag rpg_panel
    zorder 200
    key "game_menu" action Hide("skills_menu")

    modal True

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

                        use skill_entry(skill_name, description)


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

    tag rpg_panel
    zorder 200
    key "game_menu" action Hide("loadout_menu")

    modal True


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
                sensitive move_name != "Basic Attack"


# ============================================================
# INVENTORY / CRAFTING SCREEN
# ============================================================

screen inventory_grid_screen(close_action):

    modal True
    zorder 250

    key "K_z" action Function(inventory_split_held_stack)

    add "#05080ED9"

    frame:
        align (0.5, 0.5)
        xysize (1800, 1010)
        background "#101A24F7"
        padding (28, 24)

        fixed:

            text "INVENTORY • STOMACH":
                xpos 30
                ypos 10
                size 42
                bold True
                color "#EDF6F4"

            textbutton "Inventory":
                xpos 650
                ypos 8
                xsize 180
                ysize 55
                action SetVariable("inventory_ui_tab", "inventory")

            textbutton "Craft":
                xpos 845
                ypos 8
                xsize 180
                ysize 55
                action SetVariable("inventory_ui_tab", "craft")

            textbutton "X":
                xpos 1670
                ypos 5
                xsize 60
                ysize 55
                action close_action


            if inventory_ui_tab == "inventory":

                $ _occupied = inventory_occupied_map()

                draggroup:

                    # All 98 droppable cells.
                    for slot_index in range(INVENTORY_SLOT_COUNT):
                        $ slot_col = slot_index % INVENTORY_COLS
                        $ slot_row = slot_index // INVENTORY_COLS
                        $ slot_x = 85 + slot_col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)
                        $ slot_y = 105 + slot_row * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)

                        drag:
                            drag_name ("inv_target_%d" % slot_index)
                            draggable False
                            droppable True
                            xpos slot_x
                            ypos slot_y
                            xsize INVENTORY_SLOT_SIZE
                            ysize INVENTORY_SLOT_SIZE
                            add "images/inventory_ui/inventory_slot.svg"

                    # Only anchor cells draw items; large items span several cells.
                    for anchor, entry in enumerate(inventory_slots):
                        if entry is not None:
                            $ item_id = entry["item"]
                            $ item_name = inventory_item_name(item_id)
                            $ footprint_w, footprint_h = inventory_item_footprint(item_id)
                            $ anchor_col = anchor % INVENTORY_COLS
                            $ anchor_row = anchor // INVENTORY_COLS
                            $ item_x = 85 + anchor_col * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)
                            $ item_y = 105 + anchor_row * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)
                            $ item_w = footprint_w * INVENTORY_SLOT_SIZE + (footprint_w - 1) * INVENTORY_SLOT_GAP
                            $ item_h = footprint_h * INVENTORY_SLOT_SIZE + (footprint_h - 1) * INVENTORY_SLOT_GAP
                            $ item_qty = entry["qty"]

                            drag:
                                drag_name ("inv_item_%d" % anchor)
                                draggable True
                                droppable False
                                drag_raise True
                                mouse_drop True
                                activated inventory_drag_activated
                                dragged inventory_item_dragged
                                xpos item_x
                                ypos item_y
                                xsize item_w
                                ysize item_h

                                frame:
                                    xsize item_w
                                    ysize item_h
                                    background Frame("images/inventory_ui/inventory_item.svg", 16, 16, 16, 16)
                                    padding (8, 8)

                                    $ item_font_size = 20 if footprint_w == 1 else 28

                                    text "[item_name]\n×[item_qty]":
                                        xalign 0.5
                                        yalign 0.5
                                        text_align 0.5
                                        size item_font_size
                                        color "#F2F7F8"

                text "Drag and drop to move stacks. While holding a stack, press Z to split it in half. Odd stacks give the larger half to your mouse (35 → 18 held, 17 left).":
                    xpos 85
                    ypos 875
                    xsize 1510
                    size 20
                    color "#B8CBD3"


            else:

                text "CRAFTING • Predator":
                    xpos 80
                    ypos 100
                    size 32
                    color "#9EDCCA"

                text "Drag Hipoutke Herb or Magic Ore from the material tray into any crafting square.":
                    xpos 80
                    ypos 145
                    xsize 1100
                    size 21
                    color "#C9D8DD"

                # Material tray background. The draggable stacks themselves live
                # in the DragGroup below.
                frame:
                    xpos 80
                    ypos 210
                    xsize 390
                    ysize 610
                    background "#172B35"
                    padding (18, 18)

                    text "MATERIALS":
                        xpos 10
                        ypos 5
                        size 27
                        color "#EDF6F4"

                draggroup:

                    # Material tray: real inventory stacks, shown here as draggable sources.
                    $ material_row = 0
                    for anchor, entry in enumerate(inventory_slots):
                        if entry is not None and entry["item"] in ("hipokute", "magic_ore"):
                            $ tray_name = inventory_item_name(entry["item"])
                            $ tray_qty = entry["qty"]
                            $ tray_y = 275 + material_row * 125

                            drag:
                                drag_name ("inv_item_%d" % anchor)
                                draggable True
                                droppable False
                                drag_raise True
                                mouse_drop True
                                activated inventory_drag_activated
                                dragged inventory_item_dragged
                                xpos 110
                                ypos tray_y
                                xsize 330
                                ysize 100

                                frame:
                                    xsize 330
                                    ysize 100
                                    background Frame("images/inventory_ui/inventory_item.svg", 16, 16, 16, 16)
                                    text "[tray_name]\n×[tray_qty]":
                                        align (0.5, 0.5)
                                        text_align 0.5
                                        size 22
                                        color "#F2F7F8"

                            $ material_row += 1

                    # 3 x 3 crafting grid.
                    for craft_index in range(9):
                        $ craft_col = craft_index % 3
                        $ craft_row = craft_index // 3
                        $ craft_x = 610 + craft_col * 115
                        $ craft_y = 265 + craft_row * 115

                        drag:
                            drag_name ("craft_target_%d" % craft_index)
                            draggable False
                            droppable True
                            xpos craft_x
                            ypos craft_y
                            xsize 100
                            ysize 100
                            add "images/inventory_ui/craft_slot.svg"

                    for craft_index, entry in enumerate(craft_slots):
                        if entry is not None:
                            $ craft_col = craft_index % 3
                            $ craft_row = craft_index // 3
                            $ craft_x = 610 + craft_col * 115
                            $ craft_y = 265 + craft_row * 115
                            $ craft_name = inventory_item_name(entry["item"])
                            $ craft_qty = entry["qty"]

                            drag:
                                drag_name ("craft_item_%d" % craft_index)
                                draggable True
                                droppable False
                                drag_raise True
                                mouse_drop True
                                activated inventory_drag_activated
                                dragged inventory_item_dragged
                                xpos craft_x
                                ypos craft_y
                                xsize 100
                                ysize 100

                                frame:
                                    xsize 100
                                    ysize 100
                                    background Frame("images/inventory_ui/inventory_item.svg", 16, 16, 16, 16)
                                    text "[craft_name]\n×[craft_qty]":
                                        align (0.5, 0.5)
                                        text_align 0.5
                                        size 16
                                        color "#F2F7F8"

                $ recipe_info = crafting_input_summary()

                frame:
                    xpos 1000
                    ypos 250
                    xsize 360
                    ysize 360
                    background "#172B35"
                    padding (22, 20)

                    vbox:
                        spacing 14

                        text "OUTPUT":
                            size 27
                            color "#EDF6F4"

                        if recipe_info is not None:
                            $ recipe_input, recipe_output, recipe_available = recipe_info
                            $ recipe_output_name = inventory_item_name(recipe_output)

                            text "[recipe_output_name]":
                                size 28
                                color "#9EDCCA"

                            text "Available: [recipe_available]":
                                size 21
                                color "#C8D7DC"

                            hbox:
                                spacing 8
                                textbutton "-" action Function(set_craft_quantity, craft_quantity - 1)
                                text "[craft_quantity]" size 25 yalign 0.5
                                textbutton "+" action Function(set_craft_quantity, craft_quantity + 1)

                            textbutton "Craft Selected":
                                xfill True
                                action Function(craft_output, craft_quantity)

                            textbutton "Craft All":
                                xfill True
                                action Function(craft_output, recipe_available)

                        else:
                            text "No valid recipe":
                                size 23
                                color "#97AAB1"

                        textbutton "Return All Materials":
                            xfill True
                            action Function(return_all_craft_materials)

                textbutton "Recipes":
                    xpos 1425
                    ypos 245
                    xsize 250
                    ysize 58
                    action ToggleVariable("inventory_show_recipes")

                if inventory_show_recipes:
                    frame:
                        xpos 1370
                        ypos 320
                        xsize 360
                        ysize 320
                        background "#172B35F5"
                        padding (20, 18)

                        vbox:
                            spacing 16
                            text "RECIPES":
                                size 28
                                color "#EDF6F4"
                            text "Hipoutke Herb anywhere\n→ Healing Blob ×1":
                                size 22
                                color "#9EDCCA"
                            text "Magic Ore anywhere\n→ Magisteel Cluster ×1":
                                size 22
                                color "#9EDCCA"
                            text "One material crafts one output. Use Craft Selected or Craft All.":
                                size 18
                                color "#B8CBD3"

                text "Z also splits a stack while you are dragging it here.":
                    xpos 610
                    ypos 720
                    size 20
                    color "#B8CBD3"
