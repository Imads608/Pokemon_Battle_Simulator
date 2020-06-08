from PyQt5 import QtCore

class SinglesBattleWidgetsSignals(QtCore.QObject):
    sig1 = QtCore.pyqtSignal(object, object)
    pokemonHPDecreaseSignal = QtCore.pyqtSignal(int, object, int, str)
    pokemonHPIncreaseSignal = QtCore.pyqtSignal(int, object, int, str)
    battleMessageSignal = QtCore.pyqtSignal(str)
    pokemonSwitchedSignal = QtCore.pyqtSignal(int, object, str)  # switchedPokemonIndex, playerBattler
    showPokemonStatusConditionSignal = QtCore.pyqtSignal(int, object, str)
    togglePokemonSelectionSignal = QtCore.pyqtSignal(int, bool)
    togglePokemonSwitchSignal = QtCore.pyqtSignal(int, bool)
    togglePokemonMovesSelectionSignal = QtCore.pyqtSignal(int, bool)
    displayPokemonInfoSignal = QtCore.pyqtSignal(object)
    pokemonFaintedSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QObject.__init__(self)

    def getPokemonHPDecreaseSignal(self):
        return self.pokemonHPDecreaseSignal

    def getPokemonHPIncreaseSignal(self):
        return self.pokemonHPIncreaseSignal

    def getBattleMessageSignal(self):
        return self.battleMessageSignal

    def getPokemonSwitchedSignal(self):
        return self.pokemonSwitchedSignal

    def getShowPokemonStatusConditionSignal(self):
        return self.showPokemonStatusConditionSignal

    def getTogglePokemonSelectionSignal(self):
        return self.togglePokemonSelectionSignal

    def getTogglePokemonSwitchSignal(self):
        return self.togglePokemonSwitchSignal

    def getTogglePokemonMovesSelectionSignal(self):
        return self.togglePokemonMovesSelectionSignal

    def getDisplayPokemonInfoSignal(self):
        return self.displayPokemonInfoSignal

    def getPokemonFaintedSignal(self):
        return self.pokemonFaintedSignal
