import React, { useState, useEffect } from 'react';
import socketIOClient from 'socket.io-client';
import axios from 'axios';

import './App.css';
import BestScoresTable from './BestScoresTable';
import SubmitBestScore from './SubmitBestScore';

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
  const [remainingTime, setRemainingTime] = useState(15)

  const socket = socketIOClient('http://127.0.0.1:5000/game')

  useEffect(() => {
    socket.on('start_timer', (data) => {
      setRemainingTime(data.remaining_time);
    });

    socket.on('time_up', () => {
      setRemainingTime(0);
      setGameOver(true) ///ok check that this is ..necessary? I feel like we sent something
      //through the backend on this
      alert('Time is up!')
    })

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
        setSecretNumber(response.data.number)
        setGameOver(true)
        setPlayerWon(response.data.player_won[0])
      }
      setGuess("");
    })
  }

  function displayScoreSubmission() {
    if (bestScores.length == 3) {
      const maxScore = Math.max(...bestScores.map(score => score.score));
      const newScore = 10-attempts;
      return newScore < maxScore;
    }
    else {
      return true
    }
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
      {gameOver && displayScoreSubmission() && (
      <SubmitBestScore numberOfAttempts={attempts} />
    )}
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
