#explode('hello')->'h e l l o'
#removeDups('aabbcc')->'abc'
def explode(word):
   if len(word) <= 1:
      return word
   else:
      return word[0] + ' ' + explode(word[1:])

def removeDups(word):
   if len(word) <= 1:
      return word
   elif word[0]==word[1]:
      return removeDups(word[1:])
   else:
      return word[0] + removeDups(word[1:])

#print(explode('hello'))
word = 'aabbbccccdd'
print(word)
print(removeDups(word))