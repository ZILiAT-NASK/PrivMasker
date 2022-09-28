# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.matcher import Matcher

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("persname_mask")
class PersnameMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        self.matcher = make_persname_matcher(nlp)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        matches = self.matcher(doc)
        for match_id, start, end in matches:
            tokens = [token for token in doc[start:end] if token.lemma_.lower() not in ['pan', 'pani']]
            masked_tokens = masked_tokens + tokens

        for token in doc:
            if token not in masked_tokens and token.ent_type_ == 'PERSNAME':
                masked_tokens.append(token)

        return masked_tokens


def make_persname_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'_': {'priv_name': True, 'priv_stop_word': False}, 'POS': {'NOT_IN': ['VERB', 'ADV']}},
         {'TEXT': ' ', 'OP': '*'},
         {'_': {'priv_name': True, 'priv_stop_word': False}, 'OP': '?', 'POS': {'NOT_IN': ['VERB', 'ADV']}},
         {'TEXT': ' ', 'OP': '*'},
         {'_': {'priv_last_name': True, 'priv_stop_word': False}, 'POS': {'NOT_IN': ['VERB', 'ADV']}}],

        [{'_': {'priv_last_name': True, 'priv_stop_word': False}, 'POS': {'NOT_IN': ['VERB', 'ADV']}},
         {'TEXT': ' ', 'OP': '*'},
         {'_': {'priv_name': True, 'priv_stop_word': False}, 'POS': {'NOT_IN': ['VERB', 'ADV']}},
         {'TEXT': ' ', 'OP': '*'},
         {'_': {'priv_name': True, 'priv_stop_word': False}, 'OP': '?', 'POS': {'NOT_IN': ['VERB', 'ADV']}}],

        [{'LEMMA': {'IN': ['pan', 'Pan', 'pani', 'Pani']}},
         {'_': {'priv_last_name': True, 'priv_stop_word': False}}]
    ])
    return matcher
