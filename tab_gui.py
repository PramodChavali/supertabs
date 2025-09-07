import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class TabConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Guitar Tabs Converter")
        self.root.geometry("500x400")

        # PDF file path
        self.pdf_path = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="PDF to Guitar Tabs Converter", font=("Arial", 16))
        title_label.pack(pady=20)

        # Drop area
        self.drop_frame = tk.Frame(self.root, bg="lightgray", width=400, height=100)
        self.drop_frame.pack(pady=10)
        self.drop_frame.pack_propagate(False)

        drop_label = tk.Label(self.drop_frame, text="Drag and drop PDF file here\nor click to browse", bg="lightgray")
        drop_label.pack(expand=True)

        # Bind events for drag and drop
        self.drop_frame.bind("<Button-1>", self.browse_file)
        self.drop_frame.bind("<Enter>", lambda e: self.drop_frame.config(bg="lightblue"))
        self.drop_frame.bind("<Leave>", lambda e: self.drop_frame.config(bg="lightgray"))

        # File path display
        self.file_label = tk.Label(self.root, text="No file selected", fg="gray")
        self.file_label.pack(pady=5)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert to Tabs", command=self.convert, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=5)

        # Download button
        self.download_button = tk.Button(self.root, text="Download Tabs", command=self.download, state=tk.DISABLED)
        self.download_button.pack(pady=10)

    def browse_file(self, event=None):
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.set_file(file_path)

    def set_file(self, file_path):
        self.pdf_path = file_path
        filename = os.path.basename(file_path)
        self.file_label.config(text=f"Selected: {filename}", fg="black")
        self.convert_button.config(state=tk.NORMAL)
        self.status_label.config(text="")

    def convert(self):
        if not self.pdf_path:
            return

        try:
            # Copy PDF to PDFInputs
            filename = os.path.basename(self.pdf_path)
            name_without_ext = os.path.splitext(filename)[0]
            dest_path = os.path.join("PDFInputs", filename)
            shutil.copy2(self.pdf_path, dest_path)

            self.status_label.config(text="Converting...", fg="orange")

            # Run the script with the filename
            import subprocess
            result = subprocess.run(["python", "midiToTabs.py", name_without_ext], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"Conversion failed: {result.stderr}", fg="red")
            else:
                self.status_label.config(text="Conversion complete!", fg="green")
                self.download_button.config(state=tk.NORMAL)

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")

    def download(self):
        if not os.path.exists(r"OUTPUTS\FinalTabs.txt"):
            messagebox.showerror("Error", "Tabs file not found.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Tabs File"
        )
        if save_path:
            shutil.copy2(r"OUTPUTS\FinalTabs.txt", save_path)
            messagebox.showinfo("Success", "Tabs file saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabConverterGUI(root)
    root.mainloop()