import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

with open("../../data/czech_modern_200k_clean.txt", "r", encoding="utf-8") as f:
    text = f.read()

words = [word for word in text.split() if len(word) > 1]
total_words = len(words)

word_freq = Counter(words)
df_zipf = pd.DataFrame(word_freq.items(), columns=["Wyraz", "Czestosc"])
df_zipf = df_zipf.sort_values(by="Czestosc", ascending=False).reset_index(drop=True)
df_zipf["Ranga"] = df_zipf.index + 1

log_x = np.log10(df_zipf["Ranga"])
log_y = np.log10(df_zipf["Czestosc"])
slope, intercept = np.polyfit(log_x, log_y, 1)

is_satisfied = "spełnione" if -1.2 <= slope <= -0.8 else "tylko częściowo spełnione / zaburzone"

plt.figure(figsize=(16, 9))
plt.loglog(df_zipf["Ranga"], df_zipf["Czestosc"], marker=".", linestyle="none", color="b")
plt.title("Rozkład Zipfa dla wyrazów")
plt.xlabel("Ranga k (skala logarytmiczna)")
plt.ylabel("Częstość (skala logarytmiczna)")
plt.grid(True, which="both", ls="--", linewidth=0.5)
info_text = (
    f"Współczynnik kierunkowy prostej: {slope:.3f} (ideał: -1.0)\n"
    f"Wniosek: Prawo Zipfa jest {is_satisfied}"
)
plt.text(
    0.95, 0.95, info_text,
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray')
)
plt.savefig("../../results/statistical_results/prawo_zipfa.png")
plt.close()


df_zipf["Skumulowana_czestosc"] = df_zipf["Czestosc"].cumsum()
df_zipf["Skumulowany_procent"] = (df_zipf["Skumulowana_czestosc"] / total_words) * 100
idx_90 = df_zipf[df_zipf["Skumulowany_procent"] >= 90.0].index[0]
words_for_90 = df_zipf.iloc[:idx_90 + 1].copy()
words_for_90.to_csv("../../results/statistical_results/words_90.csv", index=False, encoding="utf-8")


neighbors = defaultdict(set)
for i in range(len(words)):
    current_word = words[i]
    if i > 0:
        neighbors[current_word].add(words[i - 1])
    if i < len(words) - 1:
        neighbors[current_word].add(words[i + 1])

neighbor_counts = {word: len(neighs) for word, neighs in neighbors.items()}
df_neighbors = pd.DataFrame(neighbor_counts.items(), columns=["Wyraz", "Liczba_unikalnych_sasiadow"])
df_neighbors = df_neighbors.sort_values(by="Liczba_unikalnych_sasiadow", ascending=False).reset_index(drop=True)
df_neighbors["Ranga_sasiedztwa"] = df_neighbors.index + 1
top_100_core = df_neighbors.head(100)
top_100_core.to_csv("../../results/statistical_results/core_100.csv", index=False, encoding="utf-8")
