import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import os
import music21
from music21 import converter, midi

# Temporary directory to store uploaded files and processed images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def convert_to_midi(file_path):
    try:
        # Convert PDF to images (if PDF)
        if file_path.endswith('.pdf'):
            images = convert_from_path(file_path)
            image_path = os.path.join(UPLOAD_FOLDER, "converted_image.png")
            images[0].save(image_path, 'PNG')
        else:
            image_path = file_path

        # Perform OMR (this is a placeholder; you'll need to integrate an OMR tool)
        # For now, we'll assume the OMR step is done and we have a MusicXML file
        musicxml_path = os.path.join(UPLOAD_FOLDER, "output.musicxml")
        # Here you would call your OMR tool to generate the MusicXML file
        # For example, you could use Audiveris or another OMR library

        # Convert MusicXML to MIDI
        score = converter.parse(musicxml_path)
        midi_path = os.path.join(UPLOAD_FOLDER, "output.mid")
        mf = midi.translate.music21ObjectToMidiFile(score)
        mf.open(midi_path, 'wb')
        mf.write()
        mf.close()

        return midi_path
    except Exception as e:
        raise Exception(f"Error during conversion: {str(e)}")

def upload_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("PDF Files", "*.pdf")]
    )
    if not file_path:
        return

    try:
        midi_path = convert_to_midi(file_path)
        messagebox.showinfo("Success", f"MIDI file generated successfully!\nSaved at: {midi_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the GUI
try:
    root = tk.Tk()
    root.title("Sheet Music to MIDI Converter")

    # Add a button to upload a file
    upload_button = tk.Button(root, text="Upload Sheet Music", command=upload_file)
    upload_button.pack(pady=20)

    # Run the GUI
    root.mainloop()
except Exception as e:
    print(f"Failed to start GUI: {str(e)}")
    input("Press any key to exit...")