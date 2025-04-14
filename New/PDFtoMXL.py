import os
import subprocess

def Get_XML_From_PDF(inputPDF, outputMXL):
    try:

        # Run oemer command
        cmd = f"oemer -o {outputMXL} {inputPDF}"
        result = subprocess.run(["powershell.exe", "-Command", cmd], shell=True, capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

            
    except Exception as e:
        ErrorHandler(e)
        return None



def ErrorHandler(e):
    print("Error with conversion. Try again with a better image.")
