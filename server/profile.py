"""
Profile the spelling bee module.

Last run:

* Most of the time was spent checking issubset (linear passes through the
  dictionary comparing every word to a candidate set of letters).
* 2nd-most time was the initial processing of the library.

Profiling shows that greatest gain would be an efficient lookup structure (e.g
database).

To run: `python profile.py`
"""
import cProfile, pstats, StringIO

pr = cProfile.Profile()
pr.enable()

from spelling_bee import SpellingBee

b = SpellingBee(allow_hyphen=True)
print b.generate_puzzle() 

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
