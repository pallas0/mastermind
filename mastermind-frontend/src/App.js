import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [attempts, setAttempts] = useState(10);


  const startGame = async() => {
    axios.get('http://127.0.0.1:5000/generate')
    .then(response => {
      console.log(response)
    })
  }

  return (
    <div className="App">
      <button onClick={startGame}>Start Game</button>
    </div>
  );
}

export default App;
