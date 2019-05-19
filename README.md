# river-player


New networking-based version of the game playing system that allows for the players to save information across games, etc.
To preserve the old version I left it in the `old` folder


The new version is all run from the `networking` folder. 


Files:  
`game.py`: classes that define the game rules, rounds, and tricks . 
`gamemanager.py`: starts and orchestrates gameplay, keeps score, interfaces with players.  
`state.py`: class definition for state that the player can see (cannot give player full access to trick)  
`statemachine.py`: operations on the state class - most importantly `findlegals()` and `simulate()` (NOT YET WORKING)  

Players:  
`legal.py`: legal player that plays first legal move it sees  
`baseline.py`: baseline player (bids assuming equal distribution of tricks and otherwise plays like old baseline player, but communicates differently with the game manager)  
`mcs.py`: NOT YET WORKING implementation of Monte Carlo Search player (building block of MCTS) - easy to implement once we get a working state machine  

Things we need to do  
1) MOST IMPORTANTLY: get a working `simulate()` function on the state machine. There is some logging in it right now which shows that it fails in certain cases  
2) Use working `simulate()` to implement MCS (easy)  

Running the players  
For each player: `python playername.py PORT`  
For gamemanager: `python gamemanager.py`  

For example, for two players use three command prompts:  
`$ python baseline.py 7000`  
`$ python legal.py 7001`  
`$ python gamemanager.py` 

NOTE: currently the game manager is configured to run with 2 players. Change `nplayers` in `gamemanager.py` to run with more.
