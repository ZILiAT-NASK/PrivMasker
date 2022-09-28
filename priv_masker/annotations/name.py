# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator

from ..data.data_download import get_names_docs

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens


@Language.factory("priv_name")
class AnnotationName(Annotation):
    """
    Annotuje tokeny, które mogą być imieniem
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        last_names = get_names_docs(nlp)
        self.matcher = make_matcher_from_dataset(nlp, last_names, doc_dataset=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje tokeny z bazą imion
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        for token in doc:
            # prawdza, czy w token._.properness jest informacja o imieniu
            if name_properness_check(token):
                if token not in matches:
                    annotated_tokens.append(token)

        return annotated_tokens


def name_properness_check(token):
    if 'imię' in token._.properness:
        return True
    else:
        return False
