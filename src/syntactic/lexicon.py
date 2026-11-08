"""Lexicon containing nouns, verbs, adjectives, pronouns, and determiners.
Guarantees >= 100 nouns, >= 100 verbs, >= 100 adjectives.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class VerbType(str, Enum):
    TRANSITIVE = "transitive"      # Takes direct object (SVO)
    INTRANSITIVE = "intransitive"  # No direct object (SV)
    REFLEXIVE = "reflexive"        # Reflexive action (S + V + Reflexive Pronoun)


class Gender(str, Enum):
    MASCULINE = "he"
    FEMININE = "she"
    NEUTER = "it"


@dataclass(frozen=True)
class Noun:
    singular: str
    plural: str
    countable: bool = True
    gender: Gender = Gender.NEUTER
    starts_with_vowel_sound: bool = False


@dataclass(frozen=True)
class Verb:
    base: str         # V1 (infinitive/base)
    past: str         # V2 (past simple)
    participle: str   # V3 (past participle)
    third_sing: str   # 3rd person singular present (e.g., writes)
    gerund: str       # Present participle / -ing (e.g., writing)
    verb_type: VerbType = VerbType.TRANSITIVE


@dataclass(frozen=True)
class Adjective:
    word: str
    starts_with_vowel_sound: bool = False


# ============================================================================
# 1. NOUNS (At least 120 nouns with singular, plural, countability, gender)
# ============================================================================
NOUNS: List[Noun] = [
    # People / Roles (masculine / feminine / neutral)
    Noun("boy", "boys", gender=Gender.MASCULINE),
    Noun("girl", "girls", gender=Gender.FEMININE),
    Noun("man", "men", gender=Gender.MASCULINE),
    Noun("woman", "women", gender=Gender.FEMININE),
    Noun("teacher", "teachers", gender=Gender.MASCULINE),
    Noun("doctor", "doctors", gender=Gender.FEMININE),
    Noun("student", "students", gender=Gender.MASCULINE),
    Noun("king", "kings", gender=Gender.MASCULINE),
    Noun("queen", "queens", gender=Gender.FEMININE),
    Noun("artist", "artists", gender=Gender.FEMININE, starts_with_vowel_sound=True),
    Noun("engineer", "engineers", gender=Gender.MASCULINE, starts_with_vowel_sound=True),
    Noun("actor", "actors", gender=Gender.MASCULINE, starts_with_vowel_sound=True),
    Noun("actress", "actresses", gender=Gender.FEMININE, starts_with_vowel_sound=True),
    Noun("child", "children", gender=Gender.MASCULINE),
    Noun("driver", "drivers", gender=Gender.MASCULINE),
    Noun("writer", "writers", gender=Gender.FEMININE),
    Noun("singer", "singers", gender=Gender.FEMININE),
    Noun("soldier", "soldiers", gender=Gender.MASCULINE),
    Noun("scientist", "scientists", gender=Gender.MASCULINE),
    Noun("chef", "chefs", gender=Gender.FEMININE),
    Noun("pilot", "pilots", gender=Gender.MASCULINE),
    Noun("farmer", "farmers", gender=Gender.MASCULINE),
    Noun("baker", "bakers", gender=Gender.FEMININE),
    Noun("detective", "detectives", gender=Gender.MASCULINE),
    Noun("officer", "officers", gender=Gender.MASCULINE, starts_with_vowel_sound=True),

    # Animals
    Noun("dog", "dogs"),
    Noun("cat", "cats"),
    Noun("horse", "horses"),
    Noun("bird", "birds"),
    Noun("lion", "lions"),
    Noun("tiger", "tigers"),
    Noun("elephant", "elephants", starts_with_vowel_sound=True),
    Noun("wolf", "wolves"),
    Noun("fox", "foxes"),
    Noun("bear", "bears"),
    Noun("rabbit", "rabbits"),
    Noun("monkey", "monkeys"),
    Noun("eagle", "eagles", starts_with_vowel_sound=True),
    Noun("dolphin", "dolphins"),
    Noun("whale", "whales"),
    Noun("owl", "owls", starts_with_vowel_sound=True),
    Noun("snake", "snakes"),
    Noun("deer", "deer"),
    Noun("duck", "ducks"),
    Noun("sheep", "sheep"),

    # Food and Drinks
    Noun("apple", "apples", starts_with_vowel_sound=True),
    Noun("bread", "bread", countable=False),
    Noun("cake", "cakes"),
    Noun("cheese", "cheese", countable=False),
    Noun("coffee", "coffee", countable=False),
    Noun("egg", "eggs", starts_with_vowel_sound=True),
    Noun("fish", "fish"),
    Noun("fruit", "fruits"),
    Noun("milk", "milk", countable=False),
    Noun("meat", "meat", countable=False),
    Noun("orange", "oranges", starts_with_vowel_sound=True),
    Noun("pizza", "pizzas"),
    Noun("rice", "rice", countable=False),
    Noun("soup", "soups"),
    Noun("tea", "tea", countable=False),
    Noun("water", "water", countable=False),
    Noun("wine", "wine", countable=False),
    Noun("sandwich", "sandwiches"),
    Noun("cookie", "cookies"),
    Noun("banana", "bananas"),

    # Vehicles and Transport
    Noun("car", "cars"),
    Noun("bicycle", "bicycles"),
    Noun("bus", "buses"),
    Noun("train", "trains"),
    Noun("plane", "planes"),
    Noun("boat", "boats"),
    Noun("ship", "ships"),
    Noun("truck", "trucks"),
    Noun("motorcycle", "motorcycles"),
    Noun("helicopter", "helicopters"),

    # Objects / Tools / Technology
    Noun("book", "books"),
    Noun("computer", "computers"),
    Noun("phone", "phones"),
    Noun("letter", "letters"),
    Noun("pen", "pens"),
    Noun("pencil", "pencils"),
    Noun("camera", "cameras"),
    Noun("guitar", "guitars"),
    Noun("piano", "pianos"),
    Noun("clock", "clocks"),
    Noun("key", "keys"),
    Noun("knife", "knives"),
    Noun("mirror", "mirrors"),
    Noun("hammer", "hammers"),
    Noun("lamp", "lamps"),
    Noun("radio", "radios"),
    Noun("telescope", "telescopes"),
    Noun("sword", "swords"),
    Noun("bottle", "bottles"),
    Noun("bell", "bells"),

    # Buildings / Places / Nature
    Noun("house", "houses"),
    Noun("castle", "castles"),
    Noun("bridge", "bridges"),
    Noun("school", "schools"),
    Noun("hospital", "hospitals"),
    Noun("library", "libraries"),
    Noun("museum", "museums"),
    Noun("forest", "forests"),
    Noun("mountain", "mountains"),
    Noun("river", "rivers"),
    Noun("lake", "lakes"),
    Noun("island", "islands", starts_with_vowel_sound=True),
    Noun("ocean", "oceans", starts_with_vowel_sound=True),
    Noun("garden", "gardens"),
    Noun("street", "streets"),
    Noun("room", "rooms"),
    Noun("door", "doors"),
    Noun("window", "windows"),
    Noun("wall", "walls"),
    Noun("gate", "gates"),

    # Clothes
    Noun("shirt", "shirts"),
    Noun("coat", "coats"),
    Noun("hat", "hats"),
    Noun("dress", "dresses"),
    Noun("shoe", "shoes"),
    Noun("jacket", "jackets"),
    Noun("scarf", "scarves"),
    Noun("glove", "gloves"),
    Noun("boot", "boots"),
    Noun("ring", "rings"),

    # Abstract / Communication / Other
    Noun("story", "stories"),
    Noun("song", "songs"),
    Noun("problem", "problems"),
    Noun("question", "questions"),
    Noun("idea", "ideas", starts_with_vowel_sound=True),
    Noun("secret", "secrets"),
    Noun("message", "messages"),
    Noun("lesson", "lessons"),
    Noun("project", "projects"),
    Noun("dream", "dreams"),
]


# ============================================================================
# 2. VERBS (At least 110 verbs: transitive, intransitive, reflexive)
# ============================================================================
VERBS: List[Verb] = [
    # --- TRANSITIVE VERBS (Takes Direct Object) ---
    Verb("read", "read", "read", "reads", "reading", VerbType.TRANSITIVE),
    Verb("write", "wrote", "written", "writes", "writing", VerbType.TRANSITIVE),
    Verb("eat", "ate", "eaten", "eats", "eating", VerbType.TRANSITIVE),
    Verb("drink", "drank", "drunk", "drinks", "drinking", VerbType.TRANSITIVE),
    Verb("drive", "drove", "driven", "drives", "driving", VerbType.TRANSITIVE),
    Verb("buy", "bought", "bought", "buys", "buying", VerbType.TRANSITIVE),
    Verb("sell", "sold", "sold", "sells", "selling", VerbType.TRANSITIVE),
    Verb("see", "saw", "seen", "sees", "seeing", VerbType.TRANSITIVE),
    Verb("hear", "heard", "heard", "hears", "hearing", VerbType.TRANSITIVE),
    Verb("find", "found", "found", "finds", "finding", VerbType.TRANSITIVE),
    Verb("lose", "lost", "lost", "loses", "losing", VerbType.TRANSITIVE),
    Verb("build", "built", "built", "builds", "building", VerbType.TRANSITIVE),
    Verb("destroy", "destroyed", "destroyed", "destroys", "destroying", VerbType.TRANSITIVE),
    Verb("open", "opened", "opened", "opens", "opening", VerbType.TRANSITIVE),
    Verb("close", "closed", "closed", "closes", "closing", VerbType.TRANSITIVE),
    Verb("cook", "cooked", "cooked", "cooks", "cooking", VerbType.TRANSITIVE),
    Verb("bake", "baked", "baked", "bakes", "baking", VerbType.TRANSITIVE),
    Verb("cut", "cut", "cut", "cuts", "cutting", VerbType.TRANSITIVE),
    Verb("clean", "cleaned", "cleaned", "cleans", "cleaning", VerbType.TRANSITIVE),
    Verb("wash", "washed", "washed", "washes", "washing", VerbType.TRANSITIVE),
    Verb("repair", "repaired", "repaired", "repairs", "repairing", VerbType.TRANSITIVE),
    Verb("paint", "painted", "painted", "paints", "painting", VerbType.TRANSITIVE),
    Verb("draw", "drew", "drawn", "draws", "drawing", VerbType.TRANSITIVE),
    Verb("sing", "sang", "sung", "sings", "singing", VerbType.TRANSITIVE),
    Verb("play", "played", "played", "plays", "playing", VerbType.TRANSITIVE),
    Verb("watch", "watched", "watched", "watches", "watching", VerbType.TRANSITIVE),
    Verb("wear", "wore", "worn", "wears", "wearing", VerbType.TRANSITIVE),
    Verb("carry", "carried", "carried", "carries", "carrying", VerbType.TRANSITIVE),
    Verb("hold", "held", "held", "holds", "holding", VerbType.TRANSITIVE),
    Verb("throw", "threw", "thrown", "throws", "throwing", VerbType.TRANSITIVE),
    Verb("catch", "caught", "caught", "catches", "catching", VerbType.TRANSITIVE),
    Verb("push", "pushed", "pushed", "pushes", "pushing", VerbType.TRANSITIVE),
    Verb("pull", "pulled", "pulled", "pulls", "pulling", VerbType.TRANSITIVE),
    Verb("lift", "lifted", "lifted", "lifts", "lifting", VerbType.TRANSITIVE),
    Verb("drop", "dropped", "dropped", "drops", "dropping", VerbType.TRANSITIVE),
    Verb("break", "broke", "broken", "breaks", "breaking", VerbType.TRANSITIVE),
    Verb("fix", "fixed", "fixed", "fixes", "fixing", VerbType.TRANSITIVE),
    Verb("solve", "solved", "solved", "solves", "solving", VerbType.TRANSITIVE),
    Verb("teach", "taught", "taught", "teaches", "teaching", VerbType.TRANSITIVE),
    Verb("learn", "learned", "learned", "learns", "learning", VerbType.TRANSITIVE),
    Verb("explain", "explained", "explained", "explains", "explaining", VerbType.TRANSITIVE),
    Verb("remember", "remembered", "remembered", "remembers", "remembering", VerbType.TRANSITIVE),
    Verb("forget", "forgot", "forgotten", "forgets", "forgetting", VerbType.TRANSITIVE),
    Verb("choose", "chose", "chosen", "chooses", "choosing", VerbType.TRANSITIVE),
    Verb("protect", "protected", "protected", "protects", "protecting", VerbType.TRANSITIVE),
    Verb("attack", "attacked", "attacked", "attacks", "attacking", VerbType.TRANSITIVE),
    Verb("rescue", "rescued", "rescued", "rescues", "rescuing", VerbType.TRANSITIVE),
    Verb("invite", "invited", "invited", "invites", "inviting", VerbType.TRANSITIVE),
    Verb("greet", "greeted", "greeted", "greets", "greeting", VerbType.TRANSITIVE),
    Verb("love", "loved", "loved", "loves", "loving", VerbType.TRANSITIVE),
    Verb("hate", "hated", "hated", "hates", "hating", VerbType.TRANSITIVE),
    Verb("feed", "fed", "fed", "feeds", "feeding", VerbType.TRANSITIVE),
    Verb("hire", "hired", "hired", "hires", "hiring", VerbType.TRANSITIVE),
    Verb("fire", "fired", "fired", "fires", "firing", VerbType.TRANSITIVE),
    Verb("guide", "guided", "guided", "guides", "guiding", VerbType.TRANSITIVE),
    Verb("lead", "led", "led", "leads", "leading", VerbType.TRANSITIVE),
    Verb("follow", "followed", "followed", "follows", "following", VerbType.TRANSITIVE),
    Verb("warn", "warned", "warned", "warns", "warning", VerbType.TRANSITIVE),
    Verb("support", "supported", "supported", "supports", "supporting", VerbType.TRANSITIVE),
    Verb("measure", "measured", "measured", "measures", "measuring", VerbType.TRANSITIVE),
    Verb("calculate", "calculated", "calculated", "calculates", "calculating", VerbType.TRANSITIVE),
    Verb("publish", "published", "published", "publishes", "publishing", VerbType.TRANSITIVE),
    Verb("record", "recorded", "recorded", "records", "recording", VerbType.TRANSITIVE),
    Verb("examine", "examined", "examined", "examines", "examining", VerbType.TRANSITIVE),
    Verb("cure", "cured", "cured", "cures", "curing", VerbType.TRANSITIVE),
    Verb("plant", "planted", "planted", "plants", "planting", VerbType.TRANSITIVE),
    Verb("harvest", "harvested", "harvested", "harvests", "harvesting", VerbType.TRANSITIVE),
    Verb("burn", "burned", "burned", "burns", "burning", VerbType.TRANSITIVE),
    Verb("pour", "poured", "poured", "pours", "pouring", VerbType.TRANSITIVE),
    Verb("lock", "locked", "locked", "locks", "locking", VerbType.TRANSITIVE),
    Verb("unlock", "unlocked", "unlocked", "unlocks", "unlocking", VerbType.TRANSITIVE),
    Verb("deliver", "delivered", "delivered", "delivers", "delivering", VerbType.TRANSITIVE),
    Verb("store", "stored", "stored", "stores", "storing", VerbType.TRANSITIVE),
    Verb("collect", "collected", "collected", "collects", "collecting", VerbType.TRANSITIVE),
    Verb("count", "counted", "counted", "counts", "counting", VerbType.TRANSITIVE),
    Verb("borrow", "borrowed", "borrowed", "borrows", "borrowing", VerbType.TRANSITIVE),
    Verb("lend", "lent", "lent", "lends", "lending", VerbType.TRANSITIVE),
    Verb("spend", "spent", "spent", "spends", "spending", VerbType.TRANSITIVE),
    Verb("earn", "earned", "earned", "earns", "earning", VerbType.TRANSITIVE),
    Verb("steal", "stole", "stolen", "steals", "stealing", VerbType.TRANSITIVE),

    # --- INTRANSITIVE VERBS (No Direct Object) ---
    Verb("sleep", "slept", "slept", "sleeps", "sleeping", VerbType.INTRANSITIVE),
    Verb("run", "ran", "run", "runs", "running", VerbType.INTRANSITIVE),
    Verb("laugh", "laughed", "laughed", "laughs", "laughing", VerbType.INTRANSITIVE),
    Verb("smile", "smiled", "smiled", "smiles", "smiling", VerbType.INTRANSITIVE),
    Verb("cry", "cried", "cried", "cries", "crying", VerbType.INTRANSITIVE),
    Verb("arrive", "arrived", "arrived", "arrives", "arriving", VerbType.INTRANSITIVE),
    Verb("depart", "departed", "departed", "departs", "departing", VerbType.INTRANSITIVE),
    Verb("disappear", "disappeared", "disappeared", "disappears", "disappearing", VerbType.INTRANSITIVE),
    Verb("wait", "waited", "waited", "waits", "waiting", VerbType.INTRANSITIVE),
    Verb("hesitate", "hesitated", "hesitated", "hesitates", "hesitating", VerbType.INTRANSITIVE),
    Verb("fall", "fell", "fallen", "falls", "falling", VerbType.INTRANSITIVE),
    Verb("jump", "jumped", "jumped", "jumps", "jumping", VerbType.INTRANSITIVE),
    Verb("swim", "swam", "swum", "swims", "swimming", VerbType.INTRANSITIVE),
    Verb("walk", "walked", "walked", "walks", "walking", VerbType.INTRANSITIVE),
    Verb("fly", "flew", "flown", "flies", "flying", VerbType.INTRANSITIVE),
    Verb("glow", "glowed", "glowed", "glows", "glowing", VerbType.INTRANSITIVE),
    Verb("shine", "shone", "shone", "shines", "shining", VerbType.INTRANSITIVE),
    Verb("pause", "paused", "paused", "pauses", "pausing", VerbType.INTRANSITIVE),
    Verb("bark", "barked", "barked", "barks", "barking", VerbType.INTRANSITIVE),
    Verb("bloom", "bloomed", "bloomed", "blooms", "blooming", VerbType.INTRANSITIVE),

    # --- REFLEXIVE VERBS (Takes Reflexive Pronoun) ---
    Verb("prepare", "prepared", "prepared", "prepares", "preparing", VerbType.REFLEXIVE),
    Verb("introduce", "introduced", "introduced", "introduces", "introducing", VerbType.REFLEXIVE),
    Verb("blame", "blamed", "blamed", "blames", "blaming", VerbType.REFLEXIVE),
    Verb("defend", "defended", "defended", "defends", "defending", VerbType.REFLEXIVE),
    Verb("express", "expressed", "expressed", "expresses", "expressing", VerbType.REFLEXIVE),
    Verb("adapt", "adapted", "adapted", "adapts", "adapting", VerbType.REFLEXIVE),
    Verb("pride", "prided", "prided", "prides", "priding", VerbType.REFLEXIVE),
    Verb("calm", "calmed", "calmed", "calms", "calming", VerbType.REFLEXIVE),
    Verb("disguise", "disguised", "disguised", "disguises", "disguising", VerbType.REFLEXIVE),
    Verb("hurt", "hurt", "hurt", "hurts", "hurting", VerbType.REFLEXIVE),
]


# ============================================================================
# 3. ADJECTIVES (At least 110 adjectives)
# ============================================================================
ADJECTIVES: List[Adjective] = [
    # Colors
    Adjective("red"),
    Adjective("blue"),
    Adjective("green"),
    Adjective("yellow"),
    Adjective("black"),
    Adjective("white"),
    Adjective("golden"),
    Adjective("silver"),
    Adjective("gray"),
    Adjective("brown"),
    Adjective("orange", starts_with_vowel_sound=True),

    # Physical Size and Dimensions
    Adjective("big"),
    Adjective("small"),
    Adjective("large"),
    Adjective("tiny"),
    Adjective("huge"),
    Adjective("tall"),
    Adjective("short"),
    Adjective("long"),
    Adjective("wide"),
    Adjective("narrow"),
    Adjective("deep"),
    Adjective("shallow"),
    Adjective("thick"),
    Adjective("thin"),
    Adjective("heavy"),
    Adjective("light"),

    # Age and Time
    Adjective("young"),
    Adjective("old", starts_with_vowel_sound=True),
    Adjective("ancient", starts_with_vowel_sound=True),
    Adjective("modern"),
    Adjective("new"),
    Adjective("fresh"),
    Adjective("early", starts_with_vowel_sound=True),
    Adjective("late"),

    # Temperature and Touch
    Adjective("hot"),
    Adjective("cold"),
    Adjective("warm"),
    Adjective("cool"),
    Adjective("dry"),
    Adjective("wet"),
    Adjective("soft"),
    Adjective("hard"),
    Adjective("sharp"),
    Adjective("smooth"),
    Adjective("rough"),

    # Speed and Power
    Adjective("fast"),
    Adjective("slow"),
    Adjective("quick"),
    Adjective("strong"),
    Adjective("weak"),
    Adjective("powerful"),
    Adjective("energetic", starts_with_vowel_sound=True),

    # Personality / Emotions / Character
    Adjective("happy"),
    Adjective("sad"),
    Adjective("angry", starts_with_vowel_sound=True),
    Adjective("calm"),
    Adjective("brave"),
    Adjective("clever"),
    Adjective("smart"),
    Adjective("wise"),
    Adjective("polite"),
    Adjective("kind"),
    Adjective("honest", starts_with_vowel_sound=True),  # silent 'h' -> starts with vowel sound!
    Adjective("gentle"),
    Adjective("generous"),
    Adjective("lazy"),
    Adjective("curious"),
    Adjective("proud"),
    Adjective("shy"),
    Adjective("patient"),
    Adjective("nervous"),
    Adjective("friendly"),

    # Quality and State
    Adjective("good"),
    Adjective("bad"),
    Adjective("great"),
    Adjective("terrible"),
    Adjective("beautiful"),
    Adjective("ugly", starts_with_vowel_sound=True),
    Adjective("clean"),
    Adjective("dirty"),
    Adjective("rich"),
    Adjective("poor"),
    Adjective("famous"),
    Adjective("mysterious"),
    Adjective("strange"),
    Adjective("quiet"),
    Adjective("loud"),
    Adjective("silent"),
    Adjective("bright"),
    Adjective("dark"),
    Adjective("shiny"),
    Adjective("precious"),
    Adjective("simple"),
    Adjective("complex"),
    Adjective("safe"),
    Adjective("dangerous"),
    Adjective("valuable"),
    Adjective("fragile"),
    Adjective("rare"),
    Adjective("common"),
    Adjective("wild"),
    Adjective("tame"),

    # Taste / Sensory
    Adjective("sweet"),
    Adjective("bitter"),
    Adjective("sour"),
    Adjective("salty"),
    Adjective("delicious"),
    Adjective("tasty"),
    Adjective("spicy"),
    Adjective("crispy"),

    # Material
    Adjective("wooden"),
    Adjective("metallic"),
    Adjective("glass"),
    Adjective("plastic"),
    Adjective("stone"),
    Adjective("iron", starts_with_vowel_sound=True),
]


# ============================================================================
# 4. PRONOUNS (Subject, Object, Reflexive)
# ============================================================================
@dataclass(frozen=True)
class PersonalPronoun:
    subject: str        # e.g., "I", "he", "they"
    object_form: str    # e.g., "me", "him", "them"
    reflexive: str      # e.g., "myself", "himself", "themselves"
    person: int         # 1, 2, 3
    is_plural: bool     # False = singular, True = plural
    gender: Gender = Gender.NEUTER


PRONOUNS: List[PersonalPronoun] = [
    PersonalPronoun("I", "me", "myself", person=1, is_plural=False),
    PersonalPronoun("you", "you", "yourself", person=2, is_plural=False),
    PersonalPronoun("he", "him", "himself", person=3, is_plural=False, gender=Gender.MASCULINE),
    PersonalPronoun("she", "her", "herself", person=3, is_plural=False, gender=Gender.FEMININE),
    PersonalPronoun("it", "it", "itself", person=3, is_plural=False, gender=Gender.NEUTER),
    PersonalPronoun("we", "us", "ourselves", person=1, is_plural=True),
    PersonalPronoun("they", "them", "themselves", person=3, is_plural=True),
]


# ============================================================================
# 5. DETERMINERS (Articles, Possessives, Demonstratives, Quantifiers)
# ============================================================================
class DeterminerType(str, Enum):
    ARTICLE = "article"
    POSSESSIVE = "possessive"
    DEMONSTRATIVE = "demonstrative"
    QUANTIFIER = "quantifier"


@dataclass(frozen=True)
class Determiner:
    singular_word: Optional[str]  # None for zero article or context-based
    plural_word: Optional[str]
    determiner_type: DeterminerType
    allows_uncountable: bool = True


DETERMINERS: List[Determiner] = [
    # Articles
    Determiner("the", "the", DeterminerType.ARTICLE, allows_uncountable=True),
    Determiner("a/an", None, DeterminerType.ARTICLE, allows_uncountable=False),  # resolved dynamically
    Determiner(None, None, DeterminerType.ARTICLE, allows_uncountable=True),      # Zero article

    # Possessives
    Determiner("my", "my", DeterminerType.POSSESSIVE),
    Determiner("your", "your", DeterminerType.POSSESSIVE),
    Determiner("his", "his", DeterminerType.POSSESSIVE),
    Determiner("her", "her", DeterminerType.POSSESSIVE),
    Determiner("its", "its", DeterminerType.POSSESSIVE),
    Determiner("our", "our", DeterminerType.POSSESSIVE),
    Determiner("their", "their", DeterminerType.POSSESSIVE),

    # Demonstratives
    Determiner("this", "these", DeterminerType.DEMONSTRATIVE, allows_uncountable=True),
    Determiner("that", "those", DeterminerType.DEMONSTRATIVE, allows_uncountable=True),

    # Quantifiers
    Determiner("every", None, DeterminerType.QUANTIFIER, allows_uncountable=False),
    Determiner("each", None, DeterminerType.QUANTIFIER, allows_uncountable=False),
    Determiner("some", "some", DeterminerType.QUANTIFIER, allows_uncountable=True),
    Determiner("no", "no", DeterminerType.QUANTIFIER, allows_uncountable=True),
    Determiner(None, "many", DeterminerType.QUANTIFIER, allows_uncountable=False),
    Determiner(None, "few", DeterminerType.QUANTIFIER, allows_uncountable=False),
    Determiner("all", "all", DeterminerType.QUANTIFIER, allows_uncountable=True),
]

