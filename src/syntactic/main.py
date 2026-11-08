"""Main command-line and application entry point for the syntactic analysis module.
"""

import argparse
import os
import sys
from typing import Optional

from .generator import SentenceGenerator
from .grammar import Mood, Tense, Voice, NounPhrase
from .lexicon import (
    ADJECTIVES,
    DETERMINERS,
    NOUNS,
    PRONOUNS,
    VERBS,
    VerbType,
)


def generate_full_markdown_report(output_path: str = "results/syntactic/syntactic_report.md") -> str:
    """Generates an extensive, publication-ready markdown report with all grammar permutations."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    g = SentenceGenerator(seed=42)

    lines = [
        "# Analiza Syntaktyczna Języka Naturalnego (Język Angielski)",
        "## Generator Zdań Prostych Typu SVO",
        "**Autor projektu:** Jakub Białek",
        "**Prowadzący:** Dr inż. Mirosław Gajer",
        "",
        "---",
        "",
        "## 1. Wymogi projektowe i baza leksykalna",
        "",
        "Zgodnie z wymogami projektu, generator operuje na bazach leksykalnych przekraczających minimum 100 jednostek:",
        f"- **Rzeczowniki (Nouns):** {len(NOUNS)} (wymóg: min. 100) — z uwzględnieniem liczby pojedynczej, mnogiej, policzalności i rodzaju gramatycznego.",
        f"- **Czasowniki (Verbs):** {len(VERBS)} (wymóg: min. 100) — z kompletnymi formami koniugacyjnymi (V1, V2, V3, -s, -ing), w tym:",
        f"  - Czasowniki przechodnie (*transitive* — z dopełnieniem bliższym SVO): {len([v for v in VERBS if v.verb_type == VerbType.TRANSITIVE])}",
        f"  - Czasowniki nieprzechodnie (*intransitive* — schemat SV): {len([v for v in VERBS if v.verb_type == VerbType.INTRANSITIVE])}",
        f"  - Czasowniki zwrotne (*reflexive* — z zaimkiem zwrotnym): {len([v for v in VERBS if v.verb_type == VerbType.REFLEXIVE])}",
        f"- **Przymiotniki (Adjectives):** {len(ADJECTIVES)} (wymóg: min. 100) — barwy, wymiary, cechy charakteru, stany fizyczne, smaki.",
        f"- **Zaimki osobowe (Personal Pronouns):** {len(PRONOUNS)} (formy podmiotu, dopełnienia oraz formy zwrotne).",
        f"- **Określniki (Determiners):** {len(DETERMINERS)} — rodzajniki określone (*the*), nieokreślone (*a, an*), zerowe, dzierżawcze (*my, his, their*), wskazujące (*this, those*) i kwantyfikatory (*every, some, many*).",
        "",
        "---",
        "",
        "## 2. Matryca 12 czasów gramatycznych (Active Voice vs. Passive Voice)",
        "",
        "Poniższa tabela przedstawia transformację tego samego zestawu semantycznego (Podmiot: *the student*, Czasownik: *read*, Dopełnienie: *the book*) przez wszystkie 12 czasów gramatycznych w stronie czynnej i biernej:",
        "",
        "| Czas gramatyczny (Tense) | Strona czynna (Active Voice) | Strona bierna (Passive Voice) |",
        "| :--- | :--- | :--- |",
    ]

    verb_read = next(v for v in VERBS if v.base == "read")
    noun_student = next(n for n in NOUNS if n.singular == "student")
    noun_book = next(n for n in NOUNS if n.singular == "book")
    det_the = next(d for d in DETERMINERS if d.singular_word == "the")

    s_np = NounPhrase(is_pronoun=False, determiner=det_the, adjectives=[], noun=noun_student, is_plural=False)
    o_np = NounPhrase(is_pronoun=False, determiner=det_the, adjectives=[], noun=noun_book, is_plural=False)

    for t in Tense:
        sent_act = g.generate(tense=t, mood=Mood.INDICATIVE, voice=Voice.ACTIVE, verb=verb_read, subject=s_np, direct_object=o_np)
        sent_pas = g.generate(tense=t, mood=Mood.INDICATIVE, voice=Voice.PASSIVE, verb=verb_read, subject=s_np, direct_object=o_np)
        lines.append(f"| **{t.value}** | {sent_act.text} | {sent_pas.text} |")

    lines.extend([
        "",
        "---",
        "",
        "## 3. Zestawienie trybów (Moods)",
        "",
        "Generator obsługuje wszystkie wymagane tryby wypowiedzi (oznajmujący, pytający, przeczący, rozkazujący i przypuszczający):",
        "",
        "| Tryb (Mood) | Przykładowe zdanie wygenerowane | Konstrukcja składniowa |",
        "| :--- | :--- | :--- |",
    ])

    mood_notes = {
        Mood.INDICATIVE: "Szyki SVO oznajmujący: Podmiot + Orzeczenie + Dopełnienie",
        Mood.INTERROGATIVE: "Inwersja operatora posiłkowego na początek zdania + znak '?'",
        Mood.NEGATIVE: "Partykuła przecząca 'not' po pierwszym czasowniku posiłkowym",
        Mood.IMPERATIVE: "Podmiot domyślny ('you'), forma podstawowa czasownika + wykrzyknik '!'",
        Mood.CONDITIONAL: "Czasownik modalny 'would' + bezokolicznik",
    }

    for m in Mood:
        sm = g.generate(mood=m, tense=Tense.PRESENT_PERFECT, verb=verb_read, subject=s_np, direct_object=o_np)
        lines.append(f"| **{m.value}** | `{sm.text}` | {mood_notes[m]} |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Przykłady zdań dla czasowników nieprzechodnich i zwrotnych",
        "",
        "### Czasowniki zwrotne (Reflexive Verbs):",
        "Wymagają automatycznego uzgodnienia zaimka zwrotnego z osobą, liczbą i rodzajem podmiotu:",
    ])

    verb_prep = next(v for v in VERBS if v.base == "prepare")
    for subj_pron in PRONOUNS:
        s_refl = g.generate(
            tense=Tense.PAST_SIMPLE,
            mood=Mood.INDICATIVE,
            voice=Voice.ACTIVE,
            verb=verb_prep,
            subject=NounPhrase(is_pronoun=True, pronoun=subj_pron),
        )
        lines.append(f"- `{s_refl.text}` *(Podmiot: {subj_pron.subject} -> Zaimek zwrotny: {subj_pron.reflexive})*")

    lines.extend([
        "",
        "### Czasowniki nieprzechodnie (Intransitive Verbs - struktura SV):",
    ])
    intransitive_verbs = [v for v in VERBS if v.verb_type == VerbType.INTRANSITIVE][:5]
    for iv in intransitive_verbs:
        s_intr = g.generate(verb=iv, mood=Mood.INDICATIVE, voice=Voice.ACTIVE)
        lines.append(f"- `{s_intr.text}` *(Czasownik: {iv.base})*")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Drzewa struktury syntaktycznej (Parse Trees)",
        "",
        "Poniżej przedstawiono przykładowe reprezentacje drzewiaste (konstytuentowe) wygenerowanych zdań o różnym stopniu złożoności frazy rzeczownikowej:",
        "",
    ])

    sample_sentences = [
        g.generate(tense=Tense.PRESENT_CONTINUOUS, mood=Mood.INDICATIVE, voice=Voice.ACTIVE, include_adjectives=True),
        g.generate(tense=Tense.PAST_SIMPLE, mood=Mood.INTERROGATIVE, voice=Voice.ACTIVE, include_adjectives=True),
        g.generate(tense=Tense.FUTURE_PERFECT, mood=Mood.INDICATIVE, voice=Voice.PASSIVE, include_adjectives=True),
    ]

    for i, s in enumerate(sample_sentences, 1):
        lines.append(f"### Przykład {i}: `{s.text}`")
        lines.append(f"- **Czas:** {s.tense.value} | **Tryb:** {s.mood.value} | **Strona:** {s.voice.value}")
        lines.append("```text")
        lines.append(s.syntax_tree)
        lines.append("```\n")

    report_content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return output_path


def print_cli_samples(count: int = 5):
    """Prints N randomly generated sentences to the console."""
    g = SentenceGenerator()
    print("=" * 70)
    print(" SVO SENTENCE GENERATOR (Syntactic Analysis) — SAMPLE OUTPUTS")
    print("=" * 70)
    for i in range(1, count + 1):
        s = g.generate()
        print(f"\n[{i}] {s.text}")
        print(f"    • Tense:     {s.tense.value}")
        print(f"    • Mood:      {s.mood.value}")
        print(f"    • Voice:     {s.voice.value}")
        print(f"    • Verb Type: {s.verb_type.value}")
        print(f"    • Subject:   {s.subject_str}")
        print(f"    • Predicate: {s.predicate_str}")
        if s.object_str:
            print(f"    • Object:    {s.object_str}")
        if s.agent_str:
            print(f"    • Agent:     {s.agent_str}")
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="SVO Syntactic Sentence Generator (Analiza Syntaktyczna Języka)",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the interactive desktop Graphical User Interface (Tkinter)",
    )
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Generate a comprehensive markdown report (results/syntactic/syntactic_report.md)",
    )
    parser.add_argument(
        "--report-path",
        type=str,
        default="results/syntactic/syntactic_report.md",
        help="Custom output path for the markdown report",
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=0,
        help="Generate N sample sentences to console output",
    )

    args = parser.parse_args()

    # If --generate-report is requested
    if args.generate_report:
        path = generate_full_markdown_report(args.report_path)
        print(f"Pomyślnie wygenerowano raport ze wszystkimi matrycami w:\n{os.path.abspath(path)}")
        if not args.gui and args.count == 0:
            return

    # If --count is specified
    if args.count > 0:
        print_cli_samples(args.count)
        if not args.gui:
            return

    # If --gui or default (no explicit batch arguments)
    if args.gui or (not args.generate_report and args.count == 0):
        try:
            from .gui import SyntacticGUI
            app = SyntacticGUI()
            app.mainloop()
        except Exception as e:
            print(f"Błąd uruchamiania GUI: {e}")
            print("Przełączam na tryb konsolowy (CLI):")
            print_cli_samples(5)


if __name__ == "__main__":
    main()
