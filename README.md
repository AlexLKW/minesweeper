# Minesweeper

***

## Tutorial
- Each cell has three status: uncovered, covered, and flagged.                                                         
- Players can select a covered cell to uncover it.                                                                         
- Players can select a covered cell to flag it.                                                                         
- Players cannot select a flagged cell to uncover it (as a safety measure).                                           
- Players can unflag a flagged cell.                                                                                 
- Players selected a cell with hidden mine will lose a game.                                                        
- Player uncovered all cells without mines will win the game (no matter flagged or not).                           
- An uncovered cell will display the number of mines for its 8 surrounding cells.                                         
- An  uncovered  cell  with  no  surrounding  mines  will  trigger its  surrounding  cells  to  uncover.

***

## Features
- Custom Difficulties
  - Easy Mode: 3 Mines in 5 by 5 matrix
  - Default Mode: 10 Mines in 9 by 9 matrix
  - Normal Mode: 13 Mines in 9 by 9 matrix
  - Hard Mode: 20 Mines in 9 by 9 matrix
  - Custom Mode: Mines and matrix are fully customizable by players

- Time Counter
  - Time will be count in the background
  - Compete and beat your friends by clearing the level quickly

- Retry
  - Easy replay prompt at the end of the game
  - Less time loading, more time playing

- Leaderboard
  - Winners will be asked to mark a record for leaderboard
  - Record includes player's name, time to clear, steps taken, and score

- Machine assist (AI mode)
  - Implemented an assisted mode for players which would randomly pick a tile to uncover
