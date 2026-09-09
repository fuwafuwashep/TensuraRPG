init -2 python:
    STORY_EVENTS = {
        "met_goblins": {
            "title": "Meet the goblin patrol", "location": "goblin_route", "automatic": True,
            "when": {"flags": {"goblins_destroyed": False}}, "label": "slice_goblin_meeting",
            "variants": [
                {"id": "early_boss", "when": {"bosses": ["orc_lord"]}, "effects": {"flags": {"goblins_seek_protection": True}}},
                {"id": "forest_hunter", "when": {"events": ["horn_rabbit_defeated"]}, "effects": {"items": {"healing_blob": 1}, "relationships": {"rigurd": {"trust": 4}}}},
                {"id": "cave_arrival"},
            ],
            "effects": {"flags": {"village_access": True}, "met": ["rigurd"]},
        },
        "haruna_personal": {
            "title": "Help Haruna prepare supplies", "location": "village", "label": "slice_haruna_personal",
            "when": {"met": ["haruna"], "present": ["haruna"], "relationships": {"haruna": {"trust": 20}}, "items": {"berries": 1}},
            "effects": {"items": {"berries": -1, "stuffed_animal": 1}, "relationships": {"haruna": {"trust": 5}}},
        },
        "haruna_courtship": {
            "title": "Invite Haruna for a quiet walk", "location": "village", "label": "slice_haruna_courtship",
            "when": {"events": ["haruna_personal"], "present": ["haruna"], "relationships": {"haruna": {"trust": 60, "romance": 20}}, "choices": {"haruna_interest": "romantic"}},
            "effects": {"relationships": {"haruna": {"trust": 3, "romance": 5}}},
        },
        "ogres_met": {
            "title": "Investigate the ogre settlement (prototype)", "location": "ogre_border", "label": "slice_ogre_meeting",
            "variants": [
                {"id": "after_orc_lord", "when": {"bosses": ["orc_lord"]}, "effects": {"choices": {"ogre_alliance": "reconstruction"}}},
                {"id": "before_orc_lord", "effects": {"choices": {"ogre_alliance": "defence"}}},
            ],
            "effects": {"met": ["benimaru", "shuna", "shion", "souei"]},
        },
        "kijin_recruited": {
            "title": "Offer the ogres an alliance (prototype)", "location": "ogre_border", "label": "slice_ogre_alliance",
            "when": {"events": ["ogres_met"]},
            "effects": {"flags": {"kijin_recruited": True}, "recruited": ["benimaru", "shuna", "shion", "souei"]},
        },
        "orc_aftermath": {
            "title": "Consider the changed forest", "location": "orc_approach", "label": "slice_orc_aftermath",
            "when": {"bosses": ["orc_lord"]},
            "variants": [
                {"id": "before_allies", "when": {"flags": {"orc_lord_early": True}}, "effects": {"choices": {"forest_future": "independent"}}},
                {"id": "with_allies", "effects": {"choices": {"forest_future": "alliance"}}},
            ],
        },
    }
    # These are optional vertical-slice epilogues; viewing never ends exploration.
    ENDINGS = {
        "independent_forest": {"title": "Prototype epilogue: An unexpected protector", "when": {"events": ["orc_aftermath"], "flags": {"orc_lord_early": True}}, "summary": "Rimuru defeated the Orc Lord before recruiting the kijin. The forest must build its alliances around that changed history. Full ending content is pending."},
        "allied_forest": {"title": "Prototype epilogue: A shared defence", "when": {"events": ["orc_aftermath"], "flags": {"orc_lord_early": False, "kijin_recruited": True}}, "summary": "The ogres allied with Rimuru before the Orc Lord fell. Their shared campaign shapes the forest's future. Full ending content is pending."},
        "lost_village": {"title": "Prototype epilogue: An empty settlement", "when": {"flags": {"goblins_destroyed": True}, "choices": {"goblin_defence": "refused"}}, "summary": "Rimuru's refusal left the goblin settlement to the wolves. Its inhabitants will not appear in later village scenes. Full ending content is pending."},
    }
