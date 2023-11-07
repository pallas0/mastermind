import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [guess, setGuess] = useState("")
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [attempts, setAttempts] = useState(10);
  const [gameStarted, setGameStarted] = useState(false)
  const [gameOver, setGameOver] = useState(false);
  const [playerWon, setPlayerWon] = useState(false);


  const startGame = async() => {
    axios.get('http://127.0.0.1:5000/generate')
    .then(response => {
      setGameStarted(true)
      setGameOver(false)
      setPlayerWon(false)
      setGuess("")
      setGuesses([])
      setFeedback([])
      setAttempts(response.data.attempts);
    })
  }

  const submitGuess = () => {
    axios.post('http://127.0.0.1:5000/compare_guess', {guess})
    .then(response => {
      console.log(response.data);
      setAttempts(attempts-1)
      setGuesses([...guesses, guess])
      setFeedback([...feedback, response.data.feedback])
      if (response.data.player_won.length > 0) {
        setGameOver(true)
        setPlayerWon(response.data.player_won[0])
      }
      setGuess("");
    })
  }

  return (
    <div className="App">
      <button onClick={startGame}>Generate Number + Start Game</button>
      <input
        type="text"
        placeholder="Enter your guess"
        value={guess}
        onChange={(e) => setGuess(e.target.value)}
        disabled={!gameStarted || gameOver}
      />
      <button onClick={submitGuess} disabled={!gameStarted || gameOver}>Submit Guess</button>
      {gameOver && (
        <div className="game-over-message">
          {playerWon ? "You won!" : "You lost =("}
        </div>
      )}
      <p>Attempts: {attempts}</p>
      <div className="guess-feedback">
        <div className="guesses">
          <h3>Guesses</h3>
          <ul>
            {guesses.map((guess, index) => (
              <li key={index}>{guess}</li>
            ))}
          </ul>
        </div>
        <div className="feedback">
          <h3>Feedback</h3>
          <ul>
            {feedback.map((fb, index) => (
              <li key={index}>{fb}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
