import re


def get_words():
    with open("/usr/share/dict/words") as f:
        return set(word.lower().strip() for word in f.read().split("\n"))


def edit_distance(word1, word2):
    return sum(map(lambda (c1, c2): int(c1 != c2),
                   zip(list(word1), list(word2))))


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
