def calc(op1, op2, op):
   if op == '+':
      return op1 + op2
   elif op == '-':
      return op1 - op2
   elif op == '*':
      return op1 * op2
   elif op == '/':
      return op1 / op2

import os

print("Enter file name to open: ")
name = input()
while not os.path.isfile(name):
   print("File does not exist.")
   print("Enter file name to open: ")
   name = input()
file = open(name, 'r')
for line in file:
   print(line,end='')

#cont = 'y'
#while cont != 'n':
#   print("Enter the first number: ")
#   num1 = int(input())
#   print("Enter the second number: ")
#   num2 = int(input())
#   print("Enter operation: ")
#   op = input()
#   if op == '/' and num2 == 0:
#      print("Cannot divide by zero.")
#      continue
#   else:
#      print(calc(num1, num2, op))
#   print("Do you want to continue(y/n)?")
#   cont = input()

