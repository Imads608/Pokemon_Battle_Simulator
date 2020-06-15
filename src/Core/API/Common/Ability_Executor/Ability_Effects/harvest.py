from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects


class Harvest(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    # TODO: Must implement later
    def singlesEndOfTurnEffects(self):
        return


    ######## Doubles Effects ########

