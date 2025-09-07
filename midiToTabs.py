from music21 import converter, note, chord
from PDFtoMXL import *
import subprocess
import os
from itertools import product, combinations
import tkinter as tk


filename = "CMajorChords"
inputPDF = filename +".pdf"
inputXML = Get_XML_From_PDF(inputPDF)

# close the bat file that runs the ai

strings = ["null", "E4", "B3", "G3", "D3", "A2", "E2"]
allNotes = ["A", "B", "C", "D", "E", "F", "G"]
noteArray = []
beats = 0

numFrets = 22

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

midi_path = "OUTPUTS\output.mid"
xml_path = "PDFInputs/" + filename + ".mxl"
# Path to save the MIDI file

# Convert MusicXML to MIDI
convert_musicxml_to_midi(xml_path, midi_path)



noteMap = [
    "0",
    firstString, 
    secondString, 
    thirdString, 
    fourthString, 
    fifthString, 
    sixthString
]



# ...existing code...

# Load MIDI file and extract notes
score = converter.parse(midi_path)
notes_list = []
chordArray = []
beats_counter = 0.0

# Iterate through all parts and extract notes
for part in score.parts:
    for element in part.recurse():
        if isinstance(element, note.Note):
            # Add single note
            if element.nameWithOctave in [note for string in noteMap[1:] for note in string]:
                notes_list.append(element.nameWithOctave)
                beats_counter += element.duration.quarterLength

            print(element.nameWithOctave)
        elif isinstance(element, chord.Chord):
            # Process chord notes
            valid_chord_notes = []
            for chord_note in element:

                chordArray.append(chord_note.nameWithOctave)
            
            notes_list.append(chordArray)
            beats_counter += element.duration.quarterLength
            print(chordArray)
            chordArray = []

print("Notes extracted from MIDI:", notes_list)

# ...rest of existing code...

print("notes added to list")





def find_all_note_positions(note, noteMap):
    """
    Given a note or chord, return all possible positions on the guitar.
    Only returns positions for notes that actually exist on the fretboard.
    """
    positions = []

    # Get all valid notes on the fretboard
    valid_notes = set(note for string in noteMap[1:] for note in string)

    # Handle single notes
    if not isinstance(note, list):
        if note not in valid_notes:
            return []
        
        for string_index in range(1, 7):
            if note in noteMap[string_index]:
                fret_index = noteMap[string_index].index(note)
                positions.append((string_index, fret_index))
        return positions

    # Handle chords
    else:
        # Only process notes that exist on the fretboard
        valid_chord_notes = [n for n in note if n in valid_notes]
        if not valid_chord_notes or len(valid_chord_notes) != len(note):
            return []

        # Get positions for each valid note
        note_positions = []
        for chord_note in valid_chord_notes:
            note_pos = []
            for string_index in range(1, 7):
                if chord_note in noteMap[string_index]:
                    fret_index = noteMap[string_index].index(chord_note)
                    note_pos.append((string_index, fret_index))
            note_positions.append(note_pos)

        # Generate valid chord combinations
        valid_chord_positions = []
        for combo in product(*note_positions):
            used_strings = set(pos[0] for pos in combo)
            if len(used_strings) == len(combo):
                valid_chord_positions.append(list(combo))
        return valid_chord_positions if valid_chord_positions else []

# ...rest of existing code...

def get_shortest_horizontal_distance_and_positions(notes, noteMap):
    """
    Given a list of notes (can include chords), find the best fretboard positions.
    """
    print("Input notes to process:", notes)  # Debug print
    note_positions = []
    
    for note in notes:
        positions = find_all_note_positions(note, noteMap)
        if positions:  # Only add valid positions
            note_positions.append(positions)
            print(f"Found positions for {note}: {positions}")  # Debug print
    
    min_cost = float('inf')
    best_sequence = []
    
    # Process each position
    for pos_list in note_positions:
        if isinstance(pos_list[0], list):  # Chord
            min_chord_cost = float('inf')
            best_chord_pos = None
            
            for chord_pos in pos_list:
                frets = [pos[1] for pos in chord_pos]
                strings = [pos[0] for pos in chord_pos]
                
                # Calculate costs - prefer positions closer to nut and smaller spans
                fret_span = max(frets) - min(frets) if frets else 0
                avg_fret = sum(frets) / len(frets)
                position_cost = avg_fret * 2  # Prefer lower fret positions
                
                chord_cost = fret_span + position_cost
                
                if chord_cost < min_chord_cost:
                    min_chord_cost = chord_cost
                    best_chord_pos = chord_pos
            
            if best_chord_pos:
                best_sequence.append(best_chord_pos)
                print(f"Selected chord position: {best_chord_pos}")  # Debug print
                min_cost += min_chord_cost
                
        else:  # Single note
            if pos_list:
                # Prefer lower fret positions
                best_pos = min(pos_list, key=lambda x: x[1])
                best_sequence.append(best_pos)
                print(f"Selected note position: {best_pos}")  # Debug print


    # Convert to readable format, keeping chords grouped
    positions = []
    for pos in best_sequence:
        if isinstance(pos, list):  # Chord
            # Sort chord positions by string number and group them in an array
            sorted_pos = sorted(pos, key=lambda x: x[0])
            chord_positions = [f"S{p[0]} F{p[1]}" for p in sorted_pos]
            positions.append(chord_positions)  # Append whole chord as an array
        else:  # Single note
            positions.append(f"S{pos[0]} F{[1]}")  # Append single note as is
    
    print("Final positions to be printed:", positions)  # Debug print
    return min_cost, positions


    
