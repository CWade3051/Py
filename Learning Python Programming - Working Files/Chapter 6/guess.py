answer = "Watson"
print("Here is a guessing game. You get three tries.")
print("What is the name of the computer that played on Jeopardy?")
response = raw_input()
if response == answer:
   print("That is right!")
else:
   print("Sorry. Guess again: ")
   response = raw_input()
   if response == answer:
      print("That is right!")
   else:
      print("Sorry. One more guess: ")
      response = raw_input()
      if response == answer:
         print("That is right!")
      else:
         print("Sorry. No more guesses. The answer is " + answer + ".")