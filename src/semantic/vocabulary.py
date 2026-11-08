"""Vocabulary module for semantic analysis: 100 transitive verbs and 1000+ nouns.
Each noun is annotated with a ground-truth semantic category for quantitative evaluation.
"""

from typing import Dict, List, Tuple

# ============================================================================
# 1. 100 TRANSITIVE VERBS (Covering diverse action domains)
# ============================================================================
TRANSITIVE_VERBS: List[str] = [
    # Consumption / Culinary (15)
    "eat", "drink", "taste", "swallow", "cook", "bake", "boil", "fry", "chew", "slice",
    "pour", "feed", "serve", "order", "prepare",

    # Physical manipulation / Construction / Tools (30)
    "cut", "break", "repair", "build", "clean", "wash", "paint", "draw", "fix", "open",
    "close", "lock", "unlock", "carry", "lift", "hold", "drop", "push", "pull", "throw",
    "catch", "strike", "press", "bend", "burn", "shake", "measure", "weigh", "carve", "polish",

    # Intellectual / Communication / Perception (20)
    "read", "write", "hear", "see", "watch", "sing", "teach", "learn", "study", "solve",
    "explain", "remember", "forget", "understand", "prove", "calculate", "publish", "record", "print", "translate",

    # Commerce / Possession / Resource management (18)
    "buy", "sell", "pay", "spend", "earn", "rent", "own", "borrow", "lend", "steal",
    "collect", "store", "deliver", "trade", "distribute", "count", "save", "invest",

    # Social / Interpersonal / Protective (17)
    "love", "hate", "kiss", "hug", "invite", "greet", "visit", "help", "protect", "rescue",
    "cure", "guide", "lead", "hire", "fire", "advise", "warn",
]

assert len(TRANSITIVE_VERBS) == 100, f"Expected exactly 100 verbs, got {len(TRANSITIVE_VERBS)}"


# ============================================================================
# 2. 1000+ NOUNS GROUPED BY SEMANTIC FIELD
# ============================================================================
# Categories:
# 1. Food & Drink (110)
# 2. Animals & Organisms (105)
# 3. Vehicles & Transportation (90)
# 4. Clothing & Wearables (90)
# 5. Tools, Devices & Appliances (105)
# 6. Buildings, Rooms & Architecture (100)
# 7. Furniture & Household Objects (90)
# 8. Professions, Social Roles & People (110)
# 9. Nature, Plants & Geography (105)
# 10. Documents, Arts & Media (95)
# ============================================================================

