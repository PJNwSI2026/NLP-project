import re


def clean_czech_text(input_filepath, output_filepath):
    czech_alphabet = set("aábcčdďeéěfghchiíjklmnňoópqrřsštťuúůvwxyýzž")

    with open(input_filepath, "r", encoding="utf-8") as file:
        text = file.read()

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.replace("-", "")

    words = text.split()

    cleaned_words = []
    for word in words:
        if any(char.isdigit() for char in word):
            continue

        if not all(char in czech_alphabet for char in word):
            continue

        cleaned_words.append(word)

    final_text = " ".join(cleaned_words)

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write(final_text)


def main() -> None:
    input_file = "czech_modern_150k.txt"
    output_file = "czech_modern_150k_clean.txt"
    clean_czech_text(input_file, output_file)


if __name__ == "__main__":
    main()
