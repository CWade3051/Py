class Name:
   #constructor method - instantiation
   def __init__(self, first, middle, last):
      self.first = first
      self.middle = middle
      self.last = last

   #to-string method
   def __str__(self):
      return self.first + ' ' + self.middle + ' ' + self.last

   def lastFirst(self):
      return self.last + ', ' + self.first + ' ' + self.middle

   def initials(self):
      return self.first[0] + self.middle[0] + self.last[0]

aName = Name('Mary','Elizabeth','Smith')
print('aName is ' + str(aName))
print(aName.lastFirst())
print(aName.initials())