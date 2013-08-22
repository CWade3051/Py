import newton

def square(number):
   print("not from the newton module")
   return number * number


num = 12
print("Square from newton.py: ")
print(newton.square(num))
print("Square from main program: ")
print(square(num))