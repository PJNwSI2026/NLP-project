from datasets import load_dataset

ds = load_dataset("PleIAs/Czech-PD", split="train", streaming=True)

# Titles of latest books
TARGET_TITLES = [
    "Sebrané spisy",
    "Výroba lisovaného droždí",
    "Okres Benešovský"
]

collected_text = []
total_words = 0

for item in ds:
    title = item.get("title", "")
    
    if title in TARGET_TITLES:
        text = item["text"]
        words_in_doc = len(text.split())
        
        collected_text.append(text)
        total_words += words_in_doc
        
        if total_words >= 150000:
            break

with open("czech_modern_150k.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(collected_text))


