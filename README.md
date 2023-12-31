# mastermind

## Overview
This project is a take on the classic game Mastermind. The game is built using Flask, React, and PostgreSQL. The objective is to guess a four-digit number generated by the computer within a set limit of 10 guesses and a total time of five minutes. 

There is also a high scores board, which shows the top 3 games ever played (in terms of number attempts needed to guess the code) across all users. If a user gets a top 3 score, they get to put their name in and go on the high score board. 

Additionally, there is a countdown timer (server-side) with a 10 minute time limit. When the time limit hits, game-play is automatically stopped and the user is told that they have lost the game. 

## Gameplay Screenshot
![mastermind_screenshot](https://github.com/pallas0/mastermind/assets/52135849/3a1be3bb-25a0-47fe-9a54-7ff876498333)

## Setup Instructions
### General/Flask Setup
1. **Clone the Repository**
   - Begin by cloning the repository to your local machine using:
     ```
     git clone git@github.com:pallas0/mastermind.git
     ```

2. **Set Up a Virtual Environment**
   - Navigate to the cloned directory and create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On Unix or MacOS:
       ```
       source venv/bin/activate
       ```

3. **Install Requirements**
   - Install all required packages using pip:
     ```
     pip install -r requirements.txt
     ```

4. **Run the Backend**
   - Start the Flask server with:
     ```
     flask run
     ```

### Postgresql Setup
1. **Setting Up a Local Postgresql Database**
   - Install PostgreSQL and create a new database:
     ```
     createdb [database_name]
     ```

2. **Configure Database URI**
   - Determine your database URI, which typically follows the format:
     ```
     postgresql://[user]:[password]@localhost/[database_name]
     ```
   - Update the `app.config` line in the `app.py` file in Flask to use this URI:
     ```
     app.config['SQLALCHEMY_DATABASE_URI'] = '[Your Database URI]'
     ```

3. **Run Data Table Migrations**
   - Apply database migrations to set up the necessary tables:
     ```
     flask db upgrade
     ```

### React Frontend Setup
1. **Navigate to Frontend Directory**
   - Change to the frontend directory:
     ```
     cd mastermind-frontend
     ```

2. **Install Dependencies**
   - Install all necessary dependencies using npm:
     ```
     npm install
     ```

3. **Start the Frontend Application**
   - Run the React application with:
     ```
     npm start
     ```


## Code Structure

### Overview
This project is structured through a combination of Flask backend, React frontend, and a PostgreSQL database. The game's logic is managed by Python on the server-side and React on the client-side, with the database handling game state and high scores.

### Backend (Flask)
- **`app.py`**: This is the main Flask application file. It initializes the Flask app and configures it with necessary extensions like SQLAlchemy for database interaction, Migrate for database migration, and SocketIO for real-time communication.
  - **Endpoints**:
    - `/generate`: Generates a new game, creates a game state, and starts the timer.
    - `/compare_guess`: Compares the player's guess with the generated number and provides feedback.
    - `/best_scores`: Fetches the best scores from the database.
    - `/update_best_score`: Updates the best scores in the database.
  - **Real-time Communication**:
    - Uses Flask-SocketIO to handle the game timer.

- **`gametimer.py`**: Manages the game timer, sending a 'time_up' event through SocketIO upon completion.
- **`models.py`**: Defines SQLAlchemy models for storing games (`Game`) and best scores (`BestScores`). The Game class has methods for generating the secret code, processing guesses, and checking for gameover.  The BestScores class has methods for returning and updating the best scores.
- **`timer_manager.py`**: Manages multiple game timers, ensuring that each game instance has its own independent timer and storing it in application memory.

### Frontend (React)
- **`App.js`**: The main React component managing the game's front-end logic.
  - Handles game initialization, processing of guesses, and real-time updates from the server.
  - Manages the game's state like the number of attempts, game status, player's guesses, and feedback.
  - Interacts with the Flask backend via HTTP requests for game actions and WebSocket connections for real-time updates.
- **`BestScoresTable.js` & `SubmitBestScore.js`**: Components for displaying the best scores and submitting a new high score.

### Database (PostgreSQL)
- Manages two primary data models: 
  - `Game` for generating and storing each game.
  - `BestScores` for tracking the top scores.

### Integration
- The Flask backend and React frontend are integrated via RESTful APIs for game logic and state management, while real-time communication (e.g., timer updates) is handled using WebSocket connections provided by SocketIO.
- PostgreSQL database is used by Flask to persist game states and best scores, ensuring data persistence across sessions.

## Design Decisions and Architecture
Most of the game state and functionality is stored in the Game class, which is backed by a Postgresql model. 

To create the high score functionality, I decided to create a separate BestScores data model which contains only the top 3 scores (wins with the least number of attemps) ever recorded. When a user gets a score that is better than the existing top 3 scores, we evict the worst score and then insert the user's game score. I chose to keep game scores here rather than on the Game model to avoid having to sort/fetch the top 3 scores across all games every time we show the high scores (/best_scores endpoint). 

For the timer, I decided to build the timer/time-counting functionality on the serverside (instead of a much simplier client-side implementation) so that a user wouldn't be able to "cheat' the time countdown by altering the client-end state. When a game is created, a timer is created via TimerManager and starts running on secondary thread. When the time is up, the frontend gets an alert via a websocket.
 
## Detailed Gameplay Instructions
### Game Rules
- At the start of the game, the computer will randomly select a pattern of four numbers. These numbers are chosen from a range of 0 to 7 and can include duplicates.
- The player has a maximum of 10 attempts to guess the correct number combination.
- After each guess, the computer provides feedback in the following form:
  - X correct number and X correct location

### Gameplay Example
- The game initializes with the number “0 1 3 5”.
- If a player guesses “2 2 4 6”, the response will be “0 correct number and 0 correct location”.
- A guess of “0 2 4 6” will elicit the response “1 correct number and 1 correct location”.
- For the guess “2 2 1 1”, the response will be “1 correct number and 0 correct location”.
- A guess of “0 1 5 6” results in “3 correct numbers and 2 correct locations”.

### Game Interface
- To start the game, click 'Generate Number + Start Game'.
- Enter each guess in the text field provided and submit it using the 'Submit Guess' button.
- The player’s guess history and feedback from the computer are displayed after each guess, along with the remaining number of attempts.
- The bottom of the page features a leaderboard showcasing the three best overall scores. Players who guess the number in fewer attempts than the lowest score on the leaderboard can add their name to this table.

