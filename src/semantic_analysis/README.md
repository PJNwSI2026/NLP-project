# Analiza semantyczna

Ten katalog zawiera program przypisujący rzeczowniki do neuronów samoorganizującej się mapy Kohonena (SOM). Wektory wejściowe opisują rzeczowniki przez ich powiązania z czasownikami przechodnimi; wynik analizy zapisywany jest w katalogu [`results/semantic_results/`](../../results/semantic_results/).

## Pliki

| Plik | Działanie i zawartość | Powiązania |
|---|---|---|
| [`vocabulary.py`](vocabulary.py) | Definiuje listę 100 czasowników przechodnich, kategorie semantyczne oraz listę rzeczowników zbudowaną przez połączenie kategorii. Udostępnia też mapowanie rzeczownika na kategorię (`NOUN_TO_CAT`). | Dane są importowane przez [`main.py`](main.py), który używa ich do budowy wektorów wejściowych i oceny klastrów. |
| [`main.py`](main.py) | Zawiera klasę `KohonenSOM`: inicjalizuje i normalizuje wagi, wyszukuje neuron BMU oraz trenuje mapę z malejącym współczynnikiem uczenia i promieniem sąsiedztwa. Następnie tworzy wektory rzeczowników, trenuje mapę 5 × 10, przypisuje rzeczowniki do neuronów oraz oblicza m.in. liczbę pustych neuronów, liczbę reprezentowanych kategorii i czystość klastrów. Zapisuje podsumowanie i listy klastrów w [`semantic_analysis.txt`](../../results/semantic_results/semantic_analysis.txt). | Importuje dane z [`vocabulary.py`](vocabulary.py); zapisuje wynik w [`results/semantic_results/semantic_analysis.txt`](../../results/semantic_results/semantic_analysis.txt). |
| [`README.md`](README.md) | Ten dokument — opisuje pliki źródłowe i ich powiązania. | Dokumentację wyjściowego raportu zawiera [`results/semantic_results/README.md`](../../results/semantic_results/README.md). |

## Przepływ danych

1. [`vocabulary.py`](vocabulary.py) udostępnia kategorie rzeczowników i czasowniki.
2. [`main.py`](main.py) tworzy wektory cech, trenuje SOM i przypisuje rzeczowniki do neuronów.
3. Program zapisuje podsumowanie oraz zawartość niepustych klastrów w [`results/semantic_results/semantic_analysis.txt`](../../results/semantic_results/semantic_analysis.txt).

W obecnej implementacji macierz cech powstaje w [`main.py`](main.py) z wag powiązań zdefiniowanych w tym pliku oraz losowych składników. Mapa jest inicjalizowana przy ustalonym ziarnie generatora NumPy (`67`), a wagi SOM zaczynają się od losowych wartości.

## Uruchomienie

Uruchom skrypt z tego katalogu, aby działali importy modułów i względna ścieżka zapisu:

```bash
cd src/semantic_analysis
python main.py
```

Wynik pojawi się w [`results/semantic_results/`](../../results/semantic_results/). Opis pliku wynikowego: [`results/semantic_results/README.md`](../../results/semantic_results/README.md).

## Powiązane katalogi

- Katalog wyników analizy semantycznej: [`results/semantic_results/`](../../results/semantic_results/).
- Dokumentacja wyników: [`results/semantic_results/README.md`](../../results/semantic_results/README.md).
