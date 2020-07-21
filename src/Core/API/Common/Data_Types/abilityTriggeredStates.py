from enum import IntEnum

class AbilitryTriggeredStates(IntEnum):
    ENTRY = 0
    PRIORITY = 1
    ATTACKER_MOVE_EFFECTS = 2
    ATTACKER_MOVE_EXECUTION = 3
    OPPONENT_MOVE_EFFECTS = 4
    OPPONENT_MOVE_EXECUTION = 5
    END_OF_TURN = 6
    SWITCHED_OUT = 7
    SWITCHED_IN = 8
