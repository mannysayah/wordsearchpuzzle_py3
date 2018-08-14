#!/usr/bin/env python3
# 2018 Manny Sayah - Victoria University of Wellington

import random
import string
import numpy as np
import numpy.ma as ma

# How much meaningful words should take up the puzzle
make_up_total = 0.70

# Grid size 
width = 10
height = 10

# Probabilities
ph = 0.3
pd = 0.3
pv = 0.4

total_words_letters = int(width * height * make_up_total)

filename = 'n_words.txt'
with open(filename) as f:
    data = f.readlines()
#  remove whitespace characters like `\n` at the end of each line
data = [x.strip() for x in data] 
list_of_all_words = []
for x in data:
    if len(x) < width and len(x) < height:
        list_of_all_words.append(x)

data = list_of_all_words

total_take = 0

word_list = []

while total_take < total_words_letters - 4:
    
    item = random.choice(data)

    if len(item) < total_words_letters - total_take:
        word_list.append(item)
        total_take += len(item)

print(word_list)

puzzle = np.zeros((width, height)).astype(int).astype(str)

directions = [[1,0],[0,1],[1,1]]

def existing_word(d,word):
    
    xsize = width if d[0] == 0 else width - len(word)
    ysize = width if d[1] == 0 else height - len(word)

    x = random.randrange(0,xsize)
    y = random.randrange(0,ysize)

    temp_word = []
    
    for i in range(0,len(word)):
        temp_word.append(str(puzzle[y+d[1]*i][x+d[0]*i]))
    return("".join(temp_word),x,y)
    
def compare_them(w1, w2):
    comp = []
    for i,j in zip(w1, w2):
        if j == "0":
            comp.append("Zero")
        else:
            if i == j:
                comp.append("Match")
            else:
                comp.append(False)
            
    if ( comp.count("Match") <= 1 and comp.count(False) == 0 ):
        return True
    else:
        return False

def fill_with_rand(puzzle,w,h):
    mask = ([puzzle == "0"])
    new_puzzle = np.copy(puzzle)
    alpha_puzzle = np.copy([[random.choice(string.ascii_uppercase) for i in range(0,w)] for j in range(0,h)])
    new_puzzle[tuple(mask)] = alpha_puzzle[tuple(mask)]
    return new_puzzle
    
for word in word_list:

    while (True):
        
        word = random.choice([word, word[::-1]]) # word can be backwards
        d = np.random.choice([0,1,2],p=[ph,pv,pd]) # Take a random choice of [0,1,2]
        d = directions[d] # now take that out of [directions]
        
        from_puzzle = existing_word(d, word) # now take an empty space from the puzzle with the same length as the word
    
        x = from_puzzle[1]
        y = from_puzzle[2]
        
        if compare_them(word, from_puzzle[0]):
            for i in range(0,len(word)):
                puzzle[y+d[1]*i][x+d[0]*i] = word[i]
            break
        
print(fill_with_rand(puzzle, width, height))
