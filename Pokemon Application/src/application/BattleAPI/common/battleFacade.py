class BattleFacade(object):
    def ___init__(self, battleUI, pokemonDB, typeBattle, playerTeam1, playerTeam2):
        self.battleType = typeBattle
        self.singlesBattleAdapter = None
        self.doublesBattleAdapter = None
        self.battleObserver = BattleObserver(battleUI)

        if (typeBattle == "Singles"):
            self.singlesBattleAdapter = SinglesBattle(self.battleUI, PlayerBattler(1, playerTeam1), PlayerBattler(2, playerTeam2), pokemonDB)
        else:
            self.doublesBattleAdapter = DoublesBattle(self.battleUI, PlayerBattler(1, playerTeam1), PlayerBattler(2, playerTeam2), pokemonDB)


    def startBattle(self):
        if (self.battleType == "Singles"):
            self.singlesBattleAdapter.startBattle()
        else:
            self.doublesBattleAdapter.startBattle()

    def executeMove(self, playerNum):
        pass

    def switchPokemon(self, playerNum):
        pass

    def getBattleWidgets(self):
        if (self.battleType == "Singles"):
            return self.singlesBattleAdapter.getBattleUI()
        return self.doublesBattleAdapter.getBattleUI()

    def restartBattle(self):
        pass


class MinionAdapter:
    _initialised = False

    def __init__(self, minion, **adapted_methods):
        self.minion = minion

    @data.setter
    def setMethod(self, val):
        self.minion = val
        self.notify()


if __name__ == "__main__":