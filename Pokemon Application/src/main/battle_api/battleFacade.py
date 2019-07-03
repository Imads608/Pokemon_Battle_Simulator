import sys
sys.path.append("singles/")
sys.path.append("doubles/")
sys.path.append("common/")

from singlesBattle import SinglesBattle
from playerBattler import PlayerBattler

class BattleFacade(object):
    def __init__(self, battleWidgets, pokemonMetadata, typeBattle, playerTeam1, playerTeam2):
        self.battleType = typeBattle
        self.battleWidgets = battleWidgets
        self.singlesBattleAdapter = None
        self.doublesBattleAdapter = None

        if (typeBattle == "singles"):
            battleWidgets.setPlayerWidgetShortcuts(playerTeam1, playerTeam2)
            self.singlesBattleAdapter = SinglesBattle(battleWidgets, PlayerBattler(1, playerTeam1), PlayerBattler(2, playerTeam2), pokemonMetadata)
        else:
            self.doublesBattleAdapter = DoublesBattle(battleWidgets, PlayerBattler(1, playerTeam1), PlayerBattler(2, playerTeam2), pokemonMetadata)

    ###### Getters #########
    def getBattleType(self):
        return self.battleType

    def getBattlerAdapter(self, typeAdapter):
        if (typeAdapter == "singles"):
            return self.singlesBattleAdapter
        return self.doublesBattleAdapter

    def getBattleWidgets(self):
        return self.battleWidgets

    ############# Battle Events #####################
    def startBattle(self):
        if (self.battleType == "singles"):
            self.singlesBattleAdapter.startBattle()
        else:
            self.doublesBattleAdapter.startBattle()

    def selectMove(self, playerNum):
        if (self.battleType == "singles"):
            moveChosenIndex = self.battleWidgets.getMoveChosenIndex()
            self.singlesBattleAdapter.selectAction(playerNum, "move", moveChosenIndex)
        else:
            self.doublesBattleAdapter.selectAction(playerNum, "move")

    def switchPokemon(self, playerNum):
        if (self.battleType == "singles"):
            chosenPokemonIndex = self.battleWidgets.getChosenPokemonIndex()
            self.singlesBattleAdapter.selectAction(playerNum, "switch", chosenPokemonIndex)
        else:
            self.doublesBattleAdapter.selectAction(playerNum, "switch")

    def restartBattle(self):
        pass

    def viewPokemon(self, num):
        return

'''
class MinionAdapter:
    _initialised = False

    def __init__(self, minion, **adapted_methods):
        self.minion = minion

    @data.setter
    def setMethod(self, val):
        self.minion = val
        self.notify()
'''