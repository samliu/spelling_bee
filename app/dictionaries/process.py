"""
Gather words from various word files used by word game makers and combine into a
JSON object that saves where the word is from.
"""
import json

word_files = ['enable1.txt', 'sowpods.txt', 'TWL06.txt', 'yawl.txt']

words = {}
for word_file in word_files:
  f = open(word_file, 'r')

  for line in f.readlines():
      word = line.split("\n")[0].split("\r")[0].lower()
      words[word] = "From {0}".format(word_file)

print json.dumps(words)
