import os
import subprocess



def Get_XML_From_PDF(inputPDF):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    bat_file = os.path.join(script_dir, "Audiveris", "bin", "Audiveris.bat")
    pdf_file = os.path.join(script_dir, "PDFInputs", inputPDF)

    xml_file = os.path.join(script_dir, "PDFInputs", os.path.splitext(inputPDF)[0] + ".xml")
    
    command = f'powershell.exe -Command "& \'{bat_file}\' -export \'{pdf_file}\'"'
    print(command)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if os.path.exists(xml_file):
        return xml_file
    else:
        print("Error: MXL file was not created.")
        return None
