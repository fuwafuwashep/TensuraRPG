# ============================================================
# STORM DRAGON'S CAVE
# ============================================================
# The file was renamed from Veldoras_Cave.rpy to Stormdragons_Cave.rpy.
# The project still uses a few old internal flag/character keys for save
# compatibility, but the player-facing Storm Dragon name is chosen by the user.


# ============================================================
# CAVE BACKGROUNDS
# ============================================================
# Your repository still currently uses the original PNG filenames.
# If you rename those PNGs later, only change the paths in this block.

image cave_blind = Solid("#000000")

image cave_branch_d = "images/backgrounds/VeldoracaveBranchD.png"
image cave_branch_lr = "images/backgrounds/VeldoracaveBranchLR.png"
image cave_branch_lsr = "images/backgrounds/VeldoracaveBranchLSR.png"
image cave_branch_s = "images/backgrounds/VeldoracaveBranchS.png"
image cave_branch_sg = "images/backgrounds/VeldoracaveBranchSG.png"

image cave_lake_1 = "images/backgrounds/VeldoracaveLake1.png"
image cave_lake_2 = "images/backgrounds/VeldoracaveLake2.png"

image cave_lake_empty_1 = "images/backgrounds/VeldoracaveLakeEmpty1.png"
image cave_lake_empty_2 = "images/backgrounds/VeldoracaveLakeEmpty2.png"


# ============================================================
# CHASM BACKGROUNDS
# ============================================================

image cave_chasm_l = "images/backgrounds/VeldoracaveChasmL.png"
image cave_chasm_m = "images/backgrounds/VeldoracaveChasmM.png"
image cave_chasm_s = "images/backgrounds/VeldoracaveChasmS.png"
image cave_chasm_r = "images/backgrounds/VeldoracaveChasmR.png"


# ============================================================
# STORM DRAGON CUTSCENE IMAGES
# ============================================================
# These are the filenames that currently exist in your repository.

image storm_dragon_cutscene_normal = "images/veldoracutscene/VeldoraCutsceneNormal.png"
image storm_dragon_cutscene_tsundere = "images/veldoracutscene/VeldoraCutsceneTsundere.png"
image storm_dragon_cutscene_laughing = "images/veldoracutscene/VeldoraCutsceneLaughing.png"
image storm_dragon_cutscene_swallowed = "images/veldoracutscene/VeldoraCutsceneSwallowed.png"

image storm_dragon_cutscene_story_1 = "images/veldoracutscene/VeldoraCutsceneStorypart1.png"
image storm_dragon_cutscene_story_2 = "images/veldoracutscene/VeldoraCutsceneStorypart2.png"
image storm_dragon_cutscene_story_3 = "images/veldoracutscene/VeldoraCutsceneStorypart3.png"
image storm_dragon_cutscene_story_4 = "images/veldoracutscene/VeldoraCutsceneStorypart4.png"
image storm_dragon_cutscene_story_5 = "images/veldoracutscene/VeldoraCutsceneStorypart5.png"
image storm_dragon_cutscene_story_6 = "images/veldoracutscene/VeldoraCutsceneStorypart6.png"
image storm_dragon_cutscene_story_7 = "images/veldoracutscene/VeldoraCutsceneStorypart7.png"
image storm_dragon_cutscene_story_8 = "images/veldoracutscene/VeldoraCutsceneStorypart8.png"
image storm_dragon_cutscene_story_9 = "images/veldoracutscene/VeldoraCutsceneStorypart9.png"
image storm_dragon_cutscene_story_10 = "images/veldoracutscene/VeldoraCutsceneStorypart10.png"

image storm_dragon_vision_white = Solid("#FFFFFF")


# ============================================================
# PLACEHOLDER EXIT
# ============================================================

image cave_exit_placeholder = Solid("#555555")


# Compatibility alias used by older code.
image cave_visible = "images/backgrounds/VeldoracaveBranchD.png"


# ============================================================
# PLAYER ABILITIES
# ============================================================

default mana_perception = False
default telepathy = False

default water_manipulation = False
default heat_resistance = False
default cold_resistance = False
default electricity_resistance = False
default paralysis_resistance = False


# ============================================================
# STORY FLAGS
# ============================================================
# These old variable names are kept because core/state.rpy already migrates and
# reads them. They are internal only; the chosen Storm Dragon name is displayed.

default met_veldora = False
default veldora_in_stomach = False
default gecko_hint_seen = False


# ============================================================
# FIVE-PANEL INTRO FLAGS
# ============================================================

default storm_intro_panel2_herb = False
default storm_intro_panel2_ore = False
default storm_intro_panel4_herb = False
default storm_intro_panel4_ore = False

default hipokute_analysis_seen = False
default magic_ore_analysis_seen = False


# ============================================================
# PART 1 CREATURE FLAGS
# ============================================================

default heat_lizard_absorbed = False
default cold_lizard_absorbed = False
default electric_lizard_absorbed = False
default thunder_frog_defeated = False


# ============================================================
# PART 2 CREATURE FLAGS
# ============================================================

