"""spelling_bee.py: Creates random puzzles for NYT's spelling bee game.

Computers are fast. This leverages a ton of linear passes through a dictionary
because it's just for fun and puzzle examples still come back in seconds.
Performance improvements left as exercise to the reader (low hanging fruit
in the puzzle retrieval area, I left everything as linear word lists with
no preprocessing).

Most other implementations I've seen precompute a lot of puzzles, and if you
were running a real game server you'd probably want to do the same (serve a
puzzle at random). I didn't want the inconvenience of precomputing things and
just wanted something that worked even if generating a puzzle takes a while. So
that is what this is.

No dependencies beyond Python 2.7+.

Author: Sam Liu <sam@ambushnetworks.com>
License: MIT

Expects input as a json file containing values in this format:

{
 "word": "definition or other metadata",
 "word2": "definition2 or other metadata"
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

MIN_WORD_LENGTH = 5


class SpellingBee(object):

    def __init__(self, allow_hyphen=False, allow_joint=False,
                 min_puzzle_words=None,
                 min_whole_puzzle_words=None):
        f = open('dictionaries/google_popular_TWL06.json', 'r')
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

    def _count_vowels(self, s):
        return s.count('a') + s.count('e') + s.count('i') + s.count('o') + s.count('u')

    def _get_random_letters(self, num_letters=7):
        """Retrieve `num_letters` random letters from the alphabet forcing at
        least 1 vowel. """
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                   'y', 'z']
        while True:
            random.shuffle(letters)
            if self._count_vowels(letters[0:num_letters]) > 0:
                return set(letters[0:num_letters])

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
            central_letter = list(
                letters)[random.randrange(0, len(list(letters)))]
            whole_puzzle_words = []
            puzzle_words = []

            # O(n) iteration through word list. TODO: improve by building an
            # index that can be queried more efficiently.
            #
            # Query params:
            #   1. If the word uses the central letter.
            #   2. If the word's letters are a subset of the current letter set.
            #   3. If the length of the word is at least <5>.
            for word in self.word_lookup:
                if self.word_lookup[word] == letters:
                    whole_puzzle_words.append(word)
                elif self.word_lookup[word].issubset(letters) and len(word) > MIN_WORD_LENGTH and len(list(self.word_lookup[word].intersection(central_letter))) == 1:
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
