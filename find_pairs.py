from collections import defaultdict
import itertools
import re
import string

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
            self.endings = dict(parse_cmudict('./cmudict.0.7a'))
            self.word_to_endings = {}
            self.letter_index = defaultdict(list)
            for ending, words in self.endings.items():
                for word in words:
                    self.word_to_endings[word] = ending
                    self.letter_index[word[0]] = word

    def _all_endings(self, letter):
        return set(self.word_to_endings[word]
                   for word in self.letter_index[letter])

    def all_pairs(self, letters):
        letters = map(string.upper, list(letters))
        endings = self._all_endings(letters[0])
        for letter in letters[1:]:
            endings &= self._all_endings(letter)
        candidates = []
        startletter_pattern = re.compile("^[%s]" % "".join(letters))
        for ending in endings:
            candidates.append(
                filter(startletter_pattern.match, self.endings[ending]))
        return candidates
