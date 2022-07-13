import numpy as np

with open('Downloads\wordle\wordle_words.txt') as f:
    lines = f.readlines()

def filter_black_letter(cur_words, letter, unknowns, blacks, yellows, bi, yi):
    for i in bi:
        cur_words = list(filter(lambda x: letter not in x[i], cur_words))
    for i in yi:
        if not (letter in blacks and letter in yellows):
            cur_words = list(filter(lambda x: letter not in x[i], cur_words))
    return cur_words

def filter_green_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: letter == x[pos], cur_words))
    return new_cur_words

def filter_yellow_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: (letter != x[pos]) and (letter in x), cur_words))
    return new_cur_words

def get_words_from_guess(cur_words, word, colors):
    unknowns, bi, yi  = get_unknowns(colors)
    blacks = []
    yellows = []
    for b in bi:
        blacks.append(word[b])
    for y in yi:
        yellows.append(word[y])
    for i in range(5):
        if colors[i] == 'b':
            cur_words = filter_black_letter(cur_words, word[i], unknowns, blacks, yellows, bi, yi)
        elif colors[i] == 'y':
            cur_words = filter_yellow_letter(cur_words, word[i], i)
        elif colors[i] == 'g':
            cur_words = filter_green_letter(cur_words, word[i], i)
        else:
            return "error"

    return cur_words

def get_unknowns(colors):
    blacks = []
    yellows = []
    unknowns = []
    for i in range(5):
        if colors[i] != 'g':
            unknowns.append(i)
            if colors[i] == 'b':
                blacks.append(i)
            elif colors[i] == 'y':
                yellows.append(i)
    return unknowns, blacks, yellows

def get_suggestion(cur_words, unknowns):
    score_record = np.zeros(len(cur_words))
    for u in unknowns:
        for i in range(len(cur_words)):
            for j in range(len(cur_words)):
                word = cur_words[i]
                other = cur_words[j]
                if i != j and word[u] == other[u]:
                    score_record[i] += 1
    index = np.argmax(score_record)
    return cur_words[index]

def run_game():
    cur_wordlist = lines
    starters = ['slice', 'tried', 'crane']
    print("##################### START #######################")
    guess = np.random.choice(starters)
    guess = get_suggestion(cur_wordlist, get_unknowns('bbbbb')[0])
    print("NEXT GUESS:", guess)
    count = 0
    while True:
        print("Enter the colors you got:")
        colors = str(input())
        if colors == 'ggggg':
            print("hurray! we won :)")
            break
        cur_wordlist = get_words_from_guess(cur_wordlist, guess, colors)
        if not cur_wordlist:
            print("no more words!!!")
            break
        guess = get_suggestion(cur_wordlist, get_unknowns(colors)[0])
        print("NEXT GUESS:", guess)
        count += 1
        if count == 6:
            print("Out of Tries!")
            break

run_game()