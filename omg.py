from collections import defaultdict
import re

from nltk.corpus import cmudict


d = cmudict.dict()


def get_rhymes_dict():
    rhymes = defaultdict(list)
    for (word, prons) in d.iteritems():
        for pron in prons:
            rhymes[tuple(pron[1:])].append(word)
    return rhymes


def get_rhymes(target_word):
    return [
        (word, pron)
        for word, pron in d.items()
        if any(subpron[1:] == target_pron[1:]
               for subpron in pron for target_pron in d[target_word])]


def words_starting_with(letter):
    for word in d.iterkeys():
        if word.startswith(letter):
            yield word


def get_first_letter_variants(letters):
    rhymes_dict = get_rhymes_dict()
    pairs = []
    needs_letters = set(letters)
    pattern = re.compile("^[%s]" % ''.join(letters))
    seen_words = set()
    for word in words_starting_with(letters[0]):
        for pronunciation in d[word]:
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
