# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define p1 = Character("Bob")
define p2 = Character("Rob")
define p3 = Character("Ana")
define p4 = Character("Alice")

define p5 = Character("Grandma")
# Anagram Game Words
define anagram_words = ["gold", "treasure", "neighborhood", "park", "legend"]


# The game starts here.
label start:

    scene intro
    with fade
    "Game Description" "Embark on an exciting adventure in Golden Quest, where you and your friends race against time and contractors to uncover hidden treasure and save your beloved neighborhood."
    "Game Description pt.2" "As rumors of impending demolition swirl, you stumble upon the legend of buried gold that could change everything. Can you outsmart the contractors and secure the future of your community?"
    
    

menu: 
    "Let's do it!":
        jump choice_a
    "Maybe some other time":
        jump choice_b

label show_sign:
    play music "audio/bgm.mp3" volume 0.5
    scene sign
    p1 "Guys, have you seen those before?"
    p2 "..."
    
    menu:
        "Investigate the signs":
            jump investigate_signs
        "Ignore them for now":
            jump ignore_signs

"""label bgm:
    play music "audio/bgm.mp3" fadein 1.0 volume 0.5
    scene start
"""
label first_mission:
    #image walking = Movie(play="walking.webm")

    scene intro
    with fade
    p4 "I've heard they're demolishing the entire neighborhood, including the park... </3"
    p1 "We've got to do something about this"
    "Fast forward ->>"
    p2 "Where are we going to get the money?"
    p1 "My grandma told me a story about some kind of hidden treasure. We should stop by on the way back. It's not too far."
    menu:
        "Let's go! ->":
            jump grandmaHouse #Redirect to walk_to_granmas once completed 
    "Quest" "Go to grandma's house"
    #scene walking
    return

label grandmaHouse:
    show ghouse
    p1 "Hi Grandma!"
    p5 "Hi Bobby, how have you been?"
    menu: 
        "Chat with grandma":
            "jump to chat_grandma"
        "Ask her about the gold":
            "jump to ask_t"
    with fade
    p5 "*Handed you a newspaper"
    jump anagram_game
#label walk_to_grandmas:
    #pass

# Anagram Game Section
label anagram_game:
    
    $ anagram_characters = ['g','o','l','d','t','r','e','a','s','u','r','e','n','e','i','g','h','b','o','r','h','o','o','d','p','a','r','k','l','e','g','e','n','d']
    $ renpy.random.shuffle(anagram_characters)
    $ character_display = ','.join(anagram_characters)
    menu:
        "Word1":
            "jump to choice_x"
            #jump choice_x
        "Word2":
            "jump to choice_y"
            #jump choice_y
        "Word3":
            "jump to choice_z"
            #jump choicie_Z



        
"""label anagram_game:
    # Randomly select a word from the anagram_words list
    $ word_index = renpy.random.randint(0, len(anagram_words) - 1)
    $ scrambled_word = renpy.random.shuffle(anagram_words[word_index])
    
    scene intro
    with fade
    "Anagram Game"
    "Unscramble the word to proceed:"
    "[scrambled_word]"

    #input "Enter your answer:" action Check_Answer:  # Move the input statement here

label Check_Answer:
    $ player_answer = renpy.input("Enter your answer:")
    $ correct_answer = anagram_words[word_index]

    if player_answer.lower() == correct_answer:
        "Correct! You've unscrambled the word."
        jump first_mission  # Proceed with the story
    else:
        "Incorrect! Try again."
        jump anagram_game  # Repeat the anagram game"""

label choice_a:
    jump show_sign

label choice_b:
    "Are you sure?"
    menu:
        "Fine... I'll bite":
            jump show_sign
        "Not my problem":
            return
    
label investigate_signs:
    "choice 2"
    jump first_mission

label ignore_signs:
    scene burning
    p3 "Oh no! The neighborhood has perished."
    return


    
    


return 
