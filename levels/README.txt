template :
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

Take care of closing every bound of the level with walls to avoid OOB.
Don't put a button next to the door it opens,
because the player can walk into the closing door.