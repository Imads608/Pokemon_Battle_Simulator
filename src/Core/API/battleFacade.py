from src.Core.API.Singles.singlesBattle import SinglesBattle
from src.Core.API.Common.Data_Types.playerBattler import PlayerBattler
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes
from src.Core.API.Common.Data_Types.actionTypes import ActionTypes

class BattleFacade(object):
    def __init__(self, battleWidgets, pokemonDAL, typeBattle, playerTeam1, playerTeam2):
        self.battleType = typeBattle
        self.battleWidgets = battleWidgets
        self.singlesBattleAdapter = None
        self.doublesBattleAdapter = None

        if (typeBattle == BattleTypes.SINGLES):
            self.singlesBattleAdapter = SinglesBattle(battleWidgets, PlayerBattler(1, playerTeam1), PlayerBattler(2, playerTeam2), pokemonDAL)

    ###### Getters #########
    def getBattleType(self):
        return self.battleType

    def getBattlerAdapter(self, typeAdapter):
        if (typeAdapter == BattleTypes.SINGLES):
            return self.singlesBattleAdapter

    def getBattleWidgets(self):
        return self.battleWidgets

    ############# Battle Events #####################
    def startBattle(self):
        if (self.battleType == BattleTypes.SINGLES):
            self.singlesBattleAdapter.startBattle()

    def selectMove(self, playerNum):
        if (self.battleType == BattleTypes.SINGLES):
            self.singlesBattleAdapter.selectAction(playerNum, ActionTypes.MOVE)

    def switchPokemon(self, playerNum):
        if (self.battleType == BattleTypes.SINGLES):
            self.singlesBattleAdapter.selectAction(playerNum, ActionTypes.SWITCH)

    def restartBattle(self):
        pass

    def viewPokemon(self, playerNum):
        if (self.battleType == BattleTypes.SINGLES):
            self.singlesBattleAdapter.displayPokemonInfo(playerNum)
        return