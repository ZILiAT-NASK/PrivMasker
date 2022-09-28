# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token
from .components.base import Annotation
from .components.base import annotate_decorator


@Language.factory("priv_capitalized")
class AnnotationCapitalized(Annotation):
    """
    Annotuje tokeny które pisane są wielką literą
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()
        for token in doc:
            # sprawdzanie, czy pierwsza litera jest wielka oraz czy token nie jest interpunkcją
            if token.text[0].isupper() and token.tag_ != 'interp':
                annotated_tokens.append(token)

        return annotated_tokens
