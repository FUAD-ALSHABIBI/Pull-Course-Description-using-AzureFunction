import nltk
nltk.download('punkt')
nltk.download('brown')
from nltk.corpus import brown

text = "concept , objective and international business practice und er international economic , social and political environment , organization structure , policy form ulation , international finance investment , production , marketing , human resources and management information system under current economic environment ."

arr = nltk.word_tokenize(text)

word_list = brown.words()
word_set = set(word_list)

vowels = {"a","i","o","u","e"}
participle = {"ing", "ed","as"}
for i,word in enumerate(arr):
  if len(arr)-1 == i:
      break
  if word in participle:
    fixWord = arr[i-1] + word
    fixWord2 = word + arr[i+1]
    if fixWord in word_set:
      arr[i] = fixWord
      arr.pop(i-1)
      continue
    elif fixWord2 in word_set:
      arr[i] = fixWord2
      arr.pop(i-1)
      continue


  if word in vowels:
    fixWord = word + arr[i+1] 
    fixword2 = fixWord[:len(fixWord)-1]
    if fixWord in word_set or fixWord[:len(fixWord)-1] in word_set:
       arr[i] = fixWord
       arr.pop(i+1)
       continue
    
  if word in word_set:
    continue
  else:
    fixWord = word + arr[i+1] 
    if fixWord in word_set:
      arr[i] = fixWord
      arr.pop(i+1)
    elif arr[i-1] + word in word_set:
      arr[i-1] = arr[i-1] + word
      arr.pop(i)

print(arr)