# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.matcher import Matcher

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("cash_mask")
class CashMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        self.matcher = make_cash_matcher(nlp)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        matches = self.matcher(doc)
        for match_id, start, end in matches:
            tokens = [token for token in doc[start:end] if not token._.priv_currency]
            masked_tokens = masked_tokens + tokens

        cash_tokens = search_with_key_words(doc)
        masked_tokens = masked_tokens+cash_tokens
        return masked_tokens


def search_with_key_words(doc):
    out_tokens = list()
    phrases = doc._.priv_nominal_phrases
    for phrase in phrases:
        num_tokens = list()
        cash_token_flag = False
        for token in phrase:
            if token._.priv_currency:
                cash_token_flag = True
            elif token._.priv_number:
                num_tokens.append(token)
        if cash_token_flag:
            out_tokens = out_tokens+num_tokens
    return out_tokens


def make_cash_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
            [{'_': {'priv_number': True}, 'OP': '+'}, {'_': {'priv_currency': True}}],
    ])
    return matcher
