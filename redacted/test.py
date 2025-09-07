import subprocess
import os

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths relative to the script's directory
bat_file = os.path.join(script_dir, "Audiveris", "bin", "Audiveris.bat")
pdf_file = os.path.join(script_dir, "PDFInputs", "core.pdf")

# Construct the command
command = f'cmd.exe /c "{bat_file}" -export "{pdf_file}"'

# Run the command
subprocess.run(command, shell=True, check=True)




def convert_pdf_to_musicxml(pdf_file_path, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Construct the command to run Audiveris
    command = [
        'cmd', '/c', "D:/vsCode/python/New/Audiveris/bin/Audiveris.bat",  # Adjust the path to your Audiveris jar file
        '-export', pdf_file_path,
        '-output', output_directory
    ]

    command = (' ').join(command)

    command = 'cmd.exe /c ./Audiveris/bin/Audiveris.bat -export ./PDFInputs/core.pdf'
    command = ''

    # Run the command
    try:
        #subprocess.run(command, check=True)
        print(f"Successfully converted {pdf_file_path} to MusicXML in {output_directory}")
        os.system('cmd.exe /c ./Audiveris/bin/Audiveris.bat -export ./PDFInputs/core.pdf')

    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_file_path}: {e}")

# Example usage
pdf_file = "./PDFInputs/mountRockReprise.pdf"
output_dir = 'D:/vsCode/python/New/OUTPUTS'
convert_pdf_to_musicxml(pdf_file, output_dir)