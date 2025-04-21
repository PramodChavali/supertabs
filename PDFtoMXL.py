import os
import subprocess
import shutil

def Get_XML_From_PDF(filename, pdf_file):
    
    bat_file = "Audiveris/bin/Audiveris.bat"
    xml_file = f"XMLOutputs/{filename}.mxl"

    # Construct the command
    #command = f'powershell.exe -Command "& \'{bat_file}\' -export \'{pdf_file}\'"'
    command = ["powershell.exe", "-Command", f"& '{bat_file}' -batch -export '{pdf_file}'"]

    print(command)

    # Run the command
    result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)

    # Print output and errors
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    # Check if the expected XML file was created

    try:
        shutil.copy(f"PDFInputs/{filename}.mxl", xml_file)
        os.remove(f"PDFInputs/{filename}.mxl")
    

    except FileNotFoundError:
        print(f"Error with conversion. Please try again with a better file.")
        return 1

    os.remove(f"PDFInputs/{filename}.omr")

    return xml_file




