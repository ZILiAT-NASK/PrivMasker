# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

import pandas as pd
import numpy as np
import os
from .money.money_codes import MONEY_CODES, MONEY_CODES_MORFEUSZ
from .money.money_names import MONEY_NAMES
from .money.money_symbols import MONEY_SYMBOLS
from spacy.tokens._serialize import DocBin

from .numbers import LARGE_NUMBERS, LARGE_NUMBERS_ABBRS, ORDINAL_NUMBERS, NUMBERS


# for abbreviations
def get_abbreviations():
    """

    :return: pandas array: 1st column - abbreviation, 2nd - expansion
    """

    br_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abbrs.csv')
    br_df = pd.read_csv(br_path, sep=';')
    return br_df.to_numpy()


# for months
def get_months_names():
    return ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec',
            'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień']


# for months
def get_months_romanian():
    return ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


# for months
def get_months_numbers():
    nums = [str(i) for i in range(1, 13)]
    nums_with_zero = [f"0{i}" for i in range(1, 10)]

    return nums + nums_with_zero


def get_stop_words():
    stop_words_source = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stop_words.txt')
    with open(stop_words_source, encoding='UTF-8') as file:
        stop_words = [line.strip() for line in file.readlines()]
    return stop_words


# for money
def get_money_names():
    """

    :return: list of data in str.lower() needed in currency annotation
    """

    exceptions = ["polski złoty", "złoty polski"]
    all_data = MONEY_CODES + MONEY_CODES_MORFEUSZ + MONEY_SYMBOLS + MONEY_NAMES + exceptions
    return [i.upper() for i in all_data]


# for numbers
def get_large_num_abbrs():
    return LARGE_NUMBERS_ABBRS


# for numbers
def get_large_nums():
    return LARGE_NUMBERS


# for numbers
def get_ordinal_nums():
    return ORDINAL_NUMBERS


# for numbers
def get_nums():
    return NUMBERS


# for address:
# https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default
def get_streets_names():
    streets_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'address/streets.csv')
    streets_data = pd.read_csv(streets_data_path, sep=';')
    streets_data = streets_data.loc[:, ['CECHA', 'NAZWA_1', 'NAZWA_2']]
    street_names = list()
    for i, street in streets_data.iterrows():
        name = str()
        if str(street['NAZWA_2']) != 'nan':
            street_names.append(street['NAZWA_1'])
            name = name + street['NAZWA_2'] + ' '
        name = name + street['NAZWA_1']
        street_names.append(name)
    street_names = list(set(street_names))
    return street_names


def get_streets_docs(nlp):
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'address/docs/streets.spacy')
    streets = DocBin().from_disk(file_name)
    streets = list(streets.get_docs(nlp.vocab))
    return streets


def get_places_docs(nlp):
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'address/docs/places.spacy')
    places = DocBin().from_disk(file_name)
    places = list(places.get_docs(nlp.vocab))
    return places


def get_names_docs(nlp):
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/docs/names.spacy')
    names = DocBin().from_disk(file_name)
    names = list(names.get_docs(nlp.vocab))
    return names


def get_last_names_docs(nlp):
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/docs/last_names.spacy')
    last_names = DocBin().from_disk(file_name)
    last_names = list(last_names.get_docs(nlp.vocab))
    return last_names


# for address
def get_place_names():
    place_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'address/address.csv')
    place_data = pd.read_csv(place_data_path, sep=';')
    streets_data = place_data.loc[:, 'NAZWA']
    street_names = list(set(streets_data))
    return street_names


# for names
def get_names():
    f1_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/female_first_name.csv')
    f2_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/female_second_name.csv')
    m1_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/male_first_name.csv')
    m2_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/male_second_name.csv')
    names_paths = (f1_names_path, f2_names_path, m1_names_path, m2_names_path)
    names = list()
    for path in names_paths:
        data = pd.read_csv(path)
        data = np.array(data.loc[data['LICZBA_WYSTĄPIEŃ'] > 10])
        names_data = list(data[:, 0])
        names = names + list(filter(lambda x: (isinstance(x, str)), names_data))
    out_names = list()
    for name in set(names):
        if '-' in name:
            split = name.split('-')
        else:
            split = name.split()
        cap_name = list(map(lambda x: (x.capitalize()), split))
        for j in cap_name:
            if j != '.':
                out_names.append(j)
    return list(set(filter(None, out_names)))


# for names
def get_last_names():
    f_last_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/female_last_name.csv')
    m_last_names_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names/male_last_name.csv')
    last_names_paths = (f_last_names_path, m_last_names_path)
    last_names = list()
    for path in last_names_paths:
        data = pd.read_csv(path)
        data = np.array(data.loc[data['Liczba'] > 10])
        last_names_data = list(data[:, 0])
        last_names = last_names + list(filter(lambda x: (isinstance(x, str)), last_names_data))
    out_last_names = list()
    for last_name in set(last_names):
        if '-' in last_name:
            split = last_name.split('-')
        else:
            split = last_name.split()
        cap_last_name = list(map(lambda x: (x.capitalize()), split))
        for j in cap_last_name:
            if j != '.':
                out_last_names.append(j)
    return list(set(filter(None, out_last_names)))


# for contexts
def get_obvious_phrases():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'obvious_phrases.csv')
    data = np.array(pd.read_csv(path))
    return data


# def get_contexts(context_name):
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'./contexts/{context_name}.txt')
#     with open(path, 'r', encoding='utf-8') as file:
#         contexts = [context.strip() for context in file.readline().split()]
#     return contexts

