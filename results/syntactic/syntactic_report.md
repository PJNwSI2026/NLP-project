# Analiza Syntaktyczna Języka Naturalnego (Język Angielski)
## Generator Zdań Prostych Typu SVO
**Autor projektu:** Jakub Białek
**Prowadzący:** Dr inż. Mirosław Gajer

---

## 1. Wymogi projektowe i baza leksykalna

Zgodnie z wymogami projektu, generator operuje na bazach leksykalnych przekraczających minimum 100 jednostek:
- **Rzeczowniki (Nouns):** 135 (wymóg: min. 100) — z uwzględnieniem liczby pojedynczej, mnogiej, policzalności i rodzaju gramatycznego.
- **Czasowniki (Verbs):** 110 (wymóg: min. 100) — z kompletnymi formami koniugacyjnymi (V1, V2, V3, -s, -ing), w tym:
  - Czasowniki przechodnie (*transitive* — z dopełnieniem bliższym SVO): 80
  - Czasowniki nieprzechodnie (*intransitive* — schemat SV): 20
  - Czasowniki zwrotne (*reflexive* — z zaimkiem zwrotnym): 10
- **Przymiotniki (Adjectives):** 117 (wymóg: min. 100) — barwy, wymiary, cechy charakteru, stany fizyczne, smaki.
- **Zaimki osobowe (Personal Pronouns):** 7 (formy podmiotu, dopełnienia oraz formy zwrotne).
- **Określniki (Determiners):** 19 — rodzajniki określone (*the*), nieokreślone (*a, an*), zerowe, dzierżawcze (*my, his, their*), wskazujące (*this, those*) i kwantyfikatory (*every, some, many*).

---

## 2. Matryca 12 czasów gramatycznych (Active Voice vs. Passive Voice)

Poniższa tabela przedstawia transformację tego samego zestawu semantycznego (Podmiot: *the student*, Czasownik: *read*, Dopełnienie: *the book*) przez wszystkie 12 czasów gramatycznych w stronie czynnej i biernej:

| Czas gramatyczny (Tense) | Strona czynna (Active Voice) | Strona bierna (Passive Voice) |
| :--- | :--- | :--- |
| **Present Simple** | The student reads the book. | The book is read by the student. |
| **Present Continuous** | The student is reading the book. | The book is being read by the student. |
| **Present Perfect** | The student has read the book. | The book has been read by the student. |
| **Present Perfect Continuous** | The student has been reading the book. | The book has been being read by the student. |
| **Past Simple** | The student read the book. | The book was read by the student. |
| **Past Continuous** | The student was reading the book. | The book was being read by the student. |
| **Past Perfect** | The student had read the book. | The book had been read by the student. |
| **Past Perfect Continuous** | The student had been reading the book. | The book had been being read by the student. |
| **Future Simple** | The student will read the book. | The book will be read by the student. |
| **Future Continuous** | The student will be reading the book. | The book will be being read by the student. |
| **Future Perfect** | The student will have read the book. | The book will have been read by the student. |
| **Future Perfect Continuous** | The student will have been reading the book. | The book will have been being read by the student. |

---

## 3. Zestawienie trybów (Moods)

Generator obsługuje wszystkie wymagane tryby wypowiedzi (oznajmujący, pytający, przeczący, rozkazujący i przypuszczający):

| Tryb (Mood) | Przykładowe zdanie wygenerowane | Konstrukcja składniowa |
| :--- | :--- | :--- |
| **Indicative (Oznajmujący)** | `The student has read the book.` | Szyki SVO oznajmujący: Podmiot + Orzeczenie + Dopełnienie |
| **Interrogative (Pytający)** | `Has the student read the book?` | Inwersja operatora posiłkowego na początek zdania + znak '?' |
| **Negative (Przeczący)** | `The book has not been read by the student.` | Partykuła przecząca 'not' po pierwszym czasowniku posiłkowym |
| **Imperative (Rozkazujący)** | `Read the book!` | Podmiot domyślny ('you'), forma podstawowa czasownika + wykrzyknik '!' |
| **Conditional (Przypuszczający)** | `The student would read the book.` | Czasownik modalny 'would' + bezokolicznik |

---

## 4. Przykłady zdań dla czasowników nieprzechodnich i zwrotnych

### Czasowniki zwrotne (Reflexive Verbs):
Wymagają automatycznego uzgodnienia zaimka zwrotnego z osobą, liczbą i rodzajem podmiotu:
- `I prepared myself.` *(Podmiot: I -> Zaimek zwrotny: myself)*
- `You prepared yourself.` *(Podmiot: you -> Zaimek zwrotny: yourself)*
- `He prepared himself.` *(Podmiot: he -> Zaimek zwrotny: himself)*
- `She prepared herself.` *(Podmiot: she -> Zaimek zwrotny: herself)*
- `It prepared itself.` *(Podmiot: it -> Zaimek zwrotny: itself)*
- `We prepared ourselves.` *(Podmiot: we -> Zaimek zwrotny: ourselves)*
- `They prepared themselves.` *(Podmiot: they -> Zaimek zwrotny: themselves)*

### Czasowniki nieprzechodnie (Intransitive Verbs - struktura SV):
- `Ancient bakers have slept.` *(Czasownik: sleep)*
- `Our sweet eggs will run.` *(Czasownik: run)*
- `Those valuable owls laugh.` *(Czasownik: laugh)*
- `She was smiling.` *(Czasownik: smile)*
- `Hammers are crying.` *(Czasownik: cry)*

---

## 5. Drzewa struktury syntaktycznej (Parse Trees)

Poniżej przedstawiono przykładowe reprezentacje drzewiaste (konstytuentowe) wygenerowanych zdań o różnym stopniu złożoności frazy rzeczownikowej:

### Przykład 1: `She is pouring him.`
- **Czas:** Present Continuous | **Tryb:** Indicative (Oznajmujący) | **Strona:** Active (Czynna)
```text
[S
  ├── [NP (Subject): "she"]
  └── [VP (Predicate): "is pouring"
        ├── [NP (Direct Object): "him"]
      ]
]
```

### Przykład 2: `Did my fragile sword pride itself?`
- **Czas:** Past Simple | **Tryb:** Interrogative (Pytający) | **Strona:** Active (Czynna)
```text
[S
  ├── [NP (Subject): "my fragile sword"]
  └── [VP (Predicate): "did pride"
        ├── [NP (Reflexive Object): "itself"]
      ]
]
```

### Przykład 3: `Every bright bottle will have been solved by all clever tea.`
- **Czas:** Future Perfect | **Tryb:** Indicative (Oznajmujący) | **Strona:** Passive (Bierna)
```text
[S
  ├── [NP (Subject): "every bright bottle"]
  └── [VP (Predicate): "will have been solved"
        ├── [PP (Agent by-phrase): "by all clever tea"]
      ]
]
```
