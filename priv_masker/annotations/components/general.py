# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.matcher import PhraseMatcher


# tworzy matcher z bazy danych
def make_matcher_from_dataset(nlp, dataset, doc_dataset=False, matcher=None):
    if matcher is None:
        matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')
    names_patterns = list()
    if not doc_dataset:
        for text in dataset:
            try:
                names_patterns.append(nlp(text))
            except:
                pass
    else:
        names_patterns = dataset
    matcher.add('TerminologyList', names_patterns)
    return matcher


# zwraca listę dopasowanych tokenów
def give_matched_tokens(matchers, doc):
    out_matches = list()
    spans = give_matched_phrases(matchers, doc)
    for span in spans:
        for token in span:
            out_matches.append(token)
    return out_matches


# zwraca listę dopasowanych fraz
def give_matched_phrases(matchers, doc):
    out_matches = list()
    for matcher in matchers:
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            out_matches.append(span)
    return out_matches
