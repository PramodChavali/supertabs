from flask import Flask, request, send_file
from main import main
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def handle_upload():
    image = request.files['image']
    image.save('input.png')  # Save image temporarily

    outputFile = main('input.png')

    return send_file(outputFile, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)