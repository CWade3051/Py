def square(number):
   return number * number

def numVowels(string):
   string = string.lower()
   count = 0
   for i in range(len(string)):
      if string[i] == "a" or string[i] == "e" or \
         string[i] == "i" or string[i] == "o" or \
         string[i] == "u":
         count += 1 #count = count + 1
   return count

#print("Enter a number: ")
#num = int(input())
#numsquared = square(num)
#print(str(num) + " squared = " + str(numsquared))
print("Enter a string: ")
strng = input()
print("There are " + str(numVowels(strng)) + " vowels in the string.")