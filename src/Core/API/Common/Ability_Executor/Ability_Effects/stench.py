from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from random import random


#TODO: This ability needs some research for flinching attacker pokemon when executing multi-strike moves.
class Stench(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)

    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(1, 100)
            if (randNum <= 10):
                pass
            self.battleWidgetsSignals().getBattleMessageSignal(self.opponentPokemonBattler.getName() + "'s Mummy changed " + self.opponentPokemonBattler.getName() + "'s ability to Mummy")
        return

    ######## Doubles Effects ########

