# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator

from ..data.data_download import get_months_names
from ..data.data_download import get_months_numbers
from ..data.data_download import get_months_romanian

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens


@Language.factory("priv_month")
class AnnotationMonth(Annotation):
    """
    Annotuje tokeny, które mogą reprezentować miesiąc w dacie
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension("priv_month", default=False, force=True)

        self.matcher = make_months_matcher(nlp)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher]
        # matchuje token z bazą danych reprezentacji miesięcy
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        return annotated_tokens


def make_months_matcher(nlp):
    months_names = get_months_names()
    months_romanian = get_months_romanian()
    months_romanian_lower = [i.lower() for i in months_romanian]
    months_numbers = get_months_numbers()
    all_data = months_names + months_romanian + months_romanian_lower + months_numbers

    matcher = make_matcher_from_dataset(nlp, all_data)
    return matcher
