# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token
from spacy.matcher import Matcher

from .components.base import Annotation
from .components.base import annotate_decorator

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_phrases

from ..data.data_download import get_streets_docs


@Language.factory("priv_street_name")
class AnnotationStreetName(Annotation):
    """
    Annotuje token, który może być nazwą ulicy
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        places_docs = get_streets_docs(nlp)
        self.matcher = make_matcher_from_dataset(nlp, places_docs, doc_dataset=True)

        self.street_context_matcher = make_street_context_matcher(nlp)
        self.street_matcher = make_street_matcher(nlp)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje tokeny z bazą nazw ulic
        spans = give_matched_phrases(matchers, doc)

        # wyszukuje w tekście kontekst w którym może się pojawić nazwa ulicy
        # np. 'na ulicy ...', 'przy ulicy ...', 'obok alei ...'
        context_match_end_ids = [end for _, _, end in self.street_context_matcher(doc)]

        # znajdowanie tokenów, które są przymiotnikami zaczynającymi się wielką literą
        street_matches_id = [end-1 for _, _, end in self.street_matcher(doc)]

        for span in spans:
            # sprawdzanie, czy znaleziona nazwa ulicy zaczyna się, gdy kończy się kontekt ulicy
            if span[0].i in context_match_end_ids:
                annotated_tokens = annotated_tokens+list(span)
            # Jeśli token to przymiotnik zaczynający się wielką literą i jest w bazie, to jest nazwą ulicy
            elif len(span) == 1 and span[0].i in street_matches_id:
                annotated_tokens.append(span[0])

        return annotated_tokens


def make_street_context_matcher(nlp):
    street_context_matcher = Matcher(nlp.vocab)
    street_context_pattern = [[{'POS': 'ADP', 'OP': "?"},
                               {'TEXT': ' ', 'OP': '*'},
                               {'LEMMA': {'IN': ['ulica',
                                                 'plac',
                                                 'aleja',
                                                 'aleje',
                                                 'rondo',
                                                 'osiedle',
                                                 'róg'
                                                 ]}},
                               {'TEXT': ' ', 'OP': '*'}],
                              [{'POS': 'ADP', 'OP': "?"},
                               {'TEXT': ' ', 'OP': '*'},
                               {'LOWER': {'IN': ['ul',
                                                 'pl',
                                                 'al',
                                                 'os'
                                                 ]}},
                               {'TEXT': '.', 'OP': "?"},
                               {'TEXT': ' ', 'OP': '*'}]]
    street_context_matcher.add('pattern', street_context_pattern)
    return street_context_matcher


def make_street_matcher(nlp):
    street_matcher = Matcher(nlp.vocab)
    street_pattern = [[{'POS': 'ADP'},
                       {'POS': 'ADJ', 'IS_TITLE': True, 'IS_SENT_START': False}]]
    street_matcher.add('pattern', street_pattern)
    return street_matcher
