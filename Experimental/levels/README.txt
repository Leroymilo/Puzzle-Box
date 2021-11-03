template :
the first line is the size of the level (height, then width)
separate tiles by spaces, but no space at the end of a line.
. : noting
X : wall
x : grate (only bullets goes through)
P : player's initial position
W : end level tile
B : boxes' initial positions
I : interruptors
& : AND gates
| : OR gates
! : NOT gates
D : doors (closed by default)
T : targets

Take care of closing every bound of the level with walls to avoid OOB.
Or don't, if you want to make some funny things.
You can add comments lines that will be displayed under the level

The number at the end of the file name needs to be 3 digits long.
This number also needs to be in the continuity of the already existing levels.
Exemple : don't make level549.txt if level001.txt to level548.txt are not in the file.
If you don't respect these rules, the game will just crash.

You can now make your own levels!
Make sure to check logic\README.txt to learn how to connect your level's gates.