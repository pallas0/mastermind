import React, { useState } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [numbers, setNumbers] = useState(["hi!"]);
  const [guess, setGuess] = useState([]);
  const [history, setHistory] = useState([]);

  const generateNumbers = async() => {
    const response = await axios.get('http://localhost:5000/generate')
    setNumbers(response.data.split(' ').map(Number));
  }

  return (
    <div className="App">
      <button onClick={generateNumbers}>Start Game</button>
      <header>Hi!</header>
    </div>
  );
}

export default App;
