# Analiza Syntaktyczna Języka — Generator Zdań SVO

Moduł generatora zdań prostych typu **SVO** (*Subject – Verb – Object* / Podmiot – Orzeczenie – Dopełnienie bliższe) dla języka angielskiego, zrealizowany w ramach projektu z przedmiotu **Przetwarzanie Języka Naturalnego (NLP)** prowadzonego przez **dra inż. Mirosława Gajera**.

Projekt został wykonany w środowisku **Python 3.14** z wykorzystaniem menedżera pakietów **uv**.

---

## 1. Co zostało zrobione?

Moduł w 100% realizuje i przewyższa wytyczne z pliku `_wymogi.docx`:

### Baza leksykalna (wymóg: minimum po 100 jednostek):
- **135 rzeczowników (`Noun`):** każdy obiekt przechowuje formę liczby pojedynczej, mnogiej, policzalność (`countable`), rodzaj gramatyczny (`gender`) oraz znacznik fonetyczny nagłosu samogłoskowego.
- **110 czasowników (`Verb`):** każdy czasownik posiada komplet 5 form koniugacyjnych (V1 bezokolicznik, V2 Past Simple, V3 Past Participle, 3. osoba l. poj. `-s`, imiesłów czynny `-ing`):
  - **80 czasowników przechodnich (*transitive*):** wiążących się z dopełnieniem bliższym (struktura SVO),
  - **20 czasowników nieprzechodnich (*intransitive*):** niewymagających dopełnienia (struktura SV),
  - **10 czasowników zwrotnych (*reflexive*):** automatycznie wiążących się z uzgodnionym zaimkiem zwrotnym (struktura S + V + Reflexive Pronoun).
- **117 przymiotników (`Adjective`):** barwy, wymiary, cechy charakteru, stany fizyczne, smaki itp.
- **7 zaimków osobowych (`PersonalPronoun`):** z pełnymi formami mianownika (*I, you, he...*), dopełnienia (*me, him, them...*) oraz formami zwrotnymi (*myself, himself, themselves...*).
- **19 określników (`Determiner`):** rodzajniki określone (*the*), nieokreślone (*a, an*), zerowe, zaimki dzierżawcze (*my, his, their*), wskazujące (*this, that, these, those*) oraz kwantyfikatory (*every, some, many, few, all, no*).

### Pełna matryca gramatyczna:
1. **Wszystkie 12 czasów gramatycznych języka angielskiego:**
   - *Present:* Simple, Continuous, Perfect, Perfect Continuous
   - *Past:* Simple, Continuous, Perfect, Perfect Continuous
   - *Future:* Simple, Continuous, Perfect, Perfect Continuous
2. **Wszystkie 5 trybów wypowiedzi:**
   - **Oznajmujący (*Indicative*):** standardowy szyk SVO, kropka na końcu.
   - **Pytający (*Interrogative*):** automatyczna inwersja pierwszego operatora posiłkowego na początek zdania (*Do/Does/Did/Is/Are/Will/Have...*), znak zapytania `?`.
   - **Przeczący (*Negative*):** wstawienie partykuły przeczącej *not* po pierwszym operatorze posiłkowym.
   - **Rozkazujący (*Imperative*):** ukrycie podmiotu (domyślne *you*), rozpoczęcie od bezokolicznika, wykrzyknik `!`.
   - **Przypuszczający (*Conditional*):** użycie czasownika modalnego *would* + bezokolicznik.
3. **Strona czynna (*Active Voice*) i bierna (*Passive Voice*):**
   - W stronie biernej dawne dopełnienie staje się podmiotem powierzchniowym (z którym uzgadniane jest orzeczenie), orzeczenie przyjmuje formę `to be + V3`, a dawny podmiot staje się opcjonalną frazą sprawcy `by + agent`.
4. **Reguły uzgadniania cech (*Agreement*):**
   - Zgoda podmiotu i orzeczenia pod względem osoby (1., 2., 3.) i liczby (pojedyncza/mnoga).
   - Fonetyczny dobór rodzajnika nieokreślonego (*a* przed spółgłoskami, *an* przed samogłoskami i niemym 'h', np. *an actor*, *an honest man*, ale *a car*).
   - Zgodność zaimków wskazujących z liczbą (*this book* vs *these books*).
5. **Drzewa struktury syntaktycznej:**
   - Każde wygenerowane zdanie posiada wyrenderowane drzewo konstytuentowe pokazujące rozbicie na frazy `[NP (Subject)]`, `[VP (Predicate)]`, `[NP (Object)]` i `[PP (Agent)]`.
6. **Interfejs graficzny GUI:**
   - Aplikacja desktopowa w `tkinter`/`ttk` ze sterowaniem każdym parametrem, podglądem drzewa, matrycą 12 czasów, kopiowaniem do schowka i eksportem do pliku.
7. **Zestaw testów jednostkowych:**
   - 44 testy automatyczne w `pytest` weryfikujące poprawność gramatyczną, leksykon i odporność interfejsu.

---

## 2. Architektura plików w katalogu

