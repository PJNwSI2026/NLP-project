"""Interactive Graphical User Interface (GUI) for the Kohonen Semantic Classifier.
Displays the 5x10 grid of 50 neurons, allows inspecting cluster contents,
searching any noun to find its BMU, and viewing plots.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageTk
import numpy as np

from .analysis import SemanticAnalyzer
from .matrix import VOMatrixBuilder
from .som import KohonenSOM
from .vocabulary import NOUNS, TRANSITIVE_VERBS, NOUN_TO_CATEGORY, CATEGORIES


# Distinct pastel colors for semantic categories on the grid
CATEGORY_COLORS: Dict[str, str] = {
    "food_drink": "#FED7AA",           # Orange light
    "animal": "#BBF7D0",               # Green light
    "vehicle": "#BAE6FD",              # Blue light
    "clothing": "#FBCFE8",             # Pink light
    "tool_device": "#E2E8F0",          # Slate gray light
    "building_place": "#DDD6FE",       # Purple light
    "furniture_household": "#FEF08A",  # Yellow light
    "person_role": "#FCA5A5",          # Red light
    "nature_plant": "#86EFAC",         # Emerald light
    "document_media_concept": "#A5F3FC", # Cyan light
    "None (Dead Neuron)": "#EF4444",   # Red vibrant for dead
}


class SemanticGUI(tk.Tk):
    """Main desktop application window for Kohonen Semantic Analysis."""

    def __init__(self):
        super().__init__()

        self.title("Kohonen Semantic Classifier — 50 Neuronów (NLP)")
        self.geometry("1200x850")
        self.minsize(1050, 720)

        self._configure_styles()

        # Data & Model state
        self.builder = VOMatrixBuilder()
        self.raw_matrix, self.norm_matrix = self.builder.build_matrix(blend_corpus=True)

        self.som = KohonenSOM(grid_rows=5, grid_cols=10, input_dim=100, random_state=42)
        self.som.train(self.norm_matrix, epochs=60, verbose=False)

        self.analyzer = SemanticAnalyzer(self.som, self.norm_matrix)

        # Generate plots on startup
        self.analyzer.plot_u_matrix()
        self.analyzer.plot_activation_map()
        self.analyzer.plot_semantic_grid()
        self.analyzer.plot_cluster_feature_profiles()
        self.analyzer.generate_markdown_report()

        self.selected_neuron: Tuple[int, int] = (0, 0)
        self.tile_buttons: Dict[Tuple[int, int], tk.Button] = {}

        self._create_widgets()
        self._select_neuron(0, 0)

    def _configure_styles(self):
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self.configure(bg="#F4F6F9")
        self.style.configure(".", background="#F4F6F9", font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background="#FFFFFF", relief="groove")
        self.style.configure("TLabelframe.Label", background="#FFFFFF", font=("Segoe UI", 10, "bold"), foreground="#1E293B")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

    def _create_widgets(self):
        # Header banner
        header = tk.Frame(self, bg="#0F172A", height=70)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Klasyfikator Semantyczny Rzeczowników — Sieć Kohonena (SOM)",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#0F172A",
        ).pack(anchor="w", padx=20, pady=(8, 0))

        tk.Label(
            header,
            text=f"Analiza 1000+ rzeczowników w oparciu o wektory VO (100 czasowników przechodnich) | Dokładnie 50 neuronów (siatka 5x10)",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A",
        ).pack(anchor="w", padx=20, pady=(0, 8))

        # Top Action & Search Bar
        search_bar = tk.Frame(self, bg="#E2E8F0", height=50)
        search_bar.pack(fill=tk.X, padx=12, pady=(8, 4))

        tk.Label(search_bar, text="🔍 Szukaj rzeczownika:", font=("Segoe UI", 10, "bold"), bg="#E2E8F0").pack(side=tk.LEFT, padx=(12, 6), pady=8)

        self.search_var = tk.StringVar(value="apple")
        self.search_entry = ttk.Entry(search_bar, textvariable=self.search_var, width=22)
        self.search_entry.pack(side=tk.LEFT, padx=4, pady=8)
        self.search_entry.bind("<Return>", lambda e: self.on_search_noun())

        btn_search = tk.Button(
            search_bar,
            text="Znajdź neuron (BMU)",
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_search_noun,
        )
        btn_search.pack(side=tk.LEFT, padx=6, pady=8)

        self.search_result_lbl = tk.Label(search_bar, text="", font=("Segoe UI", 9, "italic"), bg="#E2E8F0", fg="#1E293B")
        self.search_result_lbl.pack(side=tk.LEFT, padx=12, pady=8)

        # Retrain Button
        btn_retrain = tk.Button(
            search_bar,
            text="🔄 Wytrenuj ponownie sieć",
            font=("Segoe UI", 9),
            bg="#475569",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_retrain_som,
        )
        btn_retrain.pack(side=tk.RIGHT, padx=12, pady=8)

        # Main Workspace: Left (5x10 Grid), Right (Neuron Inspector & Plots)
        main_split = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_split.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # LEFT: 5x10 Grid View
        grid_frame = ttk.LabelFrame(main_split, text=" Siatka 50 Neuronów Kohonena (5 wierszy x 10 kolumn) ", padding=10)
        main_split.add(grid_frame, weight=3)

        tk.Label(
            grid_frame,
            text="Kliknij dowolny neuron, aby podejrzeć przypisane do niego rzeczowniki i wagi czasowników:",
            font=("Segoe UI", 9, "italic"),
        ).pack(anchor="w", pady=(0, 8))

        tiles_container = tk.Frame(grid_frame, bg="#FFFFFF", relief="groove", bd=1)
        tiles_container.pack(fill=tk.BOTH, expand=True)

        for c in range(10):
            tiles_container.grid_columnconfigure(c, weight=1)
        for r in range(5):
            tiles_container.grid_rowconfigure(r, weight=1)

        self.tile_buttons = {}
        for r in range(5):
            for c in range(10):
                info = self.analyzer.cluster_stats[(r, c)]
                is_dead = info["is_dead"]
                cat = info["dominant_category"]
                bg_color = CATEGORY_COLORS.get(cat, "#F1F5F9")
                if is_dead:
                    bg_color = "#FEE2E2"

                btn_text = f"N({r},{c})\nn={info['count']}"
                if is_dead:
                    btn_text = f"N({r},{c})\nDEAD"

                btn = tk.Button(
                    tiles_container,
                    text=btn_text,
                    font=("Segoe UI", 9, "bold" if not is_dead else "normal"),
                    bg=bg_color,
                    fg="#991B1B" if is_dead else "#0F172A",
                    relief="solid",
                    bd=1,
                    cursor="hand2",
                    command=lambda row=r, col=c: self._select_neuron(row, col),
                )
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                self.tile_buttons[(r, c)] = btn

        # Legend under grid
        legend_frame = tk.Frame(grid_frame, bg="#F8FAFC", relief="groove", bd=1)
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        tk.Label(legend_frame, text="Legenda kolorów pól semantycznych:", font=("Segoe UI", 8, "bold"), bg="#F8FAFC").pack(anchor="w", padx=6, pady=(4, 2))

        legend_sub = tk.Frame(legend_frame, bg="#F8FAFC")
        legend_sub.pack(fill=tk.X, padx=6, pady=(0, 4))
        col_idx = 0
        for cat_name, color_hex in list(CATEGORY_COLORS.items())[:6]:
            lbl_block = tk.Label(legend_sub, text="  ", bg=color_hex, relief="solid", bd=1)
            lbl_block.grid(row=0, column=col_idx*2, padx=(4, 2), pady=2)
            lbl_text = tk.Label(legend_sub, text=cat_name, font=("Segoe UI", 7), bg="#F8FAFC")
            lbl_text.grid(row=0, column=col_idx*2+1, padx=(0, 8), pady=2)
            col_idx += 1

        # RIGHT: Inspector & Plots Notebook
        right_frame = ttk.Frame(main_split, padding=4)
        main_split.add(right_frame, weight=4)

        self.right_notebook = ttk.Notebook(right_frame)
        self.right_notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Neuron Details
        tab_details = ttk.Frame(self.right_notebook, padding=10)
        self.right_notebook.add(tab_details, text="  Szczegóły klastra  ")

        # Info card
        info_card = tk.Frame(tab_details, bg="#FFFFFF", relief="solid", bd=1)
        info_card.pack(fill=tk.X, pady=(0, 10))

        self.neuron_title_lbl = tk.Label(
            info_card,
            text="Neuron (0, 0)",
            font=("Segoe UI", 13, "bold"),
            bg="#FFFFFF",
            fg="#1E3A8A",
        )
        self.neuron_title_lbl.pack(anchor="w", padx=12, pady=(10, 2))

        self.neuron_meta_lbl = tk.Label(
            info_card,
            text="",
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#334155",
            justify="left",
        )
        self.neuron_meta_lbl.pack(anchor="w", padx=12, pady=(0, 10))

        # Top Verbs Box
        verbs_frame = ttk.LabelFrame(tab_details, text=" Czasowniki definiujące ten klaster (Top VO Weights) ", padding=8)
        verbs_frame.pack(fill=tk.X, pady=(0, 10))

        self.verbs_list_lbl = tk.Label(
            verbs_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#047857",
            justify="left",
        )
        self.verbs_list_lbl.pack(anchor="w", padx=6, pady=4)

        # Nouns List Box
        nouns_frame = ttk.LabelFrame(tab_details, text=" Rzeczowniki w tym klastrze ", padding=8)
        nouns_frame.pack(fill=tk.BOTH, expand=True)

        self.nouns_text = tk.Text(nouns_frame, font=("Segoe UI", 10), bg="#F8FAFC", wrap="word")
        nouns_scroll = ttk.Scrollbar(nouns_frame, orient="vertical", command=self.nouns_text.yview)
        self.nouns_text.configure(yscrollcommand=nouns_scroll.set)
        nouns_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.nouns_text.pack(fill=tk.BOTH, expand=True)

        # Tab 2: U-Matrix Image
        tab_u_matrix = ttk.Frame(self.right_notebook, padding=6)
        self.right_notebook.add(tab_u_matrix, text="  Wykres U-Matrix  ")
        self.lbl_u_img = tk.Label(tab_u_matrix, bg="#FFFFFF")
        self.lbl_u_img.pack(fill=tk.BOTH, expand=True)

        # Tab 3: Activation Map (Hit Map)
        tab_hit = ttk.Frame(self.right_notebook, padding=6)
        self.right_notebook.add(tab_hit, text="  Mapa Aktywacji (Hit Map)  ")
        self.lbl_hit_img = tk.Label(tab_hit, bg="#FFFFFF")
        self.lbl_hit_img.pack(fill=tk.BOTH, expand=True)

        # Tab 4: Semantic Grid Plot
        tab_grid_plot = ttk.Frame(self.right_notebook, padding=6)
        self.right_notebook.add(tab_grid_plot, text="  Siatka Pól Semantycznych  ")
        self.lbl_sem_img = tk.Label(tab_grid_plot, bg="#FFFFFF")
        self.lbl_sem_img.pack(fill=tk.BOTH, expand=True)

        self._load_tab_images()

    def _load_tab_images(self):
        """Loads generated plot images into the notebook tabs."""
        try:
            if os.path.exists("results/semantic/som_u_matrix.png"):
                u_img = Image.open("results/semantic/som_u_matrix.png").resize((580, 360), Image.Resampling.LANCZOS)
                self.tk_u_img = ImageTk.PhotoImage(u_img)
                self.lbl_u_img.config(image=self.tk_u_img)

            if os.path.exists("results/semantic/som_activation_map.png"):
                h_img = Image.open("results/semantic/som_activation_map.png").resize((580, 360), Image.Resampling.LANCZOS)
                self.tk_h_img = ImageTk.PhotoImage(h_img)
                self.lbl_hit_img.config(image=self.tk_h_img)

            if os.path.exists("results/semantic/som_semantic_grid.png"):
                s_img = Image.open("results/semantic/som_semantic_grid.png").resize((620, 360), Image.Resampling.LANCZOS)
                self.tk_s_img = ImageTk.PhotoImage(s_img)
                self.lbl_sem_img.config(image=self.tk_s_img)
        except Exception as e:
            print(f"Warning loading tab images: {e}")

    def _select_neuron(self, r: int, c: int):
        # Reset border of previously selected
        old_r, old_c = self.selected_neuron
        old_info = self.analyzer.cluster_stats[(old_r, old_c)]
        old_bg = CATEGORY_COLORS.get(old_info["dominant_category"], "#F1F5F9")
        if old_info["is_dead"]:
            old_bg = "#FEE2E2"
        self.tile_buttons[(old_r, old_c)].config(bd=1, relief="solid", bg=old_bg)

        # Highlight new selected tile
        self.selected_neuron = (r, c)
        self.tile_buttons[(r, c)].config(bd=3, relief="groove", bg="#FEF08A")

        info = self.analyzer.cluster_stats[(r, c)]
        self.neuron_title_lbl.config(
            text=f"Neuron ID: {info['neuron_id']} — Współrzędne: ({r}, {c})"
        )

        dead_txt = "🔴 NEURON MARTWY (Nie nauczył się żadnego słowa)" if info["is_dead"] else "🟢 Neuron aktywny"
        meta_str = (
            f"• Status: {dead_txt}\n"
            f"• Liczba przypisanych rzeczowników: {info['count']}\n"
            f"• Dominujące pole semantyczne: {info['dominant_category'].upper()}\n"
            f"• Spójność / Czystość klastra: {info['purity']*100:.1f}%"
        )
        self.neuron_meta_lbl.config(text=meta_str)

        # Top verbs
        verbs_formatted = "   ".join([f"★ {v[0]} ({v[1]:.2f})" for v in info["top_verbs"][:4]])
        self.verbs_list_lbl.config(text=verbs_formatted or "Brak dominujących czasowników")

        # Nouns list
        self.nouns_text.delete("1.0", tk.END)
        if info["nouns"]:
            formatted_nouns = ", ".join(info["nouns"])
            self.nouns_text.insert(tk.END, formatted_nouns)
        else:
            self.nouns_text.insert(tk.END, "(Ten neuron nie przypisał do siebie żadnego rzeczownika — neuron martwy)")

    def on_search_noun(self):
        query = self.search_var.get().strip().lower()
        if not query:
            return

        if query not in self.builder.noun_to_idx:
            # Check if plural exists
            messagebox.showwarning("Nie znaleziono", f"Rzeczownik '{query}' nie znajduje się w 1000 słów słownika.")
            return

        idx = self.builder.noun_to_idx[query]
        vec = self.norm_matrix[idx]
        r, c = self.som.find_bmu(vec)

        info = self.analyzer.cluster_stats[(r, c)]
        self._select_neuron(r, c)

        self.search_result_lbl.config(
            text=f"'{query}' trafił do Neuronu ({r}, {c}) — Pole: {info['dominant_category']}",
            fg="#15803D",
        )
        # Switch to first tab
        self.right_notebook.select(0)

    def on_retrain_som(self):
        """Retrains the SOM and refreshes all visualizations."""
        self.som = KohonenSOM(grid_rows=5, grid_cols=10, input_dim=100, random_state=None)
        self.som.train(self.norm_matrix, epochs=60, verbose=False)
        self.analyzer = SemanticAnalyzer(self.som, self.norm_matrix)

        self.analyzer.plot_u_matrix()
        self.analyzer.plot_activation_map()
        self.analyzer.plot_semantic_grid()
        self.analyzer.plot_cluster_feature_profiles()
        self.analyzer.generate_markdown_report()

        # Update tiles text and colors
        for r in range(5):
            for c in range(10):
                info = self.analyzer.cluster_stats[(r, c)]
                is_dead = info["is_dead"]
                cat = info["dominant_category"]
                bg_color = CATEGORY_COLORS.get(cat, "#F1F5F9")
                if is_dead:
                    bg_color = "#FEE2E2"

                btn_text = f"N({r},{c})\nn={info['count']}"
                if is_dead:
                    btn_text = f"N({r},{c})\nDEAD"

                self.tile_buttons[(r, c)].config(
                    text=btn_text,
                    bg=bg_color,
                    fg="#991B1B" if is_dead else "#0F172A",
                )

        self._load_tab_images()
        self._select_neuron(0, 0)
        messagebox.showinfo("Ukończono trening", "Sieć Kohonena została pomyślnie przetrenowana! Wykresy i raport zostały zaktualizowane.")


def main():
    app = SemanticGUI()
    app.mainloop()


if __name__ == "__main__":
    main()

