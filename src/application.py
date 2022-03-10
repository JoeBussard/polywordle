#!/bin/python
# copyright joe bussard

import re
import random

WORD_LENGTH = 5


def load_dicts():
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
    return 'pasta'

def generate_test_cases():
    cases = ['pasta', 'ppppp', 'aaaaa', 'sssss', \
            'ttttt', 'altar', 'whack', 'crack',  \
            'atsap', 'sapta', 'tasta', 'tatat', \
            'ooooo', 'wowow', 'snaps', 'licks', \
            'chees', 'paced', 'cough', 'under']
    return cases

def check_guess(guess, word):
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

#     print("guess / word", guess, word)
#     print("yellow letters", yellow_letters)
#     print("green letters", green_letters)

    # green letters take priority over yellow letters
    # if the same letter is yellow AND green, it gets return as green only.
    result = {}
    for i in range(5):
        result[i] = "yellow" if yellow_letters[i] else "black"
        result[i] = "green" if green_letters[i] else result[i]
    #print(result)
    return result

def update_keyboard(key_map, color_map, guess):
    # updates the keyboard
    guess_list = list(guess)
    for x in color_map:
        if key_map[guess_list[x]] != 'green':
            key_map[guess_list[x]] = color_map[x]
    #print (key_map)
    return key_map

def create_keyboard_map():
    keys_only = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g',
            'h','j','k','l','z','x','c','v','b','n','m']
    key_map = {}
    for i in keys_only:
        i = i.lower()
        key_map[i] = 'gray'
    return key_map

def pretty_print_keyboard(key_map):
    print("")
    for y in key_map:
        if y == 'a' or y == 'z':
            print('')
        x = y.upper()
        if key_map[y] == 'gray':
            print(x, '⬜', "  ", sep='',end='')
        elif key_map[y] == 'yellow':
            print(x, '🟨', "  ", sep='', end='')
        elif key_map[y] == 'green':
            print(x, '🟩', "  ", sep='', end='')
        elif key_map[y] == 'black':
            print(x, '⬛', "  ", sep='', end='')
    print("")
    print("")

def create_turn_list():
    turns = [ [] * 5] * 6
    #print(turns)

def update_all(guess, word, key_map, index_map_history):
    # check_guess returns a map from [0...4] to [green, yellow, etc]
    index_color_map = check_guess(guess, word)
    index_map_history.append(index_color_map)
    key_map = update_keyboard(key_map, index_color_map, guess)
    # i dont know what this should return
    return index_color_map, key_map

def create_emoji_hash():
    emoji_hash = {}
    emoji_hash['white'] = '⬜'
    emoji_hash['yellow'] = '🟨'
    emoji_hash['green'] = '🟩'
    emoji_hash['black'] = '⬛'
    return emoji_hash

def pretty_print_share_box(index_color_map_history, emoji_hash):
    for row in index_color_map_history:
        for column in row:
            print(emoji_hash[row[column]], sep='', end='')
        print("")


def pretty_print_index_color(index_color_map, guess, emoji_hash):
    guess_list = list(guess)
    for x in index_color_map:
    #    print('line 122',x)
        print(guess[x].upper(), emoji_hash[index_color_map[x]],"  ", sep='', end='')
    print("")

def get_todays_word(common_words):
    todays_word = random.choice(common_words)
    return todays_word

def test2():
    guess_history = []
    index_map_history = []
    common_words, all_words = load_dicts()
    todays_word = get_todays_word(common_words)
    print("cheating: todays word is", todays_word)
    key_map = create_keyboard_map()
    emoji_hash = create_emoji_hash()
    #index_color_map_history = []

    print("Welcome to Polywordle [version 0.1]")
    pretty_print_keyboard(key_map)
# TODO - add the grid of guesses

    guesses = 0
    while guesses < 6:
        invalid_guess = True
        while invalid_guess:
            current_guess = input(("Guess #"+ str(guesses)+ ": "))
            if len(current_guess) == 5:
                pattern = re.compile("[A-Za-z]+")
                if pattern.fullmatch(current_guess): break
        current_guess = current_guess.lower()

        guesses += 1
        # note sure if this is right
        index_color_map, key_map = update_all(current_guess, todays_word, key_map, index_map_history)
        #index_r_map_history.append(index_color_map)
        guess_history.append(current_guess)
    #    print("line 153", index_map_history[0], "################", guess_history)
        # clear screen
        for x in range(50):print("")
        for x in range(guesses):
    #        print(x)
            pretty_print_index_color(index_map_history[x], guess_history[x], emoji_hash)
        #pretty_print_index_color(index_color_map, current_guess, emoji_hash)
        pretty_print_keyboard(key_map)
        if current_guess == todays_word:
            break
    if current_guess == todays_word:
        print("you won")
    else:
        print("try again next time.")

    print("share your score.")
    pretty_print_share_box(index_map_history, emoji_hash)
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
