import os
import subprocess

def Get_XML_From_PDF(inputPDF):
    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the paths relative to the script's directory
    bat_file = os.path.join(script_dir, "Audiveris", "bin", "Audiveris.bat")
    pdf_file = os.path.join(script_dir, "PDFInputs", inputPDF)

    # Expected XML output file (same directory as input PDF)
    xml_file = os.path.join(script_dir, "PDFInputs", os.path.splitext(inputPDF)[0] + ".xml")

    # Construct the command
    command = f'powershell.exe -Command "& \'{bat_file}\' -export \'{pdf_file}\'"'

    print(command)

    # Run the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Print output and errors
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Check if the expected XML file was created
    if os.path.exists(xml_file):
        return xml_file
    else:
        print("Error: MXL file was not created.")
        return None



