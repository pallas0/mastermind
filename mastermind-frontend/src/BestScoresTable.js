import React from 'react';

function BestScoresTable({ bestScores }) {
  return (
    <div className="best-scores">
      <h2>Best Scores</h2>
      <table>
        <thead>
          <tr>
            <th>Player Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {bestScores.map((score, index) => (
            <tr key={index}>
              <td>{score.player_name}</td>
              <td>{score.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BestScoresTable;
