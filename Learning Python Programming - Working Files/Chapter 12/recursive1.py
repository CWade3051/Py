#5! = 5 * 4 * 3 * 2 * 1
#5! = 5 * 4!
def fact(number):
   if number <= 1:
      return 1
   else:
      return number * fact(number-1)

print(fact(10))