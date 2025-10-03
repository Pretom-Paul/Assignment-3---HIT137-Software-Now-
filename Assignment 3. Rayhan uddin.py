    # Core Functions

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select File")
        if filename:
            if self.input_text:  # text entry exists
                self.input_text.delete(0, tk.END)
                self.input_text.insert(0, filename)
            elif self.file_label:  # image-classification
                self.file_label.config(text=filename)

    def start_model_thread(self):
        """Run model in separate thread with loading animation"""
        self.progress.start(10)
        thread = threading.Thread(target=self.run_model)
        thread.start()

    def run_model(self):
        try:
            task = self.choice.get()
            input_value = ""
            if self.input_text:
                input_value = self.input_text.get()
            elif self.file_label:
                input_value = self.file_label.cget("text")

            if task == "text-generation":
                model = TextGenerationModel()
                result = model.run(input_value)
                self.output_text.insert(tk.END, f"Generated Text:\n{result}\n\n")
                self.generated_image = None

            elif task == "image-classification":
                model = ImageClassificationModel()
                result = model.run(input_value)
                self.output_text.insert(tk.END, "Classification Results:\n")
                for res in result:
                    self.output_text.insert(tk.END, f" {res['label']} ({res['score']:.2f})\n")
                try:
                    img = Image.open(input_value).resize((300, 300))
                    img_tk = ImageTk.PhotoImage(img)
                    self.image_label.configure(image=img_tk)
                    self.image_label.image = img_tk
                except:
                    pass
                self.generated_image = None

            elif task == "text-to-image":
                model = TextToImageModel()
                img = model.run(input_value)
                img_resized = img.resize((400, 400))
                img_tk = ImageTk.PhotoImage(img_resized)
                self.image_label.configure(image=img_tk)
                self.image_label.image = img_tk
                self.output_text.insert(tk.END, "Image generated from text prompt!\n\n")
                self.generated_image = img

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()

    def save_image(self):
        if self.generated_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.generated_image.save(file_path)
                messagebox.showinfo("Saved", f"Image saved to {file_path}")
        else:
            messagebox.showwarning("No Image", "No generated image to save!")

    def zoom_image(self, event=None):
        if self.generated_image:
            top = Toplevel(self)
            top.title("Image Preview")
            img_tk = ImageTk.PhotoImage(self.generated_image)
            lbl = Label(top, image=img_tk)
            lbl.image = img_tk
            lbl.pack()

    def show_explanations(self):
        self.explain_text.delete("1.0", tk.END)
        for key, value in explanations().items():
            self.explain_text.insert(tk.END, f"{key}: {value}\n\n")

    def show_model_info(self):
        self.model_info_box.delete("1.0", tk.END)
        for key, value in model_info().items():
            self.model_info_box.insert(tk.END, f"{key}:\n{value}\n\n")


if __name__ == "__main__":
    app = AIApp()
    app.mainloop()