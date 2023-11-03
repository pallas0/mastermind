import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css';

function App() {
  const [numbers, setNumbers] = useState(['hi!']);
  const [guesses, setGuesses] = useState([]);
  const [feedback, setFeedback] = useState([]);
  const [attempts, setAttempts] = useState(10);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/generate')
    .then(response => {
      setNumbers(response.data.numbers);
      setAttempts(response.data.attempts);
    })
  }, [])

  return (
    <div className="App">
      <header>{numbers}</header>
    </div>
  );
}

export default App;
