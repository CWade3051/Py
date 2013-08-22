#inFile = open('text.txt', 'r')
#line = inFile.readline()
#print(line)
#line = inFile.readline()
#print(line)
count = 0
total = 0
inFile = open('grades.txt', 'r')
grade = inFile.readline()
while (grade):
   print(grade)
   count = count+1
   total = total + int(grade)
   grade = inFile.readline()
average = total / count
print("Average: " + str(average))