def fact(number):
   product = 1
   for i in range(1,number+1):
      product *= i
   return product

print("Enter a number: ")
num = int(input())
print(str(num) + "! equals " + str(fact(num)))