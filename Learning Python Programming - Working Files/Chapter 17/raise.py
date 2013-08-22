class Rational:
   def __init__(self, x, y):
      numer = x
      if y == 0:
         raise ZeroDivisionError()
      else:
         denom = y

try:
   rat1 = Rational(4,1)
   rat2 = Rational(3,0)
except:
   print("Cannot have a rational number with 0 for denominator.")