# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator


@Language.factory("mask")
class AnnotationMask(Annotation):
    """
    Pusty annotator do późniejszego maskowania tokenów
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=None)

    @annotate_decorator
    def __call__(self, doc):
        return list()
