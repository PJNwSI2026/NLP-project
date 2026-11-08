# NLP University Project

Projekt z przetwarzania języka naturalnego (NLP) — dr inż. Mirosław Gajer.

Projekt realizowany przy użyciu środowiska **Python 3.14** i menedżera pakietów **uv**.

---

## Struktura projektu

- `src/data/` oraz `src/czech_nlp/` — **Część 1: Analiza statystyczna języka** (język czeski: korpus 150k słów, prawo Zipfa, rdzeń języka, słowa pokrywające 90% tekstu).
- `src/syntactic/` — **Część 2: Analiza syntaktyczna języka** (język angielski: generator zdań prostych typu SVO, 12 czasów, 5 trybów, strona czynna/bierna, czasowniki przechodnie, nieprzechodnie i zwrotne, interfejs graficzny GUI).
- `tests/` — Testy jednostkowe (`pytest`).
- `results/` — Wygenerowane raporty i zestawienia tabelaryczne do sprawozdania.

---

## Część 2: Analiza syntaktyczna (Generator zdań SVO)

Moduł syntaktyczny w pełni implementuje wymagania projektowe dla języka angielskiego:
- **Baza leksykalna:**
  - 135 rzeczowników (l. pojedyncza, mnoga, policzalność, rodzaj gramatyczny),
  - 110 czasowników (przechodnie SVO, nieprzechodnie SV, zwrotne z zaimkami zwrotnymi),
  - 117 przymiotników,
  - Zaimki osobowe (mianownik, dopełnienie, formy zwrotne),
  - 19 określników (rodzajniki określone, nieokreślone `a`/`an`, dzierżawcze, wskazujące, kwantyfikatory).
- **Czasy gramatyczne:** wszystkie 12 czasów języka angielskiego (Simple, Continuous, Perfect, Perfect Continuous dla Present, Past i Future).
- **Tryby:** oznajmujący (*indicative*), pytający (*interrogative*), przeczący (*negative*), rozkazujący (*imperative*), przypuszczający (*conditional*).
- **Strony:** czynna (*active*) oraz bierna (*passive*).
- **Drzewa składniowe:** generowanie konstytuentowych drzew rozbioru syntaktycznego dla każdego zdania.

---

## Uruchamianie

### 1. Interfejs graficzny (GUI)
Uruchamia okienkową aplikację desktopową (Tkinter/ttk) umożliwiającą sterowanie wszystkimi parametrami gramatycznymi, podgląd drzew syntaktycznych, kopiowanie do schowka oraz eksport do Markdown:
```bash
uv run syntactic-gui
```
lub:
```bash
uv run python -m src.syntactic.gui
```

### 2. Przykłady w konsoli (CLI)
Wygenerowanie N losowych zdań wraz ze szczegółowym rozbiorem:
```bash
uv run syntactic --count 5
```

### 3. Generowanie pełnego raportu ze wszystkimi matrycami
Generuje plik `results/syntactic/syntactic_report.md` zawierający zestawienie wszystkich 12 czasów (strona czynna vs bierna), wszystkich trybów, czasowników zwrotnych, nieprzechodnich i przykładowych drzew rozbioru do sprawozdania PDF:
```bash
uv run syntactic --generate-report
```

### 4. Uruchomienie testów jednostkowych
Uruchomienie kompletnego zestawu 44 testów automatycznych:
```bash
uv run pytest
```
