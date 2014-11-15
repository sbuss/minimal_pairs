import re

from nltk.corpus import cmudict


d = cmudict.dict()


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
    pairs = []
    needs_letters = set(letters[1:])
    pattern = re.compile("^[%s]" % ''.join(letters))
    for word in words_starting_with(letters[0]):
        has_letters = set()
        rhymes = get_rhymes(word)
        # Filter out words that don't start with the desired letters
        filtered_rhymes = []
        for word, prons in rhymes:
            if pattern.match(word):
                has_letters.add(word[0])
                filtered_rhymes.append(word)
            if has_letters == needs_letters:
                pairs.append(filtered_rhymes)
    return pairs
