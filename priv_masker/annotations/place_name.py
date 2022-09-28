# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens

from ..data.data_download import get_places_docs


@Language.factory("priv_place_name")
class AnnotationPlaceName(Annotation):
    """
    Annotuje token, który może być nazwą miejscowości
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        places_docs = get_places_docs(nlp)
        self.matcher = make_matcher_from_dataset(nlp, places_docs, doc_dataset=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje tokeny z bazą nazw miejscowości
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        return annotated_tokens

