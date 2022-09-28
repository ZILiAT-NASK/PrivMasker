# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from abc import ABC


# szablon annotatora
class Annotation(ABC):

    def __init__(self, nlp, name):
        self.nlp = nlp
        self.name = name

    def __call__(self, doc):
        pass


# dekorator używany przy funkcji __call__() gdy annotujemy tokeny
def annotate_decorator(call_func):
    # przypisuje odpowiedniemu komponentowi tokenu token._.priv_[...] wartość True
    def dec_func(self, doc):
        annotated_tokens = call_func(self, doc)
        for token in annotated_tokens:
            token._.set(self.name, True)
        return doc
    return dec_func


# dekorator używany przy funkcji __call__() gdy annotujemy obiekt doc
def annotate_doc_decorator(call_func):
    # przypisuje komponentowi doc._.[...] to co zwraca __call__()
    def dec_func(self, doc):
        annotation = call_func(self, doc)
        doc._.set(self.name, annotation)
        return doc
    return dec_func

