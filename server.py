from flask import Flask, request, jsonify
from main import runProgram  # import your existing function

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run():
    result = runProgram()  # call your script logic
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)