from Battle_API.Common.Ability_Executor.Ability_Effects.abilityEffects import AbilityEffects
from Battle_API.Common.Battle_Data_Types.pokemonTemporaryEffects import PokemonTemporaryEffectsNode

# TODO: Items trigger this ability
class FlashFire(AbilityEffects):
    def __init__(self, name, typeBattle, battleProperties, pokemonDataSource):
        AbilityEffects.__init__(self, name, typeBattle, battleProperties, pokemonDataSource)
    
    ######### Singles Effects ############
    def singlesOpponentMoveEffects(self):
        if (self.playerAction.getMoveProperties().getTypeMove() == "FIRE"):
            self.playerAction.getMoveProperties().setEffectiveness(0)
            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Flash Fire made it immune to Fire Type Moves")
            temporaryEffectsNode = PokemonTemporaryEffectsNode()
            temporaryEffectsNode.setTypeMovesPowered({"FIRE":1.5})
            self.opponentPokemonBattlerTempProperties.getCurrentTemporaryEffects().push(temporaryEffectsNode, -1)


    ######## Doubles Effects ########

