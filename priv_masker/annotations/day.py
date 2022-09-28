# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator


def is_like_day(token):
    if token.shape_ == 'd' or token.shape_ == 'dd':
        n = int(token.text)
        if 0 < n < 32:
            return True
    return False


@Language.factory("priv_day")
class AnnotationDay(Annotation):
    """
    Annotuje tokeny, które mogą reprezentować dzień w dacie
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        for token in doc:
            # sprawdzanie, czy token spełnia warunki
            if is_like_day(token):
                annotated_tokens.append(token)

        return annotated_tokens
