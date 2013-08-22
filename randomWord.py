# Word Jumble
#
# The computer picks a random word and then "jumbles" it
# The player has to guess the letters in the word in 5 tries, then guess the word

import random

# create a sequence of words to choose from
WORDS = ("easy", "peace", "python", "program", "analyzer")

			
# pick one word randomly from the sequence
word = random.choice(WORDS)
# create a variable to use later to see if the guess is correct
correct = word


# start the game
print(
"""
           Welcome to Word Guess!
        
Guess the word based on what letters you guess.

(Press the enter key at the prompt with NOTHING to quit.)
"""
)
print("\nThe word has", len(correct), "letters!")

# setting all my variables here
gCount = 0
gCount2 = 0
letters = ""
wletters = ""
guess = "x"
guessWord = "x"

#This is to allow the user 5 guesses of a letter to see if its in the word or not
while gCount < 5 and guess != "":
	guess = input("Guess a letter: ").lower()
	if guess not in correct:
		if guess not in wletters:
			print("\nThat letter is NOT in the word!")
			wletters += guess
			gCount += 1
		else:
			print("You already guessed the letter and it is NOT in the word!")
	if guess in correct and guess != "":
		if guess not in letters:
			print("\nThat letter IS in the word!")
			letters += guess
			gCount += 1
		else:
			print("You already guessed the letter and it IS in the word!")
		
#Now the users gets 5 guesses to figure out the WORD based on the letters they guessed
if gCount >= 5 and guessWord != "":
	input("\n\nGET Ready to guess the WORD! \n\nYour word is " + str(len(correct)) + " characters long and has these letters in it: " + '"' + letters.upper() + '"' + ", Press ENTER to continue.")
	while gCount2 <=5 and guessWord != "":
		guessWord = input("\nYour WORD guess: ").lower()
		gCount2 += 1
		if guessWord != correct and guessWord != "":
			print("\nYOU SUCK!  Sorry, that's not it.")
		elif guessWord == correct:
			print("\nThat's it!  You guessed it in", gCount2, "tries!")
			break

#End of game	
print("\nThanks for playing.")

input("\n\nPress the enter key to exit.")
