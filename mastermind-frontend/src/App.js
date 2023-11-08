import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';
import BestScoresTable from './BestScoresTable';

function App() {
  const [guess, setGuess] = useState("")
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [attempts, setAttempts] = useState(10);
  const [gameStarted, setGameStarted] = useState(false)
  const [gameOver, setGameOver] = useState(false);
  const [playerWon, setPlayerWon] = useState(false);
  const [secretNumber, setSecretNumber] = useState([]);
  const [bestScores, setBestScores] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/best_scores')
      .then(response => {
        setBestScores(response.data.best_scores);
      })
      .catch(error => {
        console.error('Error fetching best scores:', error);
      });
  }, []);

  const startGame = async() => {
    axios.get('http://127.0.0.1:5000/generate')
    .then(response => {
      console.log(response.data)
      setGameStarted(true)
      setGameOver(false)
      setPlayerWon(false)
      setGuess("")
      setGuesses([])
      setFeedback([])
      setAttempts(response.data.attempts);
      setSecretNumber(response.data.number)
    })
  }

  const submitGuess = () => {
    if (guess.length !== 4 || !/^[0-9]{4}$/.test(guess)) {
      alert("Please enter a 4-digit guess using only numeric characters.");
      return;
    }
    axios.post('http://127.0.0.1:5000/compare_guess', {guess})
    .then(response => {
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
          <div>
          The secret number was:  {secretNumber}
          </div>
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
      <BestScoresTable bestScores={bestScores} />
    </div>
  );
}

export default App;
