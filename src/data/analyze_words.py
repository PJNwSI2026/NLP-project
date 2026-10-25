from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import pandas as pd


def analyze_words(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    if not words:
        print("Plik jest pusty.")
        return

    total_words = len(words)
    print(f"Całkowita liczba wyrazów (tokenów): {total_words}")


    word_freq = Counter(words)
    df_zipf = pd.DataFrame(word_freq.items(), columns=["Wyraz", "Częstość"])
    df_zipf = df_zipf.sort_values(by="Częstość", ascending=False).reset_index(drop=True)
    df_zipf["Ranga"] = df_zipf.index + 1

    plt.figure(figsize=(10, 6))
    plt.loglog(
        df_zipf["Ranga"], df_zipf["Częstość"], marker=".", linestyle="none", color="b"
    )
    plt.title("Rozkład Zipfa dla wyrazów")
    plt.xlabel("Ranga k (skala logarytmiczna)")
    plt.ylabel("Częstość (skala logarytmiczna)")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig("rozklad_zipfa.png")
    print(
        "\n[1] Wygenerowano listę rankingową wyrazów. Wykres zapisano jako 'rozklad_zipfa.png'."
    )


    df_zipf["Skumulowana częstość"] = df_zipf["Częstość"].cumsum()
    df_zipf["Skumulowany procent (%)"] = (
        df_zipf["Skumulowana częstość"] / total_words
    ) * 100

    words_for_90_percent = df_zipf[df_zipf["Skumulowany procent (%)"] <= 90.0]
    num_words_needed = len(words_for_90_percent) + 1

    print(
        f"\n[2] Aby móc zrozumieć 90% tekstu, musisz nauczyć się {num_words_needed} najczęściej występujących wyrazów."
    )
    print("Oto top 10 z nich:")
    print(
        df_zipf[["Ranga", "Wyraz", "Częstość", "Skumulowany procent (%)"]]
        .head(10)
        .to_string(index=False)
    )


    neighbors = defaultdict(set)
    for i in range(len(words)):
        current_word = words[i]
        if i > 0:
            neighbors[current_word].add(words[i - 1])
        if i < len(words) - 1:
            neighbors[current_word].add(words[i + 1])

    neighbor_counts = {word: len(neighs) for word, neighs in neighbors.items()}
    df_neighbors = pd.DataFrame(
        neighbor_counts.items(), columns=["Wyraz", "Liczba unikalnych sąsiadów"]
    )
    df_neighbors = df_neighbors.sort_values(
        by="Liczba unikalnych sąsiadów", ascending=False
    ).reset_index(drop=True)
    df_neighbors["Ranga sąsiedztwa"] = df_neighbors.index + 1

    top_100_core = df_neighbors.head(100)
    top_100_core.to_csv("top_100_rdzen_jezyka.csv", index=False)

    print("\n[3] Ustalono rdzeń języka na podstawie liczby unikalnych sąsiadów.")
    print("Pierwsza 10-tka z Top 100 wyrazów z największą liczbą sąsiadów:")
    print(
        top_100_core[["Ranga sąsiedztwa", "Wyraz", "Liczba unikalnych sąsiadów"]]
        .head(10)
        .to_string(index=False)
    )
    print("Pełną listę 100 wyrazów zapisano do pliku 'top_100_rdzen_jezyka.csv'.")


def main():
    input_file = r"czech_modern_150k_clean.txt"
    analyze_words(input_file)


if __name__ == "__main__":
    main()
