number = 0
total = 0
average = 0.0
count = 0
while True:
    print("Enter a number: ")
    number = float(raw_input())
    if number == -1:
       break
    total = total + number
    count = count + 1
average = total / count
print("Average: " + str(average))