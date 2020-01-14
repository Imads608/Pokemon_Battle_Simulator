from battle_api.common.ability_effects.abilityEffects import AbilityEffects
import sys

class SandForce(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if ((self.playerAction.getTypeMove() in ["ROCK", "GROUND", "STEEL"]) and self.playerAction.getDamageCategory() != "Status" and self.currWeather == "sandstorm"):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.3))
    
    
    ######## Doubles Effects ########

