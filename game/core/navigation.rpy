default pending_nav_action = None

init -5 python:
    def enter_location(location_id):
        if location_id not in LOCATIONS:
            raise ValueError("Unknown location: " + location_id)
        if location_id == "charybdis_border":
            previous = store.current_location
            store.world_state["choices"]["charybdis_return"] = previous if previous in ("side1", "side2") else store.side_path_3_from
        store.current_location = location_id
        store.current_region = LOCATIONS[location_id].get("region", "West_Jura")
        if location_id not in store.world_state["discoveries"]:
            store.world_state["discoveries"].append(location_id)
        visits = store.world_state["visits"]
        visits[location_id] = visits.get(location_id, 0) + 1

    def location_view(location_id):
        data = LOCATIONS[location_id]
        for variant in data.get("variants", []):
            if conditions_met(variant["when"]):
                return variant
        return data

    def location_actions(location_id):
        view = location_view(location_id)
        actions = []
        for action in view.get("actions", []):
            if not conditions_met(action.get("visible_when", {})):
                continue
            entry = dict(action)
            entry["enabled"] = conditions_met(action.get("when", {}))
            actions.append(entry)
        for character_id in CHARACTER_DATA:
            if character_present(character_id, location_id):
                actions.append({"id": "npc_" + character_id, "text": "Talk to " + CHARACTER_DATA[character_id]["name"], "kind": "npc", "character": character_id, "enabled": True})
        for event_id in available_events(location_id, automatic=False):
            actions.append({"id": "event_" + event_id, "text": STORY_EVENTS[event_id]["title"], "kind": "event", "event": event_id, "enabled": True})
        if has_skill("keen_smell") and location_id not in ("village", "command_tent", "wolf_den"):
            actions.append({"id": "track_monsters", "text": "Track a monster • Keen Smell", "kind": "label", "label": "west_jura_keen_smell_menu", "enabled": True})
        return actions

    def resolve_location_action(action_id):
        return next((a for a in location_actions(store.current_location) if a["id"] == action_id and a["enabled"]), None)

    def gather_resource(action):
        if not conditions_met(action.get("when", {})):
            return False
        if action.get("flag") and world_flag(action["flag"]):
            return False
        add_item(action["item"], action.get("quantity", 1))
        if action.get("flag"):
            set_world_flag(action["flag"])
        record_event("gathered_" + action["item"])
        return True

label explore_location:

    $ navigation_active = True
    $ current_view = location_view(current_location)

    scene expression current_view["background"]

    $ automatic_events = available_events(automatic=True)

    if automatic_events:

        call run_story_event(automatic_events[0])

        if _return is False:
            $ renpy.pause(0.1, hard=True)

        jump explore_location


    window hide

    $ pending_nav_action = None

    show screen location_choices

    while pending_nav_action is None:
        $ renpy.pause()

    hide screen location_choices

    $ nav_action = resolve_location_action(pending_nav_action)
    $ pending_nav_action = None


    if nav_action is None:

        jump explore_location


    if nav_action["kind"] == "exit":

        $ enter_location(nav_action["target"])

        jump explore_location


    elif nav_action["kind"] == "label":

        $ navigation_active = False

        jump expression nav_action["label"]


    elif nav_action["kind"] == "gather":

        if gather_resource(nav_action):

            $ gathered_name = ITEM_DATA[nav_action["item"]]["name"]

            n "Stored: [gathered_name]."

        jump explore_location


    elif nav_action["kind"] == "battle":

        call battle_enemy(
            nav_action["enemy"],
            encounter_id=nav_action.get("encounter")
        )

        jump explore_location


    elif nav_action["kind"] == "npc":

        call npc_interaction(
            nav_action["character"]
        )

        jump explore_location


    elif nav_action["kind"] == "event":

        call run_story_event(
            nav_action["event"]
        )

        jump explore_location


    elif nav_action["kind"] == "rest":

        $ restore_player()

        n "Rimuru rests. HP, magicules and move uses are restored."

        jump explore_location


    elif nav_action["kind"] == "discover":

        $ apply_effects(nav_action["effects"])

        $ discovery_text = nav_action["message"]

        n "[discovery_text]"

        jump explore_location


    jump explore_location
