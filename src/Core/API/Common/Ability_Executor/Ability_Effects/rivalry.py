from src.Core.API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from src.Common.genders import Genders

class Rivalry(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDAL):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDAL)
    
    ######### Singles Effects ############
    def singlesAttackerMoveEffects(self):
        if (self.pokemonBattler.getGender() != Genders.GENDERLESS and self.opponentPokemonBattler.getGender() != Genders.GENDERLESS):
            if (self.pokemonBattler.getGender() == self.opponentPokemonBattler.getGender()):
                self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.25))
            else:
                self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 0.75))
    ######## Doubles Effects ########

