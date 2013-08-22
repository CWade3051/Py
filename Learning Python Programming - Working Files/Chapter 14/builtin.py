import os
import math

files = os.popen("dir *.py")
for file in files:
   print(file, end='')

print(math.fabs(-123.45))