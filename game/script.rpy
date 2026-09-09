# ============================================================
# GAME START
# ============================================================

label start:

    $ migrate_game_state()

    call opening_cutscene

    jump stormdragons_cave_start
