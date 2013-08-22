class Employee:
   def __init__(self, name, payRate):
      self.name = name
      self.payRate = payRate

   def __str__(self):
      return self.name + ", " + str(self.payRate)

   def pay(self, hoursWorked):
      return self.payRate * hoursWorked

class Manager(Employee):
   def __init__(self, name, payRate, isSalaried):
      Employee.__init__(self, name, payRate)
      self.salaried = isSalaried

   def __str__(self):
      retStr = Employee.__str__(self)
      retStr += " salaried: " + str(self.salaried)
      return retStr

   def pay(self, hoursWorked):
      if self.salaried:
         return self.payRate
      else:
         return self.payRate * hoursWorked

e1 = Employee("John Jones", 10.00)
print(e1)
print("Gross pay: " + str(e1.pay(40)))
m1 = Manager("Jane Smith", 1200, True)
print(m1)
print("Gross pay: " + str(m1.pay(40)))
m2 = Manager("Jim Brown", 20.00, False)
print(m2)
print("Gross pay: " + str(m2.pay(40)))