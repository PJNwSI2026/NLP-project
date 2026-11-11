from dataclasses import dataclass
from enum import Enum
from typing import List


class VerbType(str, Enum):
    TRANSITIVE = "transitive"
    INTRANSITIVE = "intransitive"
    REFLEXIVE = "reflexive"

class Gender(str, Enum):
    MASCULINE = "he"
    FEMININE = "she"
    NEUTER = "it"

@dataclass
class Noun:
    singular: str
    plural: str
    countable: bool = True
    gender: Gender = Gender.NEUTER
    starts_with_vowel: bool = False

@dataclass
class Verb:
    base: str
    past: str
    participle: str
    third_sing: str
    gerund: str
    verb_type: VerbType = VerbType.TRANSITIVE

@dataclass
class Adjective:
    word: str
    starts_with_vowel: bool = False

@dataclass
class Pronoun:
    subject: str
    object_form: str
    reflexive: str
    person: int
    is_plural: bool
    gender: Gender = Gender.NEUTER

@dataclass
class Determiner:
    word_sg: str
    word_pl: str
    allows_uncountable: bool = True


PRONOUNS: List[Pronoun] = [
    Pronoun("I", "me", "myself", 1, False),
    Pronoun("you", "you", "yourself", 2, False),
    Pronoun("he", "him", "himself", 3, False, Gender.MASCULINE),
    Pronoun("she", "her", "herself", 3, False, Gender.FEMININE),
    Pronoun("it", "it", "itself", 3, False, Gender.NEUTER),
    Pronoun("we", "us", "ourselves", 1, True),
    Pronoun("they", "them", "themselves", 3, True),
]

DETERMINERS: List[Determiner] = [
    Determiner("the", "the", True),
    Determiner("a/an", "", False),
    Determiner("", "", True),
    Determiner("my", "my", True),
    Determiner("this", "these", True),
    Determiner("some", "some", True),
]

