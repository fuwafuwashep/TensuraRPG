init -15 python:

    # Quantity belongs to the inventory, not to these definitions.
    # footprint = how many 100 x 100 inventory cells the item occupies.

    ITEM_DATA = {

        "healing_blob": {
            "name": "Healing Blob",
            "description": "A medicinal mixture crafted from a Hipoutke Herb. Restores 150 HP and can also be used to treat the injured goblins.",
            "category": "Consumables",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "use": {"hp": 150},
        },

        "berries": {
            "name": "Berry Bundle",
            "description": "Fresh forest berries. A simple gift or a small snack that restores 25 HP.",
            "category": "Gifts",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "gift": True,
            "use": {"hp": 25},
        },

        # Kept for compatibility with older saves. New Forest of Desire
        # encounters use the separate male/female Bull Deer entries below.
        "cattle_deer": {
            "name": "Bull Deer",
            "description": "A living Bull Deer sheltered safely inside Stomach.",
            "category": "Special Items",
            "stackable": True,
            "max_stack": 64,
            "footprint": (2, 1),
        },

        "bull_deer_male": {
            "name": "Bull Deer (Male)",
            "description": "A living male Bull Deer sheltered safely inside Stomach.",
            "category": "Special Items",
            "stackable": True,
            "max_stack": 64,
            "footprint": (2, 1),
        },

        "bull_deer_female": {
            "name": "Bull Deer (Female)",
            "description": "A living female Bull Deer sheltered safely inside Stomach.",
            "category": "Special Items",
            "stackable": True,
            "max_stack": 64,
            "footprint": (2, 1),
        },

        "hipokute": {
            "name": "Hipoutke Herb",
            "description": "A valuable medicinal herb that grows in magicule-dense areas. Predator can craft it into a Healing Blob.",
            "category": "Materials",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
        },

        "magic_ore": {
            "name": "Magic Ore Cluster",
            "description": "Mineral that has absorbed magicules over a long period of time. Predator can refine it into Magisteel.",
            "category": "Materials",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
        },

        "magisteel_cluster": {
            "name": "Magisteel Cluster",
            "description": "Magic Ore refined into a denser magical metal cluster.",
            "category": "Materials",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
        },

        "storm_dragon": {
            "name": "Storm Dragon",
            "description": "The Storm Dragon and Unlimited Imprisonment, quarantined inside Predator while the seal is analyzed.",
            "category": "Special Items",
            "stackable": False,
            "max_stack": 1,
            "footprint": (7, 7),
        },

        "stuffed_animal": {
            "name": "Stuffed Animal",
            "description": "A carefully sewn woodland animal. Provisional gift item.",
            "category": "Gifts",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "gift": True,
        },

        "strategy_book": {
            "name": "Strategy Book",
            "description": "A collection of battlefield exercises. Provisional gift item.",
            "category": "Gifts",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "gift": True,
        },

        "wildflowers": {
            "name": "Wildflowers",
            "description": "A small, fragrant bouquet from the forest.",
            "category": "Gifts",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "gift": True,
        },

        "magicule_tonic": {
            "name": "Magicule Tonic",
            "description": "Restores 40 MP. Provisional balancing item.",
            "category": "Consumables",
            "stackable": True,
            "max_stack": 64,
            "footprint": (1, 1),
            "use": {"mp": 40},
        },

        "trail_note": {
            "name": "Trail Note",
            "description": "Marks the ravine crossing and an unusually powerful presence beyond it.",
            "category": "Quest Items",
            "stackable": False,
            "max_stack": 1,
            "footprint": (1, 1),
        },
    }


    # Old counters are kept synchronized for the existing story code and saves.
    LEGACY_ITEMS = {
        "healing_blob": "healing_blobs",
        "berries": "berry_bundles",
        "cattle_deer": "cattle_deer_stored",
        "hipokute": "hipokute_herb_clusters",
        "magic_ore": "magic_ore_clusters",
    }
