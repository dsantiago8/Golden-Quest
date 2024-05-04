# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


define Dio = Character("Dio")
define Bruno = Character("Bruno")
define Inez = Character("Inez")
define Sol = Character("Sol")
define pov = Character("[pname]")
define Ofelia = Character("Doña Ofelia")

default Lives = 10


    
    
# The game starts here.

label start:
    show screen timer_screen()
    play music "audio/bgm.mp3" fadein 1.0 volume 0.5
    #inset scene
    #with fade
    python:
        pname = renpy.input("What is your name?", length=32)
        pname = pname.strip()

        if not pname:
            pname = "John"
    
    scene scenerio
    "Welcome [pname], to the city of Dorado!" "You, along with your four friends will embark on a journey to save your neighborhood from developers trying to repurpose the area."
    "The neighborhood is old and has a long mysterious history that you and your friend will discover with the hope that it can save your home."



label expo:
    scene sign
    with fade
    "Exposition" "You and your friends are hanging out in your favorite spot in Dorado Park, when you see a sign that reads “Closing Soon. Area Soon To Be Demolished.”"

label intro:
    scene diegopark
    show screen gameUI
    Dio "You guys hear?"
    scene bashopark
    Bruno "Yeah, it doesn't feel real."
    scene isapark
    Inez "I keep thinking it’s not actually going to happen."
    scene stephpark
    Sol "What are we even gonna do once it's gone?"
    scene bashopark
    Bruno "Maybe it doesn’t have to go though."
    scene stephpark
    Sol "What do you mean?"
    scene bashopark
    Bruno "Have you guys ever heard of that really old story that when this town was founded someone hid a bunch of gold somewhere?"
    scene isapark
    Inez "Gold? Like real gold? What would we even do with that?"
    scene diegopark
    Dio "We could buy out the developers! If we had enough money. That could work right?"
    scene bashopark
    Bruno "I mean, we have to do something. We have to try."
    scene stephpark
    Sol "I think we should too, but where would we start? I’m sure we aren’t the first to look for the gold. People have to know about the legend."
    scene isapark
    Inez "We could ask Doña Ofelia! She might know."
    scene stephpark
    Sol "Why? Cuz she’s old?"
    scene isapark
    Inez "Well that helps, but she kinda just seems to know everything. She has to know something about the gold, right?"
    scene diegopark
    Dio "Well we’ll start there then."
    scene bashopark
    Bruno "What do you think, [pname]?"
    menu:
        "Yeah, let’s go!":
            pass
        "Maybe some other day":
            call life_decrease
            pass
    
    
    play music "audio/purple.mp3" fadein 1.0 volume 0.5

    "Exposition" "You guys leave the park, and head to Doña Ofelia’s home on Brand Street near Old Town. You knock on the door, and she answers with a smile. You ask if she knows anything about the gold, and she invites you guys in."
    scene house with Fade(0.5, 1.0, 0.5)
    "*[Ofelia]'s House*"
    
    scene knock with Fade(0, 0.5, .5)
    play sound "audio/knocking.mp3" volume 2.0
    "*Sol knocks on the door*"
    scene diegoinside
    Dio "We’re sorry to bother out of the blue."
    scene stephinside
    Sol "Yeah, we can imagine a lot of people come to ask you about the gold."
    scene ladyinside
    Ofelia "No no, I’m happy to have visitors. People don’t come by anymore to ask about the gold."
    scene bashoinside
    Bruno "Did they used to?"
    scene ladyinside
    Ofelia "They did a few years back when the mall first opened, and rumors went around that the developers wouldn’t touch Dorado until the gold was found."
    scene isainside
    Inez "Why?"
    scene ladyinside
    Ofelia "I couldn’t tell you. Why does anyone go looking for gold?"
    pov "We thought that if we found it we might be able to save Dorado."
    Ofelia "You kids shouldn’t have to worry about your home being taken away."
    scene diegoinside
    Dio "Do you know where we might look for the gold?"
    scene ladyinside
    Ofelia "I don’t, but you might want to start by looking into the old El Pescador restaurant. The owner is the grandson of the man who is believed to have hidden the gold."
    pov "What 's El Pescador?"
    Ofelia "You’re too young to have known it, but it was a very beloved restaurant run by a wonderful family that had been one of the first families in Dorado. I have a clipping of the article about the restaurant when it first opened."
    scene stephinside
    Sol "Really? That must have been a long time ago."
    scene ladyinside
    Ofelia "It was. I don’t know if it’ll be of any use, but I’ll let you have it."
    "Exposition: You thank Doña Ofelia for her help, and you and your friends leave. You try to read the article, but some words are hard to makeout due to the paper’s old age."

