from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from lexicon import Verb, VerbType, Pronoun, Noun, Determiner, Adjective


class Tense(str, Enum):
    PRS_S = "Present Simple"; PRS_C = "Present Continuous"; PRS_P = "Present Perfect"; PRS_PC = "Present Perfect Continuous"
    PST_S = "Past Simple"; PST_C = "Past Continuous"; PST_P = "Past Perfect"; PST_PC = "Past Perfect Continuous"
    FUT_S = "Future Simple"; FUT_C = "Future Continuous"; FUT_P = "Future Perfect"; FUT_PC = "Future Perfect Continuous"

class Mood(str, Enum):
    INDICATIVE = "Indicative"; INTERROGATIVE = "Interrogative"; NEGATIVE = "Negative"; IMPERATIVE = "Imperative"; CONDITIONAL = "Conditional"

class Voice(str, Enum):
    ACTIVE = "Active"; PASSIVE = "Passive"

@dataclass
class NounPhrase:
    is_pronoun: bool
    pronoun: Optional[Pronoun] = None
    determiner: Optional[Determiner] = None
    adjective: Optional[Adjective] = None
    noun: Optional[Noun] = None
    is_plural: bool = False

    @property
    def person(self): return self.pronoun.person if self.is_pronoun else 3

    @property
    def is_pl(self): return self.pronoun.is_plural if self.is_pronoun else self.is_plural

    def to_string(self, as_subject: bool = True) -> str:
        if self.is_pronoun: return self.pronoun.subject if as_subject else self.pronoun.object_form

        n_str = self.noun.plural if self.is_plural else self.noun.singular
        tokens = []

        if self.determiner and self.determiner.word_sg:
            d_str = self.determiner.word_pl if self.is_plural else self.determiner.word_sg
            if d_str == "a/an":
                starts_vowel = self.adjective.starts_with_vowel if self.adjective else self.noun.starts_with_vowel
                d_str = "an" if starts_vowel else "a"
            tokens.append(d_str)

        if self.adjective: tokens.append(self.adjective.word)
        tokens.append(n_str)
        return " ".join(tokens)

@dataclass
class VerbPhrase:
    aux1: str; aux_other: List[str]; main_v: str; is_negated: bool = False


def conjugate(verb: Verb, person: int, is_pl: bool, t: Tense, m: Mood, v: Voice) -> VerbPhrase:
    third_sg = (person == 3 and not is_pl)
    first_sg = (person == 1 and not is_pl)
    is_neg = (m == Mood.NEGATIVE)

    if m == Mood.IMPERATIVE:
        return VerbPhrase("do" if is_neg else "", ["be"] if v == Voice.PASSIVE else [], verb.participle if v == Voice.PASSIVE else verb.base, is_neg)
    if m == Mood.CONDITIONAL:
        return VerbPhrase("would", ["be"] if v == Voice.PASSIVE else [], verb.participle if v == Voice.PASSIVE else verb.base, is_neg)

    aux1, aux2, main = "", [], verb.base

    if v == Voice.ACTIVE:
        if t == Tense.PRS_S:
            if m == Mood.INDICATIVE: main = verb.third_sing if third_sg else verb.base
            else: aux1 = "does" if third_sg else "do"
        elif t == Tense.PRS_C: aux1 = "am" if first_sg else ("is" if third_sg else "are"); main = verb.gerund
        elif t == Tense.PRS_P: aux1 = "has" if third_sg else "have"; main = verb.participle
        elif t == Tense.PRS_PC: aux1 = "has" if third_sg else "have"; aux2 = ["been"]; main = verb.gerund
        elif t == Tense.PST_S:
            if m == Mood.INDICATIVE: main = verb.past
            else: aux1 = "did"
        elif t == Tense.PST_C: aux1 = "was" if (first_sg or third_sg) else "were"; main = verb.gerund
        elif t == Tense.PST_P: aux1 = "had"; main = verb.participle
        elif t == Tense.PST_PC: aux1 = "had"; aux2 = ["been"]; main = verb.gerund
        elif t == Tense.FUT_S: aux1 = "will"
        elif t == Tense.FUT_C: aux1 = "will"; aux2 = ["be"]; main = verb.gerund
        elif t == Tense.FUT_P: aux1 = "will"; aux2 = ["have"]; main = verb.participle
        elif t == Tense.FUT_PC: aux1 = "will"; aux2 = ["have", "been"]; main = verb.gerund
    else:
        main = verb.participle
        if t == Tense.PRS_S: aux1 = "am" if first_sg else ("is" if third_sg else "are")
        elif t == Tense.PRS_C: aux1 = "am" if first_sg else ("is" if third_sg else "are"); aux2 = ["being"]
        elif t == Tense.PRS_P: aux1 = "has" if third_sg else "have"; aux2 = ["been"]
        elif t == Tense.PRS_PC: aux1 = "has" if third_sg else "have"; aux2 = ["been", "being"]
        elif t == Tense.PST_S: aux1 = "was" if (first_sg or third_sg) else "were"
        elif t == Tense.PST_C: aux1 = "was" if (first_sg or third_sg) else "were"; aux2 = ["being"]
        elif t == Tense.PST_P: aux1 = "had"; aux2 = ["been"]
        elif t == Tense.PST_PC: aux1 = "had"; aux2 = ["been", "being"]
        elif t == Tense.FUT_S: aux1 = "will"; aux2 = ["be"]
        elif t == Tense.FUT_C: aux1 = "will"; aux2 = ["be", "being"]
        elif t == Tense.FUT_P: aux1 = "will"; aux2 = ["have", "been"]
        elif t == Tense.FUT_PC: aux1 = "will"; aux2 = ["have", "been", "being"]

    return VerbPhrase(aux1, aux2, main, is_neg)