default tempest_serpent_defeated = False
default black_spider_defeated = False
default giant_bat_defeated = False
default evil_centipede_defeated = False
default armorsaurus_defeated = False


# ============================================================
# CHASM FLAGS
# ============================================================

default chasm_thread_unlocked = False

default spider_return_location = "right"


# ============================================================
# RESOURCE FLAGS
# ============================================================

default branch3_ore_absorbed = False
default branch5_ore_absorbed = False
default veldora_ore_absorbed = False

default branch4_herbs_absorbed = False
default lake1_herbs_absorbed = False
default lake2_herbs_absorbed = False
default frog_herbs_absorbed = False


# ============================================================
# LEGACY RESOURCE COUNTERS
# ============================================================

default magic_ore_clusters = 0
default hipokute_herb_clusters = 0


# ============================================================
# COMBAT
# ============================================================

default player_max_hp = 300
default player_hp = 300


# ============================================================
# CUTSCENE SKIP BUTTON
# ============================================================

screen storm_dragon_cutscene_skip():

    zorder 300

    textbutton "Skip Cutscene":

        xalign 0.985
        yalign 0.035

        xsize 190
        ysize 54

        background "#20252BCC"
        hover_background "#39434DE8"

        text_size 21
        text_color "#F2F2F2"
        text_xalign 0.5
        text_yalign 0.5

        action Jump("storm_dragon_naming_section")


# ============================================================
# BACKGROUND HELPERS
# ============================================================

label update_cave_view(view_type="D"):

    if not mana_perception:

        if view_type == "S":
            scene cave_branch_sg

        else:
            scene cave_blind

        return


    if view_type == "D":
        scene cave_branch_d

    elif view_type == "LR":
        scene cave_branch_lr

    elif view_type == "LSR":
        scene cave_branch_lsr

    elif view_type == "S":
        scene cave_branch_s

    else:
        scene cave_branch_d

    return


label update_lake_1_view:

    if not mana_perception:
        scene cave_blind

    elif lake1_herbs_absorbed:
        scene cave_lake_empty_1

    else:
        scene cave_lake_1

    return


label update_lake_2_view:

    if not mana_perception:
        scene cave_blind

    elif lake2_herbs_absorbed:
        scene cave_lake_empty_2

    else:
        scene cave_lake_2

    return


# ============================================================
# STORM DRAGON'S CAVE START
# ============================================================

label stormdragons_cave_start:

    $ migrate_game_state()
    $ migrate_inventory_grid()
    $ navigation_active = False

    # Keep the old internal region key for compatibility with existing saves.
    $ current_region = "Veldoras_Cave"

    if met_veldora:
        jump cave_branch_2

    scene cave_branch_sg
    with fade

    centered "Storm Dragon's Cave"

    jump storm_cave_intro_panel_1


# Compatibility for older references and saves.
label veldoras_cave_start:
    jump stormdragons_cave_start


# ============================================================
# FIRST FIVE PANELS
# All five use VeldoracaveBranchSG until Mana Perception is acquired.
# ============================================================

label storm_cave_intro_panel_1:

    scene cave_branch_sg

    menu:

        "Move forward":
            jump storm_cave_intro_panel_2


label storm_cave_intro_panel_2:

    scene cave_branch_sg

    menu:

        "Gather strange plant" if not storm_intro_panel2_herb:

            $ storm_intro_panel2_herb = True
            $ add_item("hipokute", 32)

            if not hipokute_analysis_seen:

                $ hipokute_analysis_seen = True

                n "A voice appears in my mind."

                great_sage_voice "Analysis Complete."

                great_sage_voice "This substance is a Hipoutke Herb."

                great_sage_voice "A valuable herb that only grows in magicule-dense areas."

                great_sage_voice "It is used as an ingredient for healing salves and healing potions."

                great_sage_voice "You can create a healing potion with your Unique Skill Predator using the Craft function."

            jump storm_cave_intro_panel_2


        "Gather strange crystal" if not storm_intro_panel2_ore:

            $ storm_intro_panel2_ore = True
            $ add_item("magic_ore", 32)

            if not magic_ore_analysis_seen:

                $ magic_ore_analysis_seen = True

                n "A voice appears in my mind."

                great_sage_voice "Analysis Complete."

                great_sage_voice "Analyzed substance is known as Magic Ore."

                great_sage_voice "These are minerals that spend long periods of time in magicule-dense regions."

                great_sage_voice "It takes a long time, but eventually they begin taking in magicules and become Magic Ore."

                great_sage_voice "These clusters are very valuable."

            jump storm_cave_intro_panel_2


        "Move forward" if storm_intro_panel2_herb and storm_intro_panel2_ore:
            jump storm_cave_intro_panel_3


label storm_cave_intro_panel_3:

    scene cave_branch_sg

    menu:

        "Move forward":
            jump storm_cave_intro_panel_4


