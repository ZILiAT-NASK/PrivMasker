# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator
from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens

from ..data.data_download import get_last_names_docs


@Language.factory("priv_last_name")
class AnnotationLastName(Annotation):
    """
    Annotuje tokeny, które mogą być nazwiskiem
    """
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        last_names = get_last_names_docs(nlp)
        self.matcher = make_matcher_from_dataset(nlp, last_names, doc_dataset=True)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje tokeny z bazą nazwisk
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        for token in doc:
            # prawdza, czy w token._.properness jest informacja o nazwisku
            if last_name_properness_check(token):
                if token not in matches:
                    annotated_tokens.append(token)

        return annotated_tokens


def last_name_properness_check(token):
    if 'nazwisko' in token._.properness:
        return True
    else:
        return False
