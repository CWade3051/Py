# Word Jumble
#
# The computer picks a random word and then "jumbles" it
# The player has to guess the original word

import random

# create a sequence of words to choose from
WORDS = ("python", "jumble", "easy", "difficult", "answer", "xylophone")
HINT = ("Programming langauge this was written with?",
		"What kind of game is this?",
		"This game isnt?",
		"This game is very?",
		"What do you give to a question?",
		"It is a musical instrament?")
			
# pick one word randomly from the sequence
word = random.choice(WORDS)
# create a variable to use later to see if the guess is correct
correct = word

# create a jumbled version of the word
jumble =""
while word:
    position = random.randrange(len(word))
    jumble += word[position]
    word = word[:position] + word[(position + 1):]

# start the game
print(
"""
           Welcome to Word Jumble!
        
   Unscramble the letters to make a word.
If you guess wrong 5 times you will get a hint.
A perfect score is 1000, you lose 100 points for every guess.

(Press the enter key at the prompt to quit.)
"""
)
print("The jumble is:", jumble)

gCount = 0
score = 1000
guess = input("\nYour guess: ")
while guess != correct and guess != "":
	print("Sorry, that's not it.")
	gCount += 1
	guess = input("\nYour guess: ")
	if gCount > 3:
		if correct == "python":
			print(HINT[0])
		elif correct == "jumble":
			print(HINT[1])
		elif correct == "easy":
			print(HINT[2])
		elif correct == "difficult":
			print(HINT[3])
		elif correct == "answer":
			print(HINT[4])
		elif correct == "xylophone":
			print(HINT[5])
	if guess == correct:
		print("\nThat's it!  You guessed it!\n")

#This is what calculates the score
score -= 100 * gCount
if gCount > 9:
	score = '"YOU SUCK BAD"'
	
print("\nYour score is", score, "based on your total guesses count of", gCount, "!")

print("\nThanks for playing.")

input("\n\nPress the enter key to exit.")
