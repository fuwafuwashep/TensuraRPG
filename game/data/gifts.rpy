init -10 python:
    def gift_rule(reaction, trust, romance=0, text=None):
        return {"reaction": reaction, "trust": trust, "romance": romance, "text": text}

    GIFT_PREFERENCES = {
        "haruna": {
            "berries": {"early": gift_rule("favorite", 5, 1), "middle": gift_rule("like", 2), "late": gift_rule("like", 1)},
            "stuffed_animal": {"early": gift_rule("like", 3), "middle": gift_rule("favorite", 8, 4, "You remembered what I like. I'll take good care of it."), "late": gift_rule("favorite", 6, 3)},
            "strategy_book": {"default": gift_rule("neutral", 0)},
            "wildflowers": {"default": gift_rule("love", 4, 2)},
        },
        "rigurd": {"berries": {"default": gift_rule("like", 4)}, "strategy_book": {"default": gift_rule("love", 6, 1)}, "stuffed_animal": {"default": gift_rule("neutral", 1)}},
        "hostess_elves": {"wildflowers": {"default": gift_rule("love", 4, 2)}, "strategy_book": {"default": gift_rule("dislike", -1)}},
        "eren": {"berries": {"default": gift_rule("love", 5, 1)}, "stuffed_animal": {"default": gift_rule("like", 3, 1)}},
        "shion": {"strategy_book": {"default": gift_rule("like", 3)}, "wildflowers": {"default": gift_rule("love", 4, 2)}},
        "shuna": {"stuffed_animal": {"default": gift_rule("love", 5, 2)}, "wildflowers": {"default": gift_rule("favorite", 6, 2)}},
        "benimaru": {"strategy_book": {"default": gift_rule("favorite", 7, 1)}, "stuffed_animal": {"default": gift_rule("dislike", -2)}},
        "souei": {"strategy_book": {"default": gift_rule("love", 5)}, "wildflowers": {"default": gift_rule("neutral", 0)}},
        "treyni": {"wildflowers": {"default": gift_rule("dislike", -2)}, "berries": {"default": gift_rule("like", 3)}},
        "souka": {"strategy_book": {"default": gift_rule("love", 5)}, "wildflowers": {"default": gift_rule("like", 3, 1)}},
    }
    GIFT_REACTIONS = {
        "favorite": "You chose this for me? Thank you. It means a lot.",
        "love": "This is lovely. Thank you for thinking of me.",
        "like": "Thank you. I appreciate it.",
        "neutral": "Thank you for the thought.",
        "dislike": "I appreciate the intention, but this isn't really for me.",
        "hated": "Please don't give me something like this again.",
    }

