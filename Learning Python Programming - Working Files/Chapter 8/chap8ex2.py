bar = ""
for grade in open('grades.txt'):
   for i in range(1, int(grade)+1):
      if i % 5 == 0:
         bar = bar + "*"
   print(bar, i)
   bar = ""