default inventory = {}

init -10 python:
    def item_count(item_id):
        return store.inventory.get(item_id, 0)

    def set_item_count(item_id, quantity):
        data = ITEM_DATA[item_id]
        quantity = max(0, int(quantity))
        if not data.get("stackable", True):
            quantity = min(1, quantity)
        store.inventory[item_id] = quantity
        if item_id in LEGACY_ITEMS:
            setattr(store, LEGACY_ITEMS[item_id], quantity)

    def add_item(item_id, quantity=1):
        if quantity <= 0:
            return False
        set_item_count(item_id, item_count(item_id) + quantity)
        return True

    def remove_item(item_id, quantity=1):
        if quantity <= 0 or item_count(item_id) < quantity:
            return False
        set_item_count(item_id, item_count(item_id) - quantity)
        return True

    def can_use_item(item_id):
        if item_count(item_id) < 1:
            return False
        effect = ITEM_DATA[item_id].get("use", {})
        return ((effect.get("hp", 0) > 0 and store.player_hp < store.player_max_hp) or
                (effect.get("mp", 0) > 0 and store.player_mp < store.player_max_mp))

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

