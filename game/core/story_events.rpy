init -5 python:
    def event_available(event_id):
        data = STORY_EVENTS[event_id]
        return data.get("location") in (None, store.current_location) and (not has_event(event_id) or data.get("repeatable", False)) and conditions_met(data.get("when", {}))

    def available_events(location=None, automatic=None):
        location = store.current_location if location is None else location
        result = []
        for event_id, data in STORY_EVENTS.items():
            if data.get("location") not in (None, location):
                continue
            if automatic is not None and data.get("automatic", False) != automatic:
                continue
            if event_available(event_id):
                result.append(event_id)
        return sorted(result, key=lambda key: (-STORY_EVENTS[key].get("priority", 0), key))

    def event_variant(event_id):
        for variant in STORY_EVENTS[event_id].get("variants", []):
            if conditions_met(variant.get("when", {})):
                return variant["id"]
        return "default"

    def finish_story_event(event_id, variant):
        data = STORY_EVENTS[event_id]
        if has_event(event_id) and not data.get("repeatable", False):
            return
        import copy
        effects = copy.deepcopy(data.get("effects", {}))
        for entry in data.get("variants", []):
            if entry["id"] == variant:
                for key, value in entry.get("effects", {}).items():
                    if key == "items":
                        target = effects.setdefault(key, {})
                        for item, count in value.items():
                            target[item] = target.get(item, 0) + count
                    elif key == "relationships":
                        target = effects.setdefault(key, {})
                        for character, stats in value.items():
                            for stat, amount in stats.items():
                                target.setdefault(character, {})[stat] = target.get(character, {}).get(stat, 0) + amount
                    elif isinstance(value, dict):
                        effects.setdefault(key, {}).update(value)
                    elif isinstance(value, list):
                        effects.setdefault(key, []).extend(value)
                    else:
                        effects[key] = value
        if not conditions_met(data.get("when", {})) or not apply_effects(effects):
            return False
        record_event(event_id, variant)
        return True

    def eligible_endings():
        return [key for key, ending in ENDINGS.items() if conditions_met(ending["when"])]

label run_story_event(event_id):
    if not event_available(event_id):
        return False
    $ selected_variant = event_variant(event_id)
    $ event_scene = STORY_EVENTS[event_id]["label"]
    call expression event_scene pass (selected_variant)
    if _return is not False:
        $ event_completed = finish_story_event(event_id, selected_variant)
        return event_completed
    return False

label view_ending(ending_id):
    if ending_id not in eligible_endings():
        return
    $ ending_title = ENDINGS[ending_id]["title"]
    $ ending_summary = ENDINGS[ending_id]["summary"]
    n "[ending_title]"
    n "[ending_summary]"
    if ending_id not in world_state["endings"]:
        $ world_state["endings"].append(ending_id)
    return
