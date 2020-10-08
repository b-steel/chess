# Files
* Game - game class
* Pieces - classes for each individual piece
* Board - board class
* Place - place class
* Chars - unicode characters for the pieces


# Game
* runs a game, keeps track of rounds, alternates players
* asks for input and relays that to the board

# Board
* contains Squares in a dictionary
* has places for the taken pieces
* takes moves and relays that to the places and the pieces
* checks for check and checkmate (by asking the kings) after every move

# Place
* contains pieces

# Square
* knows it's neighbors
* can contain one piece or None

# Pieces
* knows where it is 
* knows it's possible moves

# King
* has a check method
* has a checkmate method


