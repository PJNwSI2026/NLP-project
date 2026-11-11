from datasets import load_dataset


ds = load_dataset("PleIAs/Czech-PD", split="train", streaming=True)

TARGET_TITLES = {
    "Sebrané spisy",
    "Výroba lisovaného droždí",
    "Okres Benešovský"
}

collected_text = []
total_words = 0

for item in ds:
    if item.get("title") in TARGET_TITLES:
        text = item.get("text", "")
        if not text:
            continue

        collected_text.append(text)
        total_words += len(text.split())

        if total_words >= 200_000:
            break

with open("../../data/czech_modern_200k.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(collected_text))
