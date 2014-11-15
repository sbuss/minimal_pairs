from collections import defaultdict
import re

from nltk.corpus import cmudict


class Singleton(object):
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


class MinPairFinder(Singleton):
    _dict = None

    def __init__(self):
        """To avoid unnecessarily repeating the word of loading the dict,
        call `get_instance` instead."""
        if not self._dict:
            self._dict = cmudict.dict()

    def get_rhymes_dict(self):
        """Get the cmudict as a rhymes dictionary.

        This maps similar phonemes to each other, skipping the first phoneme.
        You end up with a dict like

            {('AU1', 'G', 'Z'): ['dogs', 'logs', ...], ...}
        """
        rhymes = defaultdict(list)
        for (word, pronunciations) in self._dict.iteritems():
            for pronunciation in pronunciations:
                rhymes[tuple(pronunciation[1:])].append(word)
        return rhymes

    def words_starting_with(self, letter):
        for word in self._dict.iterkeys():
            if word.startswith(letter):
                yield word

    def get_first_letter_variants(self, letters):
        rhymes_dict = self.get_rhymes_dict()
        pairs = []
        needs_letters = set(letters)
        pattern = re.compile("^[%s]" % ''.join(letters))
        seen_words = set()
        for word in self.words_starting_with(letters[0]):
            for pronunciation in self._dict[word]:
                has_letters = set()
                rhymes = rhymes_dict[tuple(pronunciation[1:])]
                if len(rhymes) < len(letters):
                    break
                # Filter out words that don't start with the desired letters
                filtered_rhymes = []
                for word in rhymes:
                    if pattern.match(word) and word not in seen_words:
                        has_letters.add(word[0])
                        filtered_rhymes.append(word)
                        seen_words.add(word)
                if has_letters == needs_letters:
                    pairs.append(filtered_rhymes)
        return pairs
