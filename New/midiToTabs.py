from music21 import converter, note, chord
from PDFtoMXL import *
import subprocess
import os
from itertools import product
import tkinter as tk

class PDFtoTabConverter:
    
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Tablature Converter")
        self.root.geometry("500x300")

        # Label
        self.label = tk.Label(root, text="Upload a PDF file:", font=("Arial", 12))
        self.label.pack(pady=10)

        # Upload Button
        self.upload_btn = tk.Button(root, text="Upload PDF", command=self.upload_pdf, font=("Arial", 12))
        self.upload_btn.pack(pady=5)

        # File Path Display
        self.file_label = tk.Label(root, text="No file selected", font=("Arial", 10), fg="gray")
        self.file_label.pack(pady=5)

        # Process Button
        self.process_btn = tk.Button(root, text="Convert to Tablature", command=self.process_pdf, font=("Arial", 12))
        self.process_btn.pack(pady=20)

        # Store the selected file path
        self.file_path = None

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path), fg="black")

    def process_pdf(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a PDF first!")
            return
        
        # Replace this with your actual processing function
        messagebox.showinfo("Processing", f"Processing {self.file_path}...")

        # Example of calling your function:
        # result = your_function(self.file_path)
        # messagebox.showinfo("Success", "Processing complete!")

root = tk.Tk()

inputPDF = "TestScore.pdf"
inputXML = Get_XML_From_PDF(inputPDF)

# close the bat file that runs the ai

strings = ["null", "E4", "B3", "G3", "D3", "A2", "E2"]
noteArray = []
beats = 0

numFrets = 22

# "E4", "B3", "G3", "D3", "A2", "E2"

firstString = ["E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6"]
secondString = ["B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5"]
thirdString = ["G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5"]
fourthString = ["D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"]
fifthString = ["A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4"]
sixthString = ["E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4"]

def convert_musicxml_to_midi(musicxml_path, midi_path):
    try:
        # Parse the MusicXML file
        temp = converter.parse(musicxml_path)
        
        # Write the score to a MIDI file
        temp.write("midi", midi_path)
        
        print(f"MIDI file saved to: {midi_path}")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")

# Path to the MusicXML file
# get mxl name and stuff

midi_path = "OUTPUTS\output.mid"  # fix later
xml_path = "PDFInputs\TestScore.mxl" #fix this
# Path to save the MIDI file

# Convert MusicXML to MIDI
convert_musicxml_to_midi(xml_path, midi_path)


def getNoteInfo(note):
    noteValue = note.name
    noteOctave = note.octave
    fullNote = str(noteValue) + str(noteOctave)
    return fullNote

noteMap = [
    "0",
    firstString, 
    secondString, 
    thirdString, 
    fourthString, 
    fifthString, 
    sixthString
]



# Load MIDI file
score = converter.parse(midi_path)

# Initialize an array to store notes and a beats counter
notes_list = []
chordArray = []
beats_counter = 0.0

# Iterate through all parts and extract notes
for part in score.parts:
    for element in part.recurse():  # Recursively go through elements
        if isinstance(element, note.Note):  # If it's a single note
            notes_list.append(element.nameWithOctave)  # Store note in scientific pitch notation
            beats_counter += element.duration.quarterLength  # Add duration in beats
        elif isinstance(element, chord.Chord):  # If it's a chord
            for chord_note in element:
                chordArray.append(chord_note.nameWithOctave)
                    # Go through all notes in the chord
            notes_list.append(chordArray)  # Store note in scientific pitch notation


# Output results
print("Extracted Notes:", notes_list)
print("Total Beats:", beats_counter)

def find_all_note_positions(note, noteMap):
    """
    Given a note, return all possible (string_index, fret_index) positions on the guitar.
   
    Arguments:
    note -- the note to search for (e.g., "E4")
    noteMap -- the mapping of notes on all the guitar strings
   
    Returns:
    list -- a list of tuples (string_index, fret_index) where the note appears
    """
    positions = []
    for string_index in range(1, 7):  # Iterating from string 1 (high E) to string 6 (low E)
        if note in noteMap[string_index]:
            fret_index = noteMap[string_index].index(note)
            positions.append((string_index, fret_index))
   
    return positions

def find_all_note_positions(note, noteMap):
    """
    Given a note, return all possible (string_index, fret_index) positions on the guitar.
   
    Arguments:
    note -- the note to search for (e.g., "E4")
    noteMap -- the mapping of notes on all the guitar strings
   
    Returns:
    list -- a list of tuples (string_index, fret_index) where the note appears
    """
    positions = []
    for string_index in range(1, 7):  # Iterating from string 1 (high E) to string 6 (low E)
        if note in noteMap[string_index]:
            fret_index = noteMap[string_index].index(note)
            positions.append((string_index, fret_index))
   
    return positions

def get_shortest_horizontal_distance_and_positions(notes, noteMap):
    """
    Given a list of notes, find the best fretboard positions that minimize horizontal movement.
    This avoids brute-force checking of all orders.
    """
    # Step 1: Get all possible fretboard positions for each note
    note_positions = [find_all_note_positions(note, noteMap) for note in notes]

    # Step 2: Instead of product(), generate only unique combinations of note positions
    min_distance = float('inf')
    best_combo = None

    for combo in zip(*note_positions):  # Generates only one ordering per set of choices
        frets = [pos[1] for pos in combo]  # Extract fret numbers
        distance = max(frets) - min(frets)  # Horizontal span

        if distance < min_distance:
            min_distance = distance
            best_combo = combo

    # Convert best positions into readable format
    positions = [f"S{best_combo[i][0]} F{best_combo[i][1]}" for i in range(len(best_combo))]

    return min_distance, positions


# Calculate the shortest horizontal distance and corresponding positions
distance, positions = get_shortest_horizontal_distance_and_positions(notes_list, noteMap)

# Output the result
print(f"The shortest total horizontal distance between the notes\n{notes_list} is {distance} fret(s).")
print("The corresponding positions (string and fret coordinates) are")


stringNums = []
fretNums = []

for i in range(len(positions)):
    stringNums.append(positions[i][1])

    try:
        fretNums.append(positions[i][4:6])

    except IndexError:
        fretNums.append(positions[i][4])



stringValues = ["null", "e", "B", "G", "D", "A", "E"] 
printedHighEString = "e |-"
printedBString = "B |-"
printedGString = "G |-"
printedDString = "D |-"
printedAString = "A |-"
printedLowEString = "E |-"

for i in range(len(positions)):
    
    spacing = "--"

    if stringNums[i] == '1':
        printedHighEString += fretNums[i] + "-"
    else:
        printedHighEString += spacing
    if stringNums[i] == '2':
        printedBString += fretNums[i] + "-"
    else:
        printedBString += spacing
    if stringNums[i] == '3':
        printedGString += fretNums[i] + "-"
    else:
        printedGString += spacing
    if stringNums[i] == '4':
        printedDString += fretNums[i] + "-"
    else:
        printedDString += spacing
    if stringNums[i] == '5':
        printedAString += fretNums[i] + "-"
    else:
        printedAString += spacing
    if stringNums[i] == '6':
        printedLowEString += fretNums[i] + "-"
    else:
        printedLowEString += spacing

file = open("OUTPUTS\FinalTabs.txt", "w")
file.write(printedHighEString + "\n")
file.write(printedBString + "\n")
file.write(printedGString + "\n")
file.write(printedDString + "\n")
file.write(printedAString + "\n")
file.write(printedLowEString + "\n")
file.close()

print(printedHighEString)
print(printedBString)
print(printedGString)   
print(printedDString)
print(printedAString)
print(printedLowEString)



    