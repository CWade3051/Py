#file = open('grades.txt')
#grades = file.readlines()
#print(grades)
#for i in range(len(grades)):
#   grades[i] = grades[i].rstrip()
#print(grades)
grades = [grade.rstrip() for grade in open('grades.txt')]
print(grades)