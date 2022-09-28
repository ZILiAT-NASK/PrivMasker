# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("orgname_mask")
class OrgnameMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        for token in doc:
            if token.ent_type_ == 'ORGNAME':
                masked_tokens.append(token)

        return masked_tokens