label storm_cave_intro_panel_4:

    scene cave_branch_sg

    menu:

        "Gather strange plant" if not storm_intro_panel4_herb:

            $ storm_intro_panel4_herb = True
            $ add_item("hipokute", 32)

            n "The strange plants are absorbed into Predator."

            jump storm_cave_intro_panel_4


        "Gather strange crystal" if not storm_intro_panel4_ore:

            $ storm_intro_panel4_ore = True
            $ add_item("magic_ore", 32)

            n "The strange crystal cluster is absorbed into Predator."

            jump storm_cave_intro_panel_4


        "Move forward" if storm_intro_panel4_herb and storm_intro_panel4_ore:
            jump storm_cave_intro_panel_5


label storm_cave_intro_panel_5:

    scene cave_branch_sg

    menu:

        "Move forward":
            jump storm_dragon_first_meeting


# ============================================================
# ORIGINAL CAVE MAP - NOW ACCESSIBLE AFTER THE FIRST MEETING
# ============================================================

label cave_start:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump cave_branch_1

        "Go right":
            jump heat_lizard_cave

        "Rest":
            $ restore_player()
            n "I rest in the quiet chamber."
            jump cave_start


# ============================================================
# HEAT LIZARD
# ============================================================

label heat_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "I enter a small chamber."

        if not heat_lizard_absorbed:
            n "Something small scurries across the stone."

        menu:

            "Go back":
                jump cave_start


    if not heat_lizard_absorbed:

        n "A small lizard is clinging to the cave wall."

        menu:

            "Absorb the lizard":

                $ heat_lizard_absorbed = True
                $ learn_skill("heat_resistance", "exploration")

                n "The lizard is absorbed."

                n "Acquired: Heat Resistance."

                jump heat_lizard_cave


            "Leave it alone":
                jump cave_start


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_start


# ============================================================
# BRANCH 1
# ============================================================

label cave_branch_1:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump cold_lizard_cave

        "Go right":
            jump cave_branch_2

        "Go back":
            jump cave_start


# ============================================================
# COLD LIZARD
# ============================================================

label cold_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "The air becomes noticeably colder."

        if not cold_lizard_absorbed:
            n "I hear something moving nearby."

        menu:

            "Go back":
                jump cave_branch_1


    if not cold_lizard_absorbed:

        n "A pale lizard rests against the cold stone."

        menu:

            "Absorb the lizard":

                $ cold_lizard_absorbed = True
                $ learn_skill("cold_resistance", "exploration")

                n "The lizard is absorbed."

                n "Acquired: Cold Resistance."

                jump cold_lizard_cave


            "Leave it alone":
                jump cave_branch_1


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_branch_1


# ============================================================
# MAIN THREE-WAY BRANCH
# ============================================================

label cave_branch_2:

    call update_cave_view("LSR")

    menu:

        "Go left" if met_veldora:
            jump cave_part_2_start

        "Go forward":
            jump cave_branch_3

        "Go right":
            jump cave_branch_4

        "Go back":
            jump cave_branch_1


# ============================================================
# OLD STRAIGHT ROUTE - PANEL 1
# ============================================================

label cave_branch_3:

    call update_cave_view("S")

    if not branch3_ore_absorbed:

        n "I come across a strange mineral cluster."

        menu:

            "Absorb the mineral":

                $ branch3_ore_absorbed = True
                $ add_item("magic_ore", 1)

                n "The mineral cluster is absorbed."

                jump cave_branch_3


            "Leave it alone":
                pass


    menu:

        "Move forward":
            jump cave_branch_5

        "Go back":
            jump cave_branch_2


# ============================================================
# OLD STRAIGHT ROUTE - PANEL 2
# ============================================================

label cave_branch_5:

    call update_cave_view("S")

    if not branch5_ore_absorbed:

        n "Another mineral cluster is nearby."

        menu:

            "Absorb the mineral":

                $ branch5_ore_absorbed = True
                $ add_item("magic_ore", 1)

                n "The mineral cluster is absorbed."

                jump cave_branch_5


            "Leave it alone":
                pass


    menu:

        "Move forward":
            jump storm_dragon_approach

        "Go back":
            jump cave_branch_3


# ============================================================
# STORM DRAGON APPROACH
# ============================================================

label storm_dragon_approach:

    call update_cave_view("S")

    menu:

        "Move forward":
            jump storm_dragon_chamber

        "Go back":
            jump cave_branch_5


# Compatibility alias for older saves/calls.
label veldora_approach:
    jump storm_dragon_approach


# ============================================================
# STORM DRAGON CHAMBER
# ============================================================

label storm_dragon_chamber:

    call update_cave_view("D")

    if not met_veldora:

        call storm_dragon_first_meeting

        jump storm_dragon_chamber


    if not veldora_ore_absorbed:

        n "Six enormous clusters of Magic Ore remain near the old seal."

        menu:

            "Absorb the six clusters":

                $ veldora_ore_absorbed = True
                $ add_item("magic_ore", 6)

                n "All six clusters are absorbed."

                jump storm_dragon_chamber


            "Leave them alone":
                pass


    n "The enormous chamber is quiet now."

    menu:

        "Go back":
            jump storm_dragon_approach


# Compatibility alias for older saves/calls.
label veldora_chamber:
    jump storm_dragon_chamber


# ============================================================
# STORM DRAGON FIRST MEETING
# ============================================================

label storm_dragon_first_meeting:

    $ navigation_active = False

    scene cave_blind
    with fade

    # This is a player-facing setup prompt. The character remains unknown to
    # the slime in the story until the formal introduction below.
    $ storm_dragon_name = renpy.input("What should the Storm Dragon you are about to meet be called?", default="", length=24).strip()

    if not storm_dragon_name:
        $ storm_dragon_name = "Storm Dragon"

    $ storm_dragon_display_name = storm_dragon_name
    $ sync_storm_dragon_character_name()

    show screen storm_dragon_cutscene_skip

    v "Can you hear me, small one?"

    $ grant_skill("telepathy")

    great_sage_voice "Common Skill: Telepathy acquired."

    v "Hey! I know you can hear me!"

    slime_voice "Y-you're talking to me?"

    v "Answer me."

    slime_voice "Easy for you to say! How am I supposed to talk without a mouth!?"

    v "Small one!"

    slime_voice "Just shut up already, dumbass!"

    v "Oh? You called me a dumbass? I see you have guts."

    slime_voice "Uh ..."

    v "HRRRAAAAHHHH!!"
    with hpunch

    v "I was trying to be nice since I haven't had a visitor in so long, but you seem to have a death wish."

    slime_voice "Sorry, sorry! I didn't realize you could hear my thoughts! I don't even have a mouth or even eyes, you see ..."

    v "KUAHAHAHAHAAAHAAA! It amazed me that you would say such a thing after seeing me, but it turns out you can't see me. All right. I will give you sight."

    slime_voice "Huh?"

    v "Under conditions. What do you say?"

    slime_voice "What sort of conditions?"

    v "Simple. You must not fear me when you have the ability to see me, and you must come talk to me again. That is all. A good deal for you, is it not?"

    slime_voice "That's all?"

    v "Yes. You see, I was sealed here 300 years ago. Ever since, I've had nothing to do. It's been unbearably boring. Now what do you say?"

    slime_voice "Well, I'm curious why you were sealed, but I'll gladly do it!"

    v "Very well. There is a skill called Mana Perception. Can you use it?"

    slime_voice "Uh ... No?"

    v "It allows you to sense the magicules around you."

    slime_voice "I see ... Well, I guess I can try."

    n "I try to sense the surrounding magicules. The magicules are so dense that they are surprisingly easy to feel."

    $ grant_skill("mana_perception")

    great_sage_voice "Extra Skill: Mana Perception acquired."

    slime_voice "Huh?! Was it that easy!? Also, extra?"

    great_sage_voice "Extra Skills possess power and efficiency magnitudes higher than those of normal skills."

    slime_voice "Ohhh!? That sounds powerful!"

    menu:

        "Use Mana Perception":
            pass


    slime_voice "Ohh?!?! I can finally see!"

    scene storm_dragon_vision_white
    with Fade(0.10, 0.10, 0.20, color="#FFFFFF")

    pause 0.20

    scene storm_dragon_cutscene_normal
    with Dissolve(1.20)

    n "I look around the cavern and finally see that I am, indeed, a slime."

    v "Well?"

    slime_voice "Oh right! I did it! Thank you so much!"

    n "I bounce backward, look toward the voice, and finally see him for the first time."

    slime_voice "Waaahh?!?! A D-Dragon?!"

    n "The Storm Dragon gestures me closer, and I shuffle toward him warily."

    v "Allow me to formally introduce myself. I am the Storm Dragon, [storm_dragon_display_name]."

    slime_voice "Storm Dragon?"

    v "I am one of only four True Dragons that exist in this world. Huahaha, KUHAHAHAHAAAHAAA! You remember our promise, don't you?"

    slime_voice "O-Of course! I-I'm not scared at all! Well, I'll come to chat again sometime!"

    n "I try to shuffle away from the dragon."

    v "Hold it!"

    slime_voice "Heee!!! O-Okay ..."

    v "This is indeed unusual. Slimes normally are monsters that don't have thought, but you have self-awareness. Are you unique?"

    slime_voice "What does unique mean?"

    v "It refers to a being with extraordinary abilities."

    slime_voice "Well, I don't know if I'm unique or not. The thing is, I used to be human, but I died and, well, next thing I knew, I looked like this."

    v "I see. So you are an Otherworlder?"

    slime_voice "So they are people that came here from other worlds?"

    v "Hmmm. Indeed. We call them Otherworlders. I've heard that they gain special abilities when they cross into this world."

    slime_voice "I see. I think I'd like to try and find some of these Otherworlders."

    scene storm_dragon_cutscene_tsundere
    with dissolve

    v "What? You're leaving already?"

    slime_voice "Ehh, you're pouting!?"

    slime_voice "Ermm ... I, uhm. Maybe I'll stay a little longer ... It's not like I have anything to do."

    scene storm_dragon_cutscene_normal
    with dissolve

    v "Oh, good! Stay as long as you like!"

    slime_voice "So, um, you said earlier that you were sealed here, right?"

    v "I'm glad you asked that! It was 300 years ago ..."

    scene storm_dragon_cutscene_story_1
    with dissolve

    v "I sort of turned a town into ashes by mistake."

    slime_voice "Sort of?"

    scene storm_dragon_cutscene_story_2
    with dissolve

    v "So someone came looking to slay me. I might've underestimated my opponent a bit. I started putting my full strength into the battle partway through ... But I still lost!"

    slime_voice "But you seem so strong? Was your opponent that powerful?"

    scene storm_dragon_cutscene_story_3
    with dissolve

    v "Yes, very powerful. It was someone known to the humans as a hero, who is blessed with divine protection."

    scene storm_dragon_cutscene_story_4
    with dissolve

    slime_voice "A human hero? Sounds like something out of a video game."

    scene storm_dragon_cutscene_story_5
    with dissolve

    v "She overpowered me with her Unique Skill, Absolute Severance, and then she sealed me using Unlimited Imprisonment."

    slime_voice "Is that shiny stuff here Unlimited Imprisonment?"

    scene storm_dragon_cutscene_story_6
    with dissolve

    v "Yes. The hero called herself a Summon. A Summon takes more than 30 mages to perform a ritual that lasts several days to bring an Otherworlder here from another world."

    slime_voice "Oh! So there are mages here! This sounds more and more like a game!"

    scene storm_dragon_cutscene_story_7
    with dissolve

    v "They're expected to serve as powerful weapons."

    scene storm_dragon_cutscene_story_8
    with dissolve

    slime_voice "Weapons?"

    v "Yes, for the Summoner. Magic is used to carve a curse into the Summon's soul. This is to ensure that the Summon can't defy the Summoner."

    slime_voice "What?! That's just cruel!"

    scene storm_dragon_cutscene_story_9
    with dissolve

    v "Cruel? Hmm? I don't know what your world was like, but here survival of the fittest is the prevailing truth in this world."

    scene storm_dragon_cutscene_story_10
    with dissolve

    slime_voice "I see ... So you've been in here ever since that hero sealed you?"

    scene storm_dragon_cutscene_tsundere
    with dissolve

    v "Yes, that is correct. I've been so very bored."

    slime_voice "I can't imagine being all alone for 300 years ..."

    slime_voice "Then! How about this. Why don't you and I be friends?"

    scene storm_dragon_cutscene_laughing
    with dissolve
    with hpunch

    v "What?! A mere slime proposes friendship with me, the feared Storm Dragon?!"

    slime_voice "I-If you don't want to, I understand ..."

    scene storm_dragon_cutscene_tsundere
    with dissolve

    v "F-Fool! No one said I didn't want to!"

    slime_voice "Uh, really? Then is that a yes?"

    v "Yes, well ... if you insist ... I guess I'm willing to think about it."

    slime_voice "Are you some tsundere?!"

    slime_voice "Fine! Yes, I insist! That settles it! If you refuse, we're through. I'll never come here again!"

    scene storm_dragon_cutscene_normal
    with dissolve

    v "W-well, all right. I'll be your friend. You'd better be grateful!"

    slime_voice "You just can't be honest, can you? Well, glad to meet you."

    v "I-indeed."

    slime_voice "So, what do we do?"

    v "Hmmm?"

    slime_voice "Well, I feel bad knowing my friend's been sealed here for 300 years. So is there any way to undo the seal?"

    v "You ... would help me?"

    slime_voice "Don't give me those puppy dog eyes! It'd be one thing coming from a cute girl, but a dragon?"

    v "Well, if you have a way to get me out, I'd appreciate it."

    v "Th-the thing is ... I actually wouldn't have lasted another 100 years before my magicules ran out. I keep losing more and more magicules. If this continues, well ... It's not a huge deal. I would just die."

    slime_voice "I see ... After all those years of isolation, you just die, huh? Well, might as well try this."

    slime_voice "Great Sage, use Predator to consume the Unlimited Imprisonment."

    great_sage_voice "Failed."

    slime_voice "I guess it's not that easy."

    v "See, it's impossible."

    slime_voice "Isn't there anything we can do?"

    great_sage_voice "Examining the possibilities. Examination complete. Possibilities include analyzing Unlimited Imprisonment from inside and out. Notice: this would take a long time to complete."

    v "Are you really sure you want to stay in here that long? W-well, not that I mind, but ... That is a long time."

    slime_voice "Well, good point. Since I'm here, I'd like to search for others from my homeland. So here's a suggestion."

    v "A suggestion?"

    slime_voice "Want to get in my stomach?"

    slime_voice "Y-You'll be quarantined within my Unique Skill Predator, so you are guaranteed not to disappear."

    scene storm_dragon_cutscene_laughing
    with dissolve
    with hpunch

    v "HUAH HUAHHH HAHAHA KWAAHAHAHAHAHAHAAAHAAA! Interesting! Please, do it! I'll entrust my entirety to you!"

    slime_voice "Are you sure you want to believe me that easily?"

    scene storm_dragon_cutscene_normal
    with dissolve

    v "Of course! It sounds more fun to break through Unlimited Imprisonment together than wait here alone until you come back!"

    slime_voice "I see ... then should I?"

    jump storm_dragon_naming_section


