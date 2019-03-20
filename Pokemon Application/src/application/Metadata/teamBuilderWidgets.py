from PyQt5 import QtCore, QtGui, QtWidgets

class TeamBuilderWidgets(object):
    def __init__(self, comboBattleType, comboPlayerNumber, txtPokedexEntry, txtChosenLevel, comboGenders, txtHappinessVal, viewCurrentPokemon, evsList, ivsList, finalStats, pushRandomizeEVs, pushRandomizeIVs,
                 comboNatures, comboAvailableMoves, pushAddMove, comboItems, comboAvailableAbilities, listChosenMoves, pushFinished, listCurr_p1Team, listCurr_p2Team, pushClearP1, pushClearP2, pushDone):
        self.comboBattleType = comboBattleType
        self.comboPlayerNumber = comboPlayerNumber
        self.txtPokedexEntry = txtPokedexEntry
        self.txtChosenLevel = txtChosenLevel
        self.comboGenders = comboGenders
        self.txtHappinessVal = txtHappinessVal
        self.viewCurrentPokemon = viewCurrentPokemon
        self.evsList = evsList
        self.ivsList = ivsList
        self.finalStats = finalStats
        self.pushRandomizeEVs = pushRandomizeEVs
        self.pushRandomizeIVs = pushRandomizeIVs
        self.comboNatures = comboNatures
        self.comboAvailableMoves = comboAvailableMoves
        self.pushAddMove = pushAddMove
        self.comboItems = comboItems
        self.comboAvailableAbilities = comboAvailableAbilities
        self.listChosenMoves = listChosenMoves
        self.pushFinished = pushFinished
        self.listCurr_p1Team = listCurr_p1Team
        self.listCurr_p2Team = listCurr_p2Team
        self.pushClearP1 = pushClearP1
        self.pushClearP2 = pushClearP2
        self.pushDone = pushDone

    def displayPokemon(self, viewPokemon, pokedexEntry, pokedex):
        if (pokedexEntry != None):
            pokemonImageScene = QtWidgets.QGraphicsScene()
            pokemon = pokedex.get(pokedexEntry)
            pixmap = QtGui.QPixmap(pokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem = QtWidgets.QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, QtCore.Qt.KeepAspectRatio)
        else:
            scene = QtWidgets.QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()
