# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from abc import ABC


# szablon maski
class Masker(ABC):

    def __init__(self, nlp, name):
        self.nlp = nlp
        self.name = name

    def __call__(self, doc):
        pass


# dekorator używany przy funkcji __call__() gdy dodajemy kolejną maskę
def mask_decorator(call_func):
    # przypisuje komponentowi token._.mask nazwę maski
    def dec_func(self, doc):
        masked_tokens = call_func(self, doc)
        for token in masked_tokens:
            token._.set('mask', self.name)
        return doc
    return dec_func