# ============================================================
# CUTSCENE SKIP TARGET / NAMING / SWALLOWING
# ============================================================

label storm_dragon_naming_section:

    hide screen storm_dragon_cutscene_skip

    # Skipping the cutscene should not skip the abilities needed afterward.
    $ grant_skill("telepathy")
    $ grant_skill("mana_perception")

    scene storm_dragon_cutscene_normal
    with dissolve

    v "W-Wait! Before we start, I'll give you a name. It will engrave onto our souls the fact that we are equals. It will be what humans call a family name. But the name I will give you will even grant you divine protection. You are still nameless, so you'll become a monster with a name."

    slime_voice "Well then, our family name will be ..."

    $ player_family_name = renpy.input("What should your family name be?", default="Tempest", length=24).strip()

    if not player_family_name:
        $ player_family_name = "Tempest"

    $ storm_dragon_display_name = (storm_dragon_name + " " + player_family_name).strip()

    $ sync_storm_dragon_character_name()

    $ player_name = renpy.input("What does %s name you?" % storm_dragon_display_name, default="Rimuru", length=24).strip()

    if not player_name:
        $ player_name = "Rimuru"

    $ battle_player_name = player_name.upper()

    $ world_state["choices"]["family_name"] = player_family_name
    $ world_state["choices"]["storm_dragon_name"] = storm_dragon_display_name
    $ world_state["choices"]["player_name"] = player_name

    v "Very well. You shall be named [player_name]."

    player_voice "All right then, I'm going to eat you. Break out of that stupid seal!"

    scene storm_dragon_cutscene_swallowed
    with dissolve

    pause 1.0

    $ veldora_in_stomach = True
    $ met_veldora = True

    # These three old resource nodes represent the ore already encountered on
    # the forced five-panel approach, so do not award it a second time.
    $ branch3_ore_absorbed = True
    $ branch5_ore_absorbed = True
    $ veldora_ore_absorbed = True

    $ meet_character("veldora")
    $ sync_storm_dragon_character_name()

    $ record_event("met_veldora")
    $ record_event("veldora_in_stomach")

    $ add_item("storm_dragon", 1)

    n "[storm_dragon_display_name] and Unlimited Imprisonment are stored inside Predator."

    n "The Storm Dragon occupies a 7 by 7 section of Stomach while the seal is analyzed."

    jump storm_dragon_chamber


