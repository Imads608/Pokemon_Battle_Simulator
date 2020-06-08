from battle_api.common.AbilityProcessor.ability_effects.abilityEffects import AbilityEffects
import sys

class Torrent(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 3) and self.playerAction.getDamageCategory() != "Status" and self.playerAction.getTypeMove() == "WATER"):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    
    
    ######## Doubles Effects ########

