# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.matcher import Matcher

from .components.base import Masker


@Language.factory("invalid_unmask")
class InvalidUnmasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        self.matcher = make_numbers_to_unmask_matcher(nlp)

    def __call__(self, doc):
        tokens_to_unmask = list()
        matches = self.matcher(doc)
        for _, start, end in matches:
            for token in doc[start:end]:
                tokens_to_unmask.append(token)

        for token in tokens_to_unmask:
            token._.set('mask', None)

        return doc


def make_numbers_to_unmask_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'LOWER': {'IN': ['art', 'ust', 'str', 'poz', 'pkt', 'zał', '§', '$']}},
         {'TEXT': '.', 'OP': "?"},
         {'LOWER': 'nr', 'OP': "?"},
         {'TEXT': '.', 'OP': "?"},
         {'_': {'priv_number': True}}],
        [{'lemma': {'IN': ['artykuł', 'ustawa', 'strona', 'pozycja', 'punkt', 'załącznik', 'rozdział']}},
         {'LOWER': 'nr', 'OP': "?"},
         {'LOWER': 'numer', 'OP': "?"},
         {'TEXT': '.', 'OP': "?"},
         {'_': {'priv_number': True}}],
    ])
    return matcher
