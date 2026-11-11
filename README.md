# Projekt NLP - analiza języka naturalnego

Projekt z przetwarzania języka naturalnego przedstawia trzy uzupełniające się sposoby badania języka: analizę statystyczną korpusu czeskiego, generator struktur składniowych języka angielskiego oraz analizę semantyczną angielskich rzeczowników. Każda część ma własne moduły w [`src/`](src/) i katalog wyników w [`results/`](results/). Korpus używany w analizie statystycznej znajduje się w [`data/`](data/).

Projekt jest przygotowany dla **Pythona 3.14** i menedżera pakietów **uv**. Dokumentacja każdego obszaru opisuje jego pliki, zależności i wyniki; poniższe sekcje prowadzą bezpośrednio do kodu, danych i wygenerowanych materiałów.

## Trzy aspekty analizy

### 1. Analiza statystyczna języka czeskiego

Analiza pracuje na korpusie tekstowym: pobiera i oczyszcza tekst, a następnie bada częstość słów i znaków.

- **Dane wejściowe:** [`data/czech_modern_200k.txt`](data/czech_modern_200k.txt) - korpus źródłowy oraz [`data/czech_modern_200k_clean.txt`](data/czech_modern_200k_clean.txt) - wersja oczyszczona. Opis obu plików znajduje się w [`data/README.md`](data/README.md).
- **Kod:** [`src/statistical_analysis/`](src/statistical_analysis/) - [`download.py`](src/statistical_analysis/download.py) pobiera korpus, [`clean.py`](src/statistical_analysis/clean.py) czyści go, [`analyze_words.py`](src/statistical_analysis/analyze_words.py) analizuje słowa, a [`analyze_characters.py`](src/statistical_analysis/analyze_characters.py) wyznacza statystyki znaków i kodowanie Huffmana. Szczegóły: [`src/statistical_analysis/README.md`](src/statistical_analysis/README.md).
- **Wyniki:** [`results/statistical_results/`](results/statistical_results/) - [`prawo_zipfa.png`](results/statistical_results/prawo_zipfa.png), [`words_90.csv`](results/statistical_results/words_90.csv), [`core_100.csv`](results/statistical_results/core_100.csv), [`character_analysis.csv`](results/statistical_results/character_analysis.csv) oraz [`entropy.txt`](results/statistical_results/entropy.txt). Opisy i formaty plików: [`results/statistical_results/README.md`](results/statistical_results/README.md).

### 2. Analiza syntaktyczna języka angielskiego

Generator tworzy losowe zdania i wykorzystuje leksykon oraz reguły odmiany dla czasów, trybów i strony czynnej lub biernej. Obsługuje czasowniki przechodnie, nieprzechodnie i zwrotne.

- **Kod:** [`src/syntactic_analysis/`](src/syntactic_analysis/) - [`lexicon.py`](src/syntactic_analysis/lexicon.py) zawiera jednostki leksykalne, [`grammar.py`](src/syntactic_analysis/grammar.py) opisuje czasy, tryby, frazy i odmianę, [`generator.py`](src/syntactic_analysis/generator.py) buduje zdania, a [`main.py`](src/syntactic_analysis/main.py) przygotowuje podsumowanie i próbkę zdań. Szczegóły: [`src/syntactic_analysis/README.md`](src/syntactic_analysis/README.md).
- **Wyniki:** [`results/syntactic_results/`](results/syntactic_results/) zawiera [`syntactic_analysis.txt`](results/syntactic_results/syntactic_analysis.txt) z podsumowaniem leksykonu i przykładami wygenerowanych zdań. Opis wyniku i jego powiązań z kodem: [`results/syntactic_results/README.md`](results/syntactic_results/README.md).

### 3. Analiza semantyczna

Analiza reprezentuje rzeczowniki jako wektory powiązań z czasownikami przechodnimi i grupuje je za pomocą samoorganizującej się mapy Kohonena (SOM). Raport podsumowuje neurony, przypisane do nich rzeczowniki i czystość klastrów.

- **Kod:** [`src/semantic_analysis/`](src/semantic_analysis/) - [`vocabulary.py`](src/semantic_analysis/vocabulary.py) zawiera rzeczowniki, kategorie i czasowniki, a [`main.py`](src/semantic_analysis/main.py) buduje wektory, trenuje SOM i tworzy raport. Opis implementacji: [`src/semantic_analysis/README.md`](src/semantic_analysis/README.md).
- **Wynik:** [`results/semantic_results/semantic_analysis.txt`](results/semantic_results/semantic_analysis.txt). Opis zawartości i interpretacji: [`results/semantic_results/README.md`](results/semantic_results/README.md).

## Uruchamianie analiz

Uruchamiaj każdy skrypt z jego katalogu, ponieważ moduły używają lokalnych importów i względnych ścieżek do danych lub wyników.

Przygotowanie korpusu i uruchomienie analizy statystycznej:

```bash
cd src/statistical_analysis
uv run python download.py
uv run python clean.py
uv run python analyze_words.py
uv run python analyze_characters.py
```

Wygenerowanie próbki zdań:

```bash
cd src/syntactic_analysis
uv run python main.py
```

Uruchomienie analizy semantycznej:

```bash
cd src/semantic_analysis
uv run python main.py
```

Pobieranie korpusu wymaga dostępu do zbioru `PleIAs/Czech-PD` i może wymagać pobrania zależności. Skrypty nadpisują pliki wynikowe o tych samych nazwach w odpowiednich katalogach `results/`.

## Mapa repozytorium

| Katalog | Zawartość | Dokumentacja |
|---|---|---|
| [`data/`](data/) | Czeski korpus źródłowy i jego oczyszczona wersja. | [`data/README.md`](data/README.md) |
| [`src/statistical_analysis/`](src/statistical_analysis/) | Pobieranie, czyszczenie i analiza statystyczna korpusu. | [`README.md`](src/statistical_analysis/README.md) |
| [`src/syntactic_analysis/`](src/syntactic_analysis/) | Leksykon, reguły gramatyczne i generator zdań SVO. | [`README.md`](src/syntactic_analysis/README.md) |
| [`src/semantic_analysis/`](src/semantic_analysis/) | Leksykon semantyczny oraz implementacja SOM. | [`README.md`](src/semantic_analysis/README.md) |
| [`results/statistical_results/`](results/statistical_results/) | Tabele, wykres i podsumowanie analizy statystycznej. | [`README.md`](results/statistical_results/README.md) |
| [`results/syntactic_results/`](results/syntactic_results/) | Podsumowanie i przykładowe zdania generatora. | [`README.md`](results/syntactic_results/README.md) |
| [`results/semantic_results/`](results/semantic_results/) | Raport z klastrów mapy semantycznej. | [`README.md`](results/semantic_results/README.md) |
