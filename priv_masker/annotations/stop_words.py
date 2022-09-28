# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens

from ..data.data_download import get_stop_words


@Language.factory("priv_stop_word")
class AnnotationStopWord(Annotation):
    """
    Annotuje token jako stop word
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        stop_words = get_stop_words()
        self.matcher = make_matcher_from_dataset(nlp, stop_words)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje tokeny z bazą polskich stop words
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        return annotated_tokens
