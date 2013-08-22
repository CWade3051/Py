#word = "hello world!"
#for letter in word:
#   print(letter)
sentence = "now is the time for all good people to come to the aid"
count = 0
for letter in sentence:
   if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'u' \
        or letter == 'o':
      count = count + 1
print("The number of vowels is " + str(count))