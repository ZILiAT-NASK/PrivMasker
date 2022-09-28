# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language

from .components.base import Masker
from .components.base import mask_decorator

import re


def is_email_regex(doc):
    tokens = list()
    regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+\s?(@|Q|©)\s?[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    # regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    for match in re.finditer(regex, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        for token in span:
            tokens.append(token)
    return tokens


def search_with_key_words(doc):
    out_tokens = list()
    phrases = doc._.priv_nominal_phrases
    for phrase in phrases:
        num_tokens = list()
        phone_num_token_flag = False
        for token in phrase:
            if token.lemma_.lower() in ['kontakt', 'kontaktowy', 'telefon', 'tel', 'fax']:
                phone_num_token_flag = True
            elif token._.priv_number or token.shape_ in ['+dd', '+ddd']:
                num_tokens.append(token)
        if phone_num_token_flag:
            out_tokens = out_tokens+num_tokens
    return out_tokens


@Language.factory("contact_mask")
class ContactMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        # sprawdzanie, czy token jest e-mailem (regex)
        for token in is_email_regex(doc):
            masked_tokens.append(token)

        # sprawdzanie, czy token jest numerem telefonu:
        # jeśli występuje we frazie nominalnej w której występują
        phone_num_tokens = search_with_key_words(doc)
        masked_tokens = masked_tokens+phone_num_tokens

        return masked_tokens
