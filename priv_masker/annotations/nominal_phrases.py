# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Doc

from .components.base import Annotation
from .components.base import annotate_doc_decorator


@Language.factory("priv_nominal_phrases")
class NominalPhraseExtender(Annotation):
    """
    Przypisuje obiektowi doc listę fraz nominalnych
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Doc.set_extension(name, default=None, force=True)

    @annotate_doc_decorator
    def __call__(self, doc):
        # tworzenie fraz nominalnych
        phrases = convert_to_nominal_phrases(doc)

        return phrases


def convert_to_nominal_phrases(doc):
    nominal_phrases = list()
    for token in doc:
        if token.pos_ in ('NOUN', 'PROPN'):
            appendage = []
            for i, tree_elem in enumerate(token.subtree):
                if tree_elem == token:
                    check = i
            for el in list(token.subtree)[:check + 1]:
                if el.dep_ == 'amod':
                    appendage.append(el)
            appendage += list(token.subtree)[check:]
            nominal_phrases.append(appendage)
    return nominal_phrases


# def get_numerical_phrases(doc):
#     phrases = convert_to_nominal_phrases(doc)
#     out_phrases = list()
#     for phrase in phrases:
#         for token in phrase:
#             if token._.priv_number:
#                 out_phrases.append(phrase)
#                 break
#     return phrases
#     return out_phrases
