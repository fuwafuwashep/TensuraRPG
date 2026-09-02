# ============================================================
# GLOBAL SKILLS AND MOVE LOADOUT
# ============================================================

# Game-wide skill flags and move/loadout data.

# ============================================================
# CURRENT REGION
# ============================================================

default current_region = "Veldoras_Cave"


# ============================================================
# CORE SKILLS
# ============================================================

default great_sage = True
default predator = True

default thought_communication = False

default heat_source_perception = False
default poison_breath = False
default sticky_thread = False
default steel_thread = False
default ultra_sound_waves = False
default paralyzing_breath = False
default body_armor = False

default steel_pelt = False
default strengthen = False
default steel_strength = False
default voice_canon = False
default danger_sense = False
default keen_smell = False

default coercion = False
default shadow_motion = False
default black_lightning = False
default fire_breath = False


# ============================================================
# MOVE LOADOUT
# ============================================================

default unlocked_moves = [
    "Basic Attack",
    "Predate",
]

default battle_physical_moves = [
    "Basic Attack",
]

default battle_aura_moves = []
default battle_magic_moves = []

default battle_skill_moves = [
    "Predate",
]

# Uses persist until rest.
default move_uses_remaining = {}


# ============================================================
# MOVE DATA
# ============================================================

init python:

    import renpy.store as store

    MOVE_DATA = {

        "Basic Attack": {
            "category": "physical",
            "damage": None,
            "accuracy": 1.00,
            "max_uses": None,
        },

        "Predate": {
            "category": "skills",
            "damage": None,
            "accuracy": 1.00,
            "max_uses": None,
        },

        "Water Blade": {
            "category": "magic",
            "damage": 70,
            "accuracy": 1.00,
            "max_uses": 20,
        },

        "Misty Field": {
            "category": "magic",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": None,
        },

        "Poisonous Breath": {
            "category": "skills",
            "damage": 55,
            "accuracy": 1.00,
            "max_uses": 20,
        },

        "Sticky Web": {
            "category": "skills",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": 30,
        },

        "Sticky Shot": {
            "category": "skills",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": None,
        },

        "Steel Web": {
            "category": "skills",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": 30,
        },

        "Threaded Slash": {
            "category": "skills",
            "damage": 50,
            "accuracy": 0.95,
            "max_uses": 30,
        },

        "Steel Bind": {
            "category": "skills",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": None,
        },

        "Paralysis Breath": {
            "category": "skills",
            "damage": 30,
            "accuracy": 1.00,
            "max_uses": 20,
        },

        "Fire Breath": {
            "category": "skills",
            "damage": 55,
            "accuracy": 1.00,
            "max_uses": 20,
        },

        "Voice Canon": {
            "category": "skills",
            "damage": 120,
            "accuracy": 1.00,
            "max_uses": 10,
        },

        "Intimidation": {
            "category": "skills",
            "damage": 0,
            "accuracy": 1.00,
            "max_uses": 15,
        },

        "Black Bolt": {
            "category": "skills",
            "damage": 160,
            "accuracy": 1.00,
            "max_uses": 5,
        },

        "Black Discharge": {
            "category": "skills",
            "damage": 160,
            "accuracy": 1.00,
            "max_uses": 5,
        },
    }

    SKILL_NAMES = {
        "great_sage": "Great Sage",
        "predator": "Predator",
        "thought_communication": "Thought Communication",
        "heat_source_perception": "Heat Source Perception",
        "poison_breath": "Poison Breath",
        "sticky_thread": "Sticky Thread",
        "steel_thread": "Steel Thread",
        "ultra_sound_waves": "Ultra Sound Waves",
        "paralyzing_breath": "Paralyzing Breath",
        "body_armor": "Body Armor",
        "steel_pelt": "Steel Pelt",
        "strengthen": "Strengthen",
        "steel_strength": "Steel Strength",
        "voice_canon": "Voice Canon",
        "danger_sense": "Danger Sense",
        "keen_smell": "Keen Smell",
        "coercion": "Coercion",
        "shadow_motion": "Shadow Motion",
        "black_lightning": "Black Lightning",
        "fire_breath": "Fire Breath",
    }

    CATEGORY_LIMITS = {
        "physical": 3,
        "aura": 5,
        "magic": 5,
        "skills": 5,
    }


    def category_move_list(category):

        if category == "physical":
            return store.battle_physical_moves

        if category == "aura":
            return store.battle_aura_moves

        if category == "magic":
            return store.battle_magic_moves

        return store.battle_skill_moves


    def move_is_equipped(move_name):

        for category in ("physical", "aura", "magic", "skills"):

            if move_name in category_move_list(category):
                return True

        return False


    def unlock_move(move_name, auto_equip=True):

        if move_name not in MOVE_DATA:
            return

        if move_name not in store.unlocked_moves:
            store.unlocked_moves.append(move_name)

        max_uses = MOVE_DATA[move_name]["max_uses"]

        if max_uses is not None and move_name not in store.move_uses_remaining:
            store.move_uses_remaining[move_name] = max_uses

        if auto_equip and not move_is_equipped(move_name):

            category = MOVE_DATA[move_name]["category"]
            equipped = category_move_list(category)
            limit = CATEGORY_LIMITS[category]

            if len(equipped) < limit:
                equipped.append(move_name)


    def equip_move(move_name):

        if move_name not in store.unlocked_moves:
            renpy.notify("That move has not been unlocked.")
            return

        if move_is_equipped(move_name):
            renpy.notify("That move is already equipped.")
            return

        category = MOVE_DATA[move_name]["category"]
        equipped = category_move_list(category)
        limit = CATEGORY_LIMITS[category]

        if len(equipped) >= limit:
            renpy.notify("That category is already full.")
            return

        equipped.append(move_name)


    def unequip_move(move_name):

        for category in ("physical", "aura", "magic", "skills"):

            equipped = category_move_list(category)

            if move_name in equipped:
                equipped.remove(move_name)
                return


    def sync_skill_moves():

        # The old cave code calls this Telepathy. Treat it as
        # Thought Communication too so the old save still works.
        if getattr(store, "telepathy", False):
            store.thought_communication = True

        unlock_move("Basic Attack")

        if store.predator:
            unlock_move("Predate")

        if getattr(store, "water_manipulation", False):
            unlock_move("Water Blade")
            unlock_move("Misty Field")

        if store.poison_breath:
            unlock_move("Poisonous Breath")

        if store.sticky_thread:
            unlock_move("Sticky Web")

            if store.thought_communication or getattr(store, "telepathy", False):
                unlock_move("Sticky Shot")

        if store.steel_thread:
            unlock_move("Steel Web")

            if store.thought_communication or getattr(store, "telepathy", False):
                unlock_move("Threaded Slash")
                unlock_move("Steel Bind")

        if store.paralyzing_breath:
            unlock_move("Paralysis Breath")

        if store.fire_breath:
            unlock_move("Fire Breath")

        if store.voice_canon:
            unlock_move("Voice Canon")

        if store.coercion:
            unlock_move("Intimidation")

        if store.black_lightning:
            unlock_move("Black Bolt")
            unlock_move("Black Discharge")


    def get_equipped_moves(category, predator_allowed=True):

        sync_skill_moves()

        result = list(category_move_list(category))

        if not predator_allowed and "Predate" in result:
            result.remove("Predate")

        return result


    def move_has_uses(move_name):

        max_uses = MOVE_DATA[move_name]["max_uses"]

        if max_uses is None:
            return True

        if move_name not in store.move_uses_remaining:
            store.move_uses_remaining[move_name] = max_uses

        return store.move_uses_remaining[move_name] > 0


    def consume_move_use(move_name):

        max_uses = MOVE_DATA[move_name]["max_uses"]

        if max_uses is None:
            return

        if move_name not in store.move_uses_remaining:
            store.move_uses_remaining[move_name] = max_uses

        store.move_uses_remaining[move_name] = max(
            0,
            store.move_uses_remaining[move_name] - 1
        )


    def reset_move_uses():

        for move_name, data in MOVE_DATA.items():

            if data["max_uses"] is not None:
                store.move_uses_remaining[move_name] = data["max_uses"]


    def move_context_available(
        move_name,
        predator_allowed,
        enemy_hp,
        player_hp,
        player_max_hp
    ):

        if not move_has_uses(move_name):
            return False

        if move_name == "Predate":

            if not predator_allowed:
                return False

            if enemy_hp >= 100:
                return False

        if move_name == "Voice Canon":

            if player_hp <= player_max_hp * 0.50:
                return False

        return True


    def grant_skill(skill_key):

        if not hasattr(store, skill_key):
            return False

        if getattr(store, skill_key):
            return False

        setattr(store, skill_key, True)
        sync_skill_moves()

        return True


    def get_owned_skills():

        result = []

        # Existing cave skills/resistances.
        if getattr(store, "water_manipulation", False):
            result.append(("Water Manipulation", "Unlocks Water Blade and Misty Field."))

        if getattr(store, "heat_resistance", False):
            result.append(("Heat Resistance", "Halves heat-based damage."))

        if getattr(store, "cold_resistance", False):
            result.append(("Cold Resistance", "Halves cold-based damage."))

        if getattr(store, "electricity_resistance", False):
            result.append(("Electricity Resistance", "Halves electric damage."))

        if getattr(store, "paralysis_resistance", False):
            result.append(("Paralysis Resistance", "Halves paralysis effects."))

        owned = [
            ("great_sage", "No combat moves."),
            ("predator", "Unlocks Predate. It becomes usable when an enemy falls below 100 HP."),
            ("thought_communication", "Unlocks the Allies battle function."),
            ("heat_source_perception", "A perception skill that detects heat sources."),
            ("poison_breath", "Unlocks Poisonous Breath."),
            ("sticky_thread", "Unlocks Sticky Web. Communication also unlocks Sticky Shot."),
            ("steel_thread", "Unlocks Steel Web. Communication also unlocks Threaded Slash and Steel Bind."),
            ("ultra_sound_waves", "Allows communication through ultrasonic waves."),
            ("paralyzing_breath", "Unlocks Paralysis Breath."),
            ("body_armor", "Halves physical attack damage."),
            ("steel_pelt", "Halves physical attack damage."),
            ("strengthen", "Doubles physical attack damage."),
            ("steel_strength", "Triples physical attack damage."),
            ("voice_canon", "Unlocks Voice Canon."),
            ("danger_sense", "Adds first-turn priority. Full speed/priority math is not implemented yet."),
            ("keen_smell", "Lets you locate monsters throughout the current region."),
            ("coercion", "Unlocks Intimidation."),
            ("shadow_motion", "Adds first-turn priority. Full speed/priority math is not implemented yet."),
            ("black_lightning", "Unlocks Black Bolt and Black Discharge."),
            ("fire_breath", "Unlocks Fire Breath."),
        ]

        for key, description in owned:

            if getattr(store, key, False):
                result.append((SKILL_NAMES[key], description))

        return result


label sync_player_skills:

    $ sync_skill_moves()

    return
