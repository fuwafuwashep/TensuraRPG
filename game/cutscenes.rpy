# cutscenes.rpy

label opening_cutscene:

    scene black
    with fade

    pause 1.0

    centered "..."

    pause 1.0

    n "Everything is dark."

    n "I can't see anything."

    pause 1.0

    n "But I can feel the ground beneath me."

    n "I'm somewhere underground."

    pause 1.0

    return

label veldora_first_meeting:

    scene black
    with fade

    n "Something feels different."

    n "There is an overwhelming presence directly ahead of me."

    pause 1.0

    v "KUHAHAHAHAHA!"

    v "You finally found me!"

    n "A voice suddenly echoes throughout the cavern."

    # Placeholder conversation.
    # Replace this with the actual Veldora conversation later.

    v "Very well! I shall grant you the ability to perceive your surroundings!"

    n "Something changes inside me."

    $ mana_perception = True
    $ telepathy = True

    n "Acquired: Mana Perception."

    n "Acquired: Telepathy."

    # Eventually replace this section with the actual
    # Predator/Stomach cutscene.

    n "Veldora is stored within my Stomach."

    $ veldora_in_stomach = True
    $ met_veldora = True

    pause 1.0

    n "For the first time, the darkness disappears."

    scene cave_visible
    with dissolve

    n "I can see."

    pause 1.0

    n "A pathway I couldn't perceive before has also become visible."

    n "A new path has been unlocked."

    return