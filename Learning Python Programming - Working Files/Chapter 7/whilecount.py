#examples of count-controlled loops
#sum = 0
#number = 1
#while number <= 10:
#   sum = sum + number
#   number = number + 1
#print("The sum is " + str(sum))
balance = 5000
rate = 1.02
year = 1
while year <= 10:
   balance = balance * rate
   print("Year: " + str(year) + ": " + str(balance))
   year = year + 1

