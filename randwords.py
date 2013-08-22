# Random Words
#
# This program will print a list of random words in random order each time.
# The program should print all the words and not repeat any.

# imports
import random

# constants
WORDS = ["OVERUSED", "CLAM", "GUAM", "TAFFETA", "PYTHON"]

# initialize variables
list = []

# do the deed

while len(list) != len(WORDS):
	word = random.choice(WORDS)   # the word to be guessed
	if word not in list:
		print(word)
		list.append(word)