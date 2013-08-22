def square(number):
   return number * number

num = 2
sqnum = square(num)
sqnumber = square
sqnum = sqnumber(2)
print(sqnum)

#map higher-order function
numbers = [1,2,3,4]
numberssq = list(map(square, numbers))
print(numberssq)