# Analiza syntaktyczna — generator zdań SVO

Katalog [`src/syntactic_analysis/`](./) zawiera generator zdań angielskich oparty na strukturze podmiot–orzeczenie–dopełnienie (SVO). Moduły wykorzystują wspólny leksykon, reguły budowy fraz i odmiany czasowników. Wygenerowane zestawienia są zapisywane w katalogu [`results/syntactic_results/`](../../results/syntactic_results/).

## Pliki źródłowe

| Plik | Działanie i zawartość | Powiązania |
|---|---|---|
| [`lexicon.py`](lexicon.py) | Definiuje typy danych `Noun`, `Verb`, `Adjective`, `Pronoun`, `Determiner` oraz `Gender` i `VerbType`. Zawiera listy angielskich rzeczowników, czasowników wraz z formami, przymiotników, zaimków i określników wykorzystywane przy losowaniu zdań. | Korzystają z niego [`grammar.py`](grammar.py) i [`generator.py`](generator.py); liczebności list zestawia [`main.py`](main.py). |
| [`grammar.py`](grammar.py) | Definiuje enumeracje czasów (`Tense`), trybów (`Mood`) i strony (`Voice`), strukturę frazy rzeczownikowej `NounPhrase` oraz frazy czasownikowej `VerbPhrase`. Funkcja `conjugate()` dobiera formy czasownika i operatorów posiłkowych zależnie od gramatycznych parametrów. | Importuje typy z [`lexicon.py`](lexicon.py); jest wykorzystywany przez [`generator.py`](generator.py). |
| [`generator.py`](generator.py) | Klasa `SentenceGenerator` losuje podmiot, czasownik i — dla czasowników przechodnich — dopełnienie, po czym buduje zdanie zgodnie z wylosowanym czasem, trybem i stroną. Zwraca tekst zdania. | Korzysta z [`grammar.py`](grammar.py) i [`lexicon.py`](lexicon.py); wywołuje go [`main.py`](main.py), który zapisuje próbkę zdań do [`syntactic_analysis.txt`](../../results/syntactic_results/syntactic_analysis.txt). |
| [`main.py`](main.py) | Punkt wejścia skryptu. Zlicza elementy list leksykalnych, generuje 50 zdań i zapisuje statystyki oraz próbkę w pliku tekstowym wyników. | Odczytuje dane z [`lexicon.py`](lexicon.py), generuje zdania przez [`generator.py`](generator.py) i zapisuje [`results/syntactic_results/syntactic_analysis.txt`](../../results/syntactic_results/syntactic_analysis.txt). |
| [`README.md`](README.md) | Ten dokument: opisuje moduły i ich powiązania. | Sąsiedni katalog z wynikami opisuje [`results/syntactic_results/README.md`](../../results/syntactic_results/README.md). |

## Przepływ danych

1. [`lexicon.py`](lexicon.py) udostępnia słownictwo i formy wyrazów.
2. [`grammar.py`](grammar.py) opisuje parametry gramatyczne i odmienia frazę czasownikową.
3. [`generator.py`](generator.py) łączy elementy leksykonu i reguły gramatyczne w gotowe zdania.
4. [`main.py`](main.py) generuje podsumowanie i zapisuje je w [`results/syntactic_results/syntactic_analysis.txt`](../../results/syntactic_results/syntactic_analysis.txt).

## Uruchomienie

Uruchom skrypt z tego katalogu, aby zachować oczekiwane importy i ścieżkę zapisu:

```bash
cd src/syntactic_analysis
python main.py
```

Wyniki znajdziesz w [`results/syntactic_results/`](../../results/syntactic_results/). Opis ich zawartości: [`results/syntactic_results/README.md`](../../results/syntactic_results/README.md).

## Powiązane katalogi

- Katalog wyników analizy syntaktycznej: [`results/syntactic_results/`](../../results/syntactic_results/).
- Opis plików wynikowych: [`results/syntactic_results/README.md`](../../results/syntactic_results/README.md).