NOUNS: List[Noun] = [
    Noun("boy", "boys", gender=Gender.MASCULINE), Noun("girl", "girls", gender=Gender.FEMININE),
    Noun("man", "men", gender=Gender.MASCULINE), Noun("woman", "women", gender=Gender.FEMININE),
    Noun("teacher", "teachers"), Noun("doctor", "doctors"), Noun("student", "students"),
    Noun("king", "kings"), Noun("queen", "queens"), Noun("artist", "artists", starts_with_vowel=True),
    Noun("engineer", "engineers", starts_with_vowel=True), Noun("actor", "actors", starts_with_vowel=True),
    Noun("actress", "actresses", starts_with_vowel=True), Noun("child", "children"), Noun("driver", "drivers"),
    Noun("writer", "writers"), Noun("singer", "singers"), Noun("soldier", "soldiers"), Noun("scientist", "scientists"),
    Noun("chef", "chefs"), Noun("pilot", "pilots"), Noun("farmer", "farmers"), Noun("baker", "bakers"),
    Noun("detective", "detectives"), Noun("officer", "officers", starts_with_vowel=True), Noun("dog", "dogs"),
    Noun("cat", "cats"), Noun("horse", "horses"), Noun("bird", "birds"), Noun("lion", "lions"), Noun("tiger", "tigers"),
    Noun("elephant", "elephants", starts_with_vowel=True), Noun("wolf", "wolves"), Noun("fox", "foxes"),
    Noun("bear", "bears"), Noun("rabbit", "rabbits"), Noun("monkey", "monkeys"), Noun("eagle", "eagles", starts_with_vowel=True),
    Noun("dolphin", "dolphins"), Noun("whale", "whales"), Noun("owl", "owls", starts_with_vowel=True),
    Noun("snake", "snakes"), Noun("deer", "deer"), Noun("duck", "ducks"), Noun("sheep", "sheep"),
    Noun("apple", "apples", starts_with_vowel=True), Noun("bread", "bread", countable=False), Noun("cake", "cakes"),
    Noun("cheese", "cheese", countable=False), Noun("coffee", "coffee", countable=False), Noun("egg", "eggs", starts_with_vowel=True),
    Noun("fish", "fish"), Noun("fruit", "fruits"), Noun("milk", "milk", countable=False), Noun("meat", "meat", countable=False),
    Noun("orange", "oranges", starts_with_vowel=True), Noun("pizza", "pizzas"), Noun("rice", "rice", countable=False),
    Noun("soup", "soups"), Noun("tea", "tea", countable=False), Noun("water", "water", countable=False),
    Noun("wine", "wine", countable=False), Noun("sandwich", "sandwiches"), Noun("cookie", "cookies"), Noun("banana", "bananas"),
    Noun("car", "cars"), Noun("bicycle", "bicycles"), Noun("bus", "buses"), Noun("train", "trains"), Noun("plane", "planes"),
    Noun("boat", "boats"), Noun("ship", "ships"), Noun("truck", "trucks"), Noun("motorcycle", "motorcycles"),
    Noun("helicopter", "helicopters"), Noun("book", "books"), Noun("computer", "computers"), Noun("phone", "phones"),
    Noun("letter", "letters"), Noun("pen", "pens"), Noun("pencil", "pencils"), Noun("camera", "cameras"),
    Noun("guitar", "guitars"), Noun("piano", "pianos"), Noun("clock", "clocks"), Noun("key", "keys"), Noun("knife", "knives"),
    Noun("mirror", "mirrors"), Noun("hammer", "hammers"), Noun("lamp", "lamps"), Noun("radio", "radios"),
    Noun("telescope", "telescopes"), Noun("sword", "swords"), Noun("bottle", "bottles"), Noun("bell", "bells"),
    Noun("house", "houses"), Noun("castle", "castles"), Noun("bridge", "bridges"), Noun("school", "schools"),
    Noun("hospital", "hospitals"), Noun("library", "libraries"), Noun("museum", "museums"), Noun("forest", "forests"),
    Noun("mountain", "mountains"), Noun("river", "rivers"), Noun("lake", "lakes"), Noun("island", "islands", starts_with_vowel=True),
    Noun("ocean", "oceans", starts_with_vowel=True), Noun("garden", "gardens"), Noun("street", "streets"),
]

