import React, { useState } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [numbers, setNumbers] = useState([]);
  const [guess, setGuess] = useState([]);
  const [history, setHistory] = useState([]);

  const generateNumbers = async() => {
    const response = await axios.get('http://127.0.0.1:5000/generate')
    console.log(response);
  }

  return (
    <div className="App">
      <button onClick={generateNumbers}>Start Game</button>
      <header>{numbers}</header>
    </div>
  );
}

export default App;
