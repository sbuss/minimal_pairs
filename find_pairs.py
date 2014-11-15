from collections import defaultdict
import itertools
import re

from cmu_dict import parse_cmudict


def get_words():
    with open("/usr/share/dict/words") as f:
        return set(word.lower().strip() for word in f.read().split("\n"))


def edit_distance(word1, word2):
    return sum(map(lambda (c1, c2): int(c1 != c2),
                   itertools.izip_longest(
                       list(word1), list(word2), fillvalue='#')))


class NMP(object):
    words = None

    def __init__(self, *args, **kwargs):
        if not self.words:
            self.words = get_words()

    def words_starting_with(self, letter, max_length=6):
        pattern = re.compile("^%s[aeiouy]+" % letter)
        return filter(pattern.match,
                      filter(lambda word: len(word) <= max_length, self.words))

    def near_words(self, letter1, letter2):
        word_list_1 = self.words_starting_with(letter1)
        word_list_2 = self.words_starting_with(letter2)
        candidates = []
        for word1 in word_list_1:
            candidates.extend(
                [(word1, word2) for word2 in
                 filter(lambda x: edit_distance(word1, x) <= 2, word_list_2)])
        return candidates

    def near_words_2(self, letter1, letter2):
        word_list_1 = self.words_starting_with(letter1)
        word_list_2 = self.words_starting_with(letter2)
        candidates = []
        for word1 in word_list_1:
            w1_vowel, w1_tail = re.match(".([aeiouy]+)(.*)", word1).groups()
            pattern = re.compile(".[aeiouy]+%s$" % w1_tail)
            candidates.extend(
                [(word1, word2) for word2 in
                 filter(pattern.match, word_list_2)])
        return candidates

    def _get_tail_pattern(self, word):
        vowel, tail = re.match(".([aeiouy]+)(.*)", word).groups()
        return re.compile(".[aeiouy]+%s$" % tail)

    def near_words_all(self, letters):
        letters = list(letters)
        tails = set(map(self._get_tail_pattern,
                        self.words_starting_with(letters[0])))
        for letter in letters[1:]:
            word_list = self.words_starting_with(letter)
            new_candidates = []
            print(len(tails))
            for c, tail in enumerate(tails):
                if c % 100 == 0:
                    print(c)
                new_candidates.extend(filter(tail.match, word_list))
            tails &= set(self._get_tail_pattern(new_word)
                         for new_word in new_candidates)
        return tails


class CNMP(object):
    words = None

    def __init__(self, *args, **kwargs):
        if not self.words:
            self.words = dict(parse_cmudict('./cmudict.0.7a'))

    def startswith(self, letter):
        return filter(lambda word: word.startswith(letter),
                      self.words.keys())

    def all_words(self, letters):
        tails = set()
        # First find words starting with those letters
        words = defaultdict(lambda: defaultdict(list))
        letters = map(upper, list(letters))
        for letter in letters:
            for word in self.startswith(letter):
                words[len(word)][letter].append(word)
        return words
