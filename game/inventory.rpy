# ============================================================
# INVENTORY / STOMACH
# ============================================================
# 14 x 7 grid, 100 px cells, 64 item stacks.
# The old inventory dictionary is kept synchronized so the rest of the
# existing battle, gift, and story systems continue to work.


default inventory = {}
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


init -10 python:

    import math
    import renpy.store as store


    # ========================================================
    # ITEM HELPERS
    # ========================================================

    def inventory_item_footprint(item_id):
        return tuple(ITEM_DATA.get(item_id, {}).get("footprint", (1, 1)))


    def inventory_item_max_stack(item_id):
        data = ITEM_DATA[item_id]

        if not data.get("stackable", True):
            return 1

        return int(data.get("max_stack", 64))


    def inventory_item_name(item_id):

        if item_id == "storm_dragon":
            return getattr(store, "storm_dragon_display_name", "Storm Dragon")

        return ITEM_DATA[item_id]["name"]


    def inventory_anchor_cells(anchor, item_id):

        width, height = inventory_item_footprint(item_id)
        col = anchor % INVENTORY_COLS
        row = anchor // INVENTORY_COLS

        result = []

        for dy in range(height):
            for dx in range(width):
                result.append(
                    (row + dy) * INVENTORY_COLS + (col + dx)
                )

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

        if col + width > INVENTORY_COLS:
            return False

        if row + height > INVENTORY_ROWS:
            return False

        occupied = inventory_occupied_map(ignore_anchor=ignore_anchor)

        for cell in inventory_anchor_cells(anchor, item_id):

            if cell in occupied:
                return False

        return True


    def inventory_find_space(item_id, ignore_anchor=None):

        for index in range(INVENTORY_SLOT_COUNT):

            if inventory_can_place(
                item_id,
                index,
                ignore_anchor=ignore_anchor
            ):
                return index

        return None


    # ========================================================
    # LEGACY DICTIONARY SYNCHRONIZATION
    # ========================================================

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

            if entry is None:
                continue

            if entry["item"] != item_id:
                continue

            if entry["qty"] >= max_stack:
                continue

            moved = min(
                quantity,
                max_stack - entry["qty"]
            )

            entry["qty"] += moved
            quantity -= moved

            if quantity <= 0:
                return True

        # Make new stacks when needed.
        while quantity > 0:

            anchor = inventory_find_space(item_id)

            if anchor is None:
                return False

            amount = min(quantity, max_stack)

            store.inventory_slots[anchor] = {
                "item": item_id,
                "qty": amount,
            }

            quantity -= amount

        return True


    def migrate_inventory_grid():

        if store.inventory_grid_migrated:
            return True

        old_inventory = dict(store.inventory)

        store.inventory_slots = [None] * INVENTORY_SLOT_COUNT

        for item_id, quantity in old_inventory.items():

            if item_id not in ITEM_DATA:
                continue

            if quantity <= 0:
                continue

            if not _add_item_to_grid(item_id, quantity):

                store.inventory_slots = [None] * INVENTORY_SLOT_COUNT
                return False

        store.inventory_grid_migrated = True

        _sync_legacy_inventory()

        return True


    # ========================================================
    # NORMAL INVENTORY API
    # ========================================================

    def item_count(item_id):

        if not store.inventory_grid_migrated:
            return int(store.inventory.get(item_id, 0))

        return sum(
            int(entry["qty"])
            for entry in store.inventory_slots
            if entry is not None and entry["item"] == item_id
        )


    def set_item_count(item_id, quantity):

        if item_id not in ITEM_DATA:
            return False

        migrate_inventory_grid()

        quantity = max(0, int(quantity))

        snapshot = [
            dict(entry) if entry is not None else None
            for entry in store.inventory_slots
        ]

        for index, entry in enumerate(store.inventory_slots):

            if entry is not None and entry["item"] == item_id:
                store.inventory_slots[index] = None

        if quantity > 0:

            if not _add_item_to_grid(item_id, quantity):

                store.inventory_slots = snapshot
                _sync_legacy_inventory()

                return False

        _sync_legacy_inventory()

        return True


    def add_item(item_id, quantity=1):

        if item_id not in ITEM_DATA:
            return False

        quantity = int(quantity)

        if quantity <= 0:
            return False

        migrate_inventory_grid()

        snapshot = [
            dict(entry) if entry is not None else None
            for entry in store.inventory_slots
        ]

        if not _add_item_to_grid(item_id, quantity):

            store.inventory_slots = snapshot
            _sync_legacy_inventory()

            renpy.notify("Not enough inventory space.")

            return False

        _sync_legacy_inventory()

        return True


    def add_item_group(entries):

        migrate_inventory_grid()

        snapshot = [
            dict(entry) if entry is not None else None
            for entry in store.inventory_slots
        ]

        for item_id, quantity in entries:

            if item_id not in ITEM_DATA:

                store.inventory_slots = snapshot
                _sync_legacy_inventory()

                return False

            if not _add_item_to_grid(item_id, quantity):

                store.inventory_slots = snapshot
                _sync_legacy_inventory()

                renpy.notify("Not enough inventory space.")

                return False

        _sync_legacy_inventory()

        return True


    def remove_item(item_id, quantity=1):

        quantity = int(quantity)

        if quantity <= 0:
            return False

        migrate_inventory_grid()

        if item_count(item_id) < quantity:
            return False

        remaining = quantity

        for index in range(INVENTORY_SLOT_COUNT - 1, -1, -1):

            entry = store.inventory_slots[index]

            if entry is None:
                continue

            if entry["item"] != item_id:
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


    # ========================================================
    # USABLE ITEMS
    # ========================================================

    def can_use_item(item_id):

        if item_count(item_id) < 1:
            return False

        effect = ITEM_DATA[item_id].get("use", {})

        return (
            (
                effect.get("hp", 0) > 0
                and store.player_hp < store.player_max_hp
            )
            or
            (
                effect.get("mp", 0) > 0
                and store.player_mp < store.player_max_mp
            )
        )


    def use_item(item_id):

        if not can_use_item(item_id):
            return False

        effect = ITEM_DATA[item_id]["use"]

        remove_item(item_id)

        store.player_hp = min(
            store.player_max_hp,
            store.player_hp + effect.get("hp", 0)
        )

        store.player_mp = min(
            store.player_max_mp,
            store.player_mp + effect.get("mp", 0)
        )

        return True


    # Kept for compatibility with the old inventory button.
    def refine_healing_blob():

        if has_skill("predator") and remove_item("hipokute"):

            add_item("healing_blob")

            renpy.notify("Crafted one Healing Blob.")


    # ========================================================
    # DRAG / DROP HELPERS
    # ========================================================

    def _copy_slots(slots):

        return [
            dict(entry) if entry is not None else None
            for entry in slots
        ]


    def inventory_drag_activated(drags):

        if not drags:
            return

        name = str(drags[0].drag_name)

        if name.startswith("inv_item_"):

            store.inventory_drag_source = (
                "inventory",
                int(name.rsplit("_", 1)[1])
            )

            store.inventory_drag_held = None

        elif name.startswith("craft_item_"):

            store.inventory_drag_source = (
                "craft",
                int(name.rsplit("_", 1)[1])
            )

            store.inventory_drag_held = None


    def inventory_restore_split():

        held = store.inventory_drag_held
        source = store.inventory_drag_source

        if held is None or source is None:

            store.inventory_drag_held = None
            return

        area, index = source

        slots = (
            store.inventory_slots
            if area == "inventory"
            else store.craft_slots
        )

        entry = slots[index]

        if entry is None:

            slots[index] = {
                "item": held["item"],
                "qty": held["qty"],
            }

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

        if source is None:
            return

        if store.inventory_drag_held is not None:
            return

        area, index = source

        slots = (
            store.inventory_slots
            if area == "inventory"
            else store.craft_slots
        )

        if index < 0 or index >= len(slots):
            return

        entry = slots[index]

        if entry is None:
            return

        if entry["qty"] <= 1:
            return

        original = int(entry["qty"])

        held_amount = int(math.ceil(original / 2.0))
        left_amount = original - held_amount

        entry["qty"] = left_amount

        store.inventory_drag_held = {
            "item": entry["item"],
            "qty": held_amount,
        }

        if left_amount <= 0:
            slots[index] = None

        if area == "inventory":
            _sync_legacy_inventory()

        renpy.notify(
            "Holding %d. %d left behind."
            % (held_amount, left_amount)
        )


    def _source_entry(area, index):

        slots = (
            store.inventory_slots
            if area == "inventory"
            else store.craft_slots
        )

        if 0 <= index < len(slots):
            return slots[index]

        return None


    def _put_into_craft(item_id, quantity, target_index):

        if item_id not in ("hipokute", "magic_ore"):
            return 0

        if not 0 <= target_index < 9:
            return 0

        target = store.craft_slots[target_index]
        max_stack = inventory_item_max_stack(item_id)

        if target is None:

            moved = min(quantity, max_stack)

            store.craft_slots[target_index] = {
                "item": item_id,
                "qty": moved,
            }

            return moved

        if target["item"] != item_id:
            return 0

        moved = min(
            quantity,
            max_stack - target["qty"]
        )

        target["qty"] += moved

        return moved


    def _put_into_inventory(
        item_id,
        quantity,
        target_index,
        ignore_anchor=None
    ):

        target_anchor = inventory_anchor_covering(target_index)
        max_stack = inventory_item_max_stack(item_id)

        if target_anchor is not None and target_anchor != ignore_anchor:

            target = store.inventory_slots[target_anchor]

            if target["item"] != item_id:
                return 0

            moved = min(
                quantity,
                max_stack - target["qty"]
            )

            target["qty"] += moved

            return moved

        if not inventory_can_place(
            item_id,
            target_index,
            ignore_anchor=ignore_anchor
        ):
            return 0

        moved = min(quantity, max_stack)

        store.inventory_slots[target_index] = {
            "item": item_id,
            "qty": moved,
        }

        return moved


    def inventory_item_dragged(drags, drop):

        if not drags:
            return

        drag_name = str(drags[0].drag_name)

        if drag_name.startswith("inv_item_"):

            source = (
                "inventory",
                int(drag_name.rsplit("_", 1)[1])
            )

        elif drag_name.startswith("craft_item_"):

            source = (
                "craft",
                int(drag_name.rsplit("_", 1)[1])
            )

        else:
            return

        store.inventory_drag_source = source

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

        source_slots = (
            store.inventory_slots
            if source_area == "inventory"
            else store.craft_slots
        )

        source_entry = _source_entry(
            source_area,
            source_index
        )

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

        inventory_snapshot = _copy_slots(store.inventory_slots)
        craft_snapshot = _copy_slots(store.craft_slots)

        ignore_anchor = None

        if source_area == "inventory" and not split_move:

            ignore_anchor = source_index
            source_slots[source_index] = None

        elif source_area == "craft" and not split_move:

            source_slots[source_index] = None

        if target_area == "inventory":

            moved = _put_into_inventory(
                item_id,
                moving_qty,
                target_index,
                ignore_anchor=ignore_anchor
            )

        else:

            moved = _put_into_craft(
                item_id,
                moving_qty,
                target_index
            )

        if moved <= 0:

            store.inventory_slots = inventory_snapshot
            store.craft_slots = craft_snapshot

            store.inventory_drag_held = None
            store.inventory_drag_source = None

            _sync_legacy_inventory()

            return

        leftover = moving_qty - moved

        if split_move:

            if leftover > 0:

                original = _source_entry(
                    source_area,
                    source_index
                )

                source_slots = (
                    store.inventory_slots
                    if source_area == "inventory"
                    else store.craft_slots
                )

                if original is None:

                    source_slots[source_index] = {
                        "item": item_id,
                        "qty": leftover,
                    }

                else:
                    original["qty"] += leftover

        elif leftover > 0:

            source_slots = (
                store.inventory_slots
                if source_area == "inventory"
                else store.craft_slots
            )

            source_slots[source_index] = {
                "item": item_id,
                "qty": leftover,
            }

        store.inventory_drag_held = None
        store.inventory_drag_source = None

        _sync_legacy_inventory()


    # ========================================================
    # CRAFTING
    # ========================================================

    def crafting_input_summary():

        if not has_skill("predator"):
            return None

        present = [
            entry
            for entry in store.craft_slots
            if entry is not None and entry["qty"] > 0
        ]

        if not present:
            return None

        first_item = present[0]["item"]

        if any(entry["item"] != first_item for entry in present):
            return None

        if first_item == "hipokute":
            output = "healing_blob"

        elif first_item == "magic_ore":
            output = "magisteel_cluster"

        else:
            return None

        total = sum(
            int(entry["qty"])
            for entry in present
        )

        return first_item, output, total


    def set_craft_quantity(value):

        info = crafting_input_summary()

        max_value = info[2] if info else 1

        store.craft_quantity = max(
            1,
            min(int(value), max_value)
        )


    def _consume_craft_material(item_id, quantity):

        remaining = int(quantity)

        for index in range(8, -1, -1):

            entry = store.craft_slots[index]

            if entry is None:
                continue

            if entry["item"] != item_id:
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

        amount = max(
            1,
            min(int(quantity), available)
        )

        inventory_snapshot = _copy_slots(store.inventory_slots)
        craft_snapshot = _copy_slots(store.craft_slots)

        if not _consume_craft_material(input_item, amount):
            return False

        if not add_item(output_item, amount):

            store.inventory_slots = inventory_snapshot
            store.craft_slots = craft_snapshot

            _sync_legacy_inventory()

            return False

        store.craft_quantity = 1

        renpy.notify(
            "Crafted %d x %s."
            % (amount, inventory_item_name(output_item))
        )

        return True


    def return_all_craft_materials():

        for index in range(9):

            entry = store.craft_slots[index]

            if entry is None:
                continue

            item_id = entry["item"]
            quantity = int(entry["qty"])

            if add_item(item_id, quantity):
                store.craft_slots[index] = None


    def inventory_close_cleanup():

        inventory_cancel_drag()
        return_all_craft_materials()
