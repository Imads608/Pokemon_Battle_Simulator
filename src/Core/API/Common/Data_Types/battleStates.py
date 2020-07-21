from enum import IntEnum

class BattleStates(IntEnum):
    ENTRY = 0
    ACTION_VALIDATION = 1
    MOVE_PRE_EXECUTION = 2
    MOVE_POST_EXECUTION = 3
    END_OF_TURN = 4
    SWITCH = 5
    #ATTACKER_MOVE_EFFECTS = 2
    #ATTACKER_MOVE_EXECUTION = 3
    #OPPONENT_MOVE_EFFECTS = 4
    #OPPONENT_MOVE_EXECUTION = 5
    #END_OF_TURN = 6
    #SWITCHED_OUT = 7
    #SWITCHED_IN = 8