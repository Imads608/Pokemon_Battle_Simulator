from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class SnowCloak(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.getWeather() == "Sandstorm"):
            self.playerAction.getMoveProperties().setMoveAccuracy(int(self.playerAction.getMoveProperties().getMoveAccuracy() * 4/5))
    
    def singlesEndofTurnEffects(self):
        # Just needs checking if hurt in sandstorm which is already covered in another area of code
        pass

    ######## Doubles Effects ########

