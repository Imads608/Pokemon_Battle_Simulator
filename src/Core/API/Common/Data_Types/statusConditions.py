from enum import Enum

class NonVolatileStatusConditions(Enum):
    HEALTHY = 0
    POISONED = 1
    BADLY_POISONED = 2
    PARALYZED = 3
    ASLEEP = 4
    FROZEN = 5
    BURN = 6

class VolatileStatusConditions(Enum):
    DROWSY = 7
    CONFUSED = 8
    INFATUATED = 9


