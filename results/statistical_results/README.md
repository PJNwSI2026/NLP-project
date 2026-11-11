# Wyniki analizy statystycznej

Pliki w tym katalogu są generowane przez skrypty z [`src/statistical_analysis/`](../../src/statistical_analysis/README.md) na podstawie oczyszczonego korpusu [`data/czech_modern_200k_clean.txt`](../../data/czech_modern_200k_clean.txt).

| Wynik | Opis |
|---|---|
| [`character_analysis.csv`](character_analysis.csv) | Zestawienie znaków w korpusie bez spacji. Kolumny zawierają znak (`Litera`), liczbę wystąpień (`Czestosc`), prawdopodobieństwo (`Prawdopodobienstwo`), kod Huffmana (`Kod_Huffmana`) i długość tego kodu (`Dlugosc_kodu`). |
| [`entropy.txt`](entropy.txt) | Podsumowanie entropii źródła znaków, średniej długości kodu Huffmana oraz efektywności kodowania `H/L`. |
| [`prawo_zipfa.png`](prawo_zipfa.png) | Wykres log-log rangi słowa względem jego częstości. Wykres zawiera współczynnik kierunkowy dopasowania i informację, czy wynik jest zgodny z przyjętym zakresem prawa Zipfa. |
| [`words_90.csv`](words_90.csv) | Najczęstsze słowa aż do osiągnięcia co najmniej 90% wszystkich wystąpień słów. Zawiera częstość i rangę każdego słowa oraz skumulowaną częstość i skumulowany procent. Analiza uwzględnia słowa dłuższe niż jeden znak. |
| [`core_100.csv`](core_100.csv) | 100 słów z największą liczbą różnych bezpośrednich sąsiadów w sekwencji korpusu. Kolumny podają słowo, liczbę unikalnych sąsiadów i rangę sąsiedztwa. |

## Powiązane materiały

- Opis korpusu wejściowego: [`data/README.md`](../../data/README.md).
- Opis skryptów generujących wyniki: [`src/statistical_analysis/README.md`](../../src/statistical_analysis/README.md).
