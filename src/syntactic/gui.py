"""Graphical User Interface (GUI) for the SVO Syntactic Sentence Generator.
Built using Tkinter and ttk with modern styling, strict parameter binding,
bidirectional UI synchronization, and report export capabilities.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List

from .generator import SentenceGenerator, GeneratedSentence
from .grammar import Tense, Mood, Voice, NounPhrase
from .lexicon import (
    NOUNS,
    VERBS,
    PRONOUNS,
    DETERMINERS,
    ADJECTIVES,
    VerbType,
    Noun,
    Verb,
    PersonalPronoun,
)


class SyntacticGUI(tk.Tk):
    """Main application window for SVO Syntactic Generator."""

    def __init__(self):
        super().__init__()

        self.title("SVO Sentence Generator — Analiza Syntaktyczna (NLP)")
        self.geometry("1150x820")
        self.minsize(980, 700)

        self.generator = SentenceGenerator()
        self.last_generated: Optional[GeneratedSentence] = None
        self.last_batch: List[GeneratedSentence] = []

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.style = ttk.Style(self)
        available_themes = self.style.theme_names()
        if "clam" in available_themes:
            self.style.theme_use("clam")

        self.configure(bg="#F4F6F9")
        self.style.configure(".", background="#F4F6F9", font=("Segoe UI", 10))
        self.style.configure("TLabelframe", background="#FFFFFF", relief="groove")
        self.style.configure("TLabelframe.Label", background="#FFFFFF", font=("Segoe UI", 10, "bold"), foreground="#1E293B")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _create_widgets(self):
        # Header banner
        header_frame = tk.Frame(self, bg="#1E3A8A", height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="SVO Sentence Generator — Analiza Syntaktyczna",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#1E3A8A",
        )
        title_lbl.pack(anchor="w", padx=20, pady=(10, 0))

        sub_lbl = tk.Label(
            header_frame,
            text="Generator zdań prostych (12 czasów, 5 trybów, strona czynna/bierna, czasowniki przechodnie, nieprzechodnie i zwrotne)",
            font=("Segoe UI", 9),
            fg="#93C5FD",
            bg="#1E3A8A",
        )
        sub_lbl.pack(anchor="w", padx=20, pady=(0, 10))

        # Main Layout: Left (Controls), Right (Outputs)
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # -------------------------------------------------------------
        # LEFT PANEL: Parameters & Controls with Scrollable Canvas
        # -------------------------------------------------------------
        left_container = ttk.Frame(main_pane)
        main_pane.add(left_container, weight=1)

        left_canvas = tk.Canvas(left_container, bg="#F4F6F9", highlightthickness=0)
        left_scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=left_canvas.yview)
        self.scrollable_left = ttk.Frame(left_canvas, padding=4)

        self.scrollable_left.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")),
        )
        left_canvas.create_window((0, 0), window=self.scrollable_left, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        left_scrollbar.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)

        left_frame = self.scrollable_left

        # 1. Grammar Features Labelframe
        gf_frame = ttk.LabelFrame(left_frame, text=" 1. Cechy gramatyczne (Grammar Features) ", padding=8)
        gf_frame.pack(fill=tk.X, pady=(0, 6))

        # Tense
        ttk.Label(gf_frame, text="Czas gramatyczny:").grid(row=0, column=0, sticky="w", pady=3)
        self.tense_var = tk.StringVar(value="(Random / Dowolny)")
        tense_values = ["(Random / Dowolny)"] + [t.value for t in Tense]
        self.tense_combo = ttk.Combobox(gf_frame, textvariable=self.tense_var, values=tense_values, state="readonly", width=26)
        self.tense_combo.grid(row=0, column=1, sticky="ew", pady=3, padx=(6, 0))

        # Mood
        ttk.Label(gf_frame, text="Tryb wypowiedzi:").grid(row=1, column=0, sticky="w", pady=3)
        self.mood_var = tk.StringVar(value="(Random / Dowolny)")
        mood_values = ["(Random / Dowolny)"] + [m.value for m in Mood]
        self.mood_combo = ttk.Combobox(gf_frame, textvariable=self.mood_var, values=mood_values, state="readonly", width=26)
        self.mood_combo.grid(row=1, column=1, sticky="ew", pady=3, padx=(6, 0))

        # Voice
        ttk.Label(gf_frame, text="Strona czasownika:").grid(row=2, column=0, sticky="w", pady=3)
        self.voice_var = tk.StringVar(value="(Random / Dowolny)")
        voice_values = ["(Random / Dowolny)"] + [v.value for v in Voice]
        self.voice_combo = ttk.Combobox(gf_frame, textvariable=self.voice_var, values=voice_values, state="readonly", width=26)
        self.voice_combo.grid(row=2, column=1, sticky="ew", pady=3, padx=(6, 0))

        # 2. Verb & Predicate Labelframe
        v_frame = ttk.LabelFrame(left_frame, text=" 2. Czasownik / Orzeczenie (Verb & Type) ", padding=8)
        v_frame.pack(fill=tk.X, pady=(0, 6))

        # Verb Type
        ttk.Label(v_frame, text="Kategoria czasownika:").grid(row=0, column=0, sticky="w", pady=3)
        self.verb_type_var = tk.StringVar(value="(Random / Dowolna)")
        verb_type_values = ["(Random / Dowolna)", "Transitive (Przechodni - SVO)", "Intransitive (Nieprzechodni - SV)", "Reflexive (Zwrotny - S + V + refl)"]
        self.verb_type_combo = ttk.Combobox(v_frame, textvariable=self.verb_type_var, values=verb_type_values, state="readonly", width=26)
        self.verb_type_combo.grid(row=0, column=1, sticky="ew", pady=3, padx=(6, 0))
        self.verb_type_combo.bind("<<ComboboxSelected>>", self._on_verb_type_changed)

        # Specific Verb
        ttk.Label(v_frame, text="Konkretny czasownik:").grid(row=1, column=0, sticky="w", pady=3)
        self.specific_verb_var = tk.StringVar(value="(Random / Dowolny)")
        self.specific_verb_combo = ttk.Combobox(v_frame, textvariable=self.specific_verb_var, state="readonly", width=26)
        self.specific_verb_combo.grid(row=1, column=1, sticky="ew", pady=3, padx=(6, 0))
        self._populate_verb_list()

        # 3. Noun Phrases (Subject & Object)
        np_frame = ttk.LabelFrame(left_frame, text=" 3. Podmiot i Dopełnienie (Subject & Object) ", padding=8)
        np_frame.pack(fill=tk.X, pady=(0, 6))

        # --- SUBSECTION: SUBJECT ---
        ttk.Label(np_frame, text="PODMIOT (Subject):", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 2))

        ttk.Label(np_frame, text="Typ podmiotu:").grid(row=1, column=0, sticky="w", pady=2)
        self.subj_type_var = tk.StringVar(value="(Random / Dowolny)")
        self.subj_type_combo = ttk.Combobox(
            np_frame,
            textvariable=self.subj_type_var,
            values=["(Random / Dowolny)", "Fraza z rzeczownikiem (Noun Phrase)", "Zaimek osobowy (Personal Pronoun)"],
            state="readonly",
            width=26,
        )
        self.subj_type_combo.grid(row=1, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.subj_type_combo.bind("<<ComboboxSelected>>", self._on_subj_type_changed)

        ttk.Label(np_frame, text="Rzeczownik w podmiocie:").grid(row=2, column=0, sticky="w", pady=2)
        self.specific_subj_noun_var = tk.StringVar(value="(Random / Dowolny)")
        noun_choices = ["(Random / Dowolny)"] + sorted({n.singular for n in NOUNS})
        self.specific_subj_noun_combo = ttk.Combobox(np_frame, textvariable=self.specific_subj_noun_var, values=noun_choices, state="readonly", width=26)
        self.specific_subj_noun_combo.grid(row=2, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.specific_subj_noun_combo.bind("<<ComboboxSelected>>", self._on_subj_noun_selected)

        ttk.Label(np_frame, text="Zaimek w podmiocie:").grid(row=3, column=0, sticky="w", pady=2)
        self.specific_subj_pron_var = tk.StringVar(value="(Random / Dowolny)")
        pron_choices = ["(Random / Dowolny)"] + [p.subject for p in PRONOUNS]
        self.specific_subj_pron_combo = ttk.Combobox(np_frame, textvariable=self.specific_subj_pron_var, values=pron_choices, state="readonly", width=26)
        self.specific_subj_pron_combo.grid(row=3, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.specific_subj_pron_combo.bind("<<ComboboxSelected>>", self._on_subj_pron_selected)

        # Separator between Subject and Object
        ttk.Separator(np_frame, orient="horizontal").grid(row=4, column=0, columnspan=2, sticky="ew", pady=6)

        # --- SUBSECTION: OBJECT ---
        ttk.Label(np_frame, text="DOPEŁNIENIE BLIŻSZE (Direct Object):", font=("Segoe UI", 9, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(2, 2))

        ttk.Label(np_frame, text="Typ dopełnienia:").grid(row=6, column=0, sticky="w", pady=2)
        self.obj_type_var = tk.StringVar(value="(Random / Dowolny)")
        self.obj_type_combo = ttk.Combobox(
            np_frame,
            textvariable=self.obj_type_var,
            values=["(Random / Dowolny)", "Fraza z rzeczownikiem (Noun Phrase)", "Zaimek osobowy (Personal Pronoun)"],
            state="readonly",
            width=26,
        )
        self.obj_type_combo.grid(row=6, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.obj_type_combo.bind("<<ComboboxSelected>>", self._on_obj_type_changed)

        ttk.Label(np_frame, text="Rzeczownik w dopełnieniu:").grid(row=7, column=0, sticky="w", pady=2)
        self.specific_obj_noun_var = tk.StringVar(value="(Random / Dowolny)")
        self.specific_obj_noun_combo = ttk.Combobox(np_frame, textvariable=self.specific_obj_noun_var, values=noun_choices, state="readonly", width=26)
        self.specific_obj_noun_combo.grid(row=7, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.specific_obj_noun_combo.bind("<<ComboboxSelected>>", self._on_obj_noun_selected)

        ttk.Label(np_frame, text="Zaimek w dopełnieniu:").grid(row=8, column=0, sticky="w", pady=2)
        self.specific_obj_pron_var = tk.StringVar(value="(Random / Dowolny)")
        obj_pron_choices = ["(Random / Dowolny)"] + [p.object_form for p in PRONOUNS]
        self.specific_obj_pron_combo = ttk.Combobox(np_frame, textvariable=self.specific_obj_pron_var, values=obj_pron_choices, state="readonly", width=26)
        self.specific_obj_pron_combo.grid(row=8, column=1, sticky="ew", pady=2, padx=(6, 0))
        self.specific_obj_pron_combo.bind("<<ComboboxSelected>>", self._on_obj_pron_selected)

        # Include Adjectives
        self.incl_adj_var = tk.BooleanVar(value=True)
        self.adj_check = ttk.Checkbutton(np_frame, text="Uwzględniaj przymiotniki we frazach NP", variable=self.incl_adj_var)
        self.adj_check.grid(row=9, column=0, columnspan=2, sticky="w", pady=(6, 2))

        # Action Buttons Frame
        btn_frame = ttk.LabelFrame(left_frame, text=" Akcje i generowanie ", padding=8)
        btn_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        self.btn_random = tk.Button(
            btn_frame,
            text="🎲 Wylosuj zdanie (Pełna losowość)",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_generate_random,
        )
        self.btn_random.pack(fill=tk.X, pady=3)

        self.btn_param = tk.Button(
            btn_frame,
            text="⚙️ Wygeneruj z ustawionymi parametrami",
            font=("Segoe UI", 10, "bold"),
            bg="#059669",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_generate_configured,
        )
        self.btn_param.pack(fill=tk.X, pady=3)

        self.btn_matrix = tk.Button(
            btn_frame,
            text="📋 Wygeneruj matrycę 12 czasów dla tego zdania",
            font=("Segoe UI", 9, "bold"),
            bg="#7C3AED",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_generate_12_tenses,
        )
        self.btn_matrix.pack(fill=tk.X, pady=3)

        # -------------------------------------------------------------
        # RIGHT PANEL: Output Displays (Tabs: Result, Matrix)
        # -------------------------------------------------------------
        right_frame = ttk.Frame(main_pane, padding=6)
        main_pane.add(right_frame, weight=2)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Single Sentence View
        tab_single = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_single, text="  Aktualne zdanie (SVO)  ")

        # Sentence Box (Prominent card)
        sent_card = tk.Frame(tab_single, bg="#FFFFFF", relief="solid", bd=1)
        sent_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            sent_card,
            text="WYGENEROWANE ZDANIE:",
            font=("Segoe UI", 9, "bold"),
            fg="#64748B",
            bg="#FFFFFF",
        ).pack(anchor="w", padx=14, pady=(10, 2))

        self.sent_display_lbl = tk.Label(
            sent_card,
            text="(Kliknij przycisk po lewej, aby wygenerować zdanie)",
            font=("Segoe UI", 15, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
            wraplength=600,
            justify="left",
        )
        self.sent_display_lbl.pack(anchor="w", padx=14, pady=(2, 12))

        # Copy button
        copy_btn = tk.Button(
            sent_card,
            text="📋 Kopiuj zdanie",
            font=("Segoe UI", 8),
            bg="#E2E8F0",
            relief="flat",
            cursor="hand2",
            command=self.on_copy_sentence,
        )
        copy_btn.pack(anchor="e", padx=14, pady=(0, 10))

        # Grammatical Breakdown Table
        breakdown_frame = ttk.LabelFrame(tab_single, text=" Rozbiór gramatyczny ", padding=8)
        breakdown_frame.pack(fill=tk.X, pady=(0, 10))

        self.breakdown_tree = ttk.Treeview(
            breakdown_frame,
            columns=("Element", "Wartość / Funkcja"),
            show="headings",
            height=6,
        )
        self.breakdown_tree.heading("Element", text="Komponent / Kategoria")
        self.breakdown_tree.heading("Wartość / Funkcja", text="Wartość w zdaniu")
        self.breakdown_tree.column("Element", width=180, anchor="w")
        self.breakdown_tree.column("Wartość / Funkcja", width=420, anchor="w")
        self.breakdown_tree.pack(fill=tk.X)

        # Syntax Tree Box
        tree_frame = ttk.LabelFrame(tab_single, text=" Drzewo struktury syntaktycznej ", padding=8)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_text = tk.Text(tree_frame, font=("Consolas", 10), bg="#F8FAFC", wrap="none")
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_text.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_text.xview)
        self.tree_text.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_text.pack(fill=tk.BOTH, expand=True)

        # Tab 2: Batch / Matrix Table View
        tab_matrix = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_matrix, text="  Matryca 12 czasów  ")

        matrix_top_frame = ttk.Frame(tab_matrix)
        matrix_top_frame.pack(fill=tk.X, pady=(0, 6))

        self.matrix_info_lbl = tk.Label(
            matrix_top_frame,
            text="Tabela odmiany aktualnego zdania we wszystkich 12 czasach gramatycznych:",
            font=("Segoe UI", 9, "bold"),
            fg="#1E3A8A",
        )
        self.matrix_info_lbl.pack(side=tk.LEFT)

        self.matrix_tree = ttk.Treeview(
            tab_matrix,
            columns=("Tense", "Sentence"),
            show="headings",
        )
        self.matrix_tree.heading("Tense", text="Czas gramatyczny (Tense)")
        self.matrix_tree.heading("Sentence", text="Zdanie w danym czasie")
        self.matrix_tree.column("Tense", width=220, anchor="w")
        self.matrix_tree.column("Sentence", width=500, anchor="w")

        matrix_scroll_y = ttk.Scrollbar(tab_matrix, orient=tk.VERTICAL, command=self.matrix_tree.yview)
        self.matrix_tree.configure(yscrollcommand=matrix_scroll_y.set)
        matrix_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.matrix_tree.pack(fill=tk.BOTH, expand=True)

        # Generate initial random sentence
        self.on_generate_random()

    # -------------------------------------------------------------
    # INTERACTIVE SYNCHRONIZATION HANDLERS
    # -------------------------------------------------------------
    def _populate_verb_list(self):
        type_choice = self.verb_type_var.get()
        if "Transitive" in type_choice:
            filtered = [v.base for v in VERBS if v.verb_type == VerbType.TRANSITIVE]
        elif "Intransitive" in type_choice:
            filtered = [v.base for v in VERBS if v.verb_type == VerbType.INTRANSITIVE]
        elif "Reflexive" in type_choice:
            filtered = [v.base for v in VERBS if v.verb_type == VerbType.REFLEXIVE]
        else:
            filtered = [v.base for v in VERBS]

        self.specific_verb_combo["values"] = ["(Random / Dowolny)"] + sorted(filtered)
        self.specific_verb_var.set("(Random / Dowolny)")

    def _on_verb_type_changed(self, event=None):
        self._populate_verb_list()

    def _on_subj_type_changed(self, event=None):
        choice = self.subj_type_var.get()
        if "Pronoun" in choice or "Zaimek" in choice:
            self.specific_subj_noun_var.set("(Random / Dowolny)")
        elif "Noun Phrase" in choice or "rzeczownik" in choice:
            self.specific_subj_pron_var.set("(Random / Dowolny)")

    def _on_subj_noun_selected(self, event=None):
        val = self.specific_subj_noun_var.get()
        if val != "(Random / Dowolny)":
            self.subj_type_var.set("Fraza z rzeczownikiem (Noun Phrase)")
            self.specific_subj_pron_var.set("(Random / Dowolny)")

    def _on_subj_pron_selected(self, event=None):
        val = self.specific_subj_pron_var.get()
        if val != "(Random / Dowolny)":
            self.subj_type_var.set("Zaimek osobowy (Personal Pronoun)")
            self.specific_subj_noun_var.set("(Random / Dowolny)")

    def _on_obj_type_changed(self, event=None):
        choice = self.obj_type_var.get()
        if "Pronoun" in choice or "Zaimek" in choice:
            self.specific_obj_noun_var.set("(Random / Dowolny)")
        elif "Noun Phrase" in choice or "rzeczownik" in choice:
            self.specific_obj_pron_var.set("(Random / Dowolny)")

    def _on_obj_noun_selected(self, event=None):
        val = self.specific_obj_noun_var.get()
        if val != "(Random / Dowolny)":
            self.obj_type_var.set("Fraza z rzeczownikiem (Noun Phrase)")
            self.specific_obj_pron_var.set("(Random / Dowolny)")

    def _on_obj_pron_selected(self, event=None):
        val = self.specific_obj_pron_var.get()
        if val != "(Random / Dowolny)":
            self.obj_type_var.set("Zaimek osobowy (Personal Pronoun)")
            self.specific_obj_noun_var.set("(Random / Dowolny)")

    # -------------------------------------------------------------
    # GENERATION LOGIC
    # -------------------------------------------------------------
    def on_generate_random(self):
        sent = self.generator.generate(include_adjectives=self.incl_adj_var.get())
        self._display_sentence(sent)

    def on_generate_configured(self):
        # 1. Resolve Tense
        tense = None
        if self.tense_var.get() != "(Random / Dowolny)":
            tense = next((t for t in Tense if t.value == self.tense_var.get()), None)

        # 2. Resolve Mood
        mood = None
        if self.mood_var.get() != "(Random / Dowolny)":
            mood = next((m for m in Mood if m.value == self.mood_var.get()), None)

        # 3. Resolve Voice
        voice = None
        if self.voice_var.get() != "(Random / Dowolny)":
            voice = next((v for v in Voice if v.value == self.voice_var.get()), None)

        # 4. Resolve Verb Type
        v_type = None
        if "Transitive" in self.verb_type_var.get():
            v_type = VerbType.TRANSITIVE
        elif "Intransitive" in self.verb_type_var.get():
            v_type = VerbType.INTRANSITIVE
        elif "Reflexive" in self.verb_type_var.get():
            v_type = VerbType.REFLEXIVE

        # 5. Resolve Specific Verb
        verb = None
        if self.specific_verb_var.get() != "(Random / Dowolny)":
            verb = next((v for v in VERBS if v.base == self.specific_verb_var.get()), None)

        # 6. BULLETPROOF SUBJECT RESOLUTION
        # If the user selected a specific noun, THAT NOUN IS ABSOLUTE PRIORITY!
        subject: Optional[NounPhrase] = None
        subj_noun_val = self.specific_subj_noun_var.get()
        subj_pron_val = self.specific_subj_pron_var.get()

        if subj_noun_val != "(Random / Dowolny)":
            n = next((n for n in NOUNS if n.singular == subj_noun_val), None)
            if n:
                subject = self.generator.create_noun_phrase(
                    noun=n,
                    include_adjectives=self.incl_adj_var.get(),
                )
        elif subj_pron_val != "(Random / Dowolny)":
            p = next((p for p in PRONOUNS if p.subject == subj_pron_val), None)
            if p:
                subject = self.generator.create_noun_phrase(pronoun=p)
        else:
            # Fall back to general type selector
            subj_type_choice = self.subj_type_var.get()
            if "Zaimek" in subj_type_choice or "Pronoun" in subj_type_choice:
                subject = self.generator.random_noun_phrase(force_pronoun=True)
            elif "Fraza" in subj_type_choice or "Noun Phrase" in subj_type_choice:
                subject = self.generator.random_noun_phrase(allow_pronoun=False, include_adjective=self.incl_adj_var.get())
            else:
                subject = None

        # 7. BULLETPROOF OBJECT RESOLUTION
        direct_object: Optional[NounPhrase] = None
        obj_noun_val = self.specific_obj_noun_var.get()
        obj_pron_val = self.specific_obj_pron_var.get()

        if obj_noun_val != "(Random / Dowolny)":
            n_obj = next((n for n in NOUNS if n.singular == obj_noun_val), None)
            if n_obj:
                direct_object = self.generator.create_noun_phrase(
                    noun=n_obj,
                    include_adjectives=self.incl_adj_var.get(),
                )
        elif obj_pron_val != "(Random / Dowolny)":
            p_obj = next((p for p in PRONOUNS if p.object_form == obj_pron_val), None)
            if p_obj:
                direct_object = self.generator.create_noun_phrase(pronoun=p_obj)
        else:
            # Fall back to general type selector
            obj_type_choice = self.obj_type_var.get()
            if "Zaimek" in obj_type_choice or "Pronoun" in obj_type_choice:
                direct_object = self.generator.random_noun_phrase(force_pronoun=True)
            elif "Fraza" in obj_type_choice or "Noun Phrase" in obj_type_choice:
                direct_object = self.generator.random_noun_phrase(allow_pronoun=False, include_adjective=self.incl_adj_var.get())
            else:
                direct_object = None

        sent = self.generator.generate(
            tense=tense,
            mood=mood,
            voice=voice,
            verb=verb,
            verb_type=v_type,
            subject=subject,
            direct_object=direct_object,
            include_adjectives=self.incl_adj_var.get(),
        )
        self._display_sentence(sent)

    def on_generate_12_tenses(self):
        """Generates all 12 tenses for the exact current sentence (same subject, verb, and object)."""
        if not self.last_generated:
            self.on_generate_random()

        current = self.last_generated
        assert current is not None

        # Use the EXACT subject, verb, object, voice and mood from the current sentence!
        verb = current.verb_obj or next((v for v in VERBS if v.base == current.verb_base), VERBS[0])
        subj = current.subject_np or self.generator.random_noun_phrase(allow_pronoun=False)
        obj = current.object_np
        voice = current.voice
        mood = current.mood if current.mood != Mood.IMPERATIVE else Mood.INDICATIVE

        sentences = self.generator.generate_tense_matrix_for_pair(
            subject=subj,
            verb=verb,
            direct_object=obj,
            mood=mood,
            voice=voice,
        )

        self.last_batch = sentences

        # Clear and populate matrix tree
        for row in self.matrix_tree.get_children():
            self.matrix_tree.delete(row)

        for s in sentences:
            self.matrix_tree.insert("", tk.END, values=(s.tense.value, s.text))

        if hasattr(self, "matrix_info_lbl"):
            self.matrix_info_lbl.config(
                text=f"Odmiana aktualnego zdania: '{current.text}' ({voice.value}, {mood.value}):"
            )

        # Switch to matrix tab
        self.notebook.select(1)

    def _display_sentence(self, sent: GeneratedSentence):
        self.last_generated = sent
        self.sent_display_lbl.config(text=sent.text)

        # Clear and populate breakdown tree
        for row in self.breakdown_tree.get_children():
            self.breakdown_tree.delete(row)

        details = [
            ("Czas gramatyczny (Tense)", sent.tense.value),
            ("Tryb (Mood)", sent.mood.value),
            ("Strona (Voice)", sent.voice.value),
            ("Kategoria czasownika", sent.verb_type.value.capitalize()),
            ("Podmiot (Subject)", sent.subject_str),
            ("Orzeczenie (Predicate)", sent.predicate_str),
        ]
        if sent.object_str:
            role = "Zaimek zwrotny" if sent.verb_type == VerbType.REFLEXIVE else "Dopełnienie bliższe (Object)"
            details.append((role, sent.object_str))
        if sent.agent_str:
            details.append(("Wykonawca (Agent by-phrase)", sent.agent_str))

        for k, v in details:
            self.breakdown_tree.insert("", tk.END, values=(k, v))

        # Update syntax tree
        self.tree_text.delete("1.0", tk.END)
        self.tree_text.insert(tk.END, sent.syntax_tree)

    def on_copy_sentence(self):
        if self.last_generated:
            self.clipboard_clear()
            self.clipboard_append(self.last_generated.text)
            messagebox.showinfo("Skopiowano", f"Zdanie skopiowane do schowka:\n\n{self.last_generated.text}")


def main():
    app = SyntacticGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
