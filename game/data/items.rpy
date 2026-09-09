init -15 python:
    # Quantity belongs to inventory, not to these immutable definitions.
    ITEM_DATA = {
        "healing_blob": {"name": "Healing Blob", "description": "Restores 150 HP. Also heals the injured goblins.", "category": "Consumables", "stackable": True, "use": {"hp": 150}},
        "berries": {"name": "Berry Bundle", "description": "Fresh Jura berries. A simple gift, or a small snack restoring 25 HP.", "category": "Gifts", "stackable": True, "gift": True, "use": {"hp": 25}},
        "cattle_deer": {"name": "Cattle Deer", "description": "A living animal sheltered in Stomach. Reserved for future husbandry.", "category": "Special Items", "stackable": True},
        "hipokute": {"name": "Hipokute Herbs", "description": "Medicinal herbs. Predator can refine one cluster into a Healing Blob.", "category": "Materials", "stackable": True},
        "magic_ore": {"name": "Magic Ore", "description": "Ore rich in magicules. Useful material for future crafting.", "category": "Materials", "stackable": True},
        "stuffed_animal": {"name": "Stuffed Animal", "description": "A carefully sewn woodland animal. Provisional gift item.", "category": "Gifts", "stackable": True, "gift": True},
        "strategy_book": {"name": "Strategy Book", "description": "A collection of battlefield exercises. Provisional gift item.", "category": "Gifts", "stackable": True, "gift": True},
        "wildflowers": {"name": "Wildflowers", "description": "A small, fragrant bouquet from the forest.", "category": "Gifts", "stackable": True, "gift": True},
        "magicule_tonic": {"name": "Magicule Tonic", "description": "Restores 40 MP. Provisional balancing item.", "category": "Consumables", "stackable": True, "use": {"mp": 40}},
        "trail_note": {"name": "Trail Note", "description": "Marks the ravine crossing and an unusually powerful presence beyond it.", "category": "Quest Items", "stackable": False},
    }
    LEGACY_ITEMS = {"healing_blob": "healing_blobs", "berries": "berry_bundles", "cattle_deer": "cattle_deer_stored", "hipokute": "hipokute_herb_clusters", "magic_ore": "magic_ore_clusters"}

