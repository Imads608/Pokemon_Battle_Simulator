from PyQt5 import QtCore, QtGui, QtWidgets

class TeamBuilderWidgets(object):
    def __init__(self, comboBattleType, comboPlayerNumber, txtPokedexEntry, txtChosenLevel, comboGenders, txtHappinessVal, viewCurrentPokemon, evsList, ivsList, finalStats, pushRandomizeEVs, pushRandomizeIVs,
                 comboNatures, comboAvailableMoves, pushAddMove, comboItems, comboAvailableAbilities, listChosenMoves, pushFinished, listCurr_p1Team, listCurr_p2Team, pushClearP1, pushClearP2, pushDone, pushStartBattle, pushRestart, pushDifferentTeam):
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
        self.pushStartBattle = pushStartBattle
        self.pushRestart = pushRestart
        self.pushDifferentTeam = pushDifferentTeam

    def getBattleTypeCombinationBox(self):
        return self.comboBattleType

    def setBattleTypeCombinationBox(self, widget):
        self.comboBattleType = widget

    def getPlayerNumberCombinationBox(self):
        return self.comboPlayerNumber

    def setPlayerNumberCombinationBox(self, widget):
        self.comboPlayerNumber = widget

    def getPokedexEntryTextBox(self):
        return self.txtPokedexEntry

    def setPokedexEntryTextBox(self, widet):
        self.txtPokedexEntry = widget

    def getChosenLevelTextBox(self):
        return self.txtChosenLevel

    def setTextChosenLevel(self, widget):
        self.txtChosenLevel = widget

    def getGendersCombinationBox(self):
        return self.comboGenders

    def setGendersCombinationBox(self, widget):
        self.comboGenders = widget

    def getHappinessValueTextBox(self):
        return self.txtHappinessVal

    def setHappinessValueTextBox(self, widget):
        self.txtHappinessVal = widget

    def getCurrentPokemonView(self):
        return self.viewCurrentPokemon

    def setCurrentPokemonView(self, widget):
        self.viewCurrentPokemon = widget

    def getEvsList(self):
        return self.evsList

    def setEvsList(self, widgets):
        self.evsList = widgets

    def getIvsList(self):
        return self.ivsList

    def setIvsList(self, widgets):
        self.ivsList = widgets

    def getFinalStats(self):
        return self.finalStats

    def setFinalStats(self, widgets):
        self.finalStats = widgets

    def getRandomizeEVsPushButton(self):
        return self.pushRandomizeEVs

    def setRandomizeEVsPushButton(self, widget):
        self.pushRandomizeEVs = widget

    def getRandomizeIVsPushButton(self):
        return self.pushRandomizeIVs

    def setRandomizeIVsPushButton(self, widget):
        self.pushRandomizeIVs = widget

    def getNaturesCombinationBox(self):
        return self.comboNatures

    def setNaturesCombinationBox(self, widget):
        self.comboNatures

    def getAvailableMovesCombinationBox(self):
        return self.comboAvailableMoves

    def setAvailableMovesCombinationBox(self, widget):
        self.comboAvailableMoves = widget

    def getAddMovePushButton(self):
        return self.pushAddMove

    def setAddMovePushButton(self, widget):
        self.pushAddMove = widget

    def getItemsCombinationBox(self):
        return self.comboItems

    def setItemsCombinationBox(self, widget):
        self.comboItems = widget

    def getAvailableAbilitiesCombinationBox(self):
        return self.comboAvailableAbilities

    def setAvailableAbilitiesCombinationBox(self, widget):
        self.comboAvailableAbilities = widget

    def getChosenMovesListBox(self):
        return self.listChosenMoves

    def setChosenMovesListBox(self, widget):
        self.listChosenMoves = widget

    def getPokemonSetupFinishedPushButton(self):
        return self.pushFinished

    def setPokemonSetupFinishedPushButton(self, widget):
        self.pushFinished = widget

    def getCurrentPlayerTeam(self, playerNum):
        if (playerNum == 1):
            return self.listCurr_p1Team
        return self.listCurr_p2Team

    def setCurrentPlayerTeam(self, playerNum, widget):
        if (playerNum == 1):
            self.listCurr_p1Team = widget
        else:
            self.listCurr_p2Team = widget

    def getClearPlayerTeamPushButton(self, playerNum):
        if (playerNum == 1):
            return self.pushClearP1
        return self.pushClearP2

    def setClearPlayerTeamPushButton(self, playerNum, widget):
        if (playerNum == 1):
            self.pushClearP1 = widget
        else:
            self.pushClearP2 = widget

    def getTeamBuilderDonePushButton(self):
        return self.pushDone

    def setTeamBuilderDonePushButton(self, widget):
        self.pushDone = widget

    def getStartBattlePushButton(self):
        return self.pushStartBattle

    def setStartBattlePushButton(self, widget):
        self.pushStartBattle = widget

    def getRestartBattlePushButton(self):
        return self.pushRestart

    def setRestartBattlePushButton(self, widget):
        self.pushRestart = widget

    def getDifferentTeamsPushButton(self):
        return self.pushDifferentTeam

    def setDiffererentTeamsPushButton(self, widget):
        self.pushDifferentTeam = widget

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

    def displayMessageBox(self, header, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(header)
        msg.setInformativeText(body)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #button = msg.button(QtWidgets.QMessageBox.Ok) #### Uncomment for unit testing
        #QtCore.QTimer.singleShot(0, button.clicked)   #### Uncomment for unit testing
        msg.exec_()
