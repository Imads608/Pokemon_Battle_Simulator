from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.damageCategory import DamageCategory

class Prankster(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        pokemonMove = self.pokemonDAL.movesMetadata.get(self.playerAction.getMoveInternalName())
        if (pokemonMove.damageCategory == DamageCategory.STATUS):
            self.playerAction.setPriority(self.playerAction.getPriority()+1) 
    
    ######## Doubles Effects ########

