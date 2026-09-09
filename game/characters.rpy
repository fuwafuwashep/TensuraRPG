# ============================================================
# CHARACTERS
# ============================================================

# The Storm Dragon is named by the player before the first meeting.
default storm_dragon_name = "Storm Dragon"
default storm_dragon_display_name = "Storm Dragon"

default player_name = "Slime"
default player_family_name = "Tempest"


define v = Character("storm_dragon_display_name", dynamic=True)
define slime_voice = Character("Slime")
define player_voice = Character("player_name", dynamic=True)
define great_sage_voice = Character("Great Sage")
define n = Character(None)


# ============================================================
# STORM DRAGON SPRITE
# ============================================================
# Your repository still currently uses the old image filename/folder.
# If you rename that PNG later, only change the path below.

image storm_dragon dragon = "images/characters/veldora/veldora_dragon.png"


# ============================================================
# STORM DRAGON POSITION
# ============================================================

transform storm_dragon_large:

    xalign 0.5
    yalign 1.0

    zoom 1.05


# ============================================================
# DYNAMIC NAME SYNCHRONIZATION
# ============================================================
# The existing project still uses the internal character key "veldora" for
# save compatibility. The player-facing name is replaced with the name chosen
# for the Storm Dragon.

init 20 python:

    import renpy.store as store

    def sync_storm_dragon_character_name():

        if not hasattr(store, "CHARACTER_DATA"):
            return

        if "veldora" not in store.CHARACTER_DATA:
            return

        display_name = getattr(
            store,
            "storm_dragon_display_name",
            "Storm Dragon"
        )

        store.CHARACTER_DATA["veldora"]["name"] = display_name


    config.after_default_callbacks.append(
        sync_storm_dragon_character_name
    )

    config.after_load_callbacks.append(
        sync_storm_dragon_character_name
    )
