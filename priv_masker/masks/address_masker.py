# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from spacy.language import Language
from spacy.matcher import Matcher

from .components.base import Masker
from .components.base import mask_decorator


@Language.factory("address_mask")
class AddressMasker(Masker):
    def __init__(self, nlp, name):
        super().__init__(nlp, name)
        self.address_matcher = make_address_matcher(nlp)
        self.address_number_matcher = make_address_numbers_matcher(nlp)
        self.apartment_number_matcher = make_apartment_numbers_matcher(nlp)
        self.apartment_number_matcher_abbr = make_apartment_numbers_matcher_abbr(nlp)
        self.postal_matcher = make_postal_matcher(nlp)

    @mask_decorator
    def __call__(self, doc):
        masked_tokens = list()

        # wyszukiwanie nazw ulic i PLACENAME
        address_matches = self.address_matcher(doc)
        address_matches_ends = list()

        # wyszukiwanie tokenów, które wskazują na numer domu
        address_number_matches = self.address_number_matcher(doc)
        address_number_matches_ends = list()

        # wyszukiwanie tokenów, które wskazują na numer mieszkania wraz z kontekstem
        apartment_numbers_matches = self.apartment_number_matcher(doc) + self.apartment_number_matcher_abbr(doc)

        # wyszukiwanie tokenów, które będą wskazywać na kod pocztowy
        postal_matches = self.postal_matcher(doc)
        postal_matches_ends = list()

        # dodawanie nazw ulic do zamaskowanych tokenów
        for match_id, start, end in address_matches:
            address_matches_ends.append(end)
            masked_tokens = masked_tokens+list(doc[start:end])

        # dodanie do zamaskowanych tokenów tokeny wskazujące na numer domu gdy te występują po nazwie ulicy
        for match_id, start, end in address_number_matches:
            span = doc[start:end]
            if span[0].i in address_matches_ends:
                address_number_matches_ends.append(end)
                masked_tokens = masked_tokens+list(doc[start:end])

        # dodanie do zamaskowanych tokenów tokeny wskazujące na numer mieszkania gdy te występują po numerze domu
        for match_id, start, end in apartment_numbers_matches:
            span = doc[start:end]
            if span[0].i in address_number_matches_ends:
                masked_tokens = masked_tokens.append(doc[end])

        # wyszukiwanie liczb, które wskazują na adres:
        # gdy liczba występuje we frazie nominalnej gdzie występuje zamaskowany token wskazujący na adres, to ta liczba
        # wskazuje na adres
        new_num_tokens = search_address_nums_with_key_words(doc, masked_tokens)
        masked_tokens = masked_tokens+new_num_tokens

        # dodawanie kodu pocztowego do zamaskowanych tokenów
        for match_id, start, end in postal_matches:
            postal_matches_ends.append(end)
            masked_tokens = masked_tokens+list(doc[start:end])

        # dodanie do zamaskowanych tokenów tokeny wskazujące na nazwę miejscowości gdy ta występuje po kodzie pocztowym
        found_place_name_tokens = place_name_detector(doc, postal_matches_ends)
        masked_tokens = masked_tokens+found_place_name_tokens

        return masked_tokens


def place_name_detector(doc, postal_ends):
    found_place_names_tokens = list()
    for token in doc:
        if token._.priv_place_name:
            if token.i > 0:
                if token.i in postal_ends:
                    found_place_names_tokens.append(token)
                elif doc[token.i-1] in found_place_names_tokens:
                    found_place_names_tokens.append(token)
    return found_place_names_tokens


def make_address_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
            [{'_': {'priv_street_name': True}, 'OP': '+'}],
            [{'ent_type': 'PLACENAME', 'OP': '+'}],
            [{'ent_type': 'GEOGNAME', 'OP': '+'}],
    ])
    return matcher


def make_postal_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("PostalRule", [
        [{'_': {'priv_number': True}, 'LENGTH': {'==': 2}},
         {'TEXT': '-'},
         {'_': {'priv_number': True}, 'LENGTH': {'==': 3}},
         {'TEXT': ' ', 'OP': '*'}],
    ])
    return matcher


def make_address_numbers_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'_': {'priv_number': True}, 'LENGTH': {'<=': 4}},
         {'TEXT': '/', 'OP': '?'},
         {'TEXT': '\\', 'OP': '?'},
         {'_': {'priv_number': True}, 'OP': '?', 'LENGTH': {'<=': 4}}]
    ])
    return matcher


def make_apartment_numbers_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'POS': 'ADP', 'OP': "?"},
         {'TEXT': ',', 'OP': '?'},
         {'LEMMA': {'IN': ['mieszkanie', 'lokal', 'pokój', 'dom']}},
         {'_': {'priv_number': True}, 'LENGTH': {'<=': 4}}]
    ])
    return matcher


def make_apartment_numbers_matcher_abbr(nlp):
    matcher = Matcher(nlp.vocab)
    matcher.add("Rule", [
        [{'TEXT': {'IN': ['m', 'lok', 'pok']}},
         {'TEXT': '.', 'OP': '?'},
         {'_': {'priv_number': True}, 'LENGTH': {'<=': 4}}]
    ])
    return matcher


def search_address_nums_with_key_words(doc, tokens):
    out_tokens = list()
    phrases = doc._.priv_nominal_phrases
    for phrase in phrases:
        num_tokens = list()
        address_token_flag = False
        for token in phrase:
            if token in tokens:
                address_token_flag = True
            elif token._.priv_number:
                num_tokens.append(token)
        if address_token_flag:
            out_tokens = out_tokens+num_tokens
    return out_tokens
