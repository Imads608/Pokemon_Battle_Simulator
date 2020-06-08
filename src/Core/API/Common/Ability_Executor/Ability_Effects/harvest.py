from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects


class Harvest(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    # TODO: Must implement later
    def singlesEndOfTurnEffects(self):
        return


    ######## Doubles Effects ########

