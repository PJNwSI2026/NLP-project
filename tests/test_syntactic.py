"""Comprehensive test suite for the syntactic analysis module.
Tests lexicon sizes, morphological agreement, 12 tenses, 5 moods, voices,
reflexives, intransitives, and GUI subject/object binding behavior.
"""

import pytest

from src.syntactic.generator import SentenceGenerator
from src.syntactic.grammar import Mood, NounPhrase, Tense, Voice
from src.syntactic.lexicon import (
    ADJECTIVES,
    DETERMINERS,
    NOUNS,
    PRONOUNS,
    VERBS,
    Noun,
    VerbType,
)
from src.syntactic.morphology import choose_indefinite_article, get_reflexive_pronoun


# ============================================================================
# 1. LEXICON REQUIREMENTS TESTS (From _wymogi.docx)
# ============================================================================
def test_lexicon_minimum_sizes():
    """Verify that nouns, verbs, and adjectives meet or exceed the >= 100 requirement."""
    assert len(NOUNS) >= 100, f"Expected >= 100 nouns, got {len(NOUNS)}"
    assert len(VERBS) >= 100, f"Expected >= 100 verbs, got {len(VERBS)}"
    assert len(ADJECTIVES) >= 100, f"Expected >= 100 adjectives, got {len(ADJECTIVES)}"


def test_verb_categories_represented():
    """Verify presence of transitive, intransitive, and reflexive verbs."""
    transitive = [v for v in VERBS if v.verb_type == VerbType.TRANSITIVE]
    intransitive = [v for v in VERBS if v.verb_type == VerbType.INTRANSITIVE]
    reflexive = [v for v in VERBS if v.verb_type == VerbType.REFLEXIVE]

    assert len(transitive) >= 50, "Expected at least 50 transitive verbs"
    assert len(intransitive) >= 10, "Expected at least 10 intransitive verbs"
    assert len(reflexive) >= 5, "Expected at least 5 reflexive verbs"


# ============================================================================
# 2. SPECIFIC NOUN / PRONOUN SELECTION TESTS (Direct user bug check)
# ============================================================================
def test_specific_subject_actor_is_respected():
    """Test that choosing 'actor' as subject produces a sentence containing 'actor'."""
    generator = SentenceGenerator(seed=42)
    actor_noun = next(n for n in NOUNS if n.singular == "actor")
    attack_verb = next(v for v in VERBS if v.base == "attack")

    subj_np = generator.create_noun_phrase(noun=actor_noun, include_adjectives=False)

    sentence = generator.generate(
        tense=Tense.PRESENT_SIMPLE,
        mood=Mood.INDICATIVE,
        voice=Voice.ACTIVE,
        verb=attack_verb,
        subject=subj_np,
    )

    assert "actor" in sentence.text.lower(), f"Expected 'actor' in sentence: {sentence.text}"
    assert "it attacks it" not in sentence.text.lower()
    assert "actor" in sentence.subject_str.lower()


def test_gui_subject_priority_over_stale_pronoun_type():
    """Simulates GUI parameter resolution when user picks specific noun 'actor'
    even if subj_type_var happened to be set to 'Personal Pronoun'.
    """
    generator = SentenceGenerator(seed=123)

    # Simulated GUI variables
    specific_subj_noun = "actor"
    subj_type_choice = "Personal Pronoun (Zaimek osobowy)"  # stale dropdown choice!

    # Resolution logic as implemented in gui.py:
    if specific_subj_noun != "(Random / Dowolny)":
        n = next(n for n in NOUNS if n.singular == specific_subj_noun)
        subject = generator.create_noun_phrase(noun=n, include_adjectives=False)
    else:
        subject = generator.random_noun_phrase(force_pronoun=True)

    attack_verb = next(v for v in VERBS if v.base == "attack")
    sentence = generator.generate(
        tense=Tense.PRESENT_SIMPLE,
        mood=Mood.INDICATIVE,
        voice=Voice.ACTIVE,
        verb=attack_verb,
        subject=subject,
    )

    assert "actor" in sentence.text.lower()
    assert not sentence.text.startswith("It attacks")


def test_specific_object_selection():
    """Test that specifying an object noun produces a sentence with that object."""
    generator = SentenceGenerator(seed=99)
    verb_eat = next(v for v in VERBS if v.base == "eat")
    noun_pizza = next(n for n in NOUNS if n.singular == "pizza")

    obj_np = generator.create_noun_phrase(noun=noun_pizza, include_adjectives=False)
    sent = generator.generate(
        tense=Tense.PRESENT_SIMPLE,
        mood=Mood.INDICATIVE,
        voice=Voice.ACTIVE,
        verb=verb_eat,
        direct_object=obj_np,
    )

    assert "pizza" in sent.text.lower()


def test_12_tenses_matrix_preserves_exact_sentence_participants():
    """Verify that generating 12-tense matrix preserves the EXACT subject and object of the sentence."""
    generator = SentenceGenerator(seed=777)
    original_sentence = generator.generate()

    # Generate matrix for this exact sentence
    matrix = generator.generate_tense_matrix_for_pair(
        subject=original_sentence.subject_np,
        verb=original_sentence.verb_obj,
        direct_object=original_sentence.object_np,
        voice=original_sentence.voice,
        mood=original_sentence.mood if original_sentence.mood != Mood.IMPERATIVE else Mood.INDICATIVE,
    )

    assert len(matrix) == 12

    # Verify every sentence in the 12-tense matrix contains the exact same subject
    # and object participants
    expected_subj = original_sentence.subject_np.to_string(as_subject=True)
    for s in matrix:
        assert s.subject_np.to_string(as_subject=True) == expected_subj
        if original_sentence.object_np:
            assert s.object_np.to_string(as_subject=False) == original_sentence.object_np.to_string(as_subject=False)



