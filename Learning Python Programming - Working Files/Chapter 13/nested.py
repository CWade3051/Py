import math

def hypotenuse(s1, s2):
   def square(num):
      return num * num
   return math.sqrt(square(s1) + square(s2))

print("Enter the length of side 1: ")
side1 = int(input())
print("Enter the length of side 2: ")
side2 = int(input())
hyp = hypotenuse(side1, side2)
print("The hypotenuse is " + str(hyp))