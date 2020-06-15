from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Stall(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesPriorityEffects(self):
        self.playerAction.setQueuePosition(2)
    
    
    ######## Doubles Effects ########

