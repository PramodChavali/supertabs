import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import midiToTabs

try:
    # tkdnd is required for drag & drop
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    raise ImportError("Please install tkinterdnd2 with: pip install tkinterdnd2")

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag & Drop File App")
        self.root.geometry("500x350")
        self.root.configure(bg="#4B0082")  # Deep purple background

        self.file_path = None
        self.generated_file = "output.txt"

        # Label for drag and drop
        self.drop_label = tk.Label(
            root,
            text="Drag and drop a file here",
            relief="ridge",
            width=40,
            height=5,
            bg="#9370DB",  # Medium purple
            fg="#FFD700",  # Gold (yellow)
            font=("Arial", 12, "bold")
        )
        self.drop_label.pack(pady=30)

        # Enable drag and drop
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)

        # Button to generate text file
        self.generate_button = tk.Button(
            root,
            text="Generate Text File",
            command=self.generate_text_file,
            bg="#8A2BE2",  # Blue violet
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            padx=10,
            pady=5
        )
        self.generate_button.pack(pady=10)

        # Button to download (save as)
        self.save_button = tk.Button(
            root,
            text="Save Text File As",
            command=self.save_file,
            bg="#32CD32",  # Lime green
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            padx=10,
            pady=5
        )
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

        # Label to display status messages
        self.status_label = tk.Label(
            root,
            text="",
            bg="#4B0082",
            fg="#FFD700",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=10)

    def on_drop(self, event):
        self.file_path = event.data.strip("{}")  # Remove curly braces if present
        self.drop_label.config(text=f"File selected:\n{self.file_path}")

    def generate_text_file(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please drag and drop a file first.")
            return

        try:
            # Ensure PDFInputs directory exists
            os.makedirs("PDFInputs", exist_ok=True)

            # Copy file into PDFInputs directory
            dest_path = os.path.join("PDFInputs", os.path.basename(self.file_path))
            shutil.copy(self.file_path, dest_path)

            # Call main() from midiToTabs with copied file path
            midiToTabs.main(dest_path)

            # Point to the generated file
            self.generated_file = os.path.join("OUTPUTS", "FinalTabs.txt")

            # Update UI status
            self.status_label.config(text="File generated!")
            self.save_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate file: {e}")

    def save_file(self):
        if not os.path.exists(self.generated_file):
            messagebox.showwarning("File Missing", "Please generate the text file first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            try:
                with open(self.generated_file, "r") as src, open(save_path, "w") as dst:
                    dst.write(src.read())
                messagebox.showinfo("Saved", f"File saved as {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DragDropApp(root)
    root.mainloop()
