init -15 python:
    # Thresholds and gift values are provisional design data, not canon claims.
    # Null sprite means show a clearly labelled placeholder, never a missing file.
    CHARACTER_DATA = {
        "haruna": {"name": "Haruna", "romanceable": True, "version": 1, "stages": (25, 60), "romance_gates": ((0, 0, None), (20, 25, None), (55, 60, "haruna_personal"), (100, 85, "haruna_courtship")), "locations": [{"location": "village", "when": {"flags": {"village_access": True, "goblins_destroyed": False}}}], "assist": {"trust": 35, "heal": 12}},
        "rigurd": {"name": "Rigurd", "romanceable": True, "version": 1, "stages": (30, 65), "romance_gates": ((0, 0, None), (25, 30, None), (60, 65, "rigurd_personal"), (100, 90, "rigurd_courtship")), "locations": [{"location": "village", "when": {"flags": {"goblin_arc_complete": True, "goblins_destroyed": False}}}, {"location": "command_tent", "when": {"flags": {"village_access": True, "goblins_destroyed": False}}}], "assist": {"trust": 40, "heal": 15}},
        "hostess_elves": {"name": "Hostess Elves", "romanceable": True, "version": 1, "stages": (20, 55)},
        "eren": {"name": "Eren", "romanceable": True, "version": 1, "stages": (20, 55)},
        "shion": {"name": "Shion", "romanceable": True, "version": 1, "stages": (25, 60)},
        "shuna": {"name": "Shuna", "romanceable": True, "version": 1, "stages": (30, 65)},
        "benimaru": {"name": "Benimaru", "romanceable": True, "version": 1, "stages": (35, 70)},
        "souei": {"name": "Souei", "romanceable": True, "version": 1, "stages": (40, 75)},
        "treyni": {"name": "Treyni", "romanceable": True, "version": 1, "stages": (35, 70)},
        "souka": {"name": "Souka", "romanceable": True, "version": 1, "stages": (25, 60)},
        "geld": {"name": "Geld", "romanceable": True, "version": 2},
        "gabiru": {"name": "Gabiru", "romanceable": True, "version": 2},
        "milim": {"name": "Milim", "romanceable": True, "version": 2},
        "youm": {"name": "Youm", "romanceable": True, "version": 2},
        "mjurran": {"name": "Mjurran", "romanceable": True, "version": 2},
        "veldora": {"name": "Veldora", "romanceable": False},
        "ranga": {"name": "Ranga", "romanceable": False},
        "kaijin": {"name": "Kaijin", "romanceable": False},
        "gazel": {"name": "Gazel", "romanceable": False},
        "shizue": {"name": "Shizue", "romanceable": False},
    }
    # Unwritten routes have conservative individual gates and no available scenes.
    for cid, character in CHARACTER_DATA.items():
        if character.get("romanceable") and "romance_gates" not in character:
            middle, late = character.get("stages", (30, 65))
            character["romance_gates"] = ((0, 0, None), (20, middle, None), (60, late, cid + "_personal"), (100, min(95, late + 20), cid + "_courtship"))

