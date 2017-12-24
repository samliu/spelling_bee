"""spelling_bee.py: Creates puzzles for NYT's spelling bee game.

Computers are fast. This leverages a ton of linear passes through a dictionary
because it's just for fun and puzzle examples still come back in under a second.
Performance improvements left as exercise to the reader.

No dependencies beyond Python 2.7+.

Author: Sam Liu <sam@ambushnetworks.com>
License: MIT

Expects input as a json file containing values in this format:

{
 "word": "definition",
 "word2": "definition2"
 ...etc
}

Definitions are currently unused.

Proper nouns are not filtered out as of now but we give the option to ignore
space-separated and hyphenated words.

The use case for this module is for generating puzzles used in head-to-head
competitions. So even though the gutenberg dictionary contains a lot of weird
words it should be OK as nobody today will think of those words. Ideally the
head-to-head matchup is timed, so as to not keep everyone thinking forever.
"""
import json
import os
import sys
import random


class SpellingBee(object):

    def __init__(self, allow_hyphen=False, allow_joint=False,
                 min_puzzle_words=None,
                 min_whole_puzzle_words=None):
        f = open('webster_dictionary.json', 'r')
        webster_dictionary = json.load(f)

        # Extract just the words in alphabetical order from Webster's dictionary (from
        # project gutenberg).
        all_words = sorted([word.lower() for word in webster_dictionary])

        # Remove hyphenated words.
        if allow_hyphen:
            all_words = ["".join(word.split("-")) for word in all_words]
        else:
            all_words = [word for word in all_words if len(
                word.split("-")) < 2]

        # Remove space separated words.
        if allow_joint:
            all_words = ["".join(word.split(" ")) for word in all_words]
        else:
            all_words = [word for word in all_words if len(
                word.split(" ")) < 2]

        self.min_puzzle_words = min_puzzle_words
        self.min_whole_puzzle_words = min_whole_puzzle_words

        # Generate final word lookup structure; it's a dictionary that maps
        # dictionary words to sets containing which letters are in each word.
        self.word_lookup = {}
        for word in all_words:
            self.word_lookup[word] = set(list(word))

    def _lookup(self, query):
        return filter(lambda x: query.lower() in x, self.word_lookup)

    def _get_random_letters(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                   'y', 'z']
        random.shuffle(letters)
        return set(letters[0:7])

    def generate_puzzle(self):
        """Returns a dictionary representing the spelling bee puzzle.

        The key is the letters of the puzzle, and the value is a 3-tuple
        containing:

        1. The central letter for the puzzle.
        2. Words that solve the puzzle that don't use all letters provided (but
           certainly use the central letter.
        3. Words that solve the puzzle that use all letters provided.

        Follows NYT rules:

        1. Words must be at least 5 letters long.
        2. Words must be comprised only of letters comprising the puzzle.
        3. At least one word must exist that uses all provided letters.
        """
        puzzle = {}
        while True:
            letters = self._get_random_letters()
            central_letter = list(letters)[random.randrange(0, 7)]
            whole_puzzle_words = []
            puzzle_words = []

            for word in self.word_lookup:
                if self.word_lookup[word] == letters:
                    whole_puzzle_words.append(word)
                elif self.word_lookup[word].issubset(letters) and len(word) > 5 and len(list(self.word_lookup[word].intersection(central_letter))) == 1:
                    puzzle_words.append(word)
            if len(whole_puzzle_words) > 0:
                puzzle = {str(list(letters)): (central_letter,
                                               puzzle_words, whole_puzzle_words)}
                if self.min_puzzle_words and len(puzzle_words) < self.min_puzzle_words:
                    continue
                if self.min_whole_puzzle_words and len(whole_puzzle_words) < self.min_whole_puzzle_words:
                    continue
                break

        return puzzle


if __name__ == '__main__':
    bee = SpellingBee(allow_hyphen=True)
    print bee.generate_puzzle()