# Compatibility alias for old code.
label veldora_first_meeting:
    jump storm_dragon_first_meeting


# ============================================================
# HERB BRANCH
# ============================================================

label cave_branch_4:

    call update_cave_view("LR")

    if not branch4_herbs_absorbed:

        n "Several strange medicinal plants grow along the cave floor."

        menu:

            "Absorb the Hipoutke Herbs":

                $ branch4_herbs_absorbed = True
                $ add_item("hipokute", 1)

                n "The herbs are absorbed."

                jump cave_branch_4


            "Leave them":
                pass


    menu:

        "Go left":
            jump underground_lake_1

        "Go right":
            jump cave_branch_6

        "Go back":
            jump cave_branch_2


# ============================================================
# UNDERGROUND LAKE - LEFT
# ============================================================

label underground_lake_1:

    call update_lake_1_view

    if not lake1_herbs_absorbed:

        n "Hipoutke Herbs grow near the water."

        menu:

            "Absorb the herbs":

                $ lake1_herbs_absorbed = True
                $ add_item("hipokute", 1)

                jump underground_lake_1


            "Leave them":
                pass


    menu:

        "Drink the water" if not water_manipulation:
            jump acquire_water_manipulation

        "Continue along the lake":
            jump underground_lake_2

        "Return to Branch 4":
            jump cave_branch_4


# ============================================================
# WATER MANIPULATION
# ============================================================

label acquire_water_manipulation:

    n "I approach the underground lake."

    n "I absorb some of the water."

    pause 1.0

    n "Something changes."

    $ learn_skill("water_manipulation", "exploration")

    n "Acquired: Water Manipulation."

    jump underground_lake_1


# ============================================================
# UNDERGROUND LAKE - RIGHT
# ============================================================

label underground_lake_2:

    call update_lake_2_view

    if mana_perception and not gecko_hint_seen:

        $ gecko_hint_seen = True

        n "Something suddenly moves across the cave wall."

        n "A small gecko."

        n "It notices me and immediately disappears into a crack."

        n "Its body seemed strangely adapted to this cave."

        n "Maybe other lizards like it have developed unusual resistances."


    if not lake2_herbs_absorbed:

        n "More Hipoutke Herbs grow along the shore."

        menu:

            "Absorb the herbs":

                $ lake2_herbs_absorbed = True
                $ add_item("hipokute", 1)

                jump underground_lake_2


            "Leave them":
                pass


    menu:

        "Drink the water" if not water_manipulation:
            jump acquire_water_manipulation_right

        "Go back along the lake":
            jump underground_lake_1


