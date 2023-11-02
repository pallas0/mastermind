from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

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