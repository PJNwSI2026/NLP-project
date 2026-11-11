# Analiza statystyczna

Moduły w tym katalogu analizują czeski korpus tekstowy zapisany w [`data/`](../../data) i zapisują wyniki do [`results/statistical_results/`](../../results/statistical_results).

## Pliki

| Plik | Opis |
|---|---|
| [`download.py`](download.py) | Pobiera strumieniowo zbiór `PleIAs/Czech-PD`, wybiera teksty o wskazanych tytułach i zapisuje je do [`data/czech_modern_200k.txt`](../../data/czech_modern_200k.txt). Zatrzymuje pobieranie po zgromadzeniu co najmniej 200 000 słów (ostatni tekst może spowodować przekroczenie limitu). |
| [`clean.py`](clean.py) | Czyści pobrany korpus: zamienia tekst na małe litery, normalizuje białe znaki, usuwa interpunkcję, a następnie pozostawia wyłącznie słowa złożone z liter czeskiego alfabetu. Usuwa słowa zawierające cyfry i zapisuje wynik w [`data/czech_modern_200k_clean.txt`](../../data/czech_modern_200k_clean.txt). |
| [`analyze_words.py`](analyze_words.py) | Analizuje częstość słów w oczyszczonym korpusie. Tworzy wykres rozkładu Zipfa, listę słów odpowiadających za skumulowane 90% wystąpień oraz ranking 100 słów o największej liczbie różnych sąsiadów w tekście. Wyniki trafiają do [`results/statistical_results/`](../../results/statistical_results/README.md). |
| [`analyze_characters.py`](analyze_characters.py) | Analizuje częstość liter (bez spacji), wyznacza prawdopodobieństwa, kody Huffmana, ich długości, entropię, średnią długość kodu i efektywność kodowania. Zapisuje zestawienie CSV i podsumowanie tekstowe w [`results/statistical_results/`](../../results/statistical_results/README.md). |

## Dane i wyniki

- Opis korpusu wejściowego: [`data/README.md`](../../data/README.md).
- Opis wygenerowanych plików: [`results/statistical_results/README.md`](../../results/statistical_results/README.md).

Skrypty używają ścieżek względnych względem katalogu [`src/statistical_analysis`](../../src/statistical_analysis), dlatego należy uruchamiać je z tego katalogu. Typowa kolejność przygotowania korpusu i analizy:

```bash
python download.py
python clean.py
python analyze_words.py
python analyze_characters.py
```