CATEGORIZED_NOUNS: Dict[str, List[str]] = {
    "food_drink": [
        "apple", "banana", "orange", "pear", "peach", "grape", "lemon", "lime", "berry", "cherry",
        "strawberry", "blueberry", "raspberry", "melon", "watermelon", "pineapple", "mango", "plum", "fig", "date",
        "grapefruit", "pomegranate", "apricot", "avocado", "coconut", "kiwi", "papaya", "blackberry", "cranberry", "bread",
        "toast", "bagel", "croissant", "cake", "cookie", "biscuit", "pie", "muffin", "pancake", "waffle",
        "sandwich", "burger", "pizza", "pasta", "noodle", "rice", "soup", "stew", "salad", "curry",
        "cheese", "butter", "cream", "yogurt", "milk", "egg", "omelet", "meat", "beef", "pork",
        "chicken", "turkey", "duck", "bacon", "sausage", "ham", "steak", "fish", "salmon", "tuna",
        "shrimp", "crab", "lobster", "oyster", "clam", "mussel", "potato", "tomato", "carrot", "onion",
        "garlic", "pepper", "cucumber", "lettuce", "cabbage", "spinach", "broccoli", "mushroom", "bean", "pea",
        "corn", "sugar", "salt", "spice", "sauce", "mustard", "ketchup", "oil", "vinegar", "honey",
        "jam", "chocolate", "candy", "icecream", "pudding", "tart", "custard", "coffee", "tea", "water",
        "juice", "wine", "beer", "soda", "cider", "whiskey", "vodka", "cocktail", "broth", "porridge",
        "cereal", "snack", "dessert", "flour", "cappuccino", "espresso", "latte", "cocoa", "smoothie", "syrup",
    ],
    "animal": [
        "dog", "puppy", "cat", "kitten", "horse", "pony", "donkey", "mule", "cow", "bull",
        "calf", "sheep", "lamb", "goat", "pig", "piglet", "chicken", "rooster", "hen", "duck",
        "goose", "turkey", "rabbit", "hare", "deer", "elk", "moose", "lion", "tiger", "leopard",
        "cheetah", "jaguar", "panther", "wolf", "fox", "bear", "panda", "polarbear", "elephant", "rhino",
        "hippo", "giraffe", "zebra", "camel", "llama", "monkey", "ape", "chimpanzee", "gorilla", "baboon",
        "kangaroo", "koala", "hedgehog", "squirrel", "beaver", "otter", "badger", "raccoon", "skunk", "mouse",
        "rat", "hamster", "bat", "whale", "dolphin", "porpoise", "seal", "walrus", "shark", "octopus",
        "squid", "jellyfish", "starfish", "turtle", "tortoise", "crocodile", "alligator", "lizard", "snake", "frog",
        "toad", "eagle", "hawk", "falcon", "owl", "parrot", "sparrow", "pigeon", "crow", "raven",
        "swan", "flamingo", "penguin", "seagull", "woodpecker", "bee", "wasp", "ant", "butterfly", "moth",
        "spider", "beetle", "mosquito", "fly", "dragonfly",
    ],
    "vehicle": [
        "car", "automobile", "truck", "van", "bus", "minibus", "lorry", "taxi", "cab", "ambulance",
        "firetruck", "policecar", "tractor", "bulldozer", "forklift", "motorcycle", "scooter", "moped", "bicycle", "bike",
        "skateboard", "train", "locomotive", "tram", "subway", "metro", "monorail", "carriage", "wagon", "cart",
        "airplane", "plane", "jet", "airliner", "helicopter", "glider", "rocket", "spaceship", "spacecraft", "shuttle",
        "balloon", "airship", "boat", "ship", "vessel", "ferry", "yacht", "sailboat", "canoe", "kayak",
        "raft", "rowboat", "speedboat", "tugboat", "trawler", "submarine", "cruiser", "tanker", "barge", "steamer",
        "freighter", "hovercraft", "gondola", "sleigh", "sled", "rickshaw", "chariot", "wheelchair", "trailer", "camper",
        "caravan", "hearse", "tank", "jeep", "limousine", "convertible", "sedan", "coupe", "stationwagon", "minivan",
        "pickup", "motorhome", "snowmobile", "jetski", "catamaran", "dinghy", "glider", "dirigible", "cablecar", "trolley",
    ],
    "clothing": [
        "shirt", "tshirt", "blouse", "sweater", "pullover", "cardigan", "hoodie", "jacket", "coat", "overcoat",
        "raincoat", "trenchcoat", "parka", "blazer", "vest", "suit", "tuxedo", "dress", "gown", "skirt",
        "pants", "trousers", "jeans", "shorts", "leggings", "tights", "underwear", "boxers", "briefs", "bra",
        "pajamas", "nightgown", "robe", "bathrobe", "swimsuit", "bikini", "sock", "stocking", "shoe", "boot",
        "sneaker", "sandal", "slipper", "heel", "loafer", "hat", "cap", "beret", "beanie", "fedora",
        "helmet", "scarf", "shawl", "glove", "mitten", "belt", "tie", "bowtie", "necklace", "bracelet",
        "ring", "earring", "watch", "glasses", "sunglasses", "handbag", "purse", "backpack", "wallet", "umbrella",
        "apron", "uniform", "costume", "cape", "cloak", "mask", "bandana", "turban", "veil", "cufflink",
        "zipper", "button", "pocket", "collar", "sleeve", "lining", "shoelace", "buckle", "pendant", "brooch",
    ],
    "tool_device": [
        "hammer", "mallet", "screwdriver", "wrench", "spanner", "pliers", "pincers", "chisel", "saw", "handsaw",
        "chainsaw", "drill", "drillbit", "file", "plane", "axe", "hatchet", "knife", "blade", "scissors",
        "shears", "razor", "needle", "pin", "nail", "screw", "bolt", "nut", "washer", "rivet",
        "clamp", "vise", "anvil", "trowel", "shovel", "spade", "rake", "hoe", "pitchfork", "broom",
        "mop", "brush", "sponge", "bucket", "pail", "funnel", "ladder", "rope", "cable", "chain",
        "torch", "flashlight", "lantern", "battery", "generator", "engine", "motor", "pump", "turbine", "compressor",
        "microscope", "telescope", "binoculars", "thermometer", "barometer", "compass", "scale", "caliper", "ruler", "level",
        "computer", "laptop", "tablet", "smartphone", "screen", "monitor", "keyboard", "mouse", "printer", "scanner",
        "camera", "webcam", "projector", "microphone", "speaker", "headphones", "radio", "television", "calculator", "clock",
        "sensor", "switch", "router", "modem", "laser", "solderingiron", "multimeter", "tripod", "joystick", "antenna",
        "magnet", "fuse", "plug", "socket", "extinguisher",
    ],
    "building_place": [
        "house", "cottage", "mansion", "villa", "palace", "castle", "fortress", "tower", "skyscraper", "apartment",
        "building", "hotel", "motel", "inn", "hostel", "hospital", "clinic", "pharmacy", "school", "college",
        "university", "academy", "library", "museum", "gallery", "theater", "cinema", "stadium", "arena", "gymnasium",
        "church", "cathedral", "chapel", "mosque", "temple", "synagogue", "monastery", "shrine", "bank", "postoffice",
        "courthouse", "prison", "jail", "police station", "firestation", "townhall", "parliament", "embassy", "airport", "station",
        "harbor", "port", "dock", "pier", "terminal", "warehouse", "factory", "mill", "refinery", "plant",
        "shop", "store", "market", "supermarket", "mall", "boutique", "bakery", "butcher", "restaurant", "cafe",
        "diner", "bistro", "pub", "bar", "brewery", "winery", "office", "studio", "laboratory", "workshop",
        "garage", "shed", "barn", "stable", "greenhouse", "bridge", "tunnel", "dam", "monument", "lighthouse",
    ],
    "furniture_household": [
        "table", "desk", "chair", "armchair", "stool", "bench", "sofa", "couch", "bed", "mattress",
        "pillow", "cushion", "blanket", "sheet", "quilt", "wardrobe", "closet", "cabinet", "cupboard", "shelf",
        "bookcase", "drawer", "dresser", "nightstand", "sideboard", "buffet", "carpet", "rug", "mat", "curtain",
        "blind", "mirror", "lamp", "chandelier", "lantern", "vase", "frame", "clock", "candle", "candlestick",
        "plate", "dish", "bowl", "saucer", "cup", "mug", "glass", "goblet", "pitcher", "jug",
        "fork", "spoon", "knife", "chopstick", "napkin", "tablecloth", "tray", "pot", "pan", "skillet",
        "saucepan", "kettle", "teapot", "coffeepot", "blender", "toaster", "microwave", "oven", "stove", "fridge",
        "refrigerator", "freezer", "dishwasher", "sink", "faucet", "bathtub", "shower", "toilet", "towel", "soap",
        "shampoo", "toothbrush", "comb", "hairbrush", "iron", "ironingboard", "wastebasket", "trashcan", "basket", "hamper",
    ],
    "person_role": [
        "man", "woman", "boy", "girl", "child", "baby", "infant", "toddler", "teenager", "adult",
        "parent", "father", "mother", "son", "daughter", "brother", "sister", "grandfather", "grandmother", "uncle",
        "aunt", "cousin", "nephew", "niece", "husband", "wife", "friend", "neighbor", "guest", "visitor",
        "teacher", "professor", "student", "pupil", "scholar", "scientist", "researcher", "doctor", "physician", "surgeon",
        "nurse", "dentist", "pharmacist", "patient", "engineer", "architect", "programmer", "technician", "mechanic", "electrician",
        "carpenter", "plumber", "builder", "mason", "painter", "sculptor", "artist", "musician", "composer", "singer",
        "actor", "actress", "director", "writer", "author", "poet", "journalist", "reporter", "photographer", "editor",
        "lawyer", "attorney", "judge", "juror", "police officer", "detective", "soldier", "officer", "general", "sailor",
        "pilot", "captain", "driver", "farmer", "gardener", "chef", "cook", "baker", "butcher", "waiter",
        "waitress", "bartender", "clerk", "secretary", "manager", "president", "minister", "mayor", "politician",
        "king", "queen", "prince", "princess", "emperor", "pope", "priest", "monk", "nun", "hero",
        "coach", "athlete", "runner", "swimmer", "boxer", "referee", "umpire", "astronaut", "astronomer", "biologist",
        "chemist", "physicist", "geologist", "historian", "economist", "accountant", "banker", "investor", "broker", "librarian",
    ],
    "nature_plant": [
        "tree", "oak", "pine", "birch", "maple", "willow", "palm", "cedar", "forest", "wood",
        "jungle", "bush", "shrub", "hedge", "grass", "lawn", "moss", "fern", "flower", "rose",
        "tulip", "daisy", "lily", "sunflower", "orchid", "violet", "leaf", "branch", "twig", "trunk",
        "bark", "root", "seed", "sprout", "bud", "stem", "thorn", "petal", "pollen",
        "mountain", "hill", "valley", "canyon", "cliff", "cave", "volcano", "crater", "plateau", "ridge",
        "river", "stream", "creek", "brook", "waterfall", "lake", "pond", "swamp", "marsh", "bog",
        "ocean", "sea", "bay", "gulf", "coast", "shore", "beach", "island", "peninsula", "reef",
        "desert", "dune", "glacier", "iceberg", "plain", "meadow", "field", "prairie", "savanna", "tundra",
        "sky", "cloud", "sun", "moon", "star", "planet", "rain", "snow", "hail", "frost",
        "storm", "thunder", "lightning", "wind", "breeze", "fog", "mist", "rainbow", "wave", "tide",
        "soil", "sand", "mud", "stone", "rock", "lagoon", "estuary", "fjord", "delta", "oasis",
    ],
    "document_media_concept": [
        "book", "novel", "textbook", "dictionary", "encyclopedia", "magazine", "journal", "newspaper", "article", "essay",
        "paper", "report", "document", "manuscript", "letter", "note", "postcard", "telegram", "envelope", "stamp",
        "contract", "treaty", "license", "certificate", "passport", "ticket", "bill", "invoice", "receipt", "check",
        "map", "chart", "diagram", "blueprint", "drawing", "painting", "sketch", "photograph", "picture", "portrait",
        "film", "movie", "video", "clip", "song", "poem", "melody", "symphony", "album", "podcast",
        "broadcast", "story", "tale", "legend", "myth", "speech", "lecture", "message", "record", "file",
        "folder", "disk", "program", "code", "database", "website", "blog", "email", "password", "signal",
        "law", "rule", "statute", "decree", "policy", "project", "plan", "strategy", "task", "job",
        "problem", "question", "answer", "solution", "mystery", "secret", "truth", "lie", "fact", "idea",
        "concept", "theory", "hypothesis", "argument", "opinion", "belief", "dream", "memory", "thought", "vision",
        "manifesto", "chronicle", "biography", "anthology", "pamphlet", "brochure", "catalog", "bulletin", "manual", "guidebook",
    ],
}

# Flatten to full noun list and category mapping
NOUNS: List[str] = []
NOUN_TO_CATEGORY: Dict[str, str] = {}

for cat, noun_list in CATEGORIZED_NOUNS.items():
    for n in noun_list:
        clean_n = n.strip().lower()
        if clean_n not in NOUN_TO_CATEGORY:
            NOUN_TO_CATEGORY[clean_n] = cat
            NOUNS.append(clean_n)

assert len(NOUNS) >= 1000, f"Expected >= 1000 nouns, got {len(NOUNS)}"
assert len(TRANSITIVE_VERBS) == 100, f"Expected 100 verbs, got {len(TRANSITIVE_VERBS)}"

CATEGORIES = list(CATEGORIZED_NOUNS.keys())

