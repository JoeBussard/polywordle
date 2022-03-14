#!/bin/python
# copyright joe bussard

import re
import random

WORD_LENGTH = 5

class text_colors:
    """Defines how to use colors for terminals
    TODO: Does this work on other machines?
    TODO: Does this work on Windows terminals?"""
    BOLD = '\033[1m'
    YELLOW = BOLD + '' + '\033[93m'
    GREEN = BOLD + '' + '\033[96m'
    RED = BOLD + '' + '\033[91m'
    END = '\033[0m'

# Easier lookup (text_hash[x]) than text_colors.x
text_hash = {'yellow':text_colors.YELLOW,'green':text_colors.GREEN,'red':text_colors.RED,'white':''}

def load_dicts():
    """Opens the 2 dictionaries in use, a smaller dictionary
    of more common words, and a larger dictionary with
    words that the user could guess.
    TODO: Make this an API call to improve space constraints"""
    common_words = []
    all_words = []
    with open('common-fives') as f:
        data_common = f.read()
        for x in data_common.split():
            common_words += [x]
    with open('all-fives') as f:
        data_all = f.read()
        for word in data_all.split():
            all_words += [word]
    return common_words, all_words


def generate_word(length):
    """legacy"""
    return 'pasta'

def generate_test_cases():
    """legacy"""
    cases = ['pasta', 'ppppp', 'aaaaa', 'sssss', \
            'ttttt', 'altar', 'whack', 'crack',  \
            'atsap', 'sapta', 'tasta', 'tatat', \
            'ooooo', 'wowow', 'snaps', 'licks', \
            'chees', 'paced', 'cough', 'under']
    return cases

def check_guess(guess, word):
    """checks if a guess matches a word. returns a hash map.
    the hash map is a mapping from i in range(0,6) and 'yellow', 'green', or 'red'"""

    # print("----------------------------")
    guess_list = list(guess)
    word_list = list(word)

    green_letters = [''] * WORD_LENGTH          # array of letters that are correct & in right spot
    yellow_letters = [''] * WORD_LENGTH         # array of letters that are in the word but wrong spot
    gray_letters = [''] * WORD_LENGTH           # letters that aren't in the word at all
    remaining_letters = word_list[:]            # make a copy of the word

    index = 0
    for g, w in zip(guess_list, word_list):     # first take out the green letters
        if g == w:
            green_letters[index] = g
            remaining_letters[index] = ''
        index += 1

    index = 0

    # print("letters eligible for yellow:", remaining_letters)

    for g in guess_list:                       # letters that aren't green may be yellow.
        word_index = 0
        for r in remaining_letters:
            if g == r:
                yellow_letters[index] = g
                remaining_letters[word_index] = ''
                word_index += 1
                break
            word_index += 1
        index += 1

    # green letters take priority over yellow letters
    # if the same letter is yellow AND green, it gets return as green only.
    result = {}
    for i in range(5):
        result[i] = "yellow" if yellow_letters[i] else "red"
        result[i] = "green" if green_letters[i] else result[i]
    #print(result)
    return result

def update_keyboard(key_map, color_map, guess):
    """Input is a keyboard map. It updates that keyboard map and returns it.
    The keyboard map connects the keys 'qwerty....bnm' to collors 'red', 'yellow', or 'green'"""
    # updates the keyboard
    guess_list = list(guess)
    for x in color_map:
        if key_map[guess_list[x]] != 'green':
            key_map[guess_list[x]] = color_map[x]
    #print (key_map)
    return key_map

def create_keyboard_map():
    """Creates the keyboard map. Initializes everything to "grey" because
    the user does not know if the letter is in use or not."""
    keys_only = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g',
            'h','j','k','l','z','x','c','v','b','n','m']
    key_map = {}
    for i in keys_only:
        i = i.lower()
        key_map[i] = 'gray'
    return key_map

def pretty_print_keyboard(key_map):
    """prints the keyboard, color-coded to show which letters are in the word."""
    print("")
    for y in key_map:
        if y == 'a':
            print(f'\n\n  ', end='')
        elif y == 'z':
            print(f'\n\n    ', end='')
        x = y.upper()
        if key_map[y] == 'gray':
            print(                    x,                  "  ", sep='', end='')
        elif key_map[y] == 'yellow':
            print(text_colors.YELLOW, x, text_colors.END, "  ", sep='', end='')
        elif key_map[y] == 'green':
            print(text_colors.GREEN,  x, text_colors.END, "  ", sep='', end='')
        elif key_map[y] == 'red':
            print(text_colors.RED,    x, text_colors.END, "  ", sep='', end='')
    print("")
    print("")

def create_turn_list():
    """Might get rid of this."""
    turns = [ [] * 5] * 6
    #print(turns)

def update_all(guess, word, key_map, index_map_history):
    """Run this command after each turn.  It updates the keyboard map,
    and it updates the index map history. Index map history is what I
    call the mapping of letters in each guess to their colors."""
    # check_guess returns a map from [0...4] to [green, yellow, etc]
    index_color_map = check_guess(guess, word)
    index_map_history.append(index_color_map)
    key_map = update_keyboard(key_map, index_color_map, guess)
    # i dont know what this should return
    return index_color_map, key_map

