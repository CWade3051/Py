print("Enter a numeric grade: ")
grade = int(raw_input())
if grade >= 90:
   letterGrade = "A"
elif grade >= 80:
   letterGrade = "B"
elif grade >= 70:
   letterGrade = "C"
elif grade >= 60:
   letterGrade = "D"
elif grade <= 59:
   letterGrade = "F"
else: 
   print("Did not recognize input")
print("Your letter grade is " + letterGrade)