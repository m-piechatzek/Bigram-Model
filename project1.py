#####################################################
#                    COMP 4980-03                   #
#                   FRANCESCA RAMUNNO               #
#                      PROJECT 1                    #
#####################################################

import nltk
from nltk import FreqDist
import os
from tabulate import tabulate
import testingTrivialTokenizer as tt

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

        # get the plain frequency distribution from tokenized file from NLTK
        fdist = FreqDist(tokenized_file)

        # get the V most frequency counts
        most_common = fdist.most_common(V)

        # this will hold just the top v words to be used as headers
        v_words = []
        for a,b in most_common:
            v_words.append(a)

        # create a VxV matrix initialized with VxV zeroes
        bigram_matrix = [[0 for i in range(0,V)] for j in range (0,V)]

        print_matrix(bigram_matrix, v_words)




