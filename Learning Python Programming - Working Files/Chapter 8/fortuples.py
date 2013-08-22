#numbers = (1,2,3,4,5)
#sum = 0
#for num in numbers:
#   sum = sum + num
#   print(num)
#print("The sum is " + str(sum))
words = ("now","is","time","the")
for word in words:
   print(word)
max = 0
for i in range(1,len(words)):
   if len(words[i]) > len(words[max]):
      max = i
print("The longest word is " + words[max])