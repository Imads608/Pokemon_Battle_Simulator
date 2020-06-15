from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.stats import Stats
from src.Common.damageCategory import DamageCategory

class Torrent(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getBattleStat(Stats.HP) <= int(self.pokemonBattler.getGivenStat(Stats.HP) / 3) and self.playerAction.getDamageCategory() != DamageCategory.STATUS and self.playerAction.getTypeMove() == "WATER"):
            self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
    
    
    
    ######## Doubles Effects ########