label first_mission:
    #insert scene
    #with fade
    #show characters
    #with fade?
    "First Mission" "Instructions: Use the letter tiles to your right to unscramble the letters on the screen."
    call screen Backdrop("o, n, u, m, i, a, t, n")
    python:
        scrambled_word = "mountain"
        unscrambled = renpy.input("What word do the letters spell?", length=32)
        unscrambled = unscrambled.strip()

        while unscrambled != "mountain":
            
            Lives -= 1 
            unscrambled = renpy.input("What word do the letters spell?", length=32 ) 
            unscrambled = unscrambled.strip()
            
label eval:
    if Lives < 1:
        jump end_credits
    else:
        pass    

label second_mission:
    scene empty
    "Exposition" "You and your friends figure out that the word you couldn’t quite make out in the article is “mountain”, and decide to head to Mountain street off of El Camino road." 
    #insert scene
    #with fade
    #show characters
    #with fade?
    scene bashoempty
    Bruno "Of course, we should have guessed! This is where the old El Pescador restaurant was." 
    scene isaempty
    Inez "It’s just a pile of rubble now. We never would have known it was here if not for the article."
    scene diegoempty
    Dio "I guess developers have been trying to buy this land for a while huh? Why can’t they just leave us alone?"
    scene stephempty
    Sol "The gold might be a reason." 
    scene person
    "Store owner" "You got that right." 
    scene isaempty
    Inez "Who are you?" 
    scene person
    "Store owner" "I own the hardware store just over there. I heard you kids talking about the gold."
    scene bashoempty
    Bruno "Yeah, what about it?" 
    scene person
    "Store Owner" " I just thought you kids might wanna know that some suits came by this site earlier. They were also talking about some gold."
    scene stephempty
    Sol "Why would they be talking about the gold?" 
    scene person
    "Store owner" "Well apparently the only thing keeping them from developing this land is the rumor about the gold. They don’t want to develop until it's found."
    scene diegoempty
    Dio "That’s not good. What if they’re looking for the gold too!"
    scene person
    "Store owner" "I don’t know what you kids intend on doing with the gold, but I know I don’t want the developers finding it. It’s probably better it stay lost." 
    "Exposition" "You and your friends think about what the store owner said. What if the gold is better off staying hidden? That is, of course, until you see something catch your eye in the rubble near your feet."

    menu: 
        "Investigate":
            jump investigate
        "Leave it":
            call life_decrease
            jump third_mission

label investigate:
    pov "Look what I found! It’s a keycard!" 
    scene stephempty
    Sol "One of the developers must have dropped it when they came by earlier."
    scene diegoempty
    Dio "What should we do with it?"
    scene isaempty
    Inez "Well, now that we know the developers are interested in the gold too, shouldn’t we see what they’ve found?"
    scene diegoempty
    Dio "How would we do that?"
    scene bashoempty
    Bruno "I think she’s suggesting we break into their headquarters just outside the neighborhood."
    scene isapark
    Inez "Your words."
    pov "It wouldn’t be breaking in if we have a keycard."
    scene stephempty
    Sol "I can’t believe we’re doing this."

    
label evaluation:
    if Lives < 1:
        call screen Backdrop("You have lost all lives. Try again!")
        python:
            renpy.full_restart()
    else:
        pass    

label third_mission:
    scene building
    play music "audio/green.mp3" fadein 1.0 volume 0.5 
#music change
    #play music "audio/bgm2.mp3" fadein 1.0 volume 0.5
    #insert scene
    "Exposition" "The five of you head to the developer’s headquarters. After entering the building without any trouble, you guys spread out. It’s a small building, but there are still many places to look."
    scene stephbuild
    Sol "This is crazy! We’re gonna get caught!"
    scene bashobuild
    Bruno "We might not, it is the weekend."
    scene isabuild
    Inez "We’ll be fast. It’s not like we set off any alarms."
    "Exposition" "This is the fifth office you guys check, and everyone is starting to lose hope. You start looking around the office."
    pov "Look! This drawer is locked."
    scene diegobuild
    Dio "That’s weird. None of the other drawers were locked."
    scene stephbuild
    Sol "Well we might have a keycard but we definitely don’t have the key to this drawer."
    scene bashobuild
    Bruno "[pname], can you try picking the lock?" 
    pov "I pick one lock and now you guys think I'm a common thief! "
        
