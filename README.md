# PrivMasker

PrivMasker, to narzędzie do anonimizacji danych osobowych i wrażliwych w dokumentach. Biblioteka umożliwia automatyczną detekcję oraz szybkie i skuteczne maskowanie danych osobowych i wrażliwychw różnego typu dokumentach. W zależności od rodzaju tekstu i preferencji użytkownika możliwy jest opcjonalny wybór maskowanych komponentów:
- imię i nazwisko
- dane kontaktowe (nr. telefonów, adresy e-mail)
- adresy fizyczne
- daty
- numery identyfikacyjne
- kwoty

## Instalacja

#### 1. Zainstaluj PrivMaskera
```cmd
pip install priv_masker
```
#### 2. Pobierz i zainstaluj model Spacy
- [pobierz](http://mozart.ipipan.waw.pl/~rtuora/spacy/) `pl_nask 0.0.5`
- zainstaluj:
```cmd
python -m pip install <PATH_TO_MODEL/pl_nask-0.0.5.tar.gz>
```

## Użycie 
```python
import spacy
from priv_masker import add_pipeline, analyse_text, AnalyseOut

# dostępne maski (False - wyłączone)
masked_components = {
    'date_mask': True,
    'persname_mask': True,
    'contact_mask': True,
    'address_mask': True,
    'id_numbers_mask': True,
    'cash_mask': True,
    'orgname_mask': True
}

nlp = spacy.load('pl_nask')
nlp = add_pipeline(nlp)

text = "Halina Kowalska (tel. 228595959, adres e-mail: halina.kowalska@xyz.com), reprezentująca Stowarzyszenie Przedsiębiorców Polskich, zamieszkała w Warszawie przy ulicy Juliusza Słowackiego 13/13, identyfikująca się numerem PESEL 76121305873, złożyła w dniu 12 sierpnia 2022 oświadczenie wyjaśniające i uiściła karę grzywny w wysokości 500 złotych."

masked_text = analyse_text(text, nlp, masked_components, out=AnalyseOut.TEXT)
# [XXX] [XXX] (tel. [XXX], adres e-mail: [XXX]), reprezentująca [XXX] [XXX] [XXX], zamieszkała w [XXX] przy [XXX] [XXX] [XXX] [XXX], identyfikująca się numerem PESEL [XXX], złożyła w dniu [XXX] [XXX] [XXX] oświadczenie wyjaśniające i uiściła karę grzywny w wysokości [XXX] złotych.

doc = analyse_text(text, nlp, masked_components, out=AnalyseOut.DOC)  # obiekt Spacy
```

## Wersja

`v0.0.4`
- Dodanie kodu PrivMaskera
- Dodanie dokumentacji
- Dodanie licencji

<details>
<summary><b>Poprzednie wersje</b></summary>
</details>

## Implementacja
Szczegółowe informacje na temat biblioteki umieszczone są w dokumentacji.




## Kontakt

Zakład Inżynierii Lingwistycznej i Analizy Tekstu, Naukowa i Akademicka Sieć Komputerowa – Państwowy Instytut Badawczy\
ziliat@nask.pl

Copyright (C) 2022 NASK PIB
