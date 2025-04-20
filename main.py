import subprocess
from music21 import converter, note, chord
from PDFtoMXL import *
from itertools import product, combinations


def main(inputPDF):

    filename = inputPDF.split(".")[0]

    #inputPDF = "PDFInputs/" + filename + ".jpeg"
    midi_path = f"MIDIFiles/{filename}.mid"
    xml_file = "XMLOutputs/" + filename + ".musicxml"

    # Combine activation and oemer command into a single PowerShell session
    oemer_cmd = f"oemer -o {xml_file} {inputPDF}"
    print(f"Running command: {oemer_cmd}")
    result = subprocess.run(["powershell.exe", "-Command", oemer_cmd], shell=True, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)


    class TabStrings:

        def __init__(self, print, added, string):
            self.print = print
            self.added = added
            self.string = string
            #self.duration = duration

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


    # Convert MusicXML to MIDI
    convert_musicxml_to_midi(xml_file, midi_path)



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
    timeSignature = score.flat.getTimeSignatures()[0]

    timeSignature = str(timeSignature)
    timeSignature = timeSignature[len(timeSignature)-4:len(timeSignature)-1]
    beatsPerBar = timeSignature[0]
    beatNote = timeSignature[2]

    print(str(timeSignature))
    notes_list = []
    chordArray = []
    durationArray = []
    beats_counter = 0.0

    # Iterate through all parts and extract notes
    for part in score.parts:
        for element in part.recurse():
            if isinstance(element, note.Note):
                # Add single note
                if element.nameWithOctave in [note for string in noteMap[1:] for note in string]:
                    notes_list.append(element.nameWithOctave)
                    beats_counter += element.duration.quarterLength
                    durationArray.append(element.duration.quarterLength)
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


    def findAllNotePositions(note, noteMap):
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
        Prioritizes positions that are close to all previous positions.
        """
        print("\nProcessing notes:", notes)  # Debug print
        note_positions = []
        
        # First pass: collect all possible positions
        for note in notes:
            positions = findAllNotePositions(note, noteMap)
            print(f"\nFound positions for {note}:")
            for pos in positions:
                print(pos)
            if positions:  # Only add valid positions
                note_positions.append(positions)
        
        print(f"\nTotal notes to process: {len(note_positions)}")
        
        min_cost = float('inf')
        best_sequence = []
        
        # Process each position
        for i, pos_list in enumerate(note_positions):
            print(f"\nProcessing note {i+1}/{len(note_positions)}")
            if isinstance(pos_list[0], list):  # Chord
                min_chord_cost = float('inf')
                best_chord_pos = None
                
                for chord_pos in pos_list:
                    frets = [pos[1] for pos in chord_pos]
                    strings = [pos[0] for pos in chord_pos]
                    
                    # Calculate costs - prefer positions that are close together
                    fret_span = max(frets) - min(frets) if frets else 0
                    string_span = max(strings) - min(strings) if strings else 0
                    
                    # Calculate distance to all previous positions
                    total_distance = 0
                    for prev_pos in best_sequence:
                        if isinstance(prev_pos, list):  # Previous was a chord
                            for p in prev_pos:
                                # Find closest string in current chord to this previous position
                                min_dist = min(abs(s - p[0]) + abs(f - p[1]) for s, f in zip(strings, frets))
                                total_distance += min_dist
                        else:  # Previous was a single note
                            # Find closest string in current chord to previous note
                            min_dist = min(abs(s - prev_pos[0]) + abs(f - prev_pos[1]) for s, f in zip(strings, frets))
                            total_distance += min_dist
                    
                    # Combine spans with distance to previous positions
                    position_cost = (fret_span + string_span) * 0.5 + total_distance
                    
                    print(f"Chord position: {chord_pos}, Cost: {position_cost} (fret span: {fret_span}, string span: {string_span}, total distance: {total_distance})")
                    
                    if position_cost < min_chord_cost:
                        min_chord_cost = position_cost
                        best_chord_pos = chord_pos
                
                if best_chord_pos:
                    best_sequence.append(best_chord_pos)
                    print(f"Selected chord position: {best_chord_pos} with cost {min_chord_cost}")
                    min_cost += min_chord_cost
                    
            else:  # Single note
                if pos_list:
                    # For single notes, find position with smallest total distance to all previous positions
                    if best_sequence:
                        min_total_distance = float('inf')
                        best_pos = None
                        
                        for pos in pos_list:
                            total_distance = 0
                            for prev_pos in best_sequence:
                                if isinstance(prev_pos, list):  # Previous was a chord
                                    # Find closest string in previous chord
                                    min_dist = min(abs(pos[0] - p[0]) + abs(pos[1] - p[1]) for p in prev_pos)
                                    total_distance += min_dist
                                else:  # Previous was a single note
                                    dist = abs(pos[0] - prev_pos[0]) + abs(pos[1] - prev_pos[1])
                                    total_distance += dist
                            
                            print(f"Position: {pos}, Total distance to previous positions: {total_distance}")
                            
                            if total_distance < min_total_distance:
                                min_total_distance = total_distance
                                best_pos = pos
                    else:
                        # For first note, pick any position
                        best_pos = pos_list[0]
                        print("First note, selected position:", best_pos)
                        
                    best_sequence.append(best_pos)
                    print(f"Selected note position: {best_pos}")
        
        print(f"\nFinal sequence length: {len(best_sequence)}")
        
        # Convert to readable format, keeping chords grouped
        positions = []
        for pos in best_sequence:
            if isinstance(pos, list):  # Chord
                # Sort chord positions by string number and group them in an array
                sorted_pos = sorted(pos, key=lambda x: x[0])
                chord_positions = [f"S{p[0]} F{p[1]}" for p in sorted_pos]
                positions.append(chord_positions)
            else:  # Single note
                positions.append(f"S{pos[0]} F{pos[1]}")
        
        print("\nFinal positions to be printed:")
        for pos in positions:
            print(pos)
        
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
    def clearTabStrings(allStrings):
        for string in allStrings:
            if string.string == "1":
                string.print = "e |- "
            elif string.string == "2":
                string.print = "B |- "
            elif string.string == "3":
                string.print = "G |- "
            elif string.string == "4":
                string.print = "D |- "
            elif string.string == "5":
                string.print = "A |- "
            elif string.string == "6":
                string.print = "E |- "
        string.added = False

    characterLimit = 100
    characterCount = 0


    stringValues = ["null", "e", "B", "G", "D", "A", "E"] 
    printedHighEString = TabStrings("e |-", False, "1")
    printedBString = TabStrings("B |-", False, "2")
    printedGString = TabStrings("G |-", False, "3")
    printedDString = TabStrings("D |-", False, "4")
    printedAString = TabStrings("A |-", False, "5")
    printedLowEString = TabStrings("E |-", False, "6")
    file = open("OUTPUTS/FinalTabs.txt", "w")

    allStrings = [printedHighEString, printedBString, printedGString, printedDString, printedAString, printedLowEString]

    print("Starting tab generation with positions:", positions)
    print("Number of positions to process:", len(positions))

    for i in range(len(positions)):
        print(f"\nProcessing position {i}: {positions[i]}")
        print(f"Type of position: {type(positions[i])}")
        
        #first check if it is a chord or a single note
        if isinstance(positions[i], list):
            print("Processing chord")
            # Handle chord
            for j in range(len(positions[i])):
                print(f"  Chord note {j}: {positions[i][j]}")
                print(f"  Type of chord note: {type(positions[i][j])}")
                
                # Handle both string formats (tuple/list and string)
                if isinstance(positions[i][j], (tuple, list)):
                    if len(positions[i][j]) >= 2:
                        stringNum = positions[i][j][0]
                        fretNum = str(positions[i][j][1])
                else:
                    # Handle string format "S1 F5" etc.
                    parts = positions[i][j].split()
                    if len(parts) >= 2:
                        stringNum = parts[0][1:]  # Remove 'S' prefix
                        fretNum = parts[1][1:]   # Remove 'F' prefix
                
                print(f"    String: {stringNum}, Fret: {fretNum}")
                
                for k in range(len(allStrings)):
                    if int(stringNum) == int(allStrings[k].string):
                        print(f"    Adding to string {allStrings[k].string}")
                        allStrings[k].print += fretNum
                        if len(fretNum) == 1:
                            allStrings[k].print += "---"
                        else:
                            allStrings[k].print += "--"
                        allStrings[k].added = True

            # Add dashes for strings not used in the chord
            for j in range(len(allStrings)):
                if not allStrings[j].added:
                    allStrings[j].print += "x---"
                allStrings[j].added = False

        else:
            print("Processing single note")
            # Handle single note
            # Handle both string formats (tuple/list and string)
            if isinstance(positions[i], (tuple, list)):
                if len(positions[i]) >= 2:
                    stringNum = positions[i][0]
                    fretNum = str(positions[i][1])
            else:
                # Handle string format "S1 F5" etc.
                parts = positions[i].split()
                if len(parts) >= 2:
                    stringNum = parts[0][1:]  # Remove 'S' prefix
                    fretNum = parts[1][1:]   # Remove 'F' prefix
            
            print(f"  String: {stringNum}, Fret: {fretNum}")
            
            for j in range(len(allStrings)):
                if int(allStrings[j].string) == int(stringNum):
                    print(f"  Adding to string {allStrings[j].string}")
                    allStrings[j].print += fretNum
                    if len(fretNum) == 1:
                        allStrings[j].print += "---"
                    else:
                        allStrings[j].print += "--"
                else:
                    allStrings[j].print += "----"

        characterCount += 4
        if characterCount >= characterLimit:
            file.write(printedHighEString.print + "\n")
            file.write(printedBString.print + "\n")
            file.write(printedGString.print + "\n")
            file.write(printedDString.print + "\n")
            file.write(printedAString.print + "\n")
            file.write(printedLowEString.print + "\n")
            file.write("\n")
            clearTabStrings(allStrings)
            characterCount = 0

    print("\nFinal tab strings:")
    for string in allStrings:
        print(f"{string.string}: {string.print}")

    # Write to file and print output

    file.write(printedHighEString.print + "\n")
    file.write(printedBString.print + "\n")
    file.write(printedGString.print + "\n")
    file.write(printedDString.print + "\n")
    file.write(printedAString.print + "\n")
    file.write(printedLowEString.print + "\n")
    file.close()

    print("\nFinal tab output:")
    print(printedHighEString.print)
    print(printedBString.print)
    print(printedGString.print)   
    print(printedDString.print)
    print(printedAString.print)
    print(printedLowEString.print)

    return "OUTPUTS/FinalTabs.txt"

    #clear the

    