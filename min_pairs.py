from collections import defaultdict

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
    _rhymes_dict = None

    def __init__(self):
        """To avoid unnecessarily repeating the word of loading the dict,
        call `get_instance` instead."""
        if not self._dict:
            self._dict = cmudict.dict()
        if not self._rhymes_dict:
            self._rhymes_dict = self._get_rhymes_dict()

    def _get_rhymes_dict(self):
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

    def word_to_rhymes(self, word):
        """Get all rhymes of a word, for all pronunciations, as list of lists.
        """
        rhymes = []
        for pronunciation in self._dict[word]:
            rhymes.append(self._rhymes_dict[tuple(pronunciation[1:])])
        return rhymes

    def words_starting_with(self, letter):
        """Find all words starting with the given letter or letters."""
        for word in self._dict.iterkeys():
            if word.startswith(letter):
                yield word

    def get_first_letter_variants(self, prefixes, min_len=1, max_len=100):
        """Find all rhymes for all words starting with the given prefixes.

        Args:
            prefixes: An iterable of prefixes. Commonly a string made up of
                first-letters, but a list of prefixes works as well.
        """
        pairs = []
        needs_prefixes = set(prefixes)
        seen_words = set()
        for word in self.words_starting_with(prefixes[0]):
            for pronunciation in self._dict[word]:
                has_prefixes = set()
                rhymes = filter(lambda rhyme: min_len <= len(rhyme) <= max_len,
                                self._rhymes_dict[tuple(pronunciation[1:])])
                if len(rhymes) < len(prefixes):
                    break
                # Filter out words that don't start with the desired prefixes
                filtered_rhymes = []
                for word in rhymes:
                    for prefix in prefixes:
                        if word.startswith(prefix) and word not in seen_words:
                            has_prefixes.add(prefix)
                            filtered_rhymes.append(word)
                            seen_words.add(word)
                            break
                if has_prefixes == needs_prefixes:
                    pairs.append(filtered_rhymes)
        return pairs