def convertNotes(notes_list):
    """
    Given a list of notes, replace all flats with sharps.
    """
    for i in range(len(notes_list)):
        
        if isinstance(notes_list[i], list):

            for j in range(len(notes_list[i])):

                unusableNote = notes_list[i][j][0] + "-"

                #flats
                if unusableNote == "C-":
                    notes_list[i][j] = notes_list[i][j].replace("C-", "B")

                elif unusableNote == "D-":
                    notes_list[i][j] = notes_list[i][j].replace("D-", "C#")

                elif unusableNote == "E-":
                    notes_list[i][j] = notes_list[i][j].replace("E-", "D#")

                elif unusableNote == "F-":
                    notes_list[i][j] = notes_list[i][j].replace("F-", "E")

                elif unusableNote == "G-":
                    notes_list[i][j] = notes_list[i][j].replace("G-", "F#")

                elif unusableNote == "A-":
                    notes_list[i][j] = notes_list[i][j].replace("A-", "G#")

                elif unusableNote == "B-":
                    notes_list[i][j] = notes_list[i][j].replace("B-", "A#")

                #sharps
                elif unusableNote == "B#":
                    notes_list[i][j] = notes_list[i][j].replace("B#", "C")

                elif unusableNote == "E#":
                    notes_list[i][j] = notes_list[i][j].replace("E#", "F")


        else:
            if notes_list[i].find(notes_list[i][0] + "-") != -1:

                
                unusableNote = notes_list[i][0] + "-"

                #flats
                if unusableNote == "C-":
                    notes_list[i] = notes_list[i].replace("C-", "B")

                elif unusableNote == "D-":
                    notes_list[i] = notes_list[i].replace("D-", "C#")

                elif unusableNote == "E-":
                    notes_list[i] = notes_list[i].replace("E-", "D#")

                elif unusableNote == "F-":
                    notes_list[i] = notes_list[i].replace("F-", "E")

                elif unusableNote == "G-":
                    notes_list[i] = notes_list[i].replace("G-", "F#")

                elif unusableNote == "A-":
                    notes_list[i] = notes_list[i].replace("A-", "G#")

                elif unusableNote == "B-":
                    notes_list[i] = notes_list[i].replace("B-", "A#")

                #sharps
                elif unusableNote == "B#":
                    notes_list[i] = notes_list[i].replace("B#", "C")

                elif unusableNote == "E#":
                    notes_list[i] = notes_list[i].replace("E#", "F")

    print("notes converted")
    return notes_list

print(notes_list)
# Calculate the shortest horizontal distance and corresponding positions
notes_list = convertNotes(notes_list)
distance, positions = get_shortest_horizontal_distance_and_positions(notes_list, noteMap)
print("Extracted Notes:", notes_list)
print("Total Beats:", beats_counter)

# Output the result
print(f"The shortest total horizontal distance between the notes\n{notes_list} is {distance} fret(s).")
print("The corresponding positions (string and fret coordinates) are")




# Initialize tab strings

class TabStrings:

    def __init__(self, print, added, string):
        self.print = print
        self.added = added
        self.string = string

stringValues = ["null", "e", "B", "G", "D", "A", "E"] 
printedHighEString = TabStrings("e |-", False, "1")
printedBString = TabStrings("B |-", False, "2")
printedGString = TabStrings("G |-", False, "3")
printedDString = TabStrings("D |-", False, "4")
printedAString = TabStrings("A |-", False, "5")
printedLowEString = TabStrings("E |-", False, "6")

allStrings = [printedHighEString, printedBString, printedGString, printedDString, printedAString, printedLowEString]

for i in range(len(positions)):

    #first check if it is a chord or a single note
    if isinstance(positions[i], list):

        for j in range(len(positions[i])):

            stringNum = positions[i][j][1]
            fretNum = positions[i][j][4:6]
            #print()
            #print(stringNum, "string", fretNum, "Fret")
            

            for k in range(len(allStrings)):
                
                print(allStrings[k].string, stringNum, "both strings")
                #print()
                if int(stringNum) == int(allStrings[k].string):
                    print("called")
                    allStrings[k].print += fretNum
                    if len(fretNum) == 1:
                        allStrings[k].print += "---"

                    else:
                        allStrings[k].print += "--"

                    print("added")
                    allStrings[k].added = True

        for j in range(len(allStrings)):
            if allStrings[j].added == False:
                allStrings[j].print += "----"

        for j in range(len(allStrings)):
            allStrings[j].added = False

        

    elif isinstance(positions, note.Note):

        stringNum = positions[i][j][1]
        fretNum = positions[i][j][4:6]

        for j in range(len(allStrings)):
                
            if allStrings[j].string == stringNum:

                allStrings[j].print += fretNum
                if len(fretNum) > 1:
                    allStrings[j].print += "--"

                else:
                    allStrings[j].print += "-"


            else:
                allStrings[j].print += "---"


        



# Write to file and print output
file = open("OUTPUTS\FinalTabs.txt", "w")
file.write(printedHighEString.print + "\n")
file.write(printedBString.print + "\n")
file.write(printedGString.print + "\n")
file.write(printedDString.print + "\n")
file.write(printedAString.print + "\n")
file.write(printedLowEString.print + "\n")
file.close()

print(printedHighEString.print)
print(printedBString.print)
print(printedGString.print)   
print(printedDString.print)
print(printedAString.print)
print(printedLowEString.print)


    