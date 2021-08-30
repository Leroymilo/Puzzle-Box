WARNING : DO NOT CREATE LOGIC GATES CLOCK
It will make an infinite while loop since it loops until there's no gate updated.

template :
x1 y1 x2 y2
where x1 and y1 are the coordinates of the emitter
and x2 and y2 are the coordinates of the receiver

Interruptors, targets (todo) and logic gates can be emitters.
Doors and logic gates can be receivers.

AND and OR gates takes at least 2 Inputs,
they'll return False if there's 0 and they'll behave as open gates if there's 1 (they'll return the input).

NOT gates takes exactly one input,
they'll output False if there's 0 or more than 1 inputs.