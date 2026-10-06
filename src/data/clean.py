import re

with open("czech_modern_150k.txt", "r", encoding="utf-8") as f:
    text = f.read()

clean_text = text.lower()
# Remove every number
clean_text = re.sub(r'\d+', ' ', clean_text)

# Remove everything that isn't whitespace or czech letter
clean_text = re.sub(r'[^\w\s]|_', ' ', clean_text, flags=re.UNICODE)

# Change every whitespace to space
clean_text = re.sub(r'\s+', ' ', clean_text).strip()

# Save the clean text
with open("czech_modern_150k_clean.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)
