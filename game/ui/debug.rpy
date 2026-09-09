# All entry points and mutation helpers check developer mode; release builds hide it.
init 4 python:
    def debug_mutate(kind, key, amount=1):
        if not config.developer:
            return
        if kind == "item":
            add_item(key, amount)
        elif kind == "skill":
            learn_skill(key, "debug")
        elif kind == "trust":
            change_relationship(key, trust=amount)
        elif kind == "romance":
            change_relationship(key, romance=amount)
        elif kind == "flag":
            set_world_flag(key, not world_flag(key))
        elif kind == "event":
            record_event(key, "debug")
        elif kind == "heal":
            restore_player()

    def debug_teleport(location_id):
        if config.developer and location_id in LOCATIONS:
            enter_location(location_id)

screen rpg_debug():
    style_prefix "rpg"
    tag rpg_panel
    modal True
    zorder 200
    default debug_tab = "Travel"
    default custom_flag = ""
    key "game_menu" action Hide("rpg_debug")
    if config.developer:
        use rpg_panel("Development tools", Hide("rpg_debug")):
            hbox:
                spacing 7
                for tab in ("Travel", "Items", "People", "Skills", "Story", "Battle"):
                    textbutton tab action SetScreenVariable("debug_tab", tab)
            textbutton "Restore HP, MP and move uses" action Function(debug_mutate, "heal", "")
            if debug_tab == "Travel":
                for key, place in LOCATIONS.items():
                    $ discovered = "Visited" if key in world_state["discoveries"] else "Test location"
                    textbutton "[place['title']] • [discovered]":
                        action [Function(debug_teleport, key), Hide("rpg_debug"), Jump("explore_location")]
            elif debug_tab == "Items":
                for key, item in ITEM_DATA.items():
                    textbutton "Give [item['name']] ×5" action Function(debug_mutate, "item", key, 5)
            elif debug_tab == "People":
                text "Normal Trust and personal-event gates also apply to debug Romance changes." size 20
                for key, person in CHARACTER_DATA.items():
                    hbox:
                        spacing 8
                        text person["name"] xsize 270
                        textbutton "Trust +10" action Function(debug_mutate, "trust", key, 10)
                        textbutton "Trust -10" action Function(debug_mutate, "trust", key, -10)
                        if person.get("romanceable"):
                            textbutton "Romance +10" action Function(debug_mutate, "romance", key, 10)
                            textbutton "-10" action Function(debug_mutate, "romance", key, -10)
            elif debug_tab == "Skills":
                for key, skill in SKILL_DATA.items():
                    textbutton "Learn [skill['name']] • [skill['category']]" action Function(debug_mutate, "skill", key) sensitive not has_skill(key)
            elif debug_tab == "Story":
                text "Custom flag or event ID" size 22
                input value ScreenVariableInputValue("custom_flag") length 80 allow "abcdefghijklmnopqrstuvwxyz0123456789_"
                hbox:
                    spacing 15
                    textbutton "Toggle flag" action Function(debug_mutate, "flag", custom_flag) sensitive bool(custom_flag)
                    textbutton "Record event" action Function(debug_mutate, "event", custom_flag) sensitive bool(custom_flag)
                for key in sorted(set(LEGACY_FLAGS) | set(world_state["flags"])):
                    textbutton "[key]: [world_flag(key)]" action Function(debug_mutate, "flag", key)
                label "Event history"
                for key in world_state["history"]:
                    $ variant = world_state["event_details"][key]["variant"]
                    text "[event_index(key) + 1]. [key] • [variant]" size 21
                for key in STORY_EVENTS:
                    textbutton "Mark [key] complete" action Function(debug_mutate, "event", key)
            elif debug_tab == "Battle":
                for key, enemy in ENEMY_DATA.items():
                    textbutton "Test [enemy['name']]" action [Hide("rpg_debug"), Function(renpy.call_in_new_context, "debug_battle", key)]

label debug_battle(enemy_id):
    if not config.developer:
        return
    call battle_enemy(enemy_id, encounter_id=enemy_id if enemy_id in ENCOUNTERS else None)
    return

label debug_slice_start:
    if not config.developer:
        return
    $ migrate_game_state()
    $ learn_skill("mana_perception", "debug")
    $ learn_skill("water_manipulation", "debug")
    jump west_jura_start