label acquire_water_manipulation_right:

    n "I absorb some of the underground water."

    $ learn_skill("water_manipulation", "exploration")

    n "Acquired: Water Manipulation."

    jump underground_lake_2


# ============================================================
# BRANCH 6
# ============================================================

label cave_branch_6:

    call update_cave_view("LR")

    menu:

        "Go right":
            jump electric_lizard_cave

        "Go left":
            jump thunder_frog_area

        "Go back":
            jump cave_branch_4


# ============================================================
# ELECTRIC LIZARD
# ============================================================

label electric_lizard_cave:

    call update_cave_view("D")

    if not mana_perception:

        n "I hear something moving quickly nearby."

        menu:

            "Go back":
                jump cave_branch_6


    if not electric_lizard_absorbed:

        n "A strange lizard crawls across the cave wall."

        n "Tiny sparks occasionally jump across its skin."

        menu:

            "Absorb it":

                $ electric_lizard_absorbed = True
                $ learn_skill("electricity_resistance", "exploration")

                n "The lizard is absorbed."

                n "Acquired: Electricity Resistance."

                jump electric_lizard_cave


            "Leave it alone":
                jump cave_branch_6


    else:

        n "The chamber is empty."

        menu:

            "Go back":
                jump cave_branch_6


# ============================================================
# THUNDER FROG
# ============================================================

label thunder_frog_area:

    call update_cave_view("D")

    if not thunder_frog_defeated:

        n "A large creature blocks the path."

        n "Electricity crackles across its body."

        n "Thunder Frog"

        n "It appears highly resistant to paralysis."

        menu:

            "Fight the Thunder Frog":
                jump thunder_frog_battle

            "Retreat":
                jump cave_branch_6


    else:

        n "The defeated Thunder Frog is gone."

        if not frog_herbs_absorbed:

            n "Three clusters of Hipoutke Herbs surround the chamber."

            menu:

                "Absorb all three herb clusters":

                    $ frog_herbs_absorbed = True
                    $ add_item("hipokute", 3)

                    n "The herbs are absorbed."

                    jump thunder_frog_area


                "Leave them":
                    pass


        menu:

            "Return to Branch 6":
                jump cave_branch_6


label thunder_frog_battle:

    call battle_thunder_frog

    if _return == "won":

        n "The Thunder Frog has been defeated!"

        $ thunder_frog_defeated = True
        $ learn_skill("paralysis_resistance", "exploration")

        n "Acquired: Paralysis Resistance."

        jump thunder_frog_area


    elif _return == "ran":

        jump cave_branch_6


    else:

        n "I can't continue..."

        menu:

            "Try the battle again":
                jump thunder_frog_battle

            "Retreat to Branch 6":

                $ player_hp = player_max_hp

                jump cave_branch_6


# ============================================================
# PART 2 ENTRANCE
# ============================================================

label cave_part_2_start:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump tempest_serpent_area

        "Go right":
            jump part2_chasm_right

        "Go back":
            jump cave_branch_2


# ============================================================
# TEMPEST SERPENT
# ============================================================

label tempest_serpent_area:

    call update_cave_view("D")

    if not tempest_serpent_defeated:

        n "A massive serpent blocks the path."

        n "Its body shifts as it notices my presence."

        n "Tempest Serpent"

        n "Intrinsic Skill: Heat Source Perception."

        n "It appears capable of using Poison Breath."

        menu:

            "Fight the Tempest Serpent":

                call battle_enemy("tempest_serpent")

                if _return == "won":

                    $ tempest_serpent_defeated = True

                    n "The Tempest Serpent has been defeated."

                    jump tempest_serpent_area


                elif _return == "ran":
                    jump cave_part_2_start


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump tempest_serpent_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump cave_part_2_start


            "Retreat":
                jump cave_part_2_start


    else:

        n "The Tempest Serpent no longer blocks the passage."

        menu:

            "Go forward":
                jump part2_chasm_middle

            "Go back":
                jump cave_part_2_start


# ============================================================
# CHASM R - RIGHTMOST
# ============================================================

label part2_chasm_right:

    scene cave_chasm_r

    menu:

        "Go left":

            $ spider_return_location = "right"

            jump black_spider_area


        "Go back":
            jump cave_part_2_start


# ============================================================
# CHASM S - BLACK SPIDER
# ============================================================