VERBS: List[Verb] = [
    Verb("read", "read", "read", "reads", "reading", VerbType.TRANSITIVE), Verb("write", "wrote", "written", "writes", "writing", VerbType.TRANSITIVE),
    Verb("eat", "ate", "eaten", "eats", "eating", VerbType.TRANSITIVE), Verb("drink", "drank", "drunk", "drinks", "drinking", VerbType.TRANSITIVE),
    Verb("drive", "drove", "driven", "drives", "driving", VerbType.TRANSITIVE), Verb("buy", "bought", "bought", "buys", "buying", VerbType.TRANSITIVE),
    Verb("sell", "sold", "sold", "sells", "selling", VerbType.TRANSITIVE), Verb("see", "saw", "seen", "sees", "seeing", VerbType.TRANSITIVE),
    Verb("hear", "heard", "heard", "hears", "hearing", VerbType.TRANSITIVE), Verb("find", "found", "found", "finds", "finding", VerbType.TRANSITIVE),
    Verb("lose", "lost", "lost", "loses", "losing", VerbType.TRANSITIVE), Verb("build", "built", "built", "builds", "building", VerbType.TRANSITIVE),
    Verb("destroy", "destroyed", "destroyed", "destroys", "destroying", VerbType.TRANSITIVE), Verb("open", "opened", "opened", "opens", "opening", VerbType.TRANSITIVE),
    Verb("close", "closed", "closed", "closes", "closing", VerbType.TRANSITIVE), Verb("cook", "cooked", "cooked", "cooks", "cooking", VerbType.TRANSITIVE),
    Verb("bake", "baked", "baked", "bakes", "baking", VerbType.TRANSITIVE), Verb("cut", "cut", "cut", "cuts", "cutting", VerbType.TRANSITIVE),
    Verb("clean", "cleaned", "cleaned", "cleans", "cleaning", VerbType.TRANSITIVE), Verb("wash", "washed", "washed", "washes", "washing", VerbType.TRANSITIVE),
    Verb("repair", "repaired", "repaired", "repairs", "repairing", VerbType.TRANSITIVE), Verb("paint", "painted", "painted", "paints", "painting", VerbType.TRANSITIVE),
    Verb("draw", "drew", "drawn", "draws", "drawing", VerbType.TRANSITIVE), Verb("sing", "sang", "sung", "sings", "singing", VerbType.TRANSITIVE),
    Verb("play", "played", "played", "plays", "playing", VerbType.TRANSITIVE), Verb("watch", "watched", "watched", "watches", "watching", VerbType.TRANSITIVE),
    Verb("wear", "wore", "worn", "wears", "wearing", VerbType.TRANSITIVE), Verb("carry", "carried", "carried", "carries", "carrying", VerbType.TRANSITIVE),
    Verb("hold", "held", "held", "holds", "holding", VerbType.TRANSITIVE), Verb("throw", "threw", "thrown", "throws", "throwing", VerbType.TRANSITIVE),
    Verb("catch", "caught", "caught", "catches", "catching", VerbType.TRANSITIVE), Verb("push", "pushed", "pushed", "pushes", "pushing", VerbType.TRANSITIVE),
    Verb("pull", "pulled", "pulled", "pulls", "pulling", VerbType.TRANSITIVE), Verb("lift", "lifted", "lifted", "lifts", "lifting", VerbType.TRANSITIVE),
    Verb("drop", "dropped", "dropped", "drops", "dropping", VerbType.TRANSITIVE), Verb("break", "broke", "broken", "breaks", "breaking", VerbType.TRANSITIVE),
    Verb("fix", "fixed", "fixed", "fixes", "fixing", VerbType.TRANSITIVE), Verb("solve", "solved", "solved", "solves", "solving", VerbType.TRANSITIVE),
    Verb("teach", "taught", "taught", "teaches", "teaching", VerbType.TRANSITIVE), Verb("learn", "learned", "learned", "learns", "learning", VerbType.TRANSITIVE),
    Verb("explain", "explained", "explained", "explains", "explaining", VerbType.TRANSITIVE), Verb("remember", "remembered", "remembered", "remembers", "remembering", VerbType.TRANSITIVE),
    Verb("forget", "forgot", "forgotten", "forgets", "forgetting", VerbType.TRANSITIVE), Verb("choose", "chose", "chosen", "chooses", "choosing", VerbType.TRANSITIVE),
    Verb("protect", "protected", "protected", "protects", "protecting", VerbType.TRANSITIVE), Verb("attack", "attacked", "attacked", "attacks", "attacking", VerbType.TRANSITIVE),
    Verb("rescue", "rescued", "rescued", "rescues", "rescuing", VerbType.TRANSITIVE), Verb("invite", "invited", "invited", "invites", "inviting", VerbType.TRANSITIVE),
    Verb("greet", "greeted", "greeted", "greets", "greeting", VerbType.TRANSITIVE), Verb("love", "loved", "loved", "loves", "loving", VerbType.TRANSITIVE),
    Verb("hate", "hated", "hated", "hates", "hating", VerbType.TRANSITIVE), Verb("feed", "fed", "fed", "feeds", "feeding", VerbType.TRANSITIVE),
    Verb("hire", "hired", "hired", "hires", "hiring", VerbType.TRANSITIVE), Verb("fire", "fired", "fired", "fires", "firing", VerbType.TRANSITIVE),
    Verb("guide", "guided", "guided", "guides", "guiding", VerbType.TRANSITIVE), Verb("lead", "led", "led", "leads", "leading", VerbType.TRANSITIVE),
    Verb("follow", "followed", "followed", "follows", "following", VerbType.TRANSITIVE), Verb("warn", "warned", "warned", "warns", "warning", VerbType.TRANSITIVE),
    Verb("support", "supported", "supported", "supports", "supporting", VerbType.TRANSITIVE), Verb("measure", "measured", "measured", "measures", "measuring", VerbType.TRANSITIVE),
    Verb("calculate", "calculated", "calculated", "calculates", "calculating", VerbType.TRANSITIVE), Verb("publish", "published", "published", "publishes", "publishing", VerbType.TRANSITIVE),
    Verb("record", "recorded", "recorded", "records", "recording", VerbType.TRANSITIVE), Verb("examine", "examined", "examined", "examines", "examining", VerbType.TRANSITIVE),
    Verb("cure", "cured", "cured", "cures", "curing", VerbType.TRANSITIVE), Verb("plant", "planted", "planted", "plants", "planting", VerbType.TRANSITIVE),
    Verb("harvest", "harvested", "harvested", "harvests", "harvesting", VerbType.TRANSITIVE), Verb("burn", "burned", "burned", "burns", "burning", VerbType.TRANSITIVE),
    Verb("pour", "poured", "poured", "pours", "pouring", VerbType.TRANSITIVE), Verb("lock", "locked", "locked", "locks", "locking", VerbType.TRANSITIVE),
    Verb("unlock", "unlocked", "unlocked", "unlocks", "unlocking", VerbType.TRANSITIVE), Verb("deliver", "delivered", "delivered", "delivers", "delivering", VerbType.TRANSITIVE),
    Verb("store", "stored", "stored", "stores", "storing", VerbType.TRANSITIVE), Verb("collect", "collected", "collected", "collects", "collecting", VerbType.TRANSITIVE),
    Verb("count", "counted", "counted", "counts", "counting", VerbType.TRANSITIVE), Verb("borrow", "borrowed", "borrowed", "borrows", "borrowing", VerbType.TRANSITIVE),
    Verb("lend", "lent", "lent", "lends", "lending", VerbType.TRANSITIVE), Verb("spend", "spent", "spent", "spends", "spending", VerbType.TRANSITIVE),
    Verb("earn", "earned", "earned", "earns", "earning", VerbType.TRANSITIVE), Verb("steal", "stole", "stolen", "steals", "stealing", VerbType.TRANSITIVE),
    Verb("sleep", "slept", "slept", "sleeps", "sleeping", VerbType.INTRANSITIVE), Verb("run", "ran", "run", "runs", "running", VerbType.INTRANSITIVE),
    Verb("laugh", "laughed", "laughed", "laughs", "laughing", VerbType.INTRANSITIVE), Verb("smile", "smiled", "smiled", "smiles", "smiling", VerbType.INTRANSITIVE),
    Verb("cry", "cried", "cried", "cries", "crying", VerbType.INTRANSITIVE), Verb("arrive", "arrived", "arrived", "arrives", "arriving", VerbType.INTRANSITIVE),
    Verb("depart", "departed", "departed", "departs", "departing", VerbType.INTRANSITIVE), Verb("disappear", "disappeared", "disappeared", "disappears", "disappearing", VerbType.INTRANSITIVE),
    Verb("wait", "waited", "waited", "waits", "waiting", VerbType.INTRANSITIVE), Verb("hesitate", "hesitated", "hesitated", "hesitates", "hesitating", VerbType.INTRANSITIVE),
    Verb("fall", "fell", "fallen", "falls", "falling", VerbType.INTRANSITIVE), Verb("jump", "jumped", "jumped", "jumps", "jumping", VerbType.INTRANSITIVE),
    Verb("prepare", "prepared", "prepared", "prepares", "preparing", VerbType.REFLEXIVE), Verb("introduce", "introduced", "introduced", "introduces", "introducing", VerbType.REFLEXIVE),
    Verb("blame", "blamed", "blamed", "blames", "blaming", VerbType.REFLEXIVE), Verb("defend", "defended", "defended", "defends", "defending", VerbType.REFLEXIVE),
    Verb("express", "expressed", "expressed", "expresses", "expressing", VerbType.REFLEXIVE), Verb("adapt", "adapted", "adapted", "adapts", "adapting", VerbType.REFLEXIVE),
    Verb("pride", "prided", "prided", "prides", "priding", VerbType.REFLEXIVE), Verb("calm", "calmed", "calmed", "calms", "calming", VerbType.REFLEXIVE),
]

