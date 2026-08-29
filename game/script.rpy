# script.rpy

label start:

    # Play the opening cutscene.
    call opening_cutscene

    # After the cutscene, begin the actual game.
    jump region_01_start
