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


def build_huffman_tree(text):
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

    return heap[0] if heap else None


def generate_huffman_codes(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code

    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)


def analyze_characters(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace(" ", "")

    if not text:
        return

    total_chars = len(text)
    freq_dict = Counter(text)

    df = pd.DataFrame(freq_dict.items(), columns=["Litera", "Liczba wystąpień"])
    df["Prawdopodobieństwo (%)"] = (df["Liczba wystąpień"] / total_chars * 100).round(2)

    df = df.sort_values(by="Liczba wystąpień", ascending=False).reset_index(drop=True)

    entropy = -sum(p * math.log2(p) for p in df["Liczba wystąpień"] / total_chars)

    root = build_huffman_tree(text)
    huffman_codes = {}
    generate_huffman_codes(root, "", huffman_codes)

    df["Kod Huffmana"] = df["Litera"].map(huffman_codes)
    df["Długość kodu"] = df["Kod Huffmana"].apply(len)

    print("=== Tabela Częstości i Kodów Huffmana ===")
    print(df.to_string())

    avg_code_length = sum(
        row["Liczba wystąpień"] / total_chars * row["Długość kodu"] for _, row in df.iterrows()
    )

    efficiency = (entropy / avg_code_length) * 100

    print("\n=== Wskaźniki Optymalności ===")
    print(f"Entropia (H):                  {entropy:.4f} bitów/znak")
    print(f"Średnia długość kodu (L):      {avg_code_length:.4f} bitów/znak")
    print(f"Efektywność kodowania (H/L):   {efficiency:.2f}%")
    print(f"Redundancja (100% - H/L):      {100 - efficiency:.2f}%")


def main():
    input_file = r"czech_modern_150k_clean.txt"
    analyze_characters(input_file)

if __name__ == "__main__":
    main()
