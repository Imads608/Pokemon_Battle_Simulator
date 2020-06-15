from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class VictoryStar(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 1.1))
        
    ######## Doubles Effects ########

