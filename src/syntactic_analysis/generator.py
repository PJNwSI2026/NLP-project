import random
from grammar import Tense, Mood, Voice, NounPhrase, conjugate
from lexicon import PRONOUNS, NOUNS, ADJECTIVES, DETERMINERS, VERBS, VerbType, Verb


class SentenceGenerator:
    def random_np(self, force_noun: bool = False, force_pronoun: bool = False) -> NounPhrase:
        if force_pronoun or (not force_noun and random.random() < 0.3):
            return NounPhrase(is_pronoun=True, pronoun=random.choice(PRONOUNS))

        noun = random.choice(NOUNS)
        is_pl = random.choice([True, False]) if noun.countable else False

        dets = [d for d in DETERMINERS if (not is_pl or d.word_pl != "") and (noun.countable or d.allows_uncountable)]
        if noun.countable and not is_pl: dets = [d for d in dets if d.word_sg != ""]

        det = random.choice(dets) if dets else DETERMINERS[0]
        adj = random.choice(ADJECTIVES) if random.random() < 0.5 else None
        return NounPhrase(is_pronoun=False, determiner=det, adjective=adj, noun=noun, is_plural=is_pl)

    def generate(self) -> str:
        verb = random.choice(VERBS)
        t = random.choice(list(Tense))
        m = random.choice(list(Mood))
        v = random.choice([Voice.ACTIVE, Voice.PASSIVE]) if verb.verb_type == VerbType.TRANSITIVE else Voice.ACTIVE

        subj = self.random_np()
        obj = self.random_np() if verb.verb_type == VerbType.TRANSITIVE else None

        obj_str, agent_str = "", ""
        if v == Voice.ACTIVE:
            gram_subj = subj
            if obj: obj_str = obj.to_string(as_subject=False)
            elif verb.verb_type == VerbType.REFLEXIVE:
                obj_str = subj.pronoun.reflexive if subj.is_pronoun else PRONOUNS[6].reflexive if subj.is_pl else PRONOUNS[4].reflexive
        else:
            gram_subj = obj
            agent_str = f"by {subj.to_string(as_subject=False)}"

        vp = conjugate(verb, gram_subj.person, gram_subj.is_pl, t, m, v)
        subj_str = gram_subj.to_string(as_subject=True)
        tokens = []

        if m == Mood.IMPERATIVE:
            if vp.is_negated: tokens.extend(["Do", "not"])
            tokens.extend(vp.aux_other + [vp.main_v, obj_str, agent_str])
            return " ".join(filter(None, tokens)).capitalize() + "!"

        elif m == Mood.INTERROGATIVE:
            tokens.extend([vp.aux1 or "do", subj_str, "not" if vp.is_negated else "", *vp.aux_other, vp.main_v, obj_str, agent_str])
            return " ".join(filter(None, tokens)).capitalize() + "?"

        else:
            tokens.append(subj_str)
            if vp.aux1: tokens.extend([vp.aux1, "not" if vp.is_negated else "", *vp.aux_other])
            elif vp.is_negated: tokens.extend(["does" if (gram_subj.person == 3 and not gram_subj.is_pl) else "do", "not"])
            tokens.extend([vp.main_v, obj_str, agent_str])
            return " ".join(filter(None, tokens)).capitalize() + "."
