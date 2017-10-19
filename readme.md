** V must be 120 or less otherwise our model runs very slow **

Our model analyzes each text file individually, not once, overall. First we do the basics and search in our directory for text files then tokenize them while clearing out all punctuation. Next we get the plain frequency distribution from the tokenized file, then we gather up the V most frequency counts of those tokens. Next we create the top most frequent bigrams by comparing both words in each tuple to our most common V words. We then organize our filtered bigrams into a nested dictionary with each value representing a count of how many times the bigram appeared.

We then created a VxV matrix initialized with VxV zeroes. Then we populated the matrix with the bigram frequency counts.

Next we administer the bigram laplace smoothing, we get L which is the number of bigrams with only 1 to 9 occurences. Then we increase each bigram count by 1/L and put into a matrix.

Then we create Laplace smoothing for unigrams, we get that by value + (V/L) and then appending to a list and output it.

Our next step is getting maximum likelihood estimate probabilities, which is bigram count / unigram count. We create an empty matrix and fill it with those values and output it.

Now we perform a sanity check. We get the sum of the probabilities in each row and each should be ~=1, which we also output.

We also created our own performance tests. In our first test, we generate a sentence in a similar way as the Shannon game is played. For that we decide the first word by generating a random number and partitioning the probabilities in a roulette selection so the change of being selected is accurate. Then we loop through and generate the next word based on the bigram probabilities, similarly using a roulette selection, so the likelihood of being selected is accurate.

In our second test we create two sentences from the previous test. We make bigrams of each sentence and get the probabilities of each and then sum them. We then compare them to see which one is more probable and then output the results.
