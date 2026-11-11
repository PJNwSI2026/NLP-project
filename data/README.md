# Dane korpusowe

Katalog zawiera czeski korpus używany w analizie statystycznej. Pliki tekstowe są wejściem dla skryptów z [`src/statistical_analysis/`](../src/statistical_analysis/README.md).

| Plik | Opis |
|---|---|
| [`czech_modern_200k.txt`](czech_modern_200k.txt) | Korpus źródłowy zapisany przez [`download.py`](../src/statistical_analysis/download.py) ze zbioru `PleIAs/Czech-PD`. Skrypt zbiera teksty o określonych tytułach do osiągnięcia co najmniej 200 000 słów. |
| [`czech_modern_200k_clean.txt`](czech_modern_200k_clean.txt) | Wersja przetworzona przez [`clean.py`](../src/statistical_analysis/clean.py): tekst małe litery, ujednolicone odstępy, bez interpunkcji, cyfr i wyrazów zawierających znaki spoza czeskiego alfabetu. To plik wejściowy dla analiz słów i znaków. |

## Powiązane materiały

- Skrypty pobierania, czyszczenia i analizy: [`src/statistical_analysis/README.md`](../src/statistical_analysis/README.md).
- Opis wyników analizy: [`results/statistical_results/README.md`](../results/statistical_results/README.md).
