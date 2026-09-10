# ============================================================
# GRID INVENTORY + CRAFTING OVERHAUL
# ============================================================
# 14 x 7 inventory, 100 px cells, 64 max stack.
# This file intentionally leaves the old inventory dictionary alive as a
# compatibility mirror so the rest of the existing project keeps working.


default inventory_slots = [None] * 98
default inventory_grid_migrated = False
default craft_slots = [None] * 9
default inventory_ui_tab = "inventory"
default inventory_show_recipes = False
default inventory_drag_source = None
default inventory_drag_held = None
default craft_quantity = 1


define INVENTORY_COLS = 14
define INVENTORY_ROWS = 7
define INVENTORY_SLOT_COUNT = 98
define INVENTORY_SLOT_SIZE = 100
define INVENTORY_SLOT_GAP = 8


init -4 python:

    import math
    import renpy.store as store

    # --------------------------------------------------------
    # ITEM DEFINITIONS
    # --------------------------------------------------------

    for _item_id, _item_data in ITEM_DATA.items():
        _item_data.setdefault("max_stack", 64 if _item_data.get("stackable", True) else 1)
        _item_data.setdefault("footprint", (1, 1))

    ITEM_DATA.setdefault("magisteel_cluster", {
        "name": "Magisteel Cluster",
        "description": "Magic Ore refined into a denser magical metal cluster.",
        "category": "Materials",
        "stackable": True,
        "max_stack": 64,
        "footprint": (1, 1),
    })

    ITEM_DATA.setdefault("bull_deer_male", {
        "name": "Bull Deer (Male)",
        "description": "A living male Bull Deer stored safely inside Stomach.",
        "category": "Special Items",
        "stackable": True,
        "max_stack": 64,
        "footprint": (2, 1),
    })

    ITEM_DATA.setdefault("bull_deer_female", {
        "name": "Bull Deer (Female)",
        "description": "A living female Bull Deer stored safely inside Stomach.",
        "category": "Special Items",
        "stackable": True,
        "max_stack": 64,
        "footprint": (2, 1),
    })

    # Explicitly lock the requested stack sizes / footprints.
    ITEM_DATA["hipokute"]["name"] = "Hipoutke Herb"
    ITEM_DATA["hipokute"]["max_stack"] = 64
    ITEM_DATA["magic_ore"]["max_stack"] = 64
    ITEM_DATA["cattle_deer"]["max_stack"] = 64


    # --------------------------------------------------------
    # BASIC GRID HELPERS
    # --------------------------------------------------------

    def inventory_item_footprint(item_id):
        return tuple(ITEM_DATA.get(item_id, {}).get("footprint", (1, 1)))


    def inventory_item_max_stack(item_id):
        data = ITEM_DATA[item_id]
        if not data.get("stackable", True):
            return 1
        return int(data.get("max_stack", 64))


    def inventory_anchor_cells(anchor, item_id):
        width, height = inventory_item_footprint(item_id)
        col = anchor % INVENTORY_COLS
        row = anchor // INVENTORY_COLS

        result = []
        for dy in range(height):
            for dx in range(width):
                result.append((row + dy) * INVENTORY_COLS + (col + dx))
        return result


    def inventory_occupied_map(ignore_anchor=None):
        occupied = {}
        for anchor, entry in enumerate(store.inventory_slots):
            if entry is None or anchor == ignore_anchor:
                continue
            for cell in inventory_anchor_cells(anchor, entry["item"]):
                occupied[cell] = anchor
        return occupied


    def inventory_anchor_covering(slot_index):
        return inventory_occupied_map().get(slot_index)


    def inventory_can_place(item_id, anchor, ignore_anchor=None):
        width, height = inventory_item_footprint(item_id)
        col = anchor % INVENTORY_COLS
        row = anchor // INVENTORY_COLS

        if col + width > INVENTORY_COLS or row + height > INVENTORY_ROWS:
            return False

        occupied = inventory_occupied_map(ignore_anchor=ignore_anchor)
        for cell in inventory_anchor_cells(anchor, item_id):
            if cell in occupied:
                return False
        return True


    def inventory_find_space(item_id, ignore_anchor=None):
        for index in range(INVENTORY_SLOT_COUNT):
            if inventory_can_place(item_id, index, ignore_anchor=ignore_anchor):
                return index
        return None


    def _sync_legacy_inventory():
        totals = {}
        for entry in store.inventory_slots:
            if entry is None:
                continue
            item_id = entry["item"]
            totals[item_id] = totals.get(item_id, 0) + int(entry["qty"])

        store.inventory.clear()
        store.inventory.update(totals)

        for item_id, variable_name in LEGACY_ITEMS.items():
            setattr(store, variable_name, totals.get(item_id, 0))


    def _add_item_to_grid(item_id, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            return True

        max_stack = inventory_item_max_stack(item_id)

        # Fill existing stacks first.
        for entry in store.inventory_slots:
            if entry is None or entry["item"] != item_id:
                continue
            if entry["qty"] >= max_stack:
                continue
            moved = min(quantity, max_stack - entry["qty"])
            entry["qty"] += moved
            quantity -= moved
            if quantity <= 0:
                return True

        # Create new stacks.
        while quantity > 0:
            anchor = inventory_find_space(item_id)
            if anchor is None:
                return False
            amount = min(quantity, max_stack)
            store.inventory_slots[anchor] = {"item": item_id, "qty": amount}
            quantity -= amount

        return True


    def migrate_inventory_grid():
        if store.inventory_grid_migrated:
            return True

        old_inventory = dict(store.inventory)
        store.inventory_slots = [None] * INVENTORY_SLOT_COUNT

        for item_id, quantity in old_inventory.items():
            if item_id not in ITEM_DATA or quantity <= 0:
                continue
            if not _add_item_to_grid(item_id, quantity):
                # This project currently has very little legacy inventory, but
                # do not destroy a save if a future one cannot fit.
                store.inventory_slots = [None] * INVENTORY_SLOT_COUNT
                return False

        store.inventory_grid_migrated = True
        _sync_legacy_inventory()
        return True


    # --------------------------------------------------------
    # COMPATIBILITY API
    # Replaces the old dict-only functions after core/inventory.rpy loads.
    # --------------------------------------------------------

    def item_count(item_id):
        if not store.inventory_grid_migrated:
            return int(store.inventory.get(item_id, 0))
        return sum(
            int(entry["qty"])
            for entry in store.inventory_slots
            if entry is not None and entry["item"] == item_id
        )


    def set_item_count(item_id, quantity):
        migrate_inventory_grid()
        quantity = max(0, int(quantity))

        snapshot = [dict(e) if e is not None else None for e in store.inventory_slots]

        for index, entry in enumerate(store.inventory_slots):
            if entry is not None and entry["item"] == item_id:
                store.inventory_slots[index] = None

        if quantity > 0 and not _add_item_to_grid(item_id, quantity):
            store.inventory_slots = snapshot
            _sync_legacy_inventory()
            return False

        _sync_legacy_inventory()
        return True


    def add_item(item_id, quantity=1):
        if item_id not in ITEM_DATA or quantity <= 0:
            return False

        migrate_inventory_grid()
        snapshot = [dict(e) if e is not None else None for e in store.inventory_slots]

        if not _add_item_to_grid(item_id, quantity):
            store.inventory_slots = snapshot
            _sync_legacy_inventory()
            renpy.notify("Not enough inventory space.")
            return False

        _sync_legacy_inventory()
        return True


    def add_item_group(entries):
        migrate_inventory_grid()
        snapshot = [dict(e) if e is not None else None for e in store.inventory_slots]

        for item_id, quantity in entries:
            if item_id not in ITEM_DATA or not _add_item_to_grid(item_id, quantity):
                store.inventory_slots = snapshot
                _sync_legacy_inventory()
                renpy.notify("Not enough inventory space.")
                return False

        _sync_legacy_inventory()
        return True


    def remove_item(item_id, quantity=1):
        if quantity <= 0:
            return False

        migrate_inventory_grid()
        quantity = int(quantity)
        if item_count(item_id) < quantity:
            return False

        remaining = quantity
        for index in range(INVENTORY_SLOT_COUNT - 1, -1, -1):
            entry = store.inventory_slots[index]
            if entry is None or entry["item"] != item_id:
                continue
            taken = min(remaining, entry["qty"])
            entry["qty"] -= taken
            remaining -= taken
            if entry["qty"] <= 0:
                store.inventory_slots[index] = None
            if remaining <= 0:
                break

        _sync_legacy_inventory()
        return True


    def can_use_item(item_id):
        if item_count(item_id) < 1:
            return False
        effect = ITEM_DATA[item_id].get("use", {})
        return (
            (effect.get("hp", 0) > 0 and store.player_hp < store.player_max_hp)
            or (effect.get("mp", 0) > 0 and store.player_mp < store.player_max_mp)
        )


    def use_item(item_id):
        if not can_use_item(item_id):
            return False
        effect = ITEM_DATA[item_id]["use"]
        remove_item(item_id)
        store.player_hp = min(store.player_max_hp, store.player_hp + effect.get("hp", 0))
        store.player_mp = min(store.player_max_mp, store.player_mp + effect.get("mp", 0))
        return True


    def refine_healing_blob():
        if has_skill("predator") and remove_item("hipokute"):
            add_item("healing_blob")
            renpy.notify("Refined one Healing Blob.")


    # --------------------------------------------------------
    # DRAG + DROP
    # --------------------------------------------------------

    def _copy_slots(slots):
        return [dict(e) if e is not None else None for e in slots]


    def inventory_drag_activated(drags):
        if not drags:
            return
        name = str(drags[0].drag_name)
        if name.startswith("inv_item_"):
            store.inventory_drag_source = ("inventory", int(name.rsplit("_", 1)[1]))
            store.inventory_drag_held = None
        elif name.startswith("craft_item_"):
            store.inventory_drag_source = ("craft", int(name.rsplit("_", 1)[1]))
            store.inventory_drag_held = None


    def inventory_restore_split():
        held = store.inventory_drag_held
        source = store.inventory_drag_source
        if held is None or source is None:
            store.inventory_drag_held = None
            return

        area, index = source
        slots = store.inventory_slots if area == "inventory" else store.craft_slots
        entry = slots[index]

        if entry is None:
            slots[index] = {"item": held["item"], "qty": held["qty"]}
        elif entry["item"] == held["item"]:
            entry["qty"] += held["qty"]

        store.inventory_drag_held = None
        if area == "inventory":
            _sync_legacy_inventory()


    def inventory_cancel_drag():
        inventory_restore_split()
        store.inventory_drag_source = None
        store.inventory_drag_held = None


    def inventory_split_held_stack():
        source = store.inventory_drag_source
        if source is None or store.inventory_drag_held is not None:
            return

        area, index = source
        slots = store.inventory_slots if area == "inventory" else store.craft_slots

        if index < 0 or index >= len(slots):
            return
        entry = slots[index]
        if entry is None or entry["qty"] <= 1:
            return

        original = int(entry["qty"])
        held_amount = int(math.ceil(original / 2.0))
        left_amount = original - held_amount

        entry["qty"] = left_amount
        store.inventory_drag_held = {"item": entry["item"], "qty": held_amount}

        if left_amount <= 0:
            slots[index] = None

        if area == "inventory":
            _sync_legacy_inventory()

        renpy.notify("Holding %d. %d left behind." % (held_amount, left_amount))


    def _source_entry(area, index):
        slots = store.inventory_slots if area == "inventory" else store.craft_slots
        if 0 <= index < len(slots):
            return slots[index]
        return None


    def _put_into_craft(item_id, quantity, target_index):
        if item_id not in ("hipokute", "magic_ore"):
            return 0
        if not (0 <= target_index < 9):
            return 0

        target = store.craft_slots[target_index]
        max_stack = inventory_item_max_stack(item_id)

        if target is None:
            moved = min(quantity, max_stack)
            store.craft_slots[target_index] = {"item": item_id, "qty": moved}
            return moved

        if target["item"] != item_id:
            return 0

        moved = min(quantity, max_stack - target["qty"])
        target["qty"] += moved
        return moved


    def _put_into_inventory(item_id, quantity, target_index, ignore_anchor=None):
        target_anchor = inventory_anchor_covering(target_index)
        max_stack = inventory_item_max_stack(item_id)

        if target_anchor is not None and target_anchor != ignore_anchor:
            target = store.inventory_slots[target_anchor]
            if target["item"] != item_id:
                return 0
            moved = min(quantity, max_stack - target["qty"])
            target["qty"] += moved
            return moved

        if not inventory_can_place(item_id, target_index, ignore_anchor=ignore_anchor):
            return 0

        moved = min(quantity, max_stack)
        store.inventory_slots[target_index] = {"item": item_id, "qty": moved}
        return moved


    def inventory_item_dragged(drags, drop):
        source = store.inventory_drag_source
        if source is None or not drags:
            return

        if drop is None:
            inventory_restore_split()
            store.inventory_drag_source = None
            return

        drop_name = str(drop.drag_name)
        if drop_name.startswith("inv_target_"):
            target_area = "inventory"
            target_index = int(drop_name.rsplit("_", 1)[1])
        elif drop_name.startswith("craft_target_"):
            target_area = "craft"
            target_index = int(drop_name.rsplit("_", 1)[1])
        else:
            inventory_restore_split()
            store.inventory_drag_source = None
            return

        source_area, source_index = source
        source_slots = store.inventory_slots if source_area == "inventory" else store.craft_slots
        source_entry = _source_entry(source_area, source_index)

        held = store.inventory_drag_held
        if held is not None:
            item_id = held["item"]
            moving_qty = int(held["qty"])
            split_move = True
        else:
            if source_entry is None:
                store.inventory_drag_source = None
                return
            item_id = source_entry["item"]
            moving_qty = int(source_entry["qty"])
            split_move = False

        inv_snapshot = _copy_slots(store.inventory_slots)
        craft_snapshot = _copy_slots(store.craft_slots)

        ignore_anchor = None
        if source_area == "inventory" and not split_move:
            ignore_anchor = source_index
            # Temporarily remove it so its footprint does not block the new spot.
            source_slots[source_index] = None

        if source_area == "craft" and not split_move:
            source_slots[source_index] = None

        if target_area == "inventory":
            moved = _put_into_inventory(item_id, moving_qty, target_index, ignore_anchor=ignore_anchor)
        else:
            moved = _put_into_craft(item_id, moving_qty, target_index)

        if moved <= 0:
            store.inventory_slots = inv_snapshot
            store.craft_slots = craft_snapshot
            store.inventory_drag_held = None
            store.inventory_drag_source = None
            _sync_legacy_inventory()
            return

        leftover = moving_qty - moved

        if split_move:
            # The split amount was already removed from the original stack.
            if leftover > 0:
                original = _source_entry(source_area, source_index)
                if original is None:
                    source_slots = store.inventory_slots if source_area == "inventory" else store.craft_slots
                    source_slots[source_index] = {"item": item_id, "qty": leftover}
                else:
                    original["qty"] += leftover
        else:
            if leftover > 0:
                source_slots = store.inventory_slots if source_area == "inventory" else store.craft_slots
                source_slots[source_index] = {"item": item_id, "qty": leftover}

        store.inventory_drag_held = None
        store.inventory_drag_source = None
        _sync_legacy_inventory()


    # --------------------------------------------------------
    # CRAFTING
    # --------------------------------------------------------

    def crafting_input_summary():
        present = [e for e in store.craft_slots if e is not None and e["qty"] > 0]
        if not present:
            return None

        first_item = present[0]["item"]
        if any(e["item"] != first_item for e in present):
            return None

        if first_item == "hipokute":
            output = "healing_blob"
        elif first_item == "magic_ore":
            output = "magisteel_cluster"
        else:
            return None

        total = sum(int(e["qty"]) for e in present)
        return first_item, output, total


    def set_craft_quantity(value):
        info = crafting_input_summary()
        max_value = info[2] if info else 1
        store.craft_quantity = max(1, min(int(value), max_value))


    def _consume_craft_material(item_id, quantity):
        remaining = int(quantity)
        for index in range(8, -1, -1):
            entry = store.craft_slots[index]
            if entry is None or entry["item"] != item_id:
                continue
            taken = min(remaining, entry["qty"])
            entry["qty"] -= taken
            remaining -= taken
            if entry["qty"] <= 0:
                store.craft_slots[index] = None
            if remaining <= 0:
                return True
        return remaining <= 0


    def craft_output(quantity):
        info = crafting_input_summary()
        if info is None:
            return False

        input_item, output_item, available = info
        amount = max(1, min(int(quantity), available))

        inv_snapshot = _copy_slots(store.inventory_slots)
        craft_snapshot = _copy_slots(store.craft_slots)

        if not _consume_craft_material(input_item, amount):
            return False

        if not add_item(output_item, amount):
            store.inventory_slots = inv_snapshot
            store.craft_slots = craft_snapshot
            _sync_legacy_inventory()
            return False

        store.craft_quantity = 1
        renpy.notify("Crafted %d x %s." % (amount, ITEM_DATA[output_item]["name"]))
        return True


    def return_all_craft_materials():
        for index in range(9):
            entry = store.craft_slots[index]
            if entry is None:
                continue
            item_id = entry["item"]
            quantity = entry["qty"]
            if add_item(item_id, quantity):
                store.craft_slots[index] = None
    
    def inventory_close_cleanup():

        inventory_cancel_drag()
        return_all_craft_materials()

        store.inventory_ui_tab = "inventory"
        store.inventory_show_recipes = False
        store.craft_quantity = 1

        _sync_legacy_inventory()

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

            text "INVENTORY":
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
                            $ item_name = ITEM_DATA[item_id]["name"]
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
                            $ tray_name = ITEM_DATA[entry["item"]]["name"]
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
                            $ craft_name = ITEM_DATA[entry["item"]]["name"]
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
                            $ recipe_output_name = ITEM_DATA[recipe_output]["name"]

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
