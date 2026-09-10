# Optional panels, leaving the art unobstructed until the player opens one.
style rpg_text is default:
    size 25
    color "#EDF6F4"
style rpg_button is button:
    background "#213E48"
    hover_background "#345D67"
    insensitive_background "#243237"
    padding (18, 12)
    yminimum 52
style rpg_button_text is button_text:
    size 24
    color "#EDF6F4"
    hover_color "#FFFFFF"
    insensitive_color "#819397"
style rpg_label_text is rpg_text:
    size 34
    color "#9EDCCA"

screen rpg_panel(title, close_action):
    style_prefix "rpg"
    add "#050D14C8"
    frame:
        align (0.5, 0.5)
        xysize (1120, 860)
        background "#122933FA"
        padding (36, 30)
        vbox:
            spacing 22
            hbox:
                xfill True
                label title xsize 870
                textbutton "Close" action close_action
            viewport:
                xfill True
                ysize 710
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                mousewheel True
                draggable True
                vbox:
                    xfill True
                    spacing 16
                    transclude

screen location_choices():
    style_prefix "rpg"
    $ place = location_view(current_location)
    $ actions = location_actions(current_location)
    frame:
        xpos 36
        ypos 100
        xsize 910
        background "#10252CC0"
        padding (22, 18)
        vbox:
            spacing 8
            label place["title"]
            text place.get("description", "") size 21
    frame:
        xalign 0.98
        yalign 0.90
        xsize 535
        background "#10252CE8"
        padding (16, 16)
        viewport:
            xfill True
            ysize min(700, len(actions) * 78)
            mousewheel True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                spacing 10
                for action in actions:
                    textbutton action["text"]:
                        id action["id"]
                        xfill True
                        sensitive action["enabled"]
                        action [
                            SetVariable(
                                "pending_nav_action",
                                action["id"]
                            ),
                            Hide("location_choices")
                        ]

screen rpg_inventory_contents(battle=False):
    style_prefix "rpg"
    $ owned = [(key, data) for key, data in ITEM_DATA.items() if item_count(key) > 0]
    if not owned:
        text "Stomach is empty."
    for key, item in owned:
        frame:
            xfill True
            background "#1C3540"
            padding (18, 14)
            vbox:
                spacing 6
                hbox:
                    text "[item['name']]  ×[item_count(key)]" xsize 770
                    if item.get("use"):
                        textbutton "Use":
                            sensitive can_use_item(key)
                            if battle:
                                action [Hide("battle_stomach_menu"), Return(("item", key))]
                            else:
                                action Function(use_item, key)
                text item["category"] size 18 color "#9EDCCA"
                text item["description"] size 21
    if not battle and has_skill("predator") and item_count("hipokute") > 0:
        textbutton "Use Predator • Refine a Healing Blob" action Function(refine_healing_blob)

screen relationships_menu():
    style_prefix "rpg"
    tag rpg_panel
    modal True
    zorder 200
    key "game_menu" action Hide("relationships_menu")
    use rpg_panel("Relationships", Hide("relationships_menu")):
        $ met = [key for key in CHARACTER_DATA if character_state(key).get("met")]
        if not met:
            text "Meet people during your travels to learn about them."
        for key in met:
            $ person = CHARACTER_DATA[key]
            frame:
                xfill True
                background "#1C3540"
                padding (22, 16)
                vbox:
                    spacing 8
                    label person["name"]
                    if not character_state(key).get("alive", True):
                        text "Lost in this timeline" color "#E3ACAF"
                    text "Trust"
                    bar value StaticValue(relationship_value(key, "trust"), 100) xsize 900 ysize 18 left_bar "#77C8B1" right_bar "#2F4851"
                    if person.get("romanceable"):
                        text "Romance • [relationship_intent.get(key, 'friendly').title()]"
                        bar value StaticValue(relationship_value(key, "romance"), 100) xsize 900 ysize 18 left_bar "#D5A0BF" right_bar "#2F4851"
                    text "[relationship_stage(key).title()] connection" size 20 color "#A7BDC5"
        text "Visit people at their current locations to talk or give gifts." size 21

screen status_menu():
    style_prefix "rpg"
    tag rpg_panel
    modal True
    zorder 200
    key "game_menu" action Hide("status_menu")
    use rpg_panel("Rimuru • Status & Journey", Hide("status_menu")):
        text "Level [player_level] • Experience [player_experience] / [player_level * 75]"
        text "HP [player_hp] / [player_max_hp]     Magicules [player_mp] / [player_max_mp]"
        text "Attack bonus [player_attack]     Defence [player_defense]     Speed [player_speed]"
        text "Immunities: [', '.join(player_immunities) or 'None']" size 22
        text "Resistances and learned abilities appear in Skills." size 22
        label "Journey"
        for entry in world_state["history"]:
            text "[event_index(entry) + 1]. [entry.replace('_', ' ').title()]" size 23
        for entry in world_state["legacy_events"]:
            text "Earlier save • [entry.replace('_', ' ').title()] (order unknown)" size 21
        if eligible_endings():
            label "Available epilogues"
            for ending in eligible_endings():
                textbutton ENDINGS[ending]["title"] action Function(renpy.call_in_new_context, "view_ending", ending)

screen npc_portrait(character_id):
    $ person = CHARACTER_DATA[character_id]
    if person.get("sprite"):
        add person["sprite"] xalign 0.35 yalign 1.0
    else:
        frame:
            xpos 340
            ypos 220
            xysize (460, 480)
            background "#203B47D9"
            vbox:
                align (0.5, 0.5)
                spacing 18
                text person["name"] size 38 color "#D9F1E8" xalign 0.5
                text "SPRITE PLACEHOLDER" size 19 color "#A0B9C3" xalign 0.5

screen npc_choices(character_id):
    style_prefix "rpg"
    frame:
        align (0.97, 0.55)
        xsize 510
        padding (20, 20)
        background "#122933EE"
        vbox:
            spacing 12
            textbutton "Talk" action Return("talk") xfill True
            textbutton "Give Gift" action Return("gift") xfill True
            if CHARACTER_DATA[character_id].get("romanceable"):
                if relationship_intent.get(character_id) != "romantic":
                    textbutton "Express romantic interest" action Return("romantic") xfill True
                else:
                    textbutton "Keep things friendly" action Return("friendly") xfill True
            textbutton "Leave" action Return("leave") xfill True

screen gift_selection(character_id):
    style_prefix "rpg"
    modal True
    zorder 200
    key "game_menu" action Return(None)
    use rpg_panel("Choose a gift", Return(None)):
        $ gifts = [key for key, data in ITEM_DATA.items() if data.get("gift") and item_count(key) > 0]
        if not gifts:
            text "You have no gifts. Try gathering in the forest."
        for key in gifts:
            $ name = ITEM_DATA[key]["name"]
            textbutton "[name]  ×[item_count(key)]" action Return(key) xfill True

screen rpg_toolbar():
    style_prefix "rpg"
    if not in_battle:
        hbox:
            xalign 0.98
            ypos 22
            spacing 8
            textbutton "Inventory" action Show("storage_menu")
            textbutton "Skills" action Show("skills_menu")
            textbutton "Loadout" action Show("loadout_menu")
            textbutton "Relationships" action Show("relationships_menu")
            textbutton "Status" action Show("status_menu")
            textbutton "Save" action ShowMenu("save")
            textbutton "Load" action ShowMenu("load")
            textbutton "Settings" action ShowMenu("preferences")
            if config.developer and navigation_active and not renpy.get_screen("npc_portrait"):
                textbutton "Debug" action Show("rpg_debug")
