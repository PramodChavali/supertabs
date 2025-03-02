import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from music21 import converter
import music21

# Temporary directory to store uploaded files and processed files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Specify the path to the Audiveris executable
AUDIVERIS_PATH = r"D:\vs code\python\New folder\Audiveris\bin\Audiveris.bat"  # Update this path as needed

def convert_pdf_to_midi(file_path):
    try:
        # Step 1: Convert PDF to MusicXML using Audiveris (OMR)
        musicxml_path = os.path.join(UPLOAD_FOLDER, "output.musicxml")
        
        # Debug: Print the command being executed
        command = [AUDIVERIS_PATH, "-batch", "-output", musicxml_path, file_path]
        print(f"Executing command: {' '.join(command)}")
        
        # Run Audiveris
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Audiveris output: {result.stdout}")
        print(f"Audiveris errors: {result.stderr}")

        # Verify the MusicXML file was created
        if not os.path.exists(musicxml_path):
            raise Exception(f"MusicXML file not found at: {musicxml_path}")

        # Step 2: Convert MusicXML to MIDI using music21
        midi_path = os.path.join(UPLOAD_FOLDER, "output.mid")
        print(f"Parsing MusicXML file: {musicxml_path}")
        score = converter.parse(musicxml_path)
        print(f"Writing MIDI file: {midi_path}")
        score.write("midi", midi_path)

        return midi_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"Audiveris failed: {e.stderr}")
    except Exception as e:
        raise Exception(f"Error during conversion: {str(e)}")

def upload_file():
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not file_path:
        return

    try:
        midi_path = convert_pdf_to_midi(file_path)
        messagebox.showinfo("Success", f"MIDI file generated successfully!\nSaved at: {midi_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the GUI
root = tk.Tk()
root.title("Sheet Music to MIDI Converter")

# Add a button to upload a file
upload_button = tk.Button(root, text="Upload PDF", command=upload_file)
upload_button.pack(pady=20)

# Run the GUI
root.mainloop()