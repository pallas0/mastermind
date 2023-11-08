import React, { useState } from 'react';
import axios from 'axios';

function SubmitBestScore({ numberOfAttempts }) {
  const [name, setName] = useState('');
  const [score, setScore] = useState(numberOfAttempts);

  const handleSubmit = () => {
    var new_score = 10 - score;
    axios.post('http://127.0.0.1:5000/update_best_score', { name, new_score })
      .then(response => {
        console.log('Best score submitted successfully');
      })
      .catch(error => {
        console.error('Error submitting best score:', error);
      });
  };

  return (
    <div className="submit-best-score">
      <h2>Submit Your Best Score</h2>
      <label>
        Name:
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <br />
      <p>Attempts: {numberOfAttempts}</p>
      <button onClick={handleSubmit}>Submit Score</button>
    </div>
  );
}

export default SubmitBestScore;
