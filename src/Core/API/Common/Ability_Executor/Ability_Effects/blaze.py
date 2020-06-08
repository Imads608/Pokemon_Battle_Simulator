from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from Common_Data_Types.damageCategory import DamageCategory

class Blaze(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getGivenStats()[0] / 3) and self.playerAction.getDamageCategory() != DamageCategory.STATUS and self.playerAction.getTypeMove() == "FIRE"):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    
    
    ######## Doubles Effects ########

