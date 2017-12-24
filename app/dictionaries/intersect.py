"""
Intersects google's 300k list with game words to filter out uncommon words.
"""
import json

words = {}
goog_300 = open('google_300k.json', 'r')
goog_300 = set(json.load(goog_300))

game_words = open('TWL06.json', 'r')
game_words = set(json.load(game_words))

for word in goog_300.intersection(game_words):
    words[word] = 'Intersected from google_300k.json + TWL06.json'

print json.dumps(words)