ADJECTIVES: List[Adjective] = [
    Adjective("red"), Adjective("blue"), Adjective("green"), Adjective("yellow"), Adjective("black"),
    Adjective("white"), Adjective("golden"), Adjective("silver"), Adjective("gray"), Adjective("brown"),
    Adjective("orange", starts_with_vowel=True), Adjective("big"), Adjective("small"), Adjective("large"),
    Adjective("tiny"), Adjective("huge"), Adjective("tall"), Adjective("short"), Adjective("long"),
    Adjective("wide"), Adjective("narrow"), Adjective("deep"), Adjective("shallow"), Adjective("thick"),
    Adjective("thin"), Adjective("heavy"), Adjective("light"), Adjective("young"), Adjective("old", starts_with_vowel=True),
    Adjective("ancient", starts_with_vowel=True), Adjective("modern"), Adjective("new"), Adjective("fresh"),
    Adjective("early", starts_with_vowel=True), Adjective("late"), Adjective("hot"), Adjective("cold"),
    Adjective("warm"), Adjective("cool"), Adjective("dry"), Adjective("wet"), Adjective("soft"),
    Adjective("hard"), Adjective("sharp"), Adjective("smooth"), Adjective("rough"), Adjective("fast"),
    Adjective("slow"), Adjective("quick"), Adjective("strong"), Adjective("weak"), Adjective("powerful"),
    Adjective("energetic", starts_with_vowel=True), Adjective("happy"), Adjective("sad"), Adjective("angry", starts_with_vowel=True),
    Adjective("calm"), Adjective("brave"), Adjective("clever"), Adjective("smart"), Adjective("wise"),
    Adjective("polite"), Adjective("kind"), Adjective("honest", starts_with_vowel=True), Adjective("gentle"),
    Adjective("generous"), Adjective("lazy"), Adjective("curious"), Adjective("proud"), Adjective("shy"),
    Adjective("patient"), Adjective("nervous"), Adjective("friendly"), Adjective("good"), Adjective("bad"),
    Adjective("great"), Adjective("terrible"), Adjective("beautiful"), Adjective("ugly", starts_with_vowel=True),
    Adjective("clean"), Adjective("dirty"), Adjective("rich"), Adjective("poor"), Adjective("famous"),
    Adjective("mysterious"), Adjective("strange"), Adjective("quiet"), Adjective("loud"), Adjective("silent"),
    Adjective("bright"), Adjective("dark"), Adjective("shiny"), Adjective("precious"), Adjective("simple"),
    Adjective("complex"), Adjective("safe"), Adjective("dangerous"), Adjective("valuable"), Adjective("fragile"),
    Adjective("rare"), Adjective("common"), Adjective("wild"), Adjective("tame"), Adjective("sweet"),
    Adjective("bitter"), Adjective("sour"), Adjective("salty"), Adjective("delicious"), Adjective("tasty"),
    Adjective("spicy"), Adjective("crispy"), Adjective("wooden"), Adjective("metallic"), Adjective("glass"),
    Adjective("plastic"), Adjective("stone"), Adjective("iron", starts_with_vowel=True),
]
