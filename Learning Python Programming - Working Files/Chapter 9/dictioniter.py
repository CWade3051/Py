grades = {'Cynthia':88, 'David':77, 'Clayton':99}
#for key in grades.keys():
#   print(key, grades[key])
it = iter(grades)
print(next(it))
print(next(it))
for key in grades:
   print(key, grades[key])