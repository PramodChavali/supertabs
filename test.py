import subprocess
import os



def convert_pdf_to_musicxml(pdf_file_path, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Construct the command to run Audiveris
    command = [
        'java', '-jar', 'path/to/audiveris.jar',  # Adjust the path to your Audiveris jar file
        '-export', pdf_file_path,
        '-output', output_directory
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully converted {pdf_file_path} to MusicXML in {output_directory}")

    except subprocess.CalledProcessError as e:
        print(f"Error converting {pdf_file_path}: {e}")

# Example usage
pdf_file = 'path/to/your/music_sheet.pdf'
output_dir = 'path/to/output/directory'
convert_pdf_to_musicxml(pdf_file, output_dir)
