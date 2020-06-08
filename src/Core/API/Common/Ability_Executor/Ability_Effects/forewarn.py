from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects

class Forewarn(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        maxPower = -1
        moveName = ""
        for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
            pokemonMove = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
            basePower = pokemonMove.power
            if (basePower > maxPower):
                maxPower = basePower
                moveName = pokemonMove.name
        if (moveName != ""):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Forewarn reveals " + self.opponentPokemonBattler.getName() + "'s strongest move to be " + moveName)

    ######## Doubles Effects ########
