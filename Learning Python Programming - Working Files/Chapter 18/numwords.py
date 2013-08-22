sentence = "now is the time for all good people to come"
sentence += " to the aid of their party"
words = sentence.split(' ')
words = sorted(words)
print("Sentence in sorted order:\n")
print(words)
numWords = {}
for i in range(0, len(words)):
   if words[i] in numWords:
      numWords[words[i]] += 1
   else:
      numWords[words[i]] = 1
print("Word list and count: \n")
for key in numWords.keys():
   print(key, numWords[key])