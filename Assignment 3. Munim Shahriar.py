# Notebook & Tabs

    def create_notebook(self):
        self.notebook = tb.Notebook(self, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)
        self.tab_input = tb.Frame(self.notebook)
        self.tab_output = tb.Frame(self.notebook)
        self.tab_explain = tb.Frame(self.notebook)
        self.tab_model = tb.Frame(self.notebook)
        self.notebook.add(self.tab_input, text="Input")
        self.notebook.add(self.tab_output, text="Output")
        self.notebook.add(self.tab_explain, text="OOP Explanations")
        self.notebook.add(self.tab_model, text="Model Info")

    # Input Tab

    def create_input_tab(self):
        card = tb.Frame(self.tab_input, bootstyle="secondary", padding=15, relief="raised", borderwidth=2)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tb.Label(card, text="Select AI Model:", font=self.title_font).pack(pady=10)
        self.choice = tk.StringVar(value="text-generation")
        model_cb = tb.Combobox(card, textvariable=self.choice,
                               values=["text-generation", "image-classification", "text-to-image"], width=40)
        model_cb.pack(pady=10)
        model_cb.bind("<<ComboboxSelected>>", self.update_input_field)

        self.input_frame = tb.Frame(card)
        self.input_frame.pack(pady=10, fill="x")
        self.create_text_input()

        btn_frame = tb.Frame(card)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text="Browse File", bootstyle="outline-info", width=15,
                  command=self.browse_file).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Run Model", bootstyle="success", width=15,
                  command=self.start_model_thread).pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Save Image", bootstyle="warning", width=15,
                  command=self.save_image).pack(side=LEFT, padx=5)

# Progress bar

        self.progress = tb.Progressbar(card, mode="indeterminate", bootstyle="danger-striped")
        self.progress.pack(fill="x", pady=10)

    def update_input_field(self, event=None):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.input_text = None
        self.file_label = None

        task = self.choice.get()
        if task in ["text-generation", "text-to-image"]:
            self.create_text_input()
        else:
            tb.Label(self.input_frame, text="Choose Image File:", font=self.label_font).pack(pady=5)
            self.file_label = tb.Label(self.input_frame, text="No file selected", font=self.label_font, bootstyle="secondary")
            self.file_label.pack(pady=5)

    def create_text_input(self):
        tb.Label(self.input_frame, text="Enter Prompt:", font=self.label_font).pack(pady=5)
        self.input_text = tb.Entry(self.input_frame, width=70, bootstyle="dark")
        self.input_text.pack(pady=5)

# Output Tab

    def create_output_tab(self):
        card = tb.Frame(self.tab_output, bootstyle="light", padding=15, relief="raised", borderwidth=2)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        self.output_text = ScrolledText(card, height=20, wrap="word", font=("Segoe UI", 11))
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_label = tb.Label(card)
        self.image_label.pack(pady=15)
        self.image_label.bind("<Button-1>", self.zoom_image)

# Other Tabs

    def create_explain_tab(self):
        tb.Label(self.tab_explain, text="OOP Concepts Used", font=self.title_font).pack(pady=10)
        self.explain_text = ScrolledText(self.tab_explain, height=25, wrap="word", font=("Segoe UI", 11))
        self.explain_text.pack(fill="both", expand=True, padx=15, pady=15)
        tb.Button(self.tab_explain, text="Show Explanations", bootstyle="info",
                  command=self.show_explanations).pack(pady=10)

    def create_model_tab(self):
        tb.Label(self.tab_model, text="AI Models Information", font=self.title_font).pack(pady=10)
        self.model_info_box = ScrolledText(self.tab_model, height=25, wrap="word", font=("Segoe UI", 11))
        self.model_info_box.pack(fill="both", expand=True, padx=15, pady=15)
        tb.Button(self.tab_model, text="Show Model Info", bootstyle="warning",
                  command=self.show_model_info).pack(pady=10)