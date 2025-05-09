from flask import Flask, request, send_file
import os
from main import main  # Import your function to process the image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Route to serve the frontend HTML
@app.route('/')
def index():
    return open('index.html').read()

# Route to handle image upload and return the text file
@app.route('/upload', methods=['POST'])
def upload_image():

    required_dirs = ['PDFInputs', 'XMLOutputs', 'MIDIFiles', 'OUTPUTS']
    for dir in required_dirs:
        os.makedirs(dir, exist_ok=True)

    

    if 'image' not in request.files:
        return 'No image part', 400
    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file', 400
    
    
    
    # Save the uploaded image temporarily
    filename = os.path.join('PDFInputs/', file.filename)
    file.save(filename)
    
    # Call the function that processes the image and returns the text content
    result_text = main(filename)
    
    # Save the result text as a downloadable file
    result_filename = 'result.txt'
    with open(result_filename, 'w') as result_file:
        result_file.write(result_text)
    
    # Return the generated text file for download
    return send_file(result_filename, as_attachment=True)

if __name__ == '__main__':
    print("starting server")
    port = int(os.environ.get("PORT", 5000))  # Fallback to 5000 for local testing
    app.run(host='0.0.0.0', port=port, debug=True)