label black_spider_area:

    scene cave_chasm_s

    if not black_spider_defeated:

        n "A large black spider crawls into my path."

        n "Black Spider"

        n "It produces two different kinds of thread."

        n "Sticky Thread and Steel Thread."

        menu:

            "Fight the Black Spider":

                call battle_enemy("black_spider")

                if _return == "won":

                    $ black_spider_defeated = True
                    $ chasm_thread_unlocked = True

                    n "The Black Spider has been defeated."

                    n "Some of its thread remains anchored across the chasm."

                    n "It looks strong enough to swing from."

                    jump black_spider_area


                elif _return == "ran":

                    if spider_return_location == "middle":
                        jump part2_chasm_middle

                    else:
                        jump part2_chasm_right


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump black_spider_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            if spider_return_location == "middle":
                                jump part2_chasm_middle

                            else:
                                jump part2_chasm_right


            "Retreat":

                if spider_return_location == "middle":
                    jump part2_chasm_middle

                else:
                    jump part2_chasm_right


    else:

        menu:

            "Swing across the chasm" if chasm_thread_unlocked:
                jump part2_across_chasm

            "Go left":
                jump part2_chasm_middle

            "Go right":
                jump part2_chasm_right


# ============================================================
# CHASM M - MIDDLE
# ============================================================

label part2_chasm_middle:

    scene cave_chasm_m

    menu:

        "Go left":
            jump giant_bat_area

        "Go right":

            $ spider_return_location = "middle"

            jump black_spider_area

        "Return through the serpent passage" if tempest_serpent_defeated:
            jump tempest_serpent_area


# ============================================================
# CHASM L - GIANT BAT
# ============================================================

label giant_bat_area:

    scene cave_chasm_l

    if not giant_bat_defeated:

        n "Something large moves across the ceiling."

        n "A Giant Bat drops down in front of me."

        n "Giant Bat"

        n "Intrinsic Skills: Drain and Ultrasonic Waves."

        menu:

            "Fight the Giant Bat":

                call battle_enemy("giant_bat")

                if _return == "won":

                    $ giant_bat_defeated = True

                    n "The Giant Bat has been defeated."

                    jump giant_bat_area


                elif _return == "ran":
                    jump part2_chasm_middle


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump giant_bat_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_chasm_middle


            "Retreat":
                jump part2_chasm_middle


    else:

        n "The Giant Bat is gone."

        menu:

            "Go right":
                jump part2_chasm_middle


# ============================================================
# ACROSS THE CHASM
# ============================================================

label part2_across_chasm:

    scene cave_chasm_s

    n "I swing across the chasm using the spider's thread."

    menu:

        "Move forward":
            jump part2_final_branch

        "Swing back across":
            jump black_spider_area


# ============================================================
# FINAL BRANCH
# ============================================================

label part2_final_branch:

    call update_cave_view("LR")

    menu:

        "Go left":
            jump evil_centipede_area

        "Go right":
            jump armorsaurus_area

        "Go back":
            jump part2_across_chasm


# ============================================================
# EVIL CENTIPEDE
# ============================================================

label evil_centipede_area:

    call update_cave_view("D")

    if not evil_centipede_defeated:

        n "A long armored creature crawls across the stone."

        n "Evil Centipede"

        n "Intrinsic Skill: Paralyzing Breath."

        menu:

            "Fight the Evil Centipede":

                call battle_enemy("evil_centipede")

                if _return == "won":

                    $ evil_centipede_defeated = True

                    n "The Evil Centipede has been defeated."

                    jump evil_centipede_area


                elif _return == "ran":
                    jump part2_final_branch


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump evil_centipede_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_final_branch


            "Retreat":
                jump part2_final_branch


    else:

        menu:

            "Go back":
                jump part2_final_branch


# ============================================================
# ARMORSAURUS
# ============================================================

label armorsaurus_area:

    call update_cave_view("D")

    if not armorsaurus_defeated:

        n "A heavily armored monster blocks the tunnel."

        n "Armorsaurus"

        n "Intrinsic Skill: Body Armor."

        menu:

            "Fight the Armorsaurus":

                call battle_enemy("armorsaurus")

                if _return == "won":

                    $ armorsaurus_defeated = True

                    n "The Armorsaurus has been defeated."

                    jump armorsaurus_area


                elif _return == "ran":
                    jump part2_final_branch


                else:

                    n "I can't continue..."

                    menu:

                        "Try again":
                            jump armorsaurus_area

                        "Retreat":

                            $ player_hp = player_max_hp

                            jump part2_final_branch


            "Retreat":
                jump part2_final_branch


    else:

        menu:

            "Move forward":
                jump stormdragon_cave_exit

            "Go back":
                jump part2_final_branch


# ============================================================
# STORM DRAGON'S CAVE EXIT
# ============================================================

label stormdragon_cave_exit:

    $ navigation_active = False
    $ current_location = None

    scene cave_exit_placeholder
    with dissolve

    # Keep the old internal key for compatibility.
    $ current_region = "Veldoras_Cave"

    n "The tunnel begins to open up."

    n "Light is coming from somewhere ahead."

    n "The exit of Storm Dragon's Cave is just beyond this point."

    menu:

        "Go back into Storm Dragon's Cave":
            jump part2_final_branch

        "Step outside":

            $ current_region = "West_Jura"

            jump west_jura_start


# Compatibility alias used by data/locations.rpy and older saves.
label veldora_cave_exit:
    jump stormdragon_cave_exit
