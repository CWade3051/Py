average = 0.0
total = 0
count = 0
print("Enter a grade (-1 to quit): ")
grade = int(raw_input())
while grade != -1:
   total = total + grade
   count = count + 1
   print("Enter a grade (-1 to quit): ")
   grade = int(raw_input())
average = total / count
print("Average grade: " + str(average))