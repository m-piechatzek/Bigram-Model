import re
def trivialTokenizer(text):
   # remove \d+| if you want to get rid of all digit sequences
   pattern = re.compile(r"\d+|Mr\.|Mrs\.|Dr\.|\b[A-Z]\.|[a-zA-Z_]+-[a-zA-Z_]+-[a-zA-Z_]+|[a-zA-Z_]+-[a-zA-Z_]+|[a-zA-Z_]+|--|'s|'t|'d|'ll|'m|'re|'ve|[.,:!?;\"'()\[\]&@#-]")
   return(re.findall(pattern, text))

t = trivialTokenizer('I ran both tokenizers on the combined text of twelve novel by Dickens. The NLTK method takes over 40 seconds on my Mac; the silly tokenizer needs a mere two seconds. I compared their operation on "A Tale of Two Cities": the first 995 tokens are identical. (My elementary code misfires a little on hyphenated words over a line break.) On "Sense and Sensibility": the first 1096 tokens. (My banal code beats the NLTK tool on not attaching single quotes to following letters, and on not rewriting double quotations marks in LaTeX style. To be fair, it loses big way on not recognizing the Saxon genitive, or the possessive \'s.)')

"""
# or, if you want to program less:
import nltk
from nltk.tokenize import RegexpTokenizer
trivialTokenizer = RegexpTokenizer(r"\d+|Mr\.|Mrs\.|Dr\.|\b[A-Z]\.|[a-zA-Z_]+-[a-zA-Z_]+-[a-zA-Z_]+|[a-zA-Z_]+-[a-zA-Z_]+|[a-zA-Z_]+|--|'s|'t|'d|'ll|'m|'re|'ve|[.,:!?;\"'()\[\]&@#-]")

t = trivialTokenizer.tokenize('I ran both tokenizers on the combined text of twelve novel by Dickens. The NLTK method takes over 40 seconds on my Mac; the silly tokenizer needs a mere two seconds. I compared their operation on "A Tale of Two Cities": the first 995 tokens are identical. (My elementary code misfires a little on hyphenated words over a line break.) On "Sense and Sensibility": the first 1096 tokens. (My banal code beats the NLTK tool on not attaching single quotes to following letters, and on not rewriting double quotations marks in LaTeX style. To be fair, it loses big way on not recognizing the Saxon genitive, or the possessive \'s.)')
"""

print('')
print(t)
print('')
print(*t, sep = ' ')
print('')

import os
def file_name_input(prompt):
   path = input(prompt)
   if os.path.isfile(path):
      return path
   else:
      return file_name_input('Enter an existing file path: ')
F = file_name_input('Enter a file path: ')
text = open(F).read()

import time
def print_time(task, stage):
   print('[* clock *]', task, stage, time.clock())

print_time('trivial:', 'in')
t1 = trivialTokenizer(text)
"""
# or:
t1 = trivialTokenizer.tokenize(text)
"""
print_time('trivial:', 'out')

import nltk
print_time('clever:', 'in')
t2 = nltk.word_tokenize(text)
print_time('clever:', 'out')

n = 0
while True:
  if not t1[:n] == t2[:n]:
    break
  else:
    n += 1
print('\nThe first discrepancy: at position', n)
print(t1[n-3:n+2])
print(t2[n-3:n+2])
