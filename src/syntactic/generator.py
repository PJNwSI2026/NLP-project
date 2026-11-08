"""Sentence generator engine.
Implements SVO, SV, and SVO-reflexive sentence construction across all 12 tenses,
5 moods, and active/passive voices with full morphological agreement.
"""

from dataclasses import dataclass, field
import random
from typing import Any, Dict, List, Optional, Tuple

from .grammar import (
    Mood,
    NounPhrase,
    Tense,
    VerbConjugation,
    Voice,
    conjugate_verb_phrase,
)
from .lexicon import (
    ADJECTIVES,
    Adjective,
    DETERMINERS,
    Determiner,
    DeterminerType,
    Gender,
    NOUNS,
    Noun,
    PRONOUNS,
    PersonalPronoun,
    VERBS,
    Verb,
    VerbType,
)
from .morphology import get_reflexive_pronoun


@dataclass
class GeneratedSentence:
    """Encapsulates a fully generated sentence and its grammatical metadata."""
    text: str
    tense: Tense
    mood: Mood
    voice: Voice
    verb_type: VerbType
    verb_base: str
    subject_str: str
    predicate_str: str
    object_str: Optional[str]
    agent_str: Optional[str]
    syntax_tree: str
    subject_np: Optional[NounPhrase] = None
    object_np: Optional[NounPhrase] = None
    verb_obj: Optional[Verb] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SentenceGenerator:
    """Syntactic sentence generator supporting parameterized and random generation."""

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def random_noun_phrase(
        self,
        allow_pronoun: bool = True,
        force_pronoun: bool = False,
        include_adjective: bool = True,
        max_adjectives: int = 1,
    ) -> NounPhrase:
        """Constructs a grammatically valid random Noun Phrase."""
        if force_pronoun or (allow_pronoun and random.random() < 0.25):
            pronoun = random.choice(PRONOUNS)
            return NounPhrase(is_pronoun=True, pronoun=pronoun)

        noun = random.choice(NOUNS)
        is_plural = random.choice([False, True]) if noun.countable else False

        # Select compatible determiner
        compatible_dets = []
        for det in DETERMINERS:
            # Check number compatibility
            word = det.plural_word if is_plural else det.singular_word
            if word is None and det.determiner_type != DeterminerType.ARTICLE:
                continue
            if not noun.countable and not det.allows_uncountable:
                continue
            if is_plural and word is None and det.singular_word is not None:
                continue
            compatible_dets.append(det)

        # For singular countable nouns, a determiner is obligatory in standard English
        if noun.countable and not is_plural:
            compatible_dets = [d for d in compatible_dets if d.singular_word is not None]

        determiner = random.choice(compatible_dets) if compatible_dets else None

        # Select adjectives
        adjectives: List[Adjective] = []
        if include_adjective and random.random() < 0.6:
            k = min(max_adjectives, len(ADJECTIVES))
            adjectives = random.sample(ADJECTIVES, random.randint(1, k))

        return NounPhrase(
            is_pronoun=False,
            determiner=determiner,
            adjectives=adjectives,
            noun=noun,
            is_plural=is_plural,
        )

    def create_noun_phrase(
        self,
        noun: Optional[Noun] = None,
        pronoun: Optional[PersonalPronoun] = None,
        determiner: Optional[Determiner] = None,
        adjectives: Optional[List[Adjective]] = None,
        is_plural: bool = False,
        include_adjectives: bool = True,
    ) -> NounPhrase:
        """Constructs a specific Noun Phrase with the given noun or pronoun.
        
        Ensures proper determiner assignment for singular countable nouns.
        """
        if pronoun is not None:
            return NounPhrase(is_pronoun=True, pronoun=pronoun)

        if noun is None:
            return self.random_noun_phrase(allow_pronoun=False, include_adjective=include_adjectives)

        if not noun.countable:
            is_plural = False

        if determiner is None:
            compatible_dets = []
            for det in DETERMINERS:
                word = det.plural_word if is_plural else det.singular_word
                if word is None and det.determiner_type != DeterminerType.ARTICLE:
                    continue
                if not noun.countable and not det.allows_uncountable:
                    continue
                if is_plural and word is None and det.singular_word is not None:
                    continue
                compatible_dets.append(det)

            if noun.countable and not is_plural:
                compatible_dets = [d for d in compatible_dets if d.singular_word is not None]

            determiner = random.choice(compatible_dets) if compatible_dets else DETERMINERS[0]

        adj_list: List[Adjective] = []
        if adjectives is not None:
            adj_list = list(adjectives)
        elif include_adjectives and random.random() < 0.4:
            adj_list = [random.choice(ADJECTIVES)]

        return NounPhrase(
            is_pronoun=False,
            determiner=determiner,
            adjectives=adj_list,
            noun=noun,
            is_plural=is_plural,
        )

    def generate(
        self,
        tense: Optional[Tense] = None,
        mood: Optional[Mood] = None,
        voice: Optional[Voice] = None,
        verb: Optional[Verb] = None,
        verb_type: Optional[VerbType] = None,
        subject: Optional[NounPhrase] = None,
        direct_object: Optional[NounPhrase] = None,
        include_adjectives: bool = True,
    ) -> GeneratedSentence:
        """Generates a sentence with specified or random grammatical features."""
        # 1. Resolve verb and verb type
        if verb is None:
            candidates = VERBS
            if verb_type is not None:
                candidates = [v for v in VERBS if v.verb_type == verb_type]
            verb = random.choice(candidates)
        actual_verb_type = verb.verb_type

        # 2. Resolve Voice (Only TRANSITIVE verbs can be PASSIVE)
        if voice is None:
            if actual_verb_type == VerbType.TRANSITIVE:
                voice = random.choice([Voice.ACTIVE, Voice.PASSIVE])
            else:
                voice = Voice.ACTIVE
        else:
            if actual_verb_type != VerbType.TRANSITIVE and voice == Voice.PASSIVE:
                # Force active for intransitive/reflexive
                voice = Voice.ACTIVE

        # 3. Resolve Mood and Tense
        if mood is None:
            mood = random.choice(list(Mood))
        if tense is None:
            tense = random.choice(list(Tense))

        # 4. Resolve semantic participants
        orig_subject = subject or self.random_noun_phrase(include_adjective=include_adjectives)
        orig_object: Optional[NounPhrase] = None

        if actual_verb_type == VerbType.TRANSITIVE:
            orig_object = direct_object or self.random_noun_phrase(include_adjective=include_adjectives)

        # 5. Handle Active vs. Passive voice assignment
        agent_str: Optional[str] = None
        object_str: Optional[str] = None

        if voice == Voice.ACTIVE:
            grammatical_subject = orig_subject
            if actual_verb_type == VerbType.TRANSITIVE and orig_object is not None:
                object_str = orig_object.to_string(as_subject=False)
            elif actual_verb_type == VerbType.REFLEXIVE:
                # Direct object is reflexive pronoun agreeing with subject
                object_str = get_reflexive_pronoun(
                    grammatical_subject.person,
                    grammatical_subject.number_is_plural,
                    grammatical_subject.gender,
                )
            else:  # INTRANSITIVE
                object_str = None
        else:
            # PASSIVE VOICE:
            # The semantic object becomes the grammatical subject!
            # The semantic subject becomes the optional prepositional agent (by + agent)
            assert orig_object is not None
            grammatical_subject = orig_object
            agent_str = f"by {orig_subject.to_string(as_subject=False)}"
            object_str = None

        # 6. Verb conjugation
        person = grammatical_subject.person
        is_plural = grammatical_subject.number_is_plural

        conjugation = conjugate_verb_phrase(
            verb=verb,
            person=person,
            is_plural=is_plural,
            tense=tense,
            mood=mood,
            voice=voice,
        )

        # 7. Construct sentence tokens based on Mood
        tokens: List[str] = []
        subject_str = grammatical_subject.to_string(as_subject=True)
        predicate_tokens: List[str] = []

        if mood == Mood.IMPERATIVE:
            # Subject is omitted in imperative
            if voice == Voice.PASSIVE:
                predicate_tokens = ["be", conjugation.main_verb]
                if conjugation.is_negated:
                    tokens.append("Do not")
                tokens.extend(predicate_tokens)
                if agent_str:
                    tokens.append(agent_str)
            else:
                if conjugation.is_negated:
                    tokens.append("Do not")
                tokens.append(conjugation.main_verb)
                predicate_tokens.append(conjugation.main_verb)
                if object_str:
                    tokens.append(object_str)

            final_text = " ".join(tokens).strip() + "!"

        elif mood == Mood.INTERROGATIVE:
            # Auxiliary inversion: [Aux1] + [Subject] + [Other Aux] + [Main V] + [Obj/Agent]?
            first_aux = conjugation.first_auxiliary or "do"
            tokens.append(first_aux)
            tokens.append(subject_str)
            if conjugation.is_negated:
                tokens.append("not")
            tokens.extend(conjugation.other_auxiliaries)
            tokens.append(conjugation.main_verb)

            predicate_tokens = [first_aux] + conjugation.other_auxiliaries + [conjugation.main_verb]

            if object_str:
                tokens.append(object_str)
            if agent_str:
                tokens.append(agent_str)

            final_text = " ".join(tokens).strip() + "?"

        else:  # INDICATIVE, NEGATIVE, CONDITIONAL
            # Standard order: [Subject] + [Predicate] + [Object / Agent].
            tokens.append(subject_str)
            if conjugation.first_auxiliary:
                tokens.append(conjugation.first_auxiliary)
                predicate_tokens.append(conjugation.first_auxiliary)
                if conjugation.is_negated:
                    tokens.append("not")
                    predicate_tokens.append("not")
                tokens.extend(conjugation.other_auxiliaries)
                predicate_tokens.extend(conjugation.other_auxiliaries)
            else:
                if conjugation.is_negated:
                    # Should have auxiliary (handled in conjugation), fallback:
                    tokens.append("does not" if (person == 3 and not is_plural) else "do not")
                    predicate_tokens.append("do not")
            tokens.append(conjugation.main_verb)
            predicate_tokens.append(conjugation.main_verb)

            if object_str:
                tokens.append(object_str)
            if agent_str:
                tokens.append(agent_str)

            final_text = " ".join(tokens).strip() + "."

        # Capitalize first character of final text
        if final_text:
            final_text = final_text[0].upper() + final_text[1:]

        # 8. Build Syntax Tree string representation
        syntax_tree = self._build_syntax_tree(
            mood=mood,
            voice=voice,
            subject_str=subject_str,
            predicate_tokens=predicate_tokens,
            object_str=object_str,
            agent_str=agent_str,
            verb_type=actual_verb_type,
        )

        return GeneratedSentence(
            text=final_text,
            tense=tense,
            mood=mood,
            voice=voice,
            verb_type=actual_verb_type,
            verb_base=verb.base,
            subject_str=subject_str if mood != Mood.IMPERATIVE else "(you - implicit)",
            predicate_str=" ".join(predicate_tokens),
            object_str=object_str,
            agent_str=agent_str,
            syntax_tree=syntax_tree,
            subject_np=orig_subject,
            object_np=orig_object,
            verb_obj=verb,
            metadata={
                "person": person,
                "is_plural": is_plural,
                "is_negated": conjugation.is_negated,
                "first_auxiliary": conjugation.first_auxiliary,
            },
        )

    def _build_syntax_tree(
        self,
        mood: Mood,
        voice: Voice,
        subject_str: str,
        predicate_tokens: List[str],
        object_str: Optional[str],
        agent_str: Optional[str],
        verb_type: VerbType,
    ) -> str:
        """Creates a formatted ASCII constituent syntax tree."""
        lines = ["[S"]
        if mood != Mood.IMPERATIVE:
            lines.append(f"  ├── [NP (Subject): \"{subject_str}\"]")
        else:
            lines.append("  ├── [NP (Subject): (implicit \"you\")]")

        pred_formatted = " ".join(predicate_tokens)
        lines.append(f"  └── [VP (Predicate): \"{pred_formatted}\"")

        if object_str:
            role_label = "Reflexive Object" if verb_type == VerbType.REFLEXIVE else "Direct Object"
            lines.append(f"        ├── [NP ({role_label}): \"{object_str}\"]")

        if agent_str:
            lines.append(f"        ├── [PP (Agent by-phrase): \"{agent_str}\"]")

        lines.append("      ]")
        lines.append("]")
        return "\n".join(lines)

    def generate_tense_matrix_for_pair(
        self,
        subject: NounPhrase,
        verb: Verb,
        direct_object: Optional[NounPhrase] = None,
        mood: Mood = Mood.INDICATIVE,
        voice: Voice = Voice.ACTIVE,
    ) -> List[GeneratedSentence]:
        """Generates all 12 tenses for the exact same subject, verb, and object."""
        sentences = []
        for tense in Tense:
            s = self.generate(
                tense=tense,
                mood=mood,
                voice=voice,
                verb=verb,
                subject=subject,
                direct_object=direct_object,
            )
            sentences.append(s)
        return sentences
