# Pathfinding Pacman

Table of contents
1. Inspiration https://github.com/pranavnightsforrobotics/PathfindngPacman/blob/main/README.md?plain=1#L10
2. Explanation
3. Installation
4. Modulation


This was my first-semester project for my advanced topics and projects class. 
This project was inspired by automatic maze solvers and my constant need to play Pacman when bored!

The main difference between this and a normal Pacman game is the movement of the ghosts. In normal Pacman games, the ghosts move based on a distance heuristic, meaning that each ghost moves in the direction of the Pacman based on how far they are from the Pacman. For example, if the Ghost is 15 or more tiles away from the Pacman on the X-axis then the Ghost would prioritize movement in the x-axis towards the Pacman.

While this method is good, there are a couple problems. 
1. The ghosts often use a very inefficient path
2. The ghosts also often stack on top of each other

To fix this I decided to add 2 things to the regular pacman game.
1. 


