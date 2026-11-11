import heapq
import math
from collections import Counter
import pandas as pd


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def generate_huffman_codes(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code

    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)


with open("../../data/czech_modern_200k_clean.txt", "r", encoding="utf-8") as f:
    text = f.read().replace(" ", "")

total_chars = len(text)
freq_dict = Counter(text)

df = pd.DataFrame(freq_dict.items(), columns=["Litera", "Czestosc"])
df["Prawdopodobienstwo"] = df["Czestosc"] / total_chars
df = df.sort_values(by="Czestosc", ascending=False).reset_index(drop=True)

frequency = Counter(text)
heap = [Node(char, freq) for char, freq in frequency.items()]
heapq.heapify(heap)

while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)
    merged = Node(None, left.freq + right.freq)
    merged.left = left
    merged.right = right
    heapq.heappush(heap, merged)

root = heap[0] if heap else None
huffman_codes = {}
generate_huffman_codes(root, "", huffman_codes)

df["Kod_Huffmana"] = df["Litera"].map(huffman_codes)
df["Dlugosc_kodu"] = df["Kod_Huffmana"].apply(len)

df.to_csv("../../results/statistical_results/character_analysis.csv", index=False, encoding="utf-8")

entropy = -sum(p * math.log2(p) for p in df["Prawdopodobienstwo"])
avg_code_length = sum(row["Prawdopodobienstwo"] * row["Dlugosc_kodu"] for _, row in df.iterrows())
efficiency = (entropy / avg_code_length) * 100

wyniki = (
    f"Entropia (H): {entropy:.4f} bitów/znak\n\n"
    f"Średnia długość kodu (L): {avg_code_length:.4f} bitów/znak\n\n"
    f"Efektywność kodowania (H/L): {efficiency:.2f}%\n"
)

with open("../../results/statistical_results/entropy.txt", "w", encoding="utf-8") as text_file:
    text_file.write(wyniki)
