# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("id_numbers_mask")
class IdNumbersMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        id_tokens = search_with_key_words(doc)
        masked_tokens = masked_tokens + id_tokens
        return masked_tokens


def search_with_key_words(doc):
    out_tokens = list()
    phrases = doc._.priv_nominal_phrases
    for phrase in phrases:
        num_tokens = list()
        id_card_flag = False
        id_number_flag = False
        for token in phrase:
            if token.text in ['PESEL', 'REGON', 'NIP'] and not id_card_flag:
                id_number_flag = True
            elif token.lemma_.lower() in ['dowód', 'osobisty'] and not id_number_flag:
                id_card_flag = True
        for token in phrase:
            try:
                if token._.priv_number and len(token.text) == 6 and doc[token.i-1].shape_ == 'XXX':
                    num_tokens = num_tokens + [token, doc[token.i-1]]
            except IndexError:
                pass
            if token.shape == 'XXXdddd' and len(token.text) == 9:
                num_tokens.append(token)
            if token._.priv_number:
                num_tokens.append(token)
        if id_number_flag or id_card_flag:
            out_tokens = out_tokens+num_tokens
    for token in doc:
        if token._.priv_number and is_pesel(token):
            out_tokens.append(token)
    return out_tokens


def is_pesel(number):
    try:
        number_str = str(number)
        month = int(number_str[2:4])
        day = int(number_str[4:6])

        control_weights = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3, 1)
        control_sum = sum([control_weight*int(number_str[i]) for i, control_weight in enumerate(control_weights)])
    except:
        return False

    month_condition = month in list(range(1, 13)) + list(range(21, 33))
    day_condition = day in list(range(1, 32))
    control_sum_condition = control_sum % 10 == 0

    if month_condition and day_condition and control_sum_condition:
        return True
    else:
        return False

