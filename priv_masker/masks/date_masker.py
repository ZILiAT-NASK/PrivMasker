# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.matcher import Matcher

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("date_mask")
class DateMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        self.matcher = make_date_matcher(nlp)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        matches = self.matcher(doc)
        for match_id, start, end in matches:
            matched_tokens = [token for token in doc[start:end] if not token.is_punct]
            masked_tokens = masked_tokens+matched_tokens

        return masked_tokens


def make_date_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'_': {'priv_day': True}}, {'_': {'priv_month': True}}, {'_': {'priv_year': True}}],
        [{'_': {'priv_day': True}}, {'IS_PUNCT': True}, {'_': {'priv_month': True}}, {'IS_PUNCT': True},
         {'_': {'priv_year': True}}],
        [{'_': {'priv_year': True}}, {'_': {'priv_month': True}}, {'_': {'priv_day': True}}],
        [{'_': {'priv_year': True}}, {'IS_PUNCT': True}, {'_': {'priv_month': True}}, {'IS_PUNCT': True},
         {'_': {'priv_day': True}}],
        [{'_': {'priv_day': True}}, {'_': {'priv_month': True}}],
        [{'_': {'priv_day': True}}, {'IS_PUNCT': True}, {'_': {'priv_month': True}}],
        [{'SHAPE': {'IN': ['d/d/dddd', 'dd/d/dddd', 'd/dd/dddd', 'dd/dd/dddd', ]}}]
    ])
    return matcher
