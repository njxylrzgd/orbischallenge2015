from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *


class PlayerAI:
    def __init__(self):
        # Initialize any objects or variables you need here.
        pass

    def get_move(self, gameboard, player, opponent):
        '''
        First step of any turn is to refresh the values of each tile on the board. 
        Tile values are affected by things like turret firing in an upcoming turn, walls, power-ups, and opponent.
        
        The following is a weighted FSM. Our AI values safety over aggression.
        The AI selects the next move in the following order, depending on opportunity:
        
        1. Check if you’re in the line of sight of your enemy
        2. Check for bullets in your two tiles proximity S
        3. Avoid getting shot by turrets S
        4. Check for power ups nearby
        4. Look if you can get in the line of sight of a turret
        5. See if power up available/necessary
        
        '''
        
        
        
        return Move.NONE
