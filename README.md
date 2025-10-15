# CS50 Project: Zork like Text Adventure Game
#### Video Demo:  <URL HERE>
#### Description:

This project is a web app game inspired by Zork. The core idea of the game is similar with the main difference being that it is not CLI based like Zork.

Most of the game is essentially a reading game, since the hints of how to avoid the trap rooms is contained in the prologue and also in the room descriptions on the pathways leading up to the trap rooms. Future versions of the game will be made more complex so that the player has to collect the items in a specific order. As of now all 3 can be collected in any order and the only 2 conditions as of now are the use of torch in dark rooms and carrying limited items in the narrow passage.


The primary folder "CS50_project" contains:
- "game" folder – includes "content.json" and "engine.py"
- "templates" folder – holds all the HTML templates
- "app.py", "README.md", and "requirements.txt"

"app.py" is the core Flask application that runs the game. It defines routes and connects the browser interface to the game logic.

"game" folder contains 2 files. "content.json" which contains the layout data of the game, describing the rooms, their exits, the items they hold and their lighting state in the form of a boolean. "engine.py" is the core logic file that interprets user commands and updates the state of the game based on the command provided. It eventually decides if a user will win or loose. 

"templates" folder contains the 7 html templates. "layout.html" contains the main layout of the game and has a title block and a content block to be used by other 6 templates. The game flows as Start > Prologue > Input command > Room change > Win/loss condition.

"index.html" is loaded as the default route of the game and contains the options to begin the game or look at instructions on how to play. 

"howto".html provides an explanation of the game and what commands are to be used, including the win condition and trap rooms. It shows two options at the bottom. One is to start a new game and the second is "resume game" or "back to home" based on whether a game session is active or not.

"intro.html" provides a short prologue to the game explaining what is the target of the game and provides hints that may be useful in winning the game. It provides the option to begin the game or look at instructions.

"play.html is the main page that is re-routed while the game is in motion. At the top are 2 options to exit the game or look at instructions. Below this it contains a room name, description on the left and an inventory list of the right. Below these are the messages displayed based on the most recent command. Below the messages is the line to enter command.

"win.html" is the page that shows the game has been won and is only routed when the player enters the treasure room. It provides the option to play again or exit the game.

"gameover.html" is routed when a player enters one of the 3 trap rooms. It displays a message based on the trap room's description and informs the player that the game is over. It provides the same 2 options as "win.html".

When deciding on how to design the game after looking at Zork i realised it needs to be web based and not CLI to make it playable for a wider audience. Flask was chosen to enable this since it is the only framework i know yet to create a web app.

A json file has been used to contain the room data instead of hardcoded data or a database because it provide the most ease at editing the rooms in the future and also enabled visiually planning on how to connect the rooms without any 3rd party design software. 




