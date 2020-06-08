from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Healer(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEndOfTurnEffects(self):
        return # No effect during singles battle


    ######## Doubles Effects ########

