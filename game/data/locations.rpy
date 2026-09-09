init 3 python:
    # Constructors keep authored map data short. Definitions are init-only.
    def path(action_id, text, target, when=None, visible_when=None):
        return {"id": action_id, "text": text, "kind": "exit", "target": target, "when": when or {}, "visible_when": visible_when or {}}

    def scene_action(action_id, text, label, when=None):
        return {"id": action_id, "text": text, "kind": "label", "label": label, "when": when or {}}

    def resource(item, flag, text="Gather berries", when=None):
        LEGACY_FLAGS[flag] = flag
        return {"id": flag, "text": text, "kind": "gather", "item": item, "flag": flag, "when": when or {}, "visible_when": {"flags": {flag: False}}}

    def fight(enemy, encounter=None, repeat=False):
        LEGACY_FLAGS[enemy + "_defeated"] = enemy + "_defeated" if enemy != "orc_lord" else "orc_lord_defeated_compat"
        # New bosses use structured state, not nonexistent legacy defaults.
        if enemy == "orc_lord":
            LEGACY_FLAGS.pop("orc_lord_defeated", None)
        return {"id": "fight_" + enemy, "text": ("Fight another " if repeat else "Challenge ") + ENEMY_DATA[enemy]["name"], "kind": "battle", "enemy": enemy, "encounter": encounter, "visible_when": {} if repeat else {"flags": {enemy + "_defeated": False}}}

    def forest_node(title, actions, background="west_jura_forest", description="Placeholder artwork: Jura Forest"):
        return {"title": title, "background": background, "description": description, "actions": actions}

    LOCATIONS = {
        "cave_mouth": forest_node("Veldora's Cave • Forest edge", [scene_action("back", "Go back into Veldora's Cave", "veldora_cave_exit"), path("forward", "Go forward into the forest", "crossroads"), {"id": "rest", "text": "Rest by the cave entrance", "kind": "rest"}]),
        "crossroads": forest_node("West Jura • Crossroads", [path("forward", "Go forward • Goblin trail", "goblin_route"), path("right", "Go right • Deep forest", "rabbit_trail"), path("left", "Go left • Western ravine", "ravine"), path("back", "Go back • Cave entrance", "cave_mouth"), resource("berries", "crossroads_berries", "Gather roadside berries"), {"id": "smell", "kind": "discover", "text": "Use Keen Smell", "visible_when": {"skills": ["keen_smell"]}, "effects": {"flags": {"scent_trail_found": True}}, "message": "A sweet scent marks a hidden grove beside the ravine."}], "west_jura_crossroads"),
        "goblin_route": forest_node("West Jura • Goblin trail", [path("village", "Enter Goblin Village", "village", {"flags": {"village_access": True}}), path("back", "Go back • Crossroads", "crossroads")]),
        "village": forest_node("Goblin Village", [scene_action("tent", "Enter the Command Tent", "west_jura_command_tent"), path("grove", "Go to the Berry Grove", "village_grove"), {"id": "rest", "text": "Rest at the settlement", "kind": "rest"}, path("back", "Return to the forest", "goblin_route")], "west_jura_village"),
        "command_tent": forest_node("Goblin Village • Command Tent", [scene_action("story", "Ask Rigurd about the village", "west_jura_command_tent"), path("back", "Leave the tent", "village")], "west_jura_command_tent_injured"),
        "village_grove": forest_node("Goblin Village • Berry Grove", [resource("berries", "village_berry_grove_harvested"), path("back", "Go back • Village", "village")], "west_jura_orchard"),
        "wolf_den": forest_node("The former Goblin Village", [fight("direwolf_leader"), path("back", "Return to the forest", "goblin_route")], "west_jura_wolf_den", "The settlement has become a wolf den. Placeholder artwork."),
        "rabbit_trail": forest_node("West Jura • Horn Rabbit trail", [fight("horn_rabbit", "forest_rabbit"), path("left", "Go left • Blumund trail", "blumund_path", {"flags": {"horn_rabbit_defeated": True}}), path("forward", "Go forward • Main Branch 2", "main2", {"flags": {"horn_rabbit_defeated": True}}), path("back", "Go back • Crossroads", "crossroads"), dict(fight("horn_rabbit", "forest_rabbit", True), visible_when={"flags": {"horn_rabbit_defeated": True}})]),
        "blumund_path": forest_node("West Jura • Blumund trail", [path("forward", "Continue toward Blumund", "blumund_border"), path("clearing", "Enter the clearing", "deer_clearing"), path("back", "Go back", "rabbit_trail")]),
        "deer_clearing": forest_node("West Jura • Cattle Deer clearing", [resource("cattle_deer", "cattle_deer_captured", "Use Predator • Shelter a Cattle Deer", {"skills": ["predator"]}), path("back", "Go back", "blumund_path")], "west_jura_clearing"),
        "main2": forest_node("West Jura • Main Branch 2", [path("left", "Enter the berry orchard", "orchard1"), path("forward", "Continue along the main path", "main3"), path("back", "Go back • Horn Rabbit trail", "rabbit_trail")]),
        "orchard1": forest_node("West Jura • Outer orchard", [resource("berries", "berry_orchard_1_harvested"), path("forward", "Go deeper into the orchard", "orchard2"), path("back", "Return to the main path", "main2")], "west_jura_orchard"),
        "orchard2": forest_node("West Jura • Bear's orchard", [fight("giant_bear"), resource("berries", "berry_orchard_2_harvested", when={"flags": {"giant_bear_defeated": True}}), path("left", "Go left • Outer orchard", "orchard1"), path("right", "Go right • Third orchard", "orchard3", {"flags": {"giant_bear_defeated": True}}), dict(fight("giant_bear", repeat=True), visible_when={"flags": {"giant_bear_defeated": True}})], "west_jura_orchard"),
        "orchard3": forest_node("West Jura • Third orchard", [resource("berries", "berry_orchard_3_harvested"), path("left", "Go left • Bear's orchard", "orchard2"), path("back", "Return to the main forest path", "main3")], "west_jura_orchard"),
        "main3": forest_node("West Jura • Main Branch 3", [path("left", "Enter the berry orchard", "orchard3"), path("forward", "Continue down the main path", "main4"), path("back", "Go back • Main Branch 2", "main2")], "west_jura_clearing"),
        "main4": forest_node("West Jura • Main Branch 4", [path("left", "Take the left-side path", "barghest_trail"), path("forward", "Continue along the main path", "spider_trail"), path("back", "Go back • Main Branch 3", "main3")]),
        "barghest_trail": forest_node("West Jura • Barghest clearing", [fight("barghest"), path("forward", "Continue toward Falmuth", "falmuth_border", {"flags": {"barghest_defeated": True}}), path("back", "Go back", "main4"), dict(fight("barghest", repeat=True), visible_when={"flags": {"barghest_defeated": True}})], "west_jura_clearing"),
        "spider_trail": forest_node("West Jura • Knight Spider trail", [fight("knight_spider"), path("mountains", "Continue toward the Canaat Mountains", "canaat_border", {"flags": {"knight_spider_defeated": True}}), path("forward", "Continue to the outer forest loop", "main6", {"flags": {"knight_spider_defeated": True}}), path("back", "Go back • Main Branch 4", "main4"), dict(fight("knight_spider", repeat=True), visible_when={"flags": {"knight_spider_defeated": True}})]),
        "main6": forest_node("West Jura • Main Branch 6", [path("spider", "Head toward the Knight Spider trail", "spider_trail"), path("forward", "Continue around the forest loop", "main7"), path("side", "Take the side path", "boar_trail")]),
        "boar_trail": forest_node("West Jura • Blood Boar trail", [fight("blood_boar"), path("right", "Take the right path", "side1", {"flags": {"blood_boar_defeated": True}}), path("left", "Take the left path", "side2", {"flags": {"blood_boar_defeated": True}}), path("back", "Return to Main Branch 6", "main6"), dict(fight("blood_boar", repeat=True), visible_when={"flags": {"blood_boar_defeated": True}})], "west_jura_clearing"),
        "side1": forest_node("West Jura • Side Path 1", [path("forward", "Continue", "charybdis_border"), path("back", "Go back", "boar_trail")]),
        "side2": forest_node("West Jura • Side Path 2", [path("forward", "Continue forward", "charybdis_border"), path("dwargon", "Take the path toward Dwargon", "dwargon_border"), path("back", "Go back", "boar_trail")]),
        "charybdis_border": forest_node("Charybdis Cave • Boundary", [path("side1", "Return along Side Path 1", "side1"), path("side2", "Return along Side Path 2", "side2")], description="Charybdis Cave content is not implemented."),
        "main7": forest_node("West Jura • Main Branch 7", [path("back", "Continue toward Main Branch 6", "main6"), path("forward", "Continue around the loop", "main8"), path("oneway", "Take the one-way side trail", "tiger_trail")]),
        "tiger_trail": forest_node("West Jura • Blade Tiger trail", [fight("blade_tiger"), path("back", "Go back • Clearing", "tiger_clearing"), dict(fight("blade_tiger", repeat=True), visible_when={"flags": {"blade_tiger_defeated": True}})], "west_jura_clearing"),
        "tiger_clearing": forest_node("West Jura • Blade Tiger clearing", [path("tiger", "Go toward the Blade Tiger", "tiger_trail"), path("back", "Return to Main Branch 8", "main8")], "west_jura_clearing"),
        "main8": forest_node("West Jura • Main Branch 8", [path("back", "Continue toward Main Branch 7", "main7"), path("forward", "Continue around the loop", "main9"), path("clearing", "Take the path to the clearing", "tiger_clearing")]),
        "main9": forest_node("West Jura • Main Branch 9", [path("back", "Continue toward Main Branch 8", "main8"), path("crossroads", "Return to the original crossroads", "crossroads"), path("ogres", "Take the path toward the Ogre Village", "ogre_border")]),
        "ogre_border": forest_node("Ogre Village • Prototype encounter", [path("back", "Go back", "main9")], "west_jura_clearing", "Placeholder dialogue and art. Alliance timing changes the Orc Lord aftermath."),
        "ravine": forest_node("West Jura • Western ravine", [path("back", "Go back • Crossroads", "crossroads"), {"id": "perception", "kind": "discover", "text": "Use Mana Perception • Inspect the crossing", "visible_when": {"skills": ["mana_perception"], "flags": {"ravine_surveyed": False}}, "effects": {"flags": {"ravine_surveyed": True}, "items": {"trail_note": 1}}, "message": "Beyond the broken crossing, a powerful presence moves through the forest. Thread or water control could carry you across."}, path("cross", "Cross the ravine • Use a skill", "orc_approach", {"any": [{"skills": ["steel_thread"]}, {"skills": ["water_manipulation"]}]}, {"flags": {"ravine_surveyed": True}}), path("hidden", "Follow the hidden scent trail", "hidden_grove", visible_when={"flags": {"scent_trail_found": True}})], description="Prototype western route. A broken crossing spans the ravine."),
        "hidden_grove": forest_node("West Jura • Hidden grove", [resource("wildflowers", "hidden_flowers", "Gather wildflowers"), resource("magicule_tonic", "hidden_tonic", "Investigate the abandoned supplies"), path("back", "Return to the ravine", "ravine")], "west_jura_orchard"),
        "orc_approach": forest_node("West Jura • Orc Lord approach", [fight("orc_lord", "orc_lord"), path("back", "Retreat across the ravine", "ravine")], "west_jura_clearing", "PROTOTYPE BOSS • Extremely dangerous. No Shizue or kijin story prerequisite. Balance and scene pending."),
    }
    for key, title, target in (("blumund_border", "Blumund", "blumund_path"), ("falmuth_border", "Falmuth", "barghest_trail"), ("canaat_border", "Canaat Mountains", "spider_trail"), ("dwargon_border", "Dwargon", "side2")):
        LOCATIONS[key] = forest_node(title + " • Boundary", [path("back", "Go back", target)], "west_jura_clearing", title + " content is not implemented.")
    LOCATIONS["village"]["variants"] = [dict(LOCATIONS["wolf_den"], when={"flags": {"goblins_destroyed": True}})]
    LOCATIONS["command_tent"]["variants"] = [dict(LOCATIONS["command_tent"], background="west_jura_command_tent_healed", when={"flags": {"injured_goblins_healed": True}})]
    for action in LOCATIONS["charybdis_border"]["actions"]:
        action["visible_when"] = {"choices": {"charybdis_return": action["target"]}}

    # Legacy variables that don't yet exist use structured flags instead.
    for new_flag in ("crossroads_berries", "hidden_flowers", "hidden_tonic"):
        LEGACY_FLAGS.pop(new_flag, None)