| Plik | Rola i odpowiedzialność |
| :--- | :--- |
| [`lexicon.py`](lexicon.py) | Baza słownikowa: definicje klas `Noun`, `Verb`, `Adjective`, `PersonalPronoun`, `Determiner` oraz zbiory ponad 100 jednostek każdej kategorii. |
| [`morphology.py`](morphology.py) | Reguły fonetyczne i odmiany: dobór *a* vs *an*, uzgadnianie zaimków zwrotnych (*himself, herself...*). |
| [`grammar.py`](grammar.py) | Formalna gramatyka: definicje `Tense`, `Mood`, `Voice`, struktura `NounPhrase` oraz silnik koniugacji `conjugate_verb_phrase()`. |
| [`generator.py`](generator.py) | Silnik generatora `SentenceGenerator`: składanie zdań, inwersje, transformacje pasywne, generowanie drzewa i matrycy czasów. |
| [`gui.py`](gui.py) | Aplikacja okienkowa (GUI): interaktywne kontrolki, synchronizacja pól, tabela 12 czasów, eksport raportu. |
| [`main.py`](main.py) | Główny punkt wejścia CLI: obsługa flag `--gui`, `--count N`, `--generate-report`. |
| [`__init__.py`](__init__.py) | Plik pakietowy modułu. |

---

## 3. Jak tego użyć? (Instrukcja uruchomienia)

Wszystkie polecenia wykonujemy w terminalu w głównym katalogu projektu (`d:\studia\NLP-project`):

### Sposób 1: Uruchomienie aplikacji graficznej (GUI)
Najwygodniejszy sposób prezentacji projektu prowadzącemu:
```bash
uv run syntactic-gui
```
lub:
```bash
uv run python -m src.syntactic.gui
```
W oknie aplikacji możesz:
- Wybierać dowolny z 12 czasów, 5 trybów, stronę czynną lub bierną,
- Wpisywać/wybierać konkretne rzeczowniki (np. `actor`) lub zaimki,
- Kliknąć **„🎲 Wylosuj zdanie”** lub **„⚙️ Wygeneruj z ustawionymi parametrami”**,
- Kliknąć **„📋 Wygeneruj matrycę 12 czasów”**, aby zobaczyć tabelę odmiany zdania przez wszystkie czasy,
- Kopiować zdania do schowka za pomocą przycisku **„📋 Kopiuj zdanie”**.

---

### Sposób 2: Generowanie przykładowych zdań w konsoli (CLI)
Aby szybko wygenerować $N$ losowych zdań wraz ze szczegółowym rozbiorem:
```bash
uv run syntactic --count 5
```
Przykładowe wyjście w konsoli:
```text
[1] It is being rescued by their valuable girl.
    • Tense:     Present Continuous
    • Mood:      Indicative (Oznajmujący)
    • Voice:     Passive (Bierna)
    • Verb Type: transitive
    • Subject:   it
    • Predicate: is being rescued
    • Agent:     by their valuable girl
```

---

### Sposób 3: Generowanie pełnego raportu do sprawozdania
Polecenie tworzy gotowy dokument Markdown z kompletem tabel porównawczych:
```bash
uv run syntactic --generate-report
```
Raport zostanie zapisany w pliku:
`results/syntactic/syntactic_report.md`

Zawiera on:
1. Statystyki bazy leksykalnej,
2. Matrycę 12 czasów (strona czynna vs bierna dla tej samej pary podmiot-czasownik-dopełnienie),
3. Zestawienie wszystkich 5 trybów,
4. Zestawienie zdań zwrotnych i nieprzechodnich,
5. Przykładowe drzewa konstytuentowe.

---

### Sposób 4: Uruchomienie automatycznych testów jednostkowych
Aby zweryfikować poprawność modułu:
```bash
uv run pytest
```
Wynik:
```text
tests\test_syntactic.py ............................................ [100%]
============================= 44 passed in 0.08s ==============================
```

---

## 4. Użycie programistyczne w kodzie Pythona

Moduł można łatwo zaimportować w dowolnym własnym skrypcie:

```python
from src.syntactic.generator import SentenceGenerator
from src.syntactic.grammar import Tense, Mood, Voice
from src.syntactic.lexicon import VERBS, NOUNS

generator = SentenceGenerator(seed=42)

# 1. Wygenerowanie w pełni losowego zdania
s1 = generator.generate()
print(s1.text)

# 2. Wygenerowanie zdania o ściśle określonych parametrach
verb_attack = next(v for v in VERBS if v.base == "attack")
noun_actor = next(n for n in NOUNS if n.singular == "actor")
noun_tiger = next(n for n in NOUNS if n.singular == "tiger")

s2 = generator.generate(
    tense=Tense.PAST_CONTINUOUS,
    mood=Mood.INTERROGATIVE,
    voice=Voice.ACTIVE,
    verb=verb_attack,
    subject=generator.create_noun_phrase(noun=noun_actor),
    direct_object=generator.create_noun_phrase(noun=noun_tiger),
)

print(s2.text)
# Wynik: Was the actor attacking the tiger?

print(s2.syntax_tree)
# Drzewo konstytuentowe zdania
```

