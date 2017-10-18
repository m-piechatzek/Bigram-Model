
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
import random
import math
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
    #output_matrix = bigram_matrix[:]
    #for row in output_matrix:
    #    row.insert(0,v_words[i])
    #    i = i + 1
    print(tabulate(bigram_matrix, headers=v_words, tablefmt='orgtbl'))
    print('')

# function to get two sentences from text
# by simplying dividing it in half and adding a period
def get_two_sentences(to_read):
    length = len(to_read)
    sent_1_length = math.floor(length/2)
    sent_1 = []
    sent_2 = []
    to_return = []
    i = 0
    while i < sent_1_length:
        sent_1.append(to_read[i])
        sent_2.append(to_read[i+sent_1_length])
        i = i + 1
    sent_1.append(".")
    sent_2.append(".")
    to_return.append(sent_1)
    to_return.append(sent_2)
    return to_return


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
        #    most_common_counts.append(b)

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

        # sum the rows to get the count to be used for probabilities
        for row in bigram_matrix:
            sum = 0
            for col in row:
                sum = sum + col
            most_common_counts.append(sum)

        # most_common_counts = []

        # for word in v_words:
        #    for a,b in most_common:
        #        if a == word:
        #            most_common_counts.append(b)

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

        i = 0
        for row in smoothed_bigram_counts:
            j = 0
            for col in row:
                probability_matrix[i][j] = float(format((col / most_common_counts_smoothed[i]),'.9f'))
                # print("COL=", col, " UNIGRAM=", most_common_counts_smoothed[i], "i=", i, "j=",j)
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

        # get the sum of the probabilities in each row; each should be ~= 1
        row_num = 0
        for row in probability_matrix:
            sum = 0
            for col in row:
                sum = sum + col
            print("SUM OF PROBABILITIES IN ROW ", row_num, " = ", sum)
            row_num = row_num + 1

        # -- RUN REQUIRED TESTS -- #

        print('')
        print('--------------------------------------------------------------------------------------')
        print('--                                 PERFORM TESTS                                    --')
        print('--------------------------------------------------------------------------------------')
        print("")

        print("1) Generate some new text as in the Shannon game:")
        total_count = 0

        # get the total count to be used to calculate probabilities
        for val in most_common_counts_smoothed:
            total_count = total_count + val

        new_text = [] # will hold the generated text
        sum_1 = 0
        index = 0

        # decide the first word of the new text
        # by generating a random number, and partitioning
        # the probabilities in a roulette selection
        # so the chance of being selected is accurate

        for word in v_words:
            sum_1 = sum_1 + (most_common_counts[index]/total_count) # will eventually add up to 1
            rand_num = random.uniform(0,1) # random number between 0 and 1
            if (rand_num < sum_1):
                selected_index = index
                break
            index = index + 1
        chosen_word = v_words[selected_index]
        new_text.append(chosen_word)

        # loop through and generate the next word based on the bigram probabilities,
        # similarly using a roulette selection, so the likelihood of being selected is
        # accurate

        NUM_LOOPS = 100
        counter = 0
        while counter < NUM_LOOPS:
            rand_num = 0
            test_index = 0
            for row in probability_matrix:
                if test_index == selected_index: # find the row of the prefix of the bigram.
                    j = 0
                    sum_2 = 0
                    new_rand_num = random.uniform(0,1) # generate a random number
                    for col in row:
                        if col > 0.00000001: # overlook bigrams that seem like an error
                            sum_2 = sum_2 + col
                            if new_rand_num < sum_2:
                                # print("FIRST WORD = ", v_words[selected_index], "RAND NUM = ", new_rand_num, " SUM = ", sum_2, " WORD=", v_words[j])
                                new_text.append(v_words[j])
                                break
                            else:
                                j = j + 1
                        else:
                            j = j + 1
                            sum_2 = sum_2 + col
                    # this is now the prefix of the next bigram, calculate again in the loop similarly
                    selected_index = j
                    break
                else:
                    test_index = test_index + 1
            counter = counter + 1

        print('')
        print("-- NEW TEXT --")
        print('')
        print(*new_text)
        print('')

        print("2) Which sentence is more probable?")
        print("")
        print("-- THE SENTENCES --")
        print("")

        # break the text into two sentences
        sentences = get_two_sentences(new_text)
        sentence_1 = sentences[0]
        sentence_2 = sentences[1]
        print("Sentence 1=", *sentence_1)
        print("Sentence 2=", *sentence_2)
        print("")

        # make bigrams of each sentence.
        # probabilities of each bigram will be summed

        sent_1_bigram = list(nltk.bigrams(sentence_1))
        sent_2_bigram = list(nltk.bigrams(sentence_2))

        sent_1_prob_sum = 0

        # we need the index of both words in the bigrams
        for word1, word2 in sent_1_bigram:
            i = 0
            j = 0
            index_1 = 0
            index_2 = 0
            for word in v_words:
                if word != word1:
                    i = i + 1
                else:
                    index_1 = i
                if word != word2:
                    j = j + 1
                else:
                    index_2 = j
            # using the indices found, add to the probability sum
            bigram_probability_1 = probability_matrix[index_1][index_2]
            sent_1_prob_sum = sent_1_prob_sum + bigram_probability_1

        # similarly for the other sentence
        sent_2_prob_sum = 0
        for word1, word2 in sent_2_bigram:
            i = 0
            j = 0
            index_1 = 0
            index_2 = 0
            for word in v_words:
                if word != word1:
                    i = i + 1
                else:
                    index_1 = i
                if word != word2:
                    j = j + 1
                else:
                    index_2 = j
                if word == ".":
                    break
            bigram_probability_2 = probability_matrix[index_1][index_2]
            sent_2_prob_sum = sent_2_prob_sum + bigram_probability_2

        print("PROBABILITY OF SENTENCE 1 = ", sent_1_prob_sum)
        print("PROBABILITY OF SENTENCE 2 = ", sent_2_prob_sum)

        # the sentence with the greater overall probability is more likely
        if sent_1_prob_sum > sent_2_prob_sum:
            greater_prob = "sentence 1"
        else:
            greater_prob = "sentence 2"

        print("So", greater_prob, "is more probable in our model's vocabulary.")
        print("")
