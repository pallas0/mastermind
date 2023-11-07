import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [guess, setGuess] = useState("")
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [attempts, setAttempts] = useState(10);


  const startGame = async() => {
    axios.get('http://127.0.0.1:5000/generate')
    .then(response => {
      setGuess("")
      setAttempts(response.data.attempts);
    })
  }

  const submitGuess = () => {
    axios.post('http://127.0.0.1:5000/compare_guess', {guess})
    .then(response => {
      console.log(response.data);
      setGuesses([...guesses, guess])
      setGuess("")
    })
  }

  return (
    <div className="App">
      <button onClick={startGame}>Start Game</button>
      <input
      type="text"
      placeholder="Enter your guess"
      value={guess}
      onChange={(e) => setGuess(e.target.value)}
      />
      <button onClick={submitGuess}>Submit Guess</button>
      <p>Attempts: {attempts}</p>
    </div>
  );
}

export default App;
