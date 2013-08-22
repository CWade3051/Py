class Person:
   def __init__(self, name, sex, age):
      self.name = name
      self.sex = sex
      self.age = age

   def __str__(self):
      return self.name + ' ' + self.sex + ' ' + str(self.age)

   def changeName(self, name):
      self.name = name

   def changeAge(self):
      self.age = self.age + 1

person1 = Person('Jane Doe','F',23)
person2 = Person('Bob Smith','M',55)
print('Person 1: ' + str(person1))
person1.changeAge()
print('Person 1: ' + str(person1))
person1.changeName('Jane Brown')
print('Person 1: ' + str(person1))
print(person2)