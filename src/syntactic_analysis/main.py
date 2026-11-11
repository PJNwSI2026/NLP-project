import os
from lexicon import NOUNS, VERBS, ADJECTIVES, PRONOUNS, DETERMINERS, VerbType
from generator import SentenceGenerator


g = SentenceGenerator()

lines = [
    "ANALIZA SYNTAKTYCZNA JĘZYKA NATURALNEGO (GENERATOR SVO)\n",
    "WYMOGI LEKSYKALNE PROJEKTU",
    f"- rzeczowniki: {len(NOUNS)}",
    f"- czasowniki: {len(VERBS)} - przechodnie SVO ({sum(1 for v in VERBS if v.verb_type == VerbType.TRANSITIVE)}), nieprzechodnie SV ({sum(1 for v in VERBS if v.verb_type == VerbType.INTRANSITIVE)}), zwrotne ({sum(1 for v in VERBS if v.verb_type == VerbType.REFLEXIVE)})",
    f"- przymiotniki: {len(ADJECTIVES)}",
    f"- zaimki: {len(PRONOUNS)}",
    f"- określniki: {len(DETERMINERS)}\n",
    "PRÓBKA WYGENEROWANYCH ZDAŃ",
]

for i in range(50):
    lines.append(f"{i+1}. {g.generate()}")

with open("../../results/syntactic_results/syntactic_analysis.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
