import re


czech_alphabet = set("aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvwxyýzž")

with open("../../data/czech_modern_200k.txt", "r", encoding="utf-8") as file:
    text = file.read().lower()

text = re.sub(r"\s+", " ", text)
text = re.sub(r"[^\w\s]", "", text)

words = text.split()

cleaned_words = []
for word in words:
    if any(char.isdigit() for char in word):
        continue

    if not all(char in czech_alphabet for char in word):
        continue

    cleaned_words.append(word)

final_text = " ".join(cleaned_words)

with open("../../data/czech_modern_200k_clean.txt", "w", encoding="utf-8") as file:
    file.write(final_text)
