from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

numbers = []

@app.route('/generate', methods=['GET'])
def genereate_numbers():
    global numbers
    response = requests.get('https://www.random.org/integers', params={
        'num': 4,
        'min': 0,
        'max': 7,
        'col': 1,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'
    })
    numbers = list(map(int, response.text.split()))
    return response.text

@app.route('/guess', methods=['POST'])
def make_guess():
    global numbers
    guess = list(map(int, request.data.split()))
    return guess

if __name__ == "__main__":
    app.run(debug=True)