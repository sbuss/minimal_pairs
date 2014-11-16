This python module can calculate rhymes (or minimal pairs) for a given word,
as well as find all minimal pairs that start with given prefixes.

# Rhymes

Get rhymes for a given word, for all of its pronunciations.

```python
import min_pairs
min_pairs.get_rhymes('dogs')

# [([u'D', u'AA1', u'G', u'Z'],
#  [u'bogs', u'dogs', u'hogs', u'pogs', u"fogg's", u'togs', u'jogs']),
# ([u'D', u'AO1', u'G', u'Z'],
#  [u'bogs', u'dogs', u"dogs'", u'logs', u'boggs', u"dog's", u'fogs'])]
```

# Get minimum pairs for a word

Minimum pairs are basically the same as the rhymes

```python
import min_pairs
mf = min_pairs.MinPairFinder.get_instance()
mf.min_pairs('dogs')
# [u'bogs',
#  u'dogs',
#  u'hogs',
#  u'pogs',
#  u'togs',
#  u'jogs',
#  u'bogs',
#  u'dogs',
#  u"dogs'",
#  u'logs',
#  u'boggs',
#  u"dog's",
#  u'fogs']
```

# Get all minimum pairs for prefixes

Given an iterable of prefixes, you can find all minimum pairs for those
prefixes.

For example, say you want to find all minimum pairs that start with either
`q` or `r`:

```python
import min_pairs
mf = min_pairs.MinPairFinder.get_instance()
mf.get_first_letter_variants('qr')
# [[u'qana', u'ronna'],
#  [u'qasr', u'raiser', u'raisor', u'raser', u'rasor', u'razor'],
#  [u'qi', u'ree', u'reeh', u'rhee'],
#  [u'qian', u'qin', u'rhin', u'rihn', u'rinn', u'rinne'],
#  [u'qing', u'ring', u'ringe'],
#  [u'qom', u'rahm', u'rom', u'romm'],
#  [u'qu', u'rew', u'rhew', u'rhue', u'rioux', u'roux', u'ru', u'rue'],
#  [u'quai',
#   u'quay',
#   u'quaye',
#   u'rae',
#   u'ray',
#   u'raye',
#   u're',
#   u'rea',
#   u'reay',
#   u'rey'],
#  [u'quiche', u'riesh']]
```

Of you can give it a list of prefixes:

```python
import min_pairs
mf = min_pairs.MinPairFinder.get_instance()
mf.get_first_letter_variants(['boo', 'loo'])
# [[u'boo', u'loo'],
#  [u'booby', u'looby'],
#  [u'book', u'look'],
#  [u"book's", u'books', u"books'", u'looks'],
#  [u'booked', u'looked'],
#  [u'booker', u'looker'],
#  [u"booker's", u'bookers', u'lookers'],
#  [u'bookin', u"lookin'"],
#  [u'booking', u'looking'],
#  [u'bookout', u'lookout'],
#  [u'boom', u'loom'],
#  [u"boom's", u'booms', u'looms'],
#  [u'boomed', u'loomed'],
#  [u'boomer', u'loomer'],
#  [u'booming', u'looming'],
#  [u'boon', u'boone', u'loon'],
#  [u'boons', u'loons'],
#  [u'boop', u'loop'],
#  [u'boos', u'booz', u'booze', u'loos'],
#  [u'boose', u'loose'],
#  [u'boost', u'loosed'],
#  [u'boot', u'boote', u'loot'],
#  [u'booted', u'looted'],
#  [u'booting', u'looting']]
```
