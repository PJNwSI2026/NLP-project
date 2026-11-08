"""Corpus processing and Verb-Object (VO) co-occurrence extraction.
Processes English corpora (NLTK Gutenberg, Brown, and Reuters) with POS tagging and lemmatization.
"""

from collections import Counter, defaultdict
import os
import re
from typing import Dict, List, Optional, Set, Tuple

import nltk
from nltk.corpus import brown, gutenberg
from nltk.stem import WordNetLemmatizer

from .vocabulary import NOUNS, TRANSITIVE_VERBS


class VOCorpusExtractor:
    """Extracts (Verb, Object) pairs from English text corpora."""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.verbs_set: Set[str] = set(TRANSITIVE_VERBS)
        self.nouns_set: Set[str] = set(NOUNS)

        # Ensure required NLTK resources
        for pkg in ["punkt", "punkt_tab", "averaged_perceptron_tagger_eng", "wordnet"]:
            try:
                nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"taggers/{pkg}" if "tagger" in pkg else f"corpora/{pkg}")
            except LookupError:
                nltk.download(pkg, quiet=True)

    def extract_vo_from_tagged_sentence(
        self, tagged_sent: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """Extracts (transitive_verb, direct_object_noun) pairs from a POS-tagged sentence.
        
        Syntactic pattern for English direct object:
        VERB (VB*) + [optional adverbs/particles] + [optional determiners DT/PRP$] + [optional adjectives JJ*] + NOUN (NN*)
        """
        pairs: List[Tuple[str, str]] = []
        n = len(tagged_sent)

        for i, (word, tag) in enumerate(tagged_sent):
            # Check if current word is a verb
            if not tag.startswith("VB"):
                continue

            verb_lemma = self.lemmatizer.lemmatize(word.lower(), pos="v")
            if verb_lemma not in self.verbs_set:
                continue

            # Lookahead window for direct object (up to 4 tokens following verb)
            j = i + 1
            # Skip optional adverbs or particles (e.g. "eat quickly the apple", "pick up the book")
            while j < n and j <= i + 4 and tagged_sent[j][1] in ("RB", "RBR", "RBS", "RP", "IN"):
                # If preposition 'by', 'of', etc., stop if not direct object
                if tagged_sent[j][1] == "IN" and tagged_sent[j][0].lower() in ("to", "from", "with", "at", "by", "for", "in", "on"):
                    break
                j += 1

            # Skip determiners (DT, PRP$)
            while j < n and j <= i + 5 and tagged_sent[j][1] in ("DT", "PRP$", "CD", "PDT"):
                j += 1

            # Skip adjectives (JJ, JJR, JJS)
            while j < n and j <= i + 6 and tagged_sent[j][1].startswith("JJ"):
                j += 1

            # Target direct object noun (NN, NNS, NNP)
            if j < n and tagged_sent[j][1].startswith("NN"):
                raw_noun = tagged_sent[j][0].lower()
                noun_lemma = self.lemmatizer.lemmatize(raw_noun, pos="n")
                if noun_lemma in self.nouns_set:
                    pairs.append((verb_lemma, noun_lemma))

        return pairs

    def extract_from_nltk_corpora(
        self, max_sentences: Optional[int] = None
    ) -> Counter:
        """Extracts VO pairs from combined Gutenberg and Brown corpora."""
        counts = Counter()
        lemmatize_v = lambda w: self.lemmatizer.lemmatize(w.lower(), pos="v")
        lemmatize_n = lambda w: self.lemmatizer.lemmatize(w.lower(), pos="n")

        print("Processing Brown corpus...")
        try:
            brown_tagged = brown.tagged_sents()
            total_b = len(brown_tagged) if max_sentences is None else min(max_sentences, len(brown_tagged))
            for sent in brown_tagged[:total_b]:
                pairs = self.extract_vo_from_tagged_sentence(sent)
                for v, n in pairs:
                    counts[(v, n)] += 1
        except Exception as e:
            print(f"Warning: Could not process Brown tagged sents: {e}")

        print("Processing Gutenberg corpus...")
        try:
            gutenberg_sents = gutenberg.sents()
            total_g = len(gutenberg_sents) if max_sentences is None else min(max_sentences, len(gutenberg_sents))
            # Tag in batches for efficiency
            for sent in gutenberg_sents[:total_g]:
                tagged = nltk.pos_tag(sent)
                pairs = self.extract_vo_from_tagged_sentence(tagged)
                for v, n in pairs:
                    counts[(v, n)] += 1
        except Exception as e:
            print(f"Warning: Could not process Gutenberg sents: {e}")

        return counts

