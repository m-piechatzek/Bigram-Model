#####################################################
#                    COMP 4980-03                   #
#                   MONIKA PIECHATZEK               #
#                      PROJECT 1
#
# /Users/monikapiechatzek/Documents/school/tru/tru2017/fall2017/COMP498004/George Elliot/Dickenson/Project1/Gaskell
#
#####################################################

import nltk
from nltk import FreqDist
import os
from tabulate import tabulate
import testingTrivialTokenizer as tt
import re
import pandas as pd

# function to get user input for an existing directory
def directory_input(message):
    path = input(message)
    if os.path.isdir(path):
        return path
    else:
        return directory_input('Enter an existing directory path: ')

# function to print a nxn matrix using tabulate
def print_matrix(bigram_matrix,v_words):
    i = 0
    for row in bigram_matrix:
        row.insert(0, v_words[i])
        i = i + 1
    print(tabulate(bigram_matrix, headers=v_words))
    print('')


rootdir = directory_input("Enter a directory path: ")

# V will be used as the top V most frequency counts
V = 10

# process each file in given directory
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print("Processing ", file, "....")

        # tokenize the file using the simplistic word tokenizer
        tokenized_file = tt.trivialTokenizer(open(rootdir + "/" + file).read())
        # removes all punctuation
        toke_clean = list([])
        for x in tokenized_file:
            if re.match("^[A-Za-z-]+$", x):
                toke_clean.append(x)
        # get the plain frequency distribution from tokenized file from NLTK
        fdist = FreqDist(toke_clean)

        # get the V most frequency counts
        most_common = fdist.most_common(V)

        # this will hold just the top v words to be used as headers
        v_words = []
        for a,b in most_common:
            v_words.append(a)

        # gather all bigrams
        bgrms = list(nltk.bigrams(tokenized_file))
        # does a comparison of the first word in the bigram to the V list
        first_run_bgrms = list([b for b in bgrms if b[0] in v_words])
        # does a second comparison to the second word in the bigram to the V list
        clean_bigram = list([b for b in first_run_bgrms if b[1] in v_words])
        set_clean_bg = list(set([b for b in first_run_bgrms if b[1] in v_words]))

        # create the dictionary with all values set to 0. ex big_dict[word1][word1]=0,big_dict[word1][word2] = 0
        big_dict = {}
        for v in v_words:
            big_dict[v]={}
            for t in v_words:
                big_dict[v][t]= 0
                
        # adds up all the instances of bigrams in the dictionary
        for bg in clean_bigram:
            for k,v in big_dict.items():
                for k1,v1 in v.items():
                    # compares bigrams to dictionary keys to find how many times the bigram appeared
                    if bg[0]== k and bg[1] == k1:
                        big_dict[k][k1]= big_dict[k][k1] + 1

        # create a VxV matrix initialized with VxV zeroes
        bigram_matrix = [[0 for i in range(0,V)] for j in range (0,V)]
        print_matrix(bigram_matrix, v_words)

        # Added my own table using Pandas
        df = pd.DataFrame(big_dict).T
        print(df)
