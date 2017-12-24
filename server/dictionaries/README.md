# Word lists.

Spelling Bee takes in a json dictionary where the words are the keys and the
values are metadata for the word.

Here we have several options for dictionaries:

1. `enable1.json` contains the ENABLE word list (173k words) used by word game
   players.
2. `sowpods.json` contains the SOWPODS word list used by Scrabble players (268k
   words).
3. `TWL06.json` contains the Tournament Word List (179k words) used by North
   American scrabble players.
4. `yawl.json` contains a 264k word list formed by combining sowpods, enable1,
   and TWL06.
5. `webster_dictionary.json` contains a word list generated from the gutenberg
   webster's dictionary. It's not great in the sense that a lot of words are no
   longer in use and are kind of weird. There are also proper nouns.
6. `google_300k.json` contains the top 300k unigrams from google search circa
   2010. It contains a lot of nonsense words and stuff (example: `wwwcumshots`).
7. `game_words.json` contains a union of enable1, sowpods, twl06, and yawl.
8. `google_popular_game_words.json` contains an intersection of
   `game_words.json` and `google_300k.json`.
9. `google_popular_TWL06.json` contains an intersection of `game_words.json` and
   `TWL06.json`. I've found this one to have the best results in terms of puzzle
   generation.
