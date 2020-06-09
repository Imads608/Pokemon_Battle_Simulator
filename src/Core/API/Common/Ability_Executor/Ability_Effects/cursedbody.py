from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import  AbilityEffects
from Battle_API.Common.Battle_Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode
from Common_Data_Types.damageCategory import DamageCategory

from random import random

class CursedBody(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveExecutionEffects(self):
        if (self.playerAction.getMoveProperties().getDamageCategory() != DamageCategory.STATUS and self.playerAction.getMoveProperties().getTotalDamage() > 0):
            randNum = random.randint(0,100)
            (indefiniteEffectsNode, tempEffectsNode) = self.pokemonBattler.getTemporaryEffects().seek()
            if (randNum <= 30):
                if (self.opponentPokemonBattler.getIsFainted() == False or (self.opponentPokemonBattler.getIsFainted() == True and indefiniteEffectsNode == None) or (self.opponentPokemonBattler.getIsFainted() == True and indefiniteEffectsNode != None and indefiniteEffectsNode.getSubstituteEffect() == None)):
                    moveUsed = self.playerAction.getMoveProperties().getInternalMove()
                    effectsNode = PokemonTemporaryEffectsNode()
                    effectsNode.addMoveBlocked(moveUsed)
                    self.pokemonBattler.getTemporaryEffects().push(effectsNode, 4)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Cursed Body blocked " + moveUsed)
        return


    ######## Doubles Effects ########
