try:
   print("Enter a file name: ")
   name = input()
   file = open(name, 'w')
   display(file)
except:
   print("Error with file.")
   print("Enter a file name: ")
   name = input()
   file = open(name, 'w')
   display(file)
finally:
   file.close()