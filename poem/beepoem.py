#  Matthew Hillmer
#  Randomized Bee Movie Poetry
#  9/19/19




#Setup

from google.colab import files

uploaded = files.upload()
for fn in uploaded.keys():
  text = uploaded[fn].decode('utf-8')

import random
from textblob import TextBlob
import nltk
nltk.download('punkt')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
import inflect





#Code

blob = TextBlob(text)

adjlist=[]
for word,tag in blob.tags:
  if tag == "JJ":
   adjlist.append(word)

nounlist=[]
for word,tag in blob.tags:
  if tag == "NN":
    nounlist.append(word)

verblist=[]
for word,tag in blob.tags:
  if tag == "VB":
    verblist.append(word)

def adj():
  return adjlist[random.randint(0,len(adjlist)-1)]
def noun():
  return nounlist[random.randint(0,len(nounlist)-1)]
def verb():
  return verblist[random.randint(0,len(verblist)-1)]
def sentence():
  return blob.sentences[random.randint (0,len(blob.sentences) -1)]

p = inflect.engine()

noun1 = p.plural(noun(),1).lower()

print("\n\n-------------------------\n")
print('\033[1m' + "-The " + noun1 + " is a bee-" + '\033[0m' + "\n")

print("The " + noun1 + " is a bee.")
print("The " + p.plural(noun(),1).lower() + " is a bee.")
print("The " + p.plural(noun(),1).lower() + " is a bee.")
print("All are " + adj() + ", as is the bee.")
print("None are " + adj() + ".")
print("All are bee.\n")

print(verb().upper() + " with the bee.")
print(verb().upper() + " with the bee.")
print(verb().upper() + " with the bee.")
print("And always " + "be " + adj() + " with the bee.\n")

print("Bee is " + adj() + ".")
print("Bee is " + adj() + ".\n")

noun2 = noun()

sentence1 = sentence()

for word in sentence1.split():
  if word in nounlist:
    sentence1 = sentence1.replace(word, noun2)
  if word in verblist:
    sentence1 = sentence1.replace(word, verb())
  if word in adjlist:
    sentence1 = sentence1.replace(word, "bee")

sentence1 = sentence1.replace("I", "the bee")
sentence1 = sentence1.replace("you ", "the bee ")
sentence1 = sentence1.replace("-", "")
sentence1 = sentence1.replace("Oan't", "Can't")

print("And when the bee exclaims with all of its " + adj() + "ness: \n     \"",end='')

for i in range(len(sentence1.split())):
  if(i % 2 == 0):
    print('\033[93m' + sentence1.split()[i] + " ", end='')
  else:
    print('\033[0m' + sentence1.split()[i] + " ", end='')

print('\033[0m' + "\"")

print("The " + noun2 + " of the World becomes " + adj() + ".")
print("The " + noun2 + " of the World becomes bee.")
print("\n-------------------------\n\n")