def create_emoji_hash():
    """returns a dict object hashmap that maps color words to emojis"""
    emoji_hash = {}
    emoji_hash['white']  = '⬜'
    emoji_hash['yellow'] = '🟨'
    emoji_hash['green']  = '🟩'
    emoji_hash['black']  = '⬛'
    emoji_hash['red']    = '🟥'
    return emoji_hash

def pretty_print_share_box(index_color_map_history, emoji_hash):
    """prints the box you get at the end that visualizes guess history"""
    for row in index_color_map_history:
        for column in row:
            print(emoji_hash[row[column]], sep='', end='')
        print("")

def generate_share_box(index_color_map_history, emoji_hash):
    """creates the box you get at the end that visualizes guess history,
    but it does not print it, returns a string."""
    my_string = ''
    for row in index_color_map_history:
        for column in row:
            my_string += emoji_hash[row[column]]
        my_string += f'\n'
    return my_string

def pretty_print_blank_lines(emoji_hash, color):
    """directly prints blank lines with the emoji block of a given color.
    used to visualize the remaining guesses."""
    for x in range(0, 5):
        print("", emoji_hash[color], " ", sep='', end='')
    print(f"\n")

def generate_losing_message(the_answer):
    """useless"""
    print("You lost! The answer was", the_answer)

def generate_share_text(guesses, index_color_map_history, emoji_hash, game_day):
    """generates the full share-text that you copy and paste for friends."""
    string = ''
    string += "Polywordle #" + str(game_day)
    guess_num = guesses if guesses < 6 else 'X'
    string += " " + str(guesses) + "/6"
    string += f'\n'
    string += generate_share_box(index_color_map_history, emoji_hash)
    return string

def pretty_print_index_color(index_color_map, guess, emoji_hash):
    """prints the letters for a guess in the colors that correspond to its game status."""
    guess_list = list(guess)
    for x in index_color_map:
    #    print('line 122',x)
        print(text_hash[index_color_map[x]], guess[x].upper(), text_colors.END,"  ", sep='', end='')
    print(f"\n")

def get_todays_word(common_words):
    """all it does is pick a random word. this could be replaced with an API."""
    todays_word = random.choice(common_words)
    return todays_word

def test2():
    """main game logic. initializes several variables, then jumps into the main loop:
    1. compare a guess
    2. print the new board
    3. repeat."""
    guess_history = []
    index_map_history = []
    common_words, all_words = load_dicts()
    game_day = 0
    todays_word = get_todays_word(common_words)
    #print("cheating: todays word is", todays_word)
    key_map = create_keyboard_map()
    emoji_hash = create_emoji_hash()
    guesses = 0
    #index_color_map_history = []

    print("Welcome to Polywordle [version 0.1]")

    # Print the "blank" board with just empty squares.
    for x in range(guesses, 6):
        pretty_print_blank_lines(emoji_hash, 'white')
    pretty_print_keyboard(key_map)

    while guesses < 6:
        invalid_guess = True
        while invalid_guess:
            current_guess = input(("Guess #"+ str(guesses+1)+ ": "))
            if len(current_guess) == 5:
                pattern = re.compile("[A-Za-z]+")
                if pattern.fullmatch(current_guess):
                    if current_guess.lower() in all_words: break
                    else: print("Not in dictionary.")
                else: print("Must only be letters.")
            else: print("Must be 5 letters.")

        current_guess = current_guess.lower()

        guesses += 1
        # note sure if this is right
        index_color_map, key_map = update_all(current_guess, todays_word, key_map, index_map_history)
        guess_history.append(current_guess)

        # clear screen
        for x in range(50):print("")
        for x in range(guesses):
            pretty_print_index_color(index_map_history[x], guess_history[x], emoji_hash)

        for x in range(guesses, 6):
            pretty_print_blank_lines(emoji_hash, 'white')

        pretty_print_keyboard(key_map)
        if current_guess == todays_word:
            break
    if current_guess == todays_word:
        if guesses == 1:
            print("Unbelievable!")
        elif guesses == 2:
            print("Spectacular!")
        elif guesses == 3:
            print("Amazing")
        elif guesses == 4:
            print("Well done")
        elif guesses == 5:
            print("Pretty good...")
        elif guesses == 6:
            print("That was close")
    else:
        print("Bummer! The word was", todays_word)

    print(f"\nShare your score:\n")
    print(generate_share_text(guesses, index_map_history, emoji_hash, game_day))

    exit(0)

test2()

def test():
    create_turn_list()
    exit(1)
    key_map = create_keyboard_map()
    print(key_map)


    test_word = generate_word(WORD_LENGTH)
    test_input = input("guess a word")
    check_guess(test_input, test_word)
    check_guess("sapta", test_word)
    pretty_print_keyboard(key_map)
    key_map = update_keyboard(key_map, check_guess("pasta", test_word), "pasta")
    pretty_print_keyboard(key_map)
    print(key_map)
    for x in key_map:
        if key_map[x] == 'green':
            print(key_map[x])

    exit(2)
    check_guess("astap", test_word)
    for test in generate_test_cases():
        check_guess(test, "bozos")
    for test in generate_test_cases():
        check_guess(test, "aaaaa")


#test()
