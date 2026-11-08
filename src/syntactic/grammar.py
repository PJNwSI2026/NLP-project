"""Grammar structures, morphological rules, agreement, and tense/mood/voice conjugation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
from .lexicon import (
    Adjective,
    Determiner,
    DeterminerType,
    Gender,
    Noun,
    PersonalPronoun,
    Verb,
    VerbType,
)
from .morphology import (
    choose_indefinite_article,
    get_reflexive_pronoun,
)


class Tense(str, Enum):
    PRESENT_SIMPLE = "Present Simple"
    PRESENT_CONTINUOUS = "Present Continuous"
    PRESENT_PERFECT = "Present Perfect"
    PRESENT_PERFECT_CONTINUOUS = "Present Perfect Continuous"
    PAST_SIMPLE = "Past Simple"
    PAST_CONTINUOUS = "Past Continuous"
    PAST_PERFECT = "Past Perfect"
    PAST_PERFECT_CONTINUOUS = "Past Perfect Continuous"
    FUTURE_SIMPLE = "Future Simple"
    FUTURE_CONTINUOUS = "Future Continuous"
    FUTURE_PERFECT = "Future Perfect"
    FUTURE_PERFECT_CONTINUOUS = "Future Perfect Continuous"


class Mood(str, Enum):
    INDICATIVE = "Indicative (Oznajmujący)"
    INTERROGATIVE = "Interrogative (Pytający)"
    NEGATIVE = "Negative (Przeczący)"
    IMPERATIVE = "Imperative (Rozkazujący)"
    CONDITIONAL = "Conditional (Przypuszczający)"


class Voice(str, Enum):
    ACTIVE = "Active (Czynna)"
    PASSIVE = "Passive (Bierna)"


@dataclass
class NounPhrase:
    """Represents a Noun Phrase (NP) or Pronoun."""
    is_pronoun: bool
    pronoun: Optional[PersonalPronoun] = None
    determiner: Optional[Determiner] = None
    adjectives: List[Adjective] = field(default_factory=list)
    noun: Optional[Noun] = None
    is_plural: bool = False

    @property
    def person(self) -> int:
        if self.is_pronoun and self.pronoun:
            return self.pronoun.person
        return 3

    @property
    def number_is_plural(self) -> bool:
        if self.is_pronoun and self.pronoun:
            return self.pronoun.is_plural
        return self.is_plural

    @property
    def gender(self) -> Gender:
        if self.is_pronoun and self.pronoun:
            return self.pronoun.gender
        if self.noun:
            return self.noun.gender
        return Gender.NEUTER

    def to_string(self, as_subject: bool = True) -> str:
        """Renders the NP to a string in subject or object position."""
        if self.is_pronoun and self.pronoun:
            return self.pronoun.subject if as_subject else self.pronoun.object_form

        if not self.noun:
            return ""

        noun_str = self.noun.plural if self.is_plural else self.noun.singular
        adj_strs = [adj.word for adj in self.adjectives]

        # Determine the word immediately following the determiner for a/an resolution
        first_word_after_det = adj_strs[0] if adj_strs else noun_str
        first_word_starts_vowel = (
            self.adjectives[0].starts_with_vowel_sound
            if self.adjectives
            else self.noun.starts_with_vowel_sound
        )

        det_str = ""
        if self.determiner:
            raw_det = self.determiner.plural_word if self.is_plural else self.determiner.singular_word
            if raw_det == "a/an":
                det_str = choose_indefinite_article(first_word_after_det, first_word_starts_vowel)
            elif raw_det is not None:
                det_str = raw_det

        tokens = []
        if det_str:
            tokens.append(det_str)
        tokens.extend(adj_strs)
        tokens.append(noun_str)
        return " ".join(tokens)


@dataclass
class VerbConjugation:
    """Breakdown of conjugated verb phrase."""
    first_auxiliary: Optional[str]  # Used for inversion in questions
    other_auxiliaries: List[str]     # Remaining auxiliaries
    main_verb: str                   # Base / inflected form
    is_negated: bool = False

    def to_affirmative_string(self) -> str:
        tokens = []
        if self.first_auxiliary:
            tokens.append(self.first_auxiliary)
        if self.is_negated:
            tokens.append("not")
        tokens.extend(self.other_auxiliaries)
        tokens.append(self.main_verb)
        return " ".join(tokens)


def conjugate_verb_phrase(
    verb: Verb,
    person: int,
    is_plural: bool,
    tense: Tense,
    mood: Mood,
    voice: Voice,
) -> VerbConjugation:
    """Generates the conjugated verb phrase auxiliary and main verb elements.
    
    Handles all 12 tenses, conditional, imperative, active, passive, and negation.
    """
    is_third_singular = (person == 3 and not is_plural)
    is_first_singular = (person == 1 and not is_plural)

    # 1. IMPERATIVE MOOD
    if mood == Mood.IMPERATIVE:
        if voice == Voice.PASSIVE:
            # e.g., "Be respected!" or "Let it be done!" -> simple passive imperative: "be + participle"
            if mood == Mood.NEGATIVE:
                return VerbConjugation(
                    first_auxiliary="do",
                    other_auxiliaries=["be"],
                    main_verb=verb.participle,
                    is_negated=True,
                )
            return VerbConjugation(
                first_auxiliary=None,
                other_auxiliaries=["be"],
                main_verb=verb.participle,
                is_negated=False,
            )
        else:
            if mood == Mood.NEGATIVE:
                return VerbConjugation(
                    first_auxiliary="do",
                    other_auxiliaries=[],
                    main_verb=verb.base,
                    is_negated=True,
                )
            return VerbConjugation(
                first_auxiliary=None,
                other_auxiliaries=[],
                main_verb=verb.base,
                is_negated=False,
            )

    # 2. CONDITIONAL MOOD
    if mood == Mood.CONDITIONAL:
        if voice == Voice.PASSIVE:
            return VerbConjugation(
                first_auxiliary="would",
                other_auxiliaries=["be"],
                main_verb=verb.participle,
                is_negated=(mood == Mood.NEGATIVE),
            )
        else:
            return VerbConjugation(
                first_auxiliary="would",
                other_auxiliaries=[],
                main_verb=verb.base,
                is_negated=(mood == Mood.NEGATIVE),
            )

    # 3. 12 TENSES (ACTIVE & PASSIVE)
    first_aux: Optional[str] = None
    other_aux: List[str] = []
    main_v: str = verb.base
    is_neg = (mood == Mood.NEGATIVE)

    if voice == Voice.ACTIVE:
        if tense == Tense.PRESENT_SIMPLE:
            if mood == Mood.INDICATIVE:
                first_aux = None
                other_aux = []
                main_v = verb.third_sing if is_third_singular else verb.base
            else:  # INTERROGATIVE or NEGATIVE
                first_aux = "does" if is_third_singular else "do"
                other_aux = []
                main_v = verb.base

        elif tense == Tense.PRESENT_CONTINUOUS:
            first_aux = "am" if is_first_singular else ("is" if is_third_singular else "are")
            other_aux = []
            main_v = verb.gerund

        elif tense == Tense.PRESENT_PERFECT:
            first_aux = "has" if is_third_singular else "have"
            other_aux = []
            main_v = verb.participle

        elif tense == Tense.PRESENT_PERFECT_CONTINUOUS:
            first_aux = "has" if is_third_singular else "have"
            other_aux = ["been"]
            main_v = verb.gerund

        elif tense == Tense.PAST_SIMPLE:
            if mood == Mood.INDICATIVE:
                first_aux = None
                other_aux = []
                main_v = verb.past
            else:  # INTERROGATIVE or NEGATIVE
                first_aux = "did"
                other_aux = []
                main_v = verb.base

        elif tense == Tense.PAST_CONTINUOUS:
            first_aux = "was" if (is_first_singular or is_third_singular) else "were"
            other_aux = []
            main_v = verb.gerund

        elif tense == Tense.PAST_PERFECT:
            first_aux = "had"
            other_aux = []
            main_v = verb.participle

        elif tense == Tense.PAST_PERFECT_CONTINUOUS:
            first_aux = "had"
            other_aux = ["been"]
            main_v = verb.gerund

        elif tense == Tense.FUTURE_SIMPLE:
            first_aux = "will"
            other_aux = []
            main_v = verb.base

        elif tense == Tense.FUTURE_CONTINUOUS:
            first_aux = "will"
            other_aux = ["be"]
            main_v = verb.gerund

        elif tense == Tense.FUTURE_PERFECT:
            first_aux = "will"
            other_aux = ["have"]
            main_v = verb.participle

        elif tense == Tense.FUTURE_PERFECT_CONTINUOUS:
            first_aux = "will"
            other_aux = ["have", "been"]
            main_v = verb.gerund

    else:  # PASSIVE VOICE (Main verb is always past participle V3)
        main_v = verb.participle

        if tense == Tense.PRESENT_SIMPLE:
            first_aux = "am" if is_first_singular else ("is" if is_third_singular else "are")
            other_aux = []

        elif tense == Tense.PRESENT_CONTINUOUS:
            first_aux = "am" if is_first_singular else ("is" if is_third_singular else "are")
            other_aux = ["being"]

        elif tense == Tense.PRESENT_PERFECT:
            first_aux = "has" if is_third_singular else "have"
            other_aux = ["been"]

        elif tense == Tense.PRESENT_PERFECT_CONTINUOUS:
            first_aux = "has" if is_third_singular else "have"
            other_aux = ["been", "being"]

        elif tense == Tense.PAST_SIMPLE:
            first_aux = "was" if (is_first_singular or is_third_singular) else "were"
            other_aux = []

        elif tense == Tense.PAST_CONTINUOUS:
            first_aux = "was" if (is_first_singular or is_third_singular) else "were"
            other_aux = ["being"]

        elif tense == Tense.PAST_PERFECT:
            first_aux = "had"
            other_aux = ["been"]

        elif tense == Tense.PAST_PERFECT_CONTINUOUS:
            first_aux = "had"
            other_aux = ["been", "being"]

        elif tense == Tense.FUTURE_SIMPLE:
            first_aux = "will"
            other_aux = ["be"]

        elif tense == Tense.FUTURE_CONTINUOUS:
            first_aux = "will"
            other_aux = ["be", "being"]

        elif tense == Tense.FUTURE_PERFECT:
            first_aux = "will"
            other_aux = ["have", "been"]

        elif tense == Tense.FUTURE_PERFECT_CONTINUOUS:
            first_aux = "will"
            other_aux = ["have", "been", "being"]

    return VerbConjugation(
        first_auxiliary=first_aux,
        other_auxiliaries=other_aux,
        main_verb=main_v,
        is_negated=is_neg,
    )
