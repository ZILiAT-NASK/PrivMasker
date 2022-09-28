# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

import re
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Token

from .components.base import Annotation
from .components.base import annotate_decorator

from .components.general import make_matcher_from_dataset
from .components.general import give_matched_tokens

from ..data.data_download import get_large_nums
from ..data.data_download import get_large_num_abbrs
from ..data.data_download import get_ordinal_nums
from ..data.data_download import get_nums


@Language.factory("priv_number")
class AnnotationNumber(Annotation):
    """
    Annotowanie tokenu, który reprezentuje liczbę
    """

    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        Token.set_extension(name, default=False, force=True)

        large_abbrs = get_large_num_abbrs()
        large_nums = get_large_nums()
        ordinal_nums = get_ordinal_nums()
        nums = get_nums()

        self.abbrs_matcher = Matcher(nlp.vocab)
        self.abbrs_matcher.add("Rule", [
            [{"LEMMA": {"IN": large_abbrs}}, {'TEXT': '.'}, {'IS_SENT_START': False}],
        ], on_match=self.callback_skip_final_tokens)

        data = large_nums + ordinal_nums + nums
        self.matcher = make_matcher_from_dataset(nlp, data)

    @annotate_decorator
    def __call__(self, doc):
        annotated_tokens = list()

        matchers = [self.matcher, self.abbrs_matcher]
        matches = give_matched_tokens(matchers, doc)
        annotated_tokens = annotated_tokens + matches

        for token in doc:
            numb_matches = re.match(r'\d+', token.text)
            if token.pos_ == 'NUM' or numb_matches is not None:
                if token not in annotated_tokens:
                    annotated_tokens.append(token)

        return annotated_tokens

    def callback_skip_final_tokens(self, matcher, doc, i, matches):
        match_id, start, end = matches[i]
        span = doc[start:end]
        return span[:-1]
