"""Morphological helpers for noun and verb inflection and phonological agreement.
"""

from typing import Optional
from .lexicon import (
    Gender,
    Noun,
    PersonalPronoun,
    PRONOUNS,
)


def choose_indefinite_article(following_word: str, starts_with_vowel_sound: Optional[bool] = None) -> str:
    """Returns 'a' or 'an' based on the phonological onset of the following word.
    
    If starts_with_vowel_sound is provided, it takes precedence.
    Otherwise, applies standard English phonetic heuristics.
    """
    if starts_with_vowel_sound is not None:
        return "an" if starts_with_vowel_sound else "a"
    
    clean_word = following_word.strip().lower()
    if not clean_word:
        return "a"
    
    # Common special cases
    if clean_word.startswith(("honest", "hour", "honor", "heir")):
        return "an"
    if clean_word.startswith(("uniform", "university", "unique", "union", "useful", "european", "one", "once")):
        return "a"
    
    # General rule: initial vowel letter
    if clean_word[0] in "aeiou":
        return "an"
    return "a"


def get_reflexive_pronoun(person: int, is_plural: bool, gender: Gender = Gender.NEUTER) -> str:
    """Returns the appropriate reflexive pronoun for given grammatical person, number and gender."""
    if person == 1:
        return "ourselves" if is_plural else "myself"
    elif person == 2:
        return "yourselves" if is_plural else "yourself"
    else:  # person == 3
        if is_plural:
            return "themselves"
        if gender == Gender.MASCULINE:
            return "himself"
        elif gender == Gender.FEMININE:
            return "herself"
        else:
            return "itself"


def get_subject_pronoun_by_features(person: int, is_plural: bool, gender: Gender = Gender.NEUTER) -> PersonalPronoun:
    """Finds a personal pronoun matching the specified features."""
    for p in PRONOUNS:
        if p.person == person and p.is_plural == is_plural:
            if person == 3 and not is_plural:
                if p.gender == gender:
                    return p
            else:
                return p
    return PRONOUNS[0]
