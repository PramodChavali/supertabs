from flask import Flask, request, send_file
import os
from main import main  # Import your function to process the image

app = Flask(__name__)

# Route to serve the frontend HTML
@app.route('/')
def index():
    return open('index.html').read()

# Route to handle image upload and return the text file
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part', 400
    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file', 400
    
    # Save the uploaded image temporarily
    filename = os.path.join('uploads', file.filename)
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
    app.run(debug=True)