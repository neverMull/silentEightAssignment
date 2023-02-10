# silentEightAssignment


## Definitions

Strip: A strip is a continuous, horizontally-connected group of 1s

Closed Strip: A strip that is not in contact with any strip in the row directly below it, and therefore represents a lower boundary of an island

Open Strip: A strip that is in contact with one or more strips in the row directly before it

Island: An island can be relabeled as the set of all strips that can be connected with a continuous path that never crosses water 

## Program Logic

As we go down the array, we know that if we encounter an open strip that the island of which it is a member still hasn't been fully explored. Conversely, we know that if there are no open strips belonging to an island in a given row, that the island has been fully traversed. Because of this, when we encounter a strip, we only need to know the name of the island it belongs to and if it continues that island. When we traverse a line, we count the number of unique islands present, the number of unique isands with an open strip, and subtract the quantities to determine how many islands have been fully explored on that line.

In order to determine if a strip is open, we only have to check it against the strips in the line below it. No information about the prior lines are nessesary.

Because islands can fork and merge, in order to keep track of what island a strip belongs to, I'm using cascading inheritence: A strip is created without an island name. If there are no strips touching it in row above it, that newly created strip is assigned a new island name. Otherwise, it inherits the island name of the leftmost strip it's in contact with. That strip then passes on its island name to any subsequent strip it touches. That way, when multiple seemingly seperate islands converge, only one island name is kept and propogated. As an example:

01100110\
00101100\
00111100

the 1s in the first 2 lines of the array would have been assigned different island names, island_a and island_b, because they were unconnected. But once it's discovered they connect at the third line, everything with the assignment "island_b" gets reassigned as "island_a"


The advantage of this approach is that only two rows of text need to be held in memory at a given time, since we only need to look on row forward to determine if any terminal strips of land have been reached.

# Input requirements

The program will only accept a text file consisting solely of 1s and 0s. If the input text file contains any other character, an error message will be returned with the location of the illegal character


