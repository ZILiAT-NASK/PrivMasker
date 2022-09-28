# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator


def is_like_year(token):
    try:
        if in_years_range(int(token.text[:4])):
            if token.shape_ == 'dddd' or (token.shape_ == 'ddddx' and token.text[-1]) == 'r':
                return True
        return False
    except ValueError:
        return False


def in_years_range(n):
    return 1900 < n < 2100


@Language.factory("priv_year")
class AnnotationYear(Annotation):
    """
    Annotuje tokeny, które mogą reprezentować rok w dacie
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension("priv_year", default=False, force=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        for token in doc:
            # sprawdzanie, czy token spełnia warunki
            if is_like_year(token):
                annotated_tokens.append(token)

        return annotated_tokens