# ============================================================================
# 3. 12 TENSES AND VOICES TESTS
# ============================================================================
@pytest.mark.parametrize("tense", list(Tense))
def test_all_12_tenses_active(tense):
    """Ensure all 12 tenses produce valid non-empty active sentences."""
    generator = SentenceGenerator(seed=1)
    verb = next(v for v in VERBS if v.base == "read")
    noun_student = next(n for n in NOUNS if n.singular == "student")
    noun_book = next(n for n in NOUNS if n.singular == "book")

    s = generator.generate(
        tense=tense,
        mood=Mood.INDICATIVE,
        voice=Voice.ACTIVE,
        verb=verb,
        subject=generator.create_noun_phrase(noun=noun_student, include_adjectives=False),
        direct_object=generator.create_noun_phrase(noun=noun_book, include_adjectives=False),
    )

    assert s.text.endswith(".")
    assert s.text[0].isupper()
    assert "read" in s.text.lower()
    assert len(s.text.split()) >= 3


@pytest.mark.parametrize("tense", list(Tense))
def test_all_12_tenses_passive(tense):
    """Ensure all 12 tenses produce valid passive sentences."""
    generator = SentenceGenerator(seed=2)
    verb = next(v for v in VERBS if v.base == "write")
    noun_student = next(n for n in NOUNS if n.singular == "student")
    noun_letter = next(n for n in NOUNS if n.singular == "letter")

    s = generator.generate(
        tense=tense,
        mood=Mood.INDICATIVE,
        voice=Voice.PASSIVE,
        verb=verb,
        subject=generator.create_noun_phrase(noun=noun_student, include_adjectives=False),
        direct_object=generator.create_noun_phrase(noun=noun_letter, include_adjectives=False),
    )

    assert s.text.endswith(".")
    assert "written" in s.text.lower()  # V3 participle
    assert "by" in s.text.lower()


# ============================================================================
# 4. MOODS TESTS
# ============================================================================
def test_interrogative_mood_structure():
    """Verify interrogative sentences end with '?' and have auxiliary inversion."""
    generator = SentenceGenerator(seed=10)
    verb = next(v for v in VERBS if v.base == "see")

    s = generator.generate(
        tense=Tense.PRESENT_SIMPLE,
        mood=Mood.INTERROGATIVE,
        voice=Voice.ACTIVE,
        verb=verb,
    )

    assert s.text.endswith("?")
    first_word = s.text.split()[0].lower()
    assert first_word in ("do", "does", "did", "is", "are", "have", "has", "will")


def test_negative_mood_structure():
    """Verify negative sentences contain negation marker 'not'."""
    generator = SentenceGenerator(seed=11)
    s = generator.generate(mood=Mood.NEGATIVE, voice=Voice.ACTIVE)
    assert "not" in s.text.lower()
    assert s.text.endswith(".")


def test_imperative_mood_structure():
    """Verify imperative sentences end with '!' and omit explicit subject."""
    generator = SentenceGenerator(seed=12)
    verb = next(v for v in VERBS if v.base == "clean")

    s = generator.generate(
        mood=Mood.IMPERATIVE,
        voice=Voice.ACTIVE,
        verb=verb,
    )

    assert s.text.endswith("!")
    assert s.subject_str == "(you - implicit)"


def test_conditional_mood_structure():
    """Verify conditional sentences use modal 'would'."""
    generator = SentenceGenerator(seed=13)
    s = generator.generate(mood=Mood.CONDITIONAL, voice=Voice.ACTIVE)
    assert "would" in s.text.lower()


# ============================================================================
# 5. REFLEXIVE & INTRANSITIVE TESTS
# ============================================================================
def test_reflexive_verb_pronoun_agreement():
    """Test reflexive verbs have matching reflexive pronouns for all persons."""
    generator = SentenceGenerator(seed=20)
    verb_prep = next(v for v in VERBS if v.base == "prepare")

    for pron in PRONOUNS:
        subj = NounPhrase(is_pronoun=True, pronoun=pron)
        s = generator.generate(
            tense=Tense.PAST_SIMPLE,
            mood=Mood.INDICATIVE,
            voice=Voice.ACTIVE,
            verb=verb_prep,
            subject=subj,
        )
        assert pron.reflexive in s.text.lower(), f"Expected '{pron.reflexive}' for '{pron.subject}' in '{s.text}'"


def test_intransitive_verb_no_object():
    """Test intransitive verbs do not accept direct objects and form SV sentences."""
    generator = SentenceGenerator(seed=25)
    verb_sleep = next(v for v in VERBS if v.base == "sleep")

    s = generator.generate(
        tense=Tense.PRESENT_SIMPLE,
        mood=Mood.INDICATIVE,
        voice=Voice.ACTIVE,
        verb=verb_sleep,
    )

    assert s.object_str is None
    assert s.agent_str is None


# ============================================================================
# 6. PHONETIC ARTICLE AGREEMENT (a vs. an)
# ============================================================================
@pytest.mark.parametrize(
    "word, starts_vowel, expected",
    [
        ("actor", True, "an"),
        ("apple", True, "an"),
        ("honest", True, "an"),
        ("elephant", True, "an"),
        ("orange", True, "an"),
        ("boy", False, "a"),
        ("teacher", False, "a"),
        ("car", False, "a"),
        ("dog", False, "a"),
    ],
)
def test_indefinite_article_selection(word, starts_vowel, expected):
    article = choose_indefinite_article(word, starts_vowel)
    assert article == expected
