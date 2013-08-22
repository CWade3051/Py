try:
   print("Enter the name of a file: ")
   name = input()
   file = open(name, 'r')
   #print("Enter a numerator: ")
   #numer = int(input())
   #print("Enter a denominator: ")
   #denom = int(input())
   #quotient = numer / denom
   #print(quotient)
except IOError:
   print("Cannot open file.")
   print("Enter the name of the file to open: ")
   name = input()
   file = open(name, 'r')
except ZeroDivisionError:
   #print("Cannot divide by zero.")
   #print("Enter a new denominator: ")
   #denom = int(input())
   #quotient = numer / denom
   #print(quotient)