#anonymous function
#lambda form

#def square(number):
#   return number * number

#square = lambda x: x*x
#print(square(2))
numbers = [1,2,3,4]
numberssq = list(map(lambda x:x*x, numbers))
print(numberssq)