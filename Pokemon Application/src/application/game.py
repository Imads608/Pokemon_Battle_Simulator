import sys
sys.path.append("../automation_scripts")
sys.path.append("../user_interface")
sys.path.append("../../database")
sys.path.append("Metadata")
from battle_simulator import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from teamBuilder_Tab import *
from tab1 import *
from teamBuilderWidgets import *
import createDatabase


import subprocess
import random
import math
from multiprocessing import Process
import copy
import threading
import time

class battleConsumer(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(battleConsumer, self).__init__(parent)
        self.setupUi(self)

        # Widget Shortcuts
        self.evsList = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        self.ivsList = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        self.finalStats = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]

        # Create Pokemon Database
        self.pokemonDB = PokemonDatabase()

        # Create Team Builder Consumer
        self.teamBuilder = TeamBuilder(self.teamBuilderSetup(), self.pokemonDB)

        # Create Battle Consumer
        self.battleConsumer = None

        # Hover Information
        self.txtPokedexEntry.setToolTip("Enter the Pokedex Number here")
        self.txtChosenLevel.setToolTip("Enter the Level of the Pokemon (1-100)")

        # Battle Tab Signals
        self.listPlayer1_team.doubleClicked.connect(lambda: self.battleConsumer.showPokemonBattleInfo(self.player1B_Widgets, "view"))
        self.listPlayer2_team.doubleClicked.connect(lambda: self.battleConsumer.showPokemonBattleInfo(self.player2B_Widgets, "view"))
        self.pushStartBattle.clicked.connect(self.startBattle)
        self.pushSwitchPlayer1.clicked.connect(lambda: self.battleConsumer.playerTurnComplete(self.player1B_Widgets, "switch"))
        self.pushSwitchPlayer2.clicked.connect(lambda: self.battleConsumer.playerTurnComplete(self.player2B_Widgets, "switch"))
        self.listPokemon1_moves.clicked.connect(lambda: self.battleConsumer.playerTurnComplete(self.player1B_Widgets, "move"))  # Testing Purposes
        self.listPokemon2_moves.clicked.connect(lambda: self.battleConsumer.playerTurnComplete(self.player2B_Widgets, "move"))  # Testing Purposes
        # self.listPokemon1_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "move"))   # Use this in the end
        # self.listPokemon2_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "move"))   # Use this in the end

        # Team Builder Signals
        self.txtPokedexEntry.textChanged.connect(self.teamBuilder.updatePokemonEntry)
        self.txtChosenLevel.textChanged.connect(self.teamBuilder.checkPokemonLevel)
        self.pushAddMove.clicked.connect(self.teamBuilder.updateMoveSet)
        self.pushRandomizeEVs.clicked.connect(self.teamBuilder.randomizeEVStats)
        self.pushRandomizeIVs.clicked.connect(self.teamBuilder.randomizeIVStats)
        self.comboNatures.currentIndexChanged.connect(self.teamBuilder.updateStats)
        self.txtEV_HP.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Attack.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Defense.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_SpAttack.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_SpDefense.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Speed.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtIV_HP.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Attack.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Defense.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_SpAttack.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_SpDefense.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Speed.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtHappinessVal.textChanged.connect(self.teamBuilder.finalizePokemon)
        self.pushFinished.clicked.connect(self.teamBuilder.savePokemon)
        self.listCurr_p1Team.doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.listCurr_p1Team, self.teamBuilder.player1Team))
        self.listCurr_p2Team.doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.listCurr_p2Team, self.teamBuilder.player2Team))
        self.pushClearP1.clicked.connect(lambda: self.teamBuilder.clearPokemon(self.listCurr_p1Team, self.teamBuilder.player1Team))
        self.pushClearP2.clicked.connect(lambda: self.teamBuilder.clearPokemon(self.listCurr_p2Team, self.teamBuilder.player2Team))
        self.comboBattleType.currentIndexChanged.connect(self.teamBuilder.checkPlayerTeams)
        self.pushDone.clicked.connect(self.teamBuilder.creationDone)

        # Initialize Start of Game
        self.initializeWidgets()

    ############################### Initialization #########################################################################
    def initializeWidgets(self):

        # Battle Tab
        self.txtBattleInfo.setReadOnly(True)

        self.txtPokemon1_Level.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)

        self.pushStartBattle.setEnabled(False)
        self.pushRestart.setEnabled(False)
        self.pushDifferentTeam.setEnabled(False)
        self.pushSwitchPlayer1.setEnabled(False)
        self.pushSwitchPlayer2.setEnabled(False)

        # Team Buider Tab
        self.teamBuilder.disableDetails()

        itemKeys = list(self.pokemonDB.itemsDatabase.keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            displayName, _, description, _, _, _, _ = self.pokemonDB.itemsDatabase.get(key)
            self.comboItems.addItem(displayName)
            self.comboItems.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.teamBuilder.listInternalItems.append(key)
            count += 1

        count = 0
        for count in range(25):
            increased, decreased = self.teamBuilder.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1

        for i in range(6):
            self.finalStats[i].setEnabled(False)

        return

    ########## Signal Definitions  #########################
    def startBattle(self):
        self.battle1v1Setup()
        self.battleConsumer.setTeam(self.teamBuilder.player1Team, 1)
        self.battleConsumer.setTeam(self.teamBuilder.player2Team, 2)
        self.battleConsumer.battleUI.player1B_Widgets[6] = self.tab1Consumer.battleObject.player1Team
        self.battleConsumer.battleUI.player2B_Widgets[6] = self.tab1Consumer.battleObject.player2Team

        self.battleConsumer.battleUI.pushSwitchPlayer1.setEnabled(True)
        self.battleConsumer.battleUI.listPokemon1_moves.setEnabled(True)

        self.battleConsumer.battleUI.pushStartBattle.setEnabled(False)
        self.battleConsumer.battleUI.listPokemon2_moves.setEnabled(False)

        self.battleConsumer.battleUI.txtBattleInfo.setAlignment(QtCore.Qt.AlignHCenter)
        self.battleConsumer.battleUI.txtBattleInfo.setText("Battle Start!")

        self.battleConsumer.battleUI.listPlayer1_team.setCurrentRow(0)
        self.battleConsumer.battleUI.listPlayer2_team.setCurrentRow(0)

        self.battleConsumer.battleUI.updateBattleInfo("===================================")
        self.battleConsumer.battleUI.updateBattleInfo("Player 1 sent out " + self.battleConsumer.player1Team[self.battleConsumer.currPlayer1PokemonIndex].name)
        self.battleConsumer.battleUI.updateBattleInfo("Player 2 sent out " + self.battleConsumer.player2Team[self.battleConsumer.currPlayer2PokemonIndex].name)

        # Get Entry Level Effects for Player1 and Player2
        self.battleConsumer.executeEntryLevelEffects(self.battleConsumer.battleUI.player1B_Widgets, self.battleConsumer.battleUI.player2B_Widgets, self.battleConsumer.currPlayer1PokemonIndex, self.battleConsumer.currPlayer2PokemonIndex)
        self.battleConsumer.executeEntryLevelEffects(self.battleConsumer.battleUI.player2B_Widgets, self.battleConsumer.battleUI.player1B_Widgets, self.battleConsumer.currPlayer2PokemonIndex, self.battleConsumer.currPlayer1PokemonIndex)
        self.battleConsumer.showPokemonBattleInfo(self.battleConsumer.battleUI.player1B_Widgets, "switch")
        self.battleConsumer.showPokemonBattleInfo(self.battleConsumer.battleUI.player2B_Widgets, "switchview")
        return

    ############### Common Helper Definitions #################
    def teamBuilderSetup(self):
        return TeamBuilderWidgets(self.comboBattleType, self.comboPlayerNumber, self.txtPokedexEntry, self.txtChosenLevel, self.comboGenders, self.txtHappinessVal, self.viewCurrentPokemon, self.evsList, self.ivsList, self.finalStats,
                                          self.pushRandomizeEVs, self.pushRandomizeIVs, self.comboNatures, self.comboAvailableMoves, self.pushAddMove, self.comboItems, self.comboAvailableAbilities, self.listChosenMoves,
                                          self.pushFinished, self.listCurr_p1Team, self.listCurr_p2Team, self.pushClearP1, self.pushClearP2, self.pushDone)

    def battle1v1Setup(self):
        battleWidgets = BattleWidgets1v1(self.lbl_hpPokemon1, self.lbl_hpPokemon2, self.lbl_statusCond1, self.lbl_statusCond2, self.hpBar_Pokemon1, self.hpBar_Pokemon2, self.viewPokemon1, self.viewPokemon2, self.listPokemon1_moves, self.listPokemon2_moves, self.listPlayer1_team, self.listPlayer2_team, self.pushSwitchPlayer1, self.pushSwitchPlayer2)
        self.battleConsumer = Tab1(battleWidgets)

def playMusic():
    subprocess.call("/Users/imadsheriff/Documents/Random\ Stuff/playDancing.sh", shell=True)
    return


def executeGUI():
    currentApp = QtWidgets.QApplication(sys.argv)
    currentForm = battleConsumer()
    currentForm.show()
    currentApp.exec_()

    #currentApp.exec_()

    return


if __name__ == "__main__":
    # p1 = Process(target=executeGUI)
    # p1.start()
    # p2 = Process(target=playMusic)
    # p2.start()
    executeGUI()

    # pool = Pool()
    # pool.map()
    # result1 = pool.apply_async(playMusic())
    # result2 = pool.apply_async(executeGUI())
    # answer1 = result1.get(timeout=10)
    # answer2 = result2.get(timeout=10)