from abilityEffects import AbilityEffects
import sys

class Illusion(AbilityEffects):
    def __init__(self, name, typeBattle):
        AbilityEffects.__init__(self, name, typeBattle)
    
    ######### Singles Effects ############
    def singlesEntryEffects(self):
        # TODO: Implement switching function call for this to work
        currPlayerTeam = self.currPlayerWidgets[6]
        teamSize = len(self.playerBattler.getPokemonTeam())
        if (self.playerBattler.getPokemonTeam()[teamSize - 1].getName() != self.pokemonBattler.getName() and self.playerBattler[teamSize - 1].getIsFainted() == False):
            tempEffectsNode = PokemonTemporaryEffectsNode()
            tempEffectsNode.setIllusionEffect(True)
            self.pokemonBattler.getTemporaryEffects().enQueue(tempEffectsNode)
            self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
            self.pokemonBattler.setGender(self.opponentPokemonBattler.getGender())
            self.pokemonBattler.setTypes(copy.copy(self.opponentPokemonBattler.getTypes()))
            self.pokemonBattler.setName(self.opponentPokemonBattler.getName())
        
    ######## Doubles Effects ########
