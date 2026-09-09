init 10 python:
    def validate_game_catalogs():
        """Validate dynamic references that ordinary Ren'Py lint cannot see."""
        errors = []

        def image_exists(name):
            return renpy.loadable(name) or renpy.has_image(name)

        def check_rule(rule, source):
            for key, value in rule.items():
                if key in ("all", "any"):
                    for child in value:
                        check_rule(child, source)
                elif key == "not":
                    check_rule(value, source)
                elif key == "items":
                    errors.extend(source + ": unknown item " + item for item in value if item not in ITEM_DATA)
                elif key == "skills":
                    errors.extend(source + ": unknown skill " + skill for skill in value if skill not in SKILL_DATA)
                elif key in ("met", "alive", "present", "recruited", "relationships"):
                    errors.extend(source + ": unknown character " + c for c in value if c not in CHARACTER_DATA)
                elif key == "locations":
                    errors.extend(source + ": unknown location " + loc for loc in value if loc not in LOCATIONS)
                elif key not in ("events", "no_events", "flags", "phase_min", "phase_max", "bosses", "choices", "before", "power_min", "power_max", "discovered", "battle_turn_min", "enemy_hp_max", "player_hp_max"):
                    errors.append(source + ": unknown condition " + key)

        def check_effects(effects, source):
            for item in effects.get("items", {}):
                if item not in ITEM_DATA:
                    errors.append(source + ": unknown reward/cost " + item)
            for skill in effects.get("skills", []):
                if skill not in SKILL_DATA:
                    errors.append(source + ": unknown reward skill " + skill)

        for key, location in LOCATIONS.items():
            for view in [location] + location.get("variants", []):
                if not image_exists(view["background"]):
                    errors.append(key + ": missing background " + view["background"])
                check_rule(view.get("when", {}), key)
                action_ids = []
                for action in view["actions"]:
                    action_ids.append(action["id"])
                    for rule in ("when", "visible_when"):
                        check_rule(action.get(rule, {}), key)
                    kind = action["kind"]
                    if kind == "exit" and action["target"] not in LOCATIONS:
                        errors.append(key + ": unknown destination " + action["target"])
                    elif kind == "label" and not renpy.has_label(action["label"]):
                        errors.append(key + ": missing label " + action["label"])
                    elif kind == "battle":
                        if action["enemy"] not in ENEMY_DATA:
                            errors.append(key + ": missing enemy")
                        if action.get("encounter") and action["encounter"] not in ENCOUNTERS:
                            errors.append(key + ": missing encounter policy")
                    elif kind == "gather" and action["item"] not in ITEM_DATA:
                        errors.append(key + ": missing resource")
                # A first encounter and rematch may share an ID when mutually exclusive.
                if len(action_ids) != len(set(action_ids)):
                    duplicates = [a for a in view["actions"] if action_ids.count(a["id"]) > 1]
                    if any(not a.get("visible_when") for a in duplicates):
                        errors.append(key + ": ambiguous action IDs")
        for key, event in STORY_EVENTS.items():
            if not renpy.has_label(event["label"]):
                errors.append(key + ": missing event label")
            if event.get("location") not in (None, *LOCATIONS.keys()):
                errors.append(key + ": missing event location")
            if event.get("automatic") and event.get("repeatable"):
                errors.append(key + ": automatic repeatable events would loop")
            check_rule(event.get("when", {}), key)
            check_effects(event.get("effects", {}), key)
            for variant in event.get("variants", []):
                check_rule(variant.get("when", {}), key)
                check_effects(variant.get("effects", {}), key)
        for key, enemy in ENEMY_DATA.items():
            if not image_exists(enemy["background"]):
                errors.append(key + ": missing battle background")
            if enemy.get("sprite") and not image_exists(enemy["sprite"]):
                errors.append(key + ": missing enemy sprite")
            for skill in enemy.get("grants", []):
                if skill not in SKILL_DATA:
                    errors.append(key + ": unknown Predator reward")
        for key, person in CHARACTER_DATA.items():
            if person.get("sprite") and not image_exists(person["sprite"]):
                errors.append(key + ": missing character sprite")
            for place in person.get("locations", []):
                if place["location"] not in LOCATIONS:
                    errors.append(key + ": missing NPC location")
                check_rule(place.get("when", {}), key)
        for key, ending in ENDINGS.items():
            check_rule(ending["when"], key)
        return errors

    def lint_game_catalogs():
        for error in validate_game_catalogs():
            print("RPG catalog: " + error)

    config.lint_hooks.append(lint_game_catalogs)
