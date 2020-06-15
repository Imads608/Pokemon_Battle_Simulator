from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from src.Core.API.Common.Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode
from src.Common.genders import Genders

from random import random

class CuteCharm(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if ("a" in self.playerAction.getMoveProperties().getMoveFlags() and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(0,100)
            if (self.opponentPokemonBattler.getGender() != self.pokemonBattler.getGender() and self.opponentPokemonBattler.getGender() != Genders.GENDERLESS
                and self.pokemonBattler.getGender() != Genders.GENDERLESS):
                if (randNum <= 30):
                    effectsNode = PokemonTemporaryEffectsNode()
                    effectsNode.setInfatuation(self.opponentPokemonBattler.getName())
                    self.pokemonBattler.getTemporaryEffects().push(effectsNode, -1)
                    self.battleWidgetsSignals().getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Cute Charm infatuated " + self.pokemonBattler.getName())

        return


    ######## Doubles Effects ########

