# Wyniki analizy syntaktycznej

Katalog [`results/syntactic_results/`](./) zawiera przykładowe zdania generatora SVO. Powiązane moduły źródłowe znajdują się w [`src/syntactic_analysis/`](../../src/syntactic_analysis/), a ich opis w [`README modułu`](../../src/syntactic_analysis/README.md).

## Pliki wynikowe

| Plik | Działanie i zawartość | Źródło / powiązania |
|---|---|---|
| [`syntactic_analysis.txt`](syntactic_analysis.txt) | Tekstowe podsumowanie: liczebności kategorii leksykalnych i 50 przykładowych zdań wylosowanych przez generator. Wartości podsumowania są zapisywane dynamicznie na podstawie aktualnych list, a same zdania mogą się różnić między uruchomieniami. | Tworzy go [`main.py`](../../src/syntactic_analysis/main.py), który pobiera dane z [`lexicon.py`](../../src/syntactic_analysis/lexicon.py) i generuje zdania za pomocą [`generator.py`](../../src/syntactic_analysis/generator.py). Reguły odmiany opisuje [`grammar.py`](../../src/syntactic_analysis/grammar.py). |
| [`README.md`](README.md) | Ten dokument: opisuje pliki wynikowe i odsyła do modułów, które są z nimi powiązane. | Dokumentacja modułu źródłowego: [`src/syntactic_analysis/README.md`](../../src/syntactic_analysis/README.md). |

## Powiązania

- Katalog wyników: [`results/syntactic_results/`](./).
- Katalog generatora i reguł gramatycznych: [`src/syntactic_analysis/`](../../src/syntactic_analysis/).
- Punkt wejścia generujący próbkę zdań: [`main.py`](../../src/syntactic_analysis/main.py).
- Dane leksykalne: [`lexicon.py`](../../src/syntactic_analysis/lexicon.py).
- Reguły czasów, trybów i odmiany: [`grammar.py`](../../src/syntactic_analysis/grammar.py).
- Generator zdań: [`generator.py`](../../src/syntactic_analysis/generator.py).
- Dokumentacja kodu źródłowego: [`README modułu`](../../src/syntactic_analysis/README.md).
