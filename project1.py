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
import re
import pandas as pd
import json


# function to get user input for an existing directory
def directory_input(message):
    path = input(message)
    if os.path.isdir(path):
        return path
    else:
        return directory_input('Enter an existing directory path: ')


# function to print a nxn matrix using tabulate
def print_matrix(bigram_matrix, v_words):
    i = 0
    print(tabulate(bigram_matrix, headers=v_words, tablefmt='orgtbl'))
    print('')


rootdir = directory_input("Enter a directory path: ")

# V will be used as the top V most frequency counts
V = 4000

# process each file in given directory
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print("")
        print("--           FOR FILE: ", file, "        --")

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

        # this will hold the frequency counts, to be used later
        most_common_counts = []

        for a, b in most_common:
            v_words.append(a)
            most_common_counts.append(b)

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
            big_dict[v] = {}
            for t in v_words:
                big_dict[v][t] = 0

        # adds up all the instances of bigrams in the dictionary
        for bg in clean_bigram:
            for k, v in big_dict.items():
                for k1, v1 in v.items():
                    # compares bigrams to dictionary keys to find how many times the bigram appeared
                    if bg[0] == k and bg[1] == k1:
                        big_dict[k][k1] = float(big_dict[k][k1] + 1.0)

        # print(json.dumps(big_dict, indent=4))

        # create a VxV matrix initialized with VxV zeroes
        bigram_matrix = [[0 for i in range(0, V)] for j in range(0, V)]

        i = 0
        v_words = []
        for k,v in big_dict.items():
            v_words.append(k)
            j = 0
            for k1, v1 in v.items():
                bigram_matrix[i][j] = v1
                j = j + 1
            i = i + 1

        most_common_counts = []

        for word in v_words:
            for a,b in most_common:
                if a == word:
                    most_common_counts.append(b)

        print('')
        print('--------------------------------------------------------------------------------------')
        print('--                               POPULATED BIGRAM MATRIX                            --')
        print('--------------------------------------------------------------------------------------')
        print('')

        print_matrix(bigram_matrix, v_words)
        print('')

        # Added my own table using Pandas
        #print(" DICTIONARY AFTER POPULATION")
        #df = pd.DataFrame(big_dict).T
        #print(df)

        # -- Perform Laplace smoothing -- #

        print('--------------------------------------------------------------------------------------')
        print("--                             PERFORM LAPLACE SMOOTHING                            --")
        print('--------------------------------------------------------------------------------------')
        print('')

        # first for bigrams
        # let L = number of bigrams with only 1 to 9 occurences
        l = 0

        # get L
        for k,v in big_dict.items():
            for k1, v1 in v.items():
                if v1 > 0 and v1 < 10:
                    l = l + 1

        # this will hold the smoothed bigram values for presentation
        smoothed_bigram_counts = [[0 for i in range(0, V)] for j in range(0, V)]

        # increase each bigram count by 1 / L, put into a matrix
        i = 0
        for k,v in big_dict.items():
            j = 0
            for k1, v1 in v.items():
                smoothed_bigram_counts[i][j] = float(format((v1 + 1/l), '.5f'))
                j = j + 1
            i = i + 1

        print("AFTER BIGRAM LAPLACE SMOOTHING:")
        print('')
        print_matrix(smoothed_bigram_counts,v_words)
        print('')

        # now perform Laplace smoothing for unigrams

        print('UNIGRAMS BEFORE SMOOTHING:')
        print('')
        print(most_common_counts)
        print('')

        # this will hold the unigram count values after laplace smoothing
        most_common_counts_smoothed = []

        for val in most_common_counts:
            most_common_counts_smoothed.append(float(format((val + (V/l)),'.5f')))

        print("UNIGRAMS AFTER SMOOTHING")
        print('')
        print(most_common_counts_smoothed)
        print('')

        # -- GET MAXIMUM LIKELIHOOD ESTIMATE PROBABILITIES -- #
        # bigram count / unigram count

        probability_matrix = [[0 for i in range(0, V)] for j in range(0, V)]


        for row in smoothed_bigram_counts:
            i = 0
            for col in row:
                j = 0
                probability_matrix[i][j] = float(format((col / most_common_counts_smoothed[i]),'.5f'))
                j = j + 1
            i = i + 1


        print('-----------------------------------------------------------------------------------------------------------')
        print("--                             THE MAXIMUM LIKELIHOOD ESTIMATE PROBABILITIES                             --")
        print('-----------------------------------------------------------------------------------------------------------')
        print('')

        print_matrix(probability_matrix,v_words)

        # -- PERFORM SANITY CHECK -- #

        print('--------------------------------------------------------------------------------------')
        print('--                              PERFORM A SANITY CHECK                              --')
        print('--------------------------------------------------------------------------------------')
        print('')