#Lock picking written with the help of JessicleCat's locking script 

    # Show the lock-picking interface
    #unsure how to make work without these paarameters
    show screen lockpicking(lock_chest1_lock, "chest1")
    pause
    


label continue_game:

    # After exiting the lock-picking interface, continue with the game
    play music "audio/bgm.mp3"
    "Exposition" "You successfully pick the lock on the drawer, and open it to find a map inside. The map is of your neighborhood, except there are specific locations marked in red. The developer’s also left notes around the map. They were indeed looking for the gold."
    pov "It’s a map."
    scene map
    Bruno "What are all those red x's? There’s one at El Pescador’s demolition site."
    scene stephh
    Sol "These must be all the places they mean to look for the gold! They’re looking for the gold! "
    scene diegoh
    Dio "But why?"
    scene isah
    Inez "Just think, if they have the gold then they can go on with the development plans. It’s because of the gold that they haven’t done anything yet, that’s what that store owner said!"
    pov "Well, they don’t know we have this. We have to check all these places before they do."
    scene map
    Bruno "Where do we start? "
    scene isah
    Inez "This is probably too obvious but, should we look at Tesoro street? It literally means treasure. "
    scene diegoh
    Dio "That’s too obvious."
    scene stephh
    Sol "That could be the point. "
    scene diegoh
    Dio "No, it definitely would have been found by now. "
    menu:
        "Explore Tesoro street":
            call life_decrease
            "Waste of time" "You and your frinds have lost precious time in your quest to save Dorado"
            
        "Naah, no way. Let's go to Old Town instead":
            jump Old_town

label evaluation_3:
    if Lives < 1:
        jump end_credits
    else:
        pass    

label Old_town:
    scene museum
    "Exposition" "You and your friends walk to Old Town. It is a small strip with old storefronts on either side of the road. There isn’t much there besides a few vendors, restaurants, and a museum. You guys decide to enter the museum. "
    scene bashom
    Bruno "We might be able to find something out here. There has to be something about the gold. "
    scene isam
    Inez "You think? It’s just an urban legend. "
    scene diegom
    Dio "Everybody seems to know about it though. "
    scene stephm
    Sol "Here!" 
    "Exposition" "You all run over to where Sol is standing. She is looking at a display about a man named Salvador Romero. "
    scene isam
    Inez "Who’s Salvador Romero?"
    scene stephm
    Sol "It says here he’s the one who buried the gold. Or he knows where it's hidden. "
    scene bashom
    Bruno "Yeah! It says here that the gold was passed down to him, and he buried it for safekeeping. "
    scene diegom
    Dio "What else does it say?" 
    scene stephm
    Sol "There is a snippet from his obituary. It’s so old, I can’t really make out the words.  "
    "Instructions: Use the letter tiles to your right to unscramble the words on the screen."
    # Displaying the centered text with a backdrop
    call screen Backdrop("Use the following words to make out a sentence:\n\tvsirvdue\n\n\tyb\n\n\tsih\n\n\trtage\n\n\terhudgntdara\n\n")
    
    python:
        scrambled_sentence = "survived by his great granddaughter"
        unscrambled = renpy.input("What sentence do the words make up?", length=50)
        unscrambled = unscrambled.strip()

        while unscrambled != "survived by his great granddaughter":
            Lives -= 1
            unscrambled = renpy.input("What sentence do the words make up?", length=50)
            unscrambled = unscrambled.strip()

