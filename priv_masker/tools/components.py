# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/PrivMasker/LICENSE

from ..annotations.currency import AnnotationCurrency
from ..annotations.capitalized import AnnotationCapitalized
from ..annotations.day import AnnotationDay
from ..annotations.month import AnnotationMonth
from ..annotations.year import AnnotationYear
from ..annotations.name import AnnotationName
from ..annotations.last_name import AnnotationLastName
from ..annotations.number import AnnotationNumber
from ..annotations.street_name import AnnotationStreetName
from ..annotations.place_name import AnnotationPlaceName
from ..annotations.nominal_phrases import NominalPhraseExtender
from ..annotations.stop_words import AnnotationStopWord
from ..annotations.mask import AnnotationMask

from ..masks.date_masker import DateMasker
from ..masks.address_masker import AddressMasker
from ..masks.id_numbers_masker import IdNumbersMasker
from ..masks.cash_masker import CashMasker
from ..masks.persname_masker import PersnameMasker
from ..masks.contact_masker import ContactMasker
from ..masks.orgname_masker import OrgnameMasker
from ..masks.invalid_unmasker import InvalidUnmasker


ANNOTATIONS = [
    (AnnotationMask, 'mask'),
    (AnnotationCapitalized, 'priv_capitalized'),
    (AnnotationCurrency, 'priv_currency'),
    (AnnotationDay, 'priv_day'),
    (AnnotationMonth, 'priv_month'),
    (AnnotationYear, 'priv_year'),
    (AnnotationName, 'priv_name'),
    (AnnotationLastName, 'priv_last_name'),
    (AnnotationNumber, 'priv_number'),
    (AnnotationStreetName, 'priv_street_name'),
    (AnnotationPlaceName, 'priv_place_name'),
    (NominalPhraseExtender, 'priv_nominal_phrases'),
    (AnnotationStopWord, 'priv_stop_word'),

]

MASKS = [
    (ContactMasker, 'contact_mask'),
    (DateMasker, 'date_mask'),
    (PersnameMasker, 'persname_mask'),
    (AddressMasker, 'address_mask'),
    (IdNumbersMasker, 'id_numbers_mask'),
    (CashMasker, 'cash_mask'),
    (OrgnameMasker, 'orgname_mask'),
    (InvalidUnmasker, 'invalid_unmask')
]

