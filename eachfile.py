import PyPDF2
import pandas as pd
import urllib.request
import io
import os
import nltk
nltk.download('punkt')
nltk.download('brown')
from nltk.corpus import brown


def check_reminder(text):
    tokens = nltk.word_tokenize(text)
    container = []
    if tokens[0] == ":":
       tokens.pop(0)
    if ":" in tokens:
        for word in tokens:
          if word == ":":
               break
          container.append(word)
    else:
      container = tokens

    if "." in container:
        while container[len(container)-2] == "etc" or container[len(container)-1] != ".":
           container.pop(len(container)-1)
           
    return " ".join(container)

def clean(text):
    container = nltk.word_tokenize(text)
    arr = text.split(" ")
    arr= list(filter(None, arr))

    if arr in container  :
        for i in range(len(container)):
            if container[i] != arr[i]:
                if container[i]+container[i+1] == arr[i]:
                    container[i] = arr[i]
                    container.pop(i+1)
    if "." in container:
      while container[len(container)-2] == "etc" or container[len(container)-1] != ".":
          container.pop(len(container)-1)
    return " ".join(container)

def fixWord(text):
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
    return " ".join(arr)


pdf_file = open("D:\\Users\\FF\\Desktop\\testOCR\\Approve" + "\\"+ "test24.pdf", 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
num_pages = len(pdf_reader.pages)
description = ""
for page_num in range(num_pages):
     page = pdf_reader.pages[page_num]
 
     page_text = page.extract_text()

     page_text = page_text.lower()
        
     lines = page_text.split('\n')
     

     if len(lines) <2:
         lines = page_text.split('     ')

     found = False
     numWordPerLine = 0   
     results = ""   
     for i in range(len(lines)):
             line = lines[i]
             next_line = lines[i+1] if i+1 < len(lines) else ''

             arr = line.split(" ")
             arr = list(filter(None, arr))

             if numWordPerLine == 0:
               numWordPerLine = len(arr)
             elif numWordPerLine <len(arr):
                 numWordPerLine = len(arr)
          
            
             if line.startswith('course description'):
                found = True
                index = 18
                if ":" in line:
                     index+1
                rest = line[index:]
                if len(rest.strip()) != 0:
                    description = check_reminder(rest)
             elif 'course description' in line:
               found = True
               begin=line.find("course description")
               rest = line[(begin+18):]
               if len(rest.strip()) != 0:
                    description = check_reminder(rest)
               
             elif found == True and line == ' ':
                break
             elif found == True and numWordPerLine/2 > len(arr) and '.' in line:
                description = description + line
                break
             elif found == True: 
               description = description + line

     if description != "":    
          description = clean(description)
          description = fixWord(description)
          results = results + "\nResults of one file : \n " + description.strip() + "\n"


with open("output.txt", "r+", encoding='utf-8') as file:
          #content = file.read()
          #print(content)
          #file.write("")
          file.write(results.lower())
