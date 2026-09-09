# New dialogue is deliberately brief and provisional; original scenes stay in West_Jura.
define npc_voice = Character("[npc_name]")

label slice_goblin_meeting(variant):
    if variant == "early_boss":
        n "Prototype variant: The patrol has heard about the powerful enemy you defeated. They seek protection for their settlement."
    elif variant == "forest_hunter":
        n "Prototype variant: The patrol recognizes the cleared rabbit trail. Their elder shares a Healing Blob in thanks."
    call west_jura_goblin_meeting_cutscene
    return True

label npc_interaction(character_id):
    if not character_present(character_id):
        return
    $ meet_character(character_id)
    $ npc_name = CHARACTER_DATA[character_id]["name"]
    show screen npc_portrait(character_id)
    n "Placeholder conversation: [npc_name] is here."
    $ npc_done = False
    while not npc_done and character_present(character_id):
        call screen npc_choices(character_id)
        if _return == "talk":
            if character_id == "haruna":
                npc_voice "There's still plenty to do around the village. Thank you for stopping by."
            elif character_id == "rigurd":
                npc_voice "The village's safety comes first. We are grateful for any help."
            else:
                npc_voice "This conversation is waiting to be written."
            if record_event("talked_" + character_id):
                $ change_relationship(character_id, trust=2)
        elif _return == "gift":
            call screen gift_selection(character_id)
            if _return is not None:
                $ gift_result = give_gift(character_id, _return)
                if gift_result is not None:
                    $ reaction_text = gift_result["text"]
                    npc_voice "[reaction_text]"
        elif _return == "romantic":
            $ relationship_intent[character_id] = "romantic"
            $ world_state["choices"][character_id + "_interest"] = "romantic"
            n "Rimuru expresses romantic interest. Further progress depends on mutual trust and personal events."
        elif _return == "friendly":
            $ relationship_intent[character_id] = "friendly"
            $ world_state["choices"][character_id + "_interest"] = "friendly"
            n "Rimuru keeps the relationship friendly."
        else:
            $ npc_done = True
    hide screen npc_portrait
    return

label slice_haruna_personal(variant):
    n "Placeholder personal scene: Rimuru shares berries and helps Haruna prepare village supplies. She offers a small sewn animal in thanks."
    return True

label slice_haruna_courtship(variant):
    n "Placeholder personal scene: Haruna accepts Rimuru's invitation for a quiet walk."
    return True

label slice_ogre_meeting(variant):
    if variant == "after_orc_lord":
        n "Prototype variant: The ogres arrive after the Orc Lord's defeat. They ask about rebuilding, rather than joining a coming battle."
    else:
        n "Prototype variant: The ogres warn of the Orc Lord. An alliance is possible, but Rimuru can continue without them."
    return True

label slice_ogre_alliance(variant):
    n "Prototype alliance: Rimuru names and recruits the ogres. Full naming scenes and costs will be authored later."
    return True

label slice_orc_aftermath(variant):
    if variant == "before_allies":
        n "Prototype aftermath: The Orc Lord fell before the kijin joined Rimuru. Later recruitment will acknowledge that the war is already over."
    else:
        n "Prototype aftermath: Rimuru's alliance existed before the Orc Lord fell. That shared history remains part of the forest's future."
    return True
