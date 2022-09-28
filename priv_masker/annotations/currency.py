# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token
from .components.base import Annotation
from .components.base import annotate_decorator


from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens

from ..data.data_download import get_money_names


@Language.factory("priv_currency")
class AnnotationCurrency(Annotation):
    """
    Annotuje tokeny, które mogą reprezentować kontekst kwoty, czyli
    nazwy walut, symbole itp.
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        money_names = get_money_names()
        self.matcher = make_matcher_from_dataset(nlp, money_names)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # Matchowanie tokenów z bazą danych ./data/money/*
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        return annotated_tokens
