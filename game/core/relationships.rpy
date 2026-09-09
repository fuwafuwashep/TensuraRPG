default relationships = {}
default relationship_intent = {}
default gift_history = {}

init -5 python:
    def relationship_value(character_id, stat):
        return store.relationships.get(character_id, {}).get(stat, 0)

    def relationship_stage(character_id):
        trust = relationship_value(character_id, "trust")
        middle, late = CHARACTER_DATA[character_id].get("stages", (30, 65))
        return "late" if trust >= late else "middle" if trust >= middle else "early"

    def romance_limit(character_id, trust):
        gates = CHARACTER_DATA[character_id].get("romance_gates", ())
        return max([0] + [cap for cap, needed_trust, event in gates if trust >= needed_trust and (event is None or has_event(event))])

    def change_relationship(character_id, trust=0, romance=0):
        data = CHARACTER_DATA[character_id]
        values = dict(store.relationships.get(character_id, {"trust": 0}))
        values["trust"] = min(100, max(0, values["trust"] + trust))
        if data.get("romanceable"):
            previous = values.get("romance", 0)
            # Loss of trust does not erase attraction; it blocks further growth.
            upper = max(previous, romance_limit(character_id, values["trust"]))
            values["romance"] = max(0, min(upper, previous + romance))
        store.relationships[character_id] = values

    def gift_preview(character_id, item_id):
        preferences = GIFT_PREFERENCES.get(character_id, {}).get(item_id, {})
        stage = relationship_stage(character_id)
        reaction = dict(preferences.get(stage, preferences.get("default", gift_rule("neutral", 0))))
        repeats = store.gift_history.get(character_id + ":" + item_id, 0)
        # Common repeated gifts cannot replace personal story development.
        factor = 1.0 / (1 + repeats * 0.5)
        for stat in ("trust", "romance"):
            if reaction[stat] > 0:
                reaction[stat] = int(reaction[stat] * factor)
        if store.relationship_intent.get(character_id) != "romantic":
            reaction["romance"] = 0
        return reaction

    def give_gift(character_id, item_id):
        if not character_present(character_id) or not character_state(character_id).get("met"):
            return None
        if not ITEM_DATA[item_id].get("gift") or item_count(item_id) <= 0:
            return None
        result = gift_preview(character_id, item_id)
        remove_item(item_id)
        change_relationship(character_id, result["trust"], result["romance"])
        key = character_id + ":" + item_id
        store.gift_history[key] = store.gift_history.get(key, 0) + 1
        result["text"] = result.get("text") or GIFT_REACTIONS[result["reaction"]]
        record_event("first_gift_" + character_id, result["reaction"], {"item": item_id})
        return result
