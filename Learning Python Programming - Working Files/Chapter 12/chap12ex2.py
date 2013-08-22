# in my humble opinion
#IMHO

def first(word):
   return word[0]

def acronym(words):
   acro = ''
   acro = acro.join(list(map(first, words))).upper()
   return acro

words = ['in','my','humble','opinion']
#acro = list(map(first, words))
#print(acro)
#acro = ''
#acro = acro.join(list(map(first, words))).upper()
acro = acronym(words)
print(acro)