class Account:
   def __init__(self, acctNumber, balance):
      self.acctNumber = acctNumber
      self.balance = balance

   def __str__(self):
      return "Account number: " + str(self.acctNumber) + "\n" + \
             "Balance: " + str(self.balance)

class Checking(Account):
   def __init__(self, acctNumber, balance, fee):
      Account.__init__(self, acctNumber, balance)
      self.fee = fee

   def __str__(self):
      retStr = "Account type: Checking\n";
      retStr += Account.__str__(self)
      return retStr

   def getFee(self):
      return self.fee

   def deposit(self, amount):
      self.balance += amount

   def withdraw(self, amount):
      if amount > self.balance:
         print("Insufficient funds.")
      else:
         self.balance = self.balance - amount - self.fee

ca = Checking("123", 500, .50)
print(ca)
ca.withdraw(100)
print(ca)
ca.deposit(200)
print(ca)