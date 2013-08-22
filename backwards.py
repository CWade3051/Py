# Count
# Demonstrates the range() function

print("""
		Welcome to Chuck's backwards word program!
		
	You will start by entering a word,
	then the program will spell it back to you
	backwards!
"""
)
word = input("\nEnter a word you want spelled backwards: ")
backWord = ""

while word:
    position = len(word) - 1
    backWord += word[position]
    word = word[:position] + word[(position + 1):]

print("\nYour word spelled backwards is :", backWord)
input("\n\nPress the enter key to exit.\n")