label evaluation_4:
    if Lives < 1:
        jump end_credits
    else:
        pass    

    scene house2
    "Exposition" "The five of you decide to head to Mills court to pay his great granddaughter a visit. You knock on the door, and an older woman, perhaps in her fifties, opens the door. "
    pov "Hello, are you Salvador Romero’s great granddaughter? "
    scene grandoutside
    "Leia Marquez" "Yes, I’m Leia. Leia Marquez." 
    scene isaho
    Inez "We’re really sorry to bother you, but we were wondering if you could help us. "
    scene grandoutside
    "Mrs. Marquez" "Come on in, it isn’t often we get guests asking about my great grandfather. "
    scene diegoho
    
    Dio "Thank you. We were wonder-"
    scene grand
    "Mrs. Marquez" "My great grandfather was a very kind man. A very people oriented person. I think that’s why he was missed so much."
    scene isah
    Inez "I’m sure he was. We’ve heard our parents speak fondly of him. "
    scene bashoh
    
    Bruno "Do you know wh-"
    scene grand
    "Mrs. Marquez" "He understood the importance of community, and in preserving our shared history. Look, I know you kids are looking for the gold, and I think I know why. I can’t say I don’t admire your effort. "
    scene isah
    Inez "The developer’s visited you already didn’t they? "
    scene grand
    "Mrs. Marquez" "They did. It is important that you know that my grandfather did not hide the gold for safekeeping. He buried it as a way of returning it to the land. "
    scene diegoh
    Dio "So he never meant for it to be found? "
    scene grand
    "Mrs. Marquez" "I’m afraid not. But I can tell you what he told me. "
    pov "What did he tell you? "
    scene mapp
    "Mrs. Marquez" "Yes, before he passed. Towards the end of his life, he had a very specific routine. He would walk to the park in the morning, "
    scene map1
    "Mrs. Marquez" "visit his friend at the Los Arbolitos Housing Complex, " 
    scene map2
    "Mrs. Marquez" "go to El Pescador for lunch, "
    scene map25
    "Mrs. Marquez" "then to visit his cousin Doña Ofelia,"
    scene map4
    "Mrs. Marquez" "then to his daughter, my mother’s, house,"
    scene map5
    "Mrs. Marquez" "and then finally to the corner market before heading home. He didn’t do it everyday. He was old, and only went when his body allowed, but he didn’t want to feel disconnected from his community, especially in his old age. "
    Sol "This town was his gold. "
    scene grand
    "Mrs. Marquez" "Yes, it was. But he also liked games. I suggest you think about what I told you. I must go pick my daughter up from her friend's house now. "
    scene scenerio
    "Exposition" "Back at Dorado park, you guys sit and think about what she said. What did she mean about her great grandfather liking games? What was so important about his relationship with the town?"
    scene isapark
    Inez "Do you guys think he might’ve hid the gold at one of the places she mentioned? "
    scene diegopark
    Dio "But then we would have to check every place. "
    scene bashopark
    Bruno "Well we already know it's not at El Pescador."
    pov "But she was talking about his love for the community. I feel like there has to be a reason she told us his routine. "
    "Exposition" "Suddenly, you have an idea. You go back to the map you took from the developer’s headquarters."
    scene map5
    call screen Backdrop("Use the tacks and thread to make a map of Salvador Romero’s routine")
    


label end_choice:
    centered "Where is the gold located?"
    menu:
        "Tesoro":
            jump life_decrease_2
        "Heritage Square":
            jump success
        "Dorado Park":
            jump life_decrease_2
        "Old Town":    
            jump life_decrease_2

label end_eval:
    if Lives < 1:
        jump end_credits_2
        
    else:
        pass

label what_to_save:
    play sound winsound volume 0.75
    "Congratulations!" "You have found the gold, however it is not enough to save your entire neighborhood. You are left with a difficult decision." 
    menu:
        "Save the school":
            call screen Backdrop("You chose to save the school!")
            python:
                renpy.full_restart()
        "Save the park":
            call screen Backdrop("You chose to save the park!")
            python:
                renpy.full_restart()
        "Save Old Town":
            call screen Backdrop("You chose to save Old Town!")
            python:
                renpy.full_restart()

label life_decrease_2:
    $ Lives -= 1
    "You have lost a life" with hpunch
    jump end_choice 

label life_decrease:
    $ Lives -=1
    "You have lost a life" with hpunch
    return
    
label success:
    if Lives < 1:
        jump end_credits_2
    else:
        jump what_to_save

label end_credits:
    call screen Backdrop("You've lost all lives. Thanks for playing!")
    python:
        renpy.full_restart()

label end_credits_2:
    call screen Backdrop("Even though you found the gold at the end, you stil ran out of lives . Thanks for playing!")
    python:
        renpy.full_restart()

return
    



