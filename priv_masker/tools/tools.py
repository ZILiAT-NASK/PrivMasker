# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from .components import ANNOTATIONS, MASKS
from enum import Enum
from string import whitespace


class AnalyseOut(Enum):
    TEXT = 1
    DOC = 2
    PDF_OCR = 3


def add_pipeline(nlp):
    for _, name in ANNOTATIONS:
        nlp.add_pipe(name)
    for _, name in MASKS:
        nlp.add_pipe(name)
    return nlp


def analyse_text(text, nlp, masked_components, out=AnalyseOut.TEXT):
    doc = nlp(text)

    mask_list = list()
    for component in masked_components:
        if masked_components[component]:
            mask_list.append(component)

    if out == AnalyseOut.TEXT:
        return give_text_output(doc, mask_list)
    elif out == AnalyseOut.DOC:
        return doc
    elif out == AnalyseOut.PDF_OCR:
        return give_ocr_output(doc)


def is_whitespace(token):
    for i in token.text:
        if i in whitespace:
            return True
    return False


def give_text_output(doc, mask_list):
    out_text = str()

    for token in doc:
        if token._.mask in mask_list and not token.is_punct and not is_whitespace(token):
            # out_text = out_text + ''.join(['x' for _ in token.text])  # tyle x, ile znaków
            out_text = out_text + '[XXX]'
            out_text = out_text + token.whitespace_
        else:
            out_text = out_text + token.text_with_ws
    return out_text


def give_ocr_output(doc):
    pass
