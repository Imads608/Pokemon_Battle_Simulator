from abilityEffects import AbilityEffects
import sys

class Forewarn(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Forewarn reveals " + self.opponentPokemonBattler.getName() + "'s strongest move to be " + moveName)

    ######## Doubles Effects ########
