import sys
sys.path.append("../automation_scripts")
sys.path.append("../user_interface")
from PyQt5 import QtCore, QtGui, QtWidgets
from tab2 import *
from tab1 import *
import createDatabase
from battle_simulator import Ui_MainWindow

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

        # Create Tab 2 Consumer
        self.tab2Consumer = Tab2(self)

        # Create Tab 1 Consumer
        self.tab1Consumer = Tab1(self)

        # TODO: Create Item Effects Consumer

        # Variables to store data from database
        self.abilitiesDatabase = None
        self.moveFlags = None
        self.movesDatabase = None
        self.targetFlags = None
        self.pokemonImageDatabase = None
        self.typesDatabase = None
        self.pokedex = None
        self.itemsDatabase = None
        self.pocketMap = None
        self.usabilityInMap = None
        self.usabilityOutMap = None
        self.functionCodesMap = None
        self.databaseTuple = tuple()

        # Widget Shortcuts
        self.evsList = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        self.ivsList = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        self.finalStats = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, self.tab1Consumer.battleObject.player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1, 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2, self.txtPokemon2_Level, self.pushSwitchPlayer2, self.tab1Consumer.battleObject.player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2, 2]

        # Hover Information
        self.txtPokedexEntry.setToolTip("Enter the Pokedex Number here")
        self.txtChosenLevel.setToolTip("Enter the Level of the Pokemon (1-100)")

        # Tab 1 Signals
        self.listPlayer1_team.doubleClicked.connect(lambda: self.tab1Consumer.showPokemonBattleInfo(self.player1B_Widgets, "view"))
        self.listPlayer2_team.doubleClicked.connect(lambda: self.tab1Consumer.showPokemonBattleInfo(self.player2B_Widgets, "view"))
        self.pushStartBattle.clicked.connect(self.startBattle)
        self.pushSwitchPlayer1.clicked.connect(lambda: self.tab1Consumer.playerTurnComplete(self.player1B_Widgets, "switch"))
        self.pushSwitchPlayer2.clicked.connect(lambda: self.tab1Consumer.playerTurnComplete(self.player2B_Widgets, "switch"))
        self.listPokemon1_moves.clicked.connect(lambda: self.tab1Consumer.playerTurnComplete(self.player1B_Widgets, "move"))  # Testing Purposes
        self.listPokemon2_moves.clicked.connect(lambda: self.tab1Consumer.playerTurnComplete(self.player2B_Widgets, "move"))  # Testing Purposes
        # self.listPokemon1_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "move"))   # Use this in the end
        # self.listPokemon2_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "move"))   # Use this in the end

        # Tab 2 Signals
        self.txtPokedexEntry.textChanged.connect(self.tab2Consumer.updatePokemonEntry)
        self.txtChosenLevel.textChanged.connect(self.tab2Consumer.checkPokemonLevel)
        self.pushAddMove.clicked.connect(self.tab2Consumer.updateMoveSet)
        self.pushRandomizeEVs.clicked.connect(self.tab2Consumer.randomizeEVStats)
        self.pushRandomizeIVs.clicked.connect(self.tab2Consumer.randomizeIVStats)
        self.comboNatures.currentIndexChanged.connect(self.tab2Consumer.updateStats)
        self.txtEV_HP.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtEV_Attack.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtEV_Defense.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtEV_SpAttack.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtEV_SpDefense.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtEV_Speed.textChanged.connect(self.tab2Consumer.updateEVs)
        self.txtIV_HP.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtIV_Attack.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtIV_Defense.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtIV_SpAttack.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtIV_SpDefense.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtIV_Speed.textChanged.connect(self.tab2Consumer.updateIVs)
        self.txtHappinessVal.textChanged.connect(self.tab2Consumer.finalizePokemon)
        self.pushFinished.clicked.connect(self.tab2Consumer.savePokemon)
        self.listCurr_p1Team.doubleClicked.connect(lambda: self.tab2Consumer.restorePokemonDetails(self.listCurr_p1Team, self.tab2Consumer.player1Team))
        self.listCurr_p2Team.doubleClicked.connect(lambda: self.tab2Consumer.restorePokemonDetails(self.listCurr_p2Team, self.tab2Consumer.player2Team))
        self.pushClearP1.clicked.connect(lambda: self.tab2Consumer.clearPokemon(self.listCurr_p1Team, self.tab2Consumer.player1Team))
        self.pushClearP2.clicked.connect(lambda: self.tab2Consumer.clearPokemon(self.listCurr_p2Team, self.tab2Consumer.player2Team))
        self.comboBattleType.currentIndexChanged.connect(self.tab2Consumer.checkPlayerTeams)
        self.pushDone.clicked.connect(self.tab2Consumer.creationDone)

        # Initialize Start of Game
        self.initializeDatabase()
        self.initializeWidgets()

    ############################### Initialization #########################################################################

    def initializeDatabase(self):
        self.abilitiesDatabase = createDatabase.allAbilities("../database/abilities.csv")
        self.moveFlags = createDatabase.getMoveFlags()
        self.movesDatabase = createDatabase.allMoves("../database/moves.csv")
        self.targetFlags = createDatabase.getTargetFlags()
        self.pokemonImageDatabase = createDatabase.getPokemonImages("../database/img/*")
        self.typesDatabase = createDatabase.getAllTypes("../database/types.csv")
        self.pokedex = createDatabase.getPokedex("../database/pokemon.txt", self.typesDatabase, self.pokemonImageDatabase)
        self.itemsDatabase = createDatabase.allItems("../database/items.csv")
        self.pocketMap = createDatabase.definePocket()
        self.usabilityInMap = createDatabase.defineUsabilityInBattle()
        self.usabilityOutMap = createDatabase.defineUsabilityOutBattle()
        self.functionCodesMap = createDatabase.getFunctionCodes("../database/Function Codes/Outputs/FCDescription.xlsx")
        self.abilitiesEffectsMap = createDatabase.getAbilitiesMapping("../database/abilityTypes2.csv")
        self.databaseTuple = (self.abilitiesDatabase, self.moveFlags, self.movesDatabase, self.targetFlags, self.pokemonImageDatabase, self.typesDatabase, self.pokedex, self.itemsDatabase, self.pocketMap, self.usabilityInMap, self.usabilityInMap, self.functionCodesMap, self.abilitiesEffectsMap)

    def initializeWidgets(self):

        # Tab 1
        self.txtBattleInfo.setReadOnly(True)

        self.txtPokemon1_Level.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)

        self.pushStartBattle.setEnabled(False)
        self.pushRestart.setEnabled(False)
        self.pushDifferentTeam.setEnabled(False)
        self.pushSwitchPlayer1.setEnabled(False)
        self.pushSwitchPlayer2.setEnabled(False)

        # Tab 2
        self.tab2Consumer.disableDetails()

        itemKeys = list(self.itemsDatabase.keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            displayName, _, description, _, _, _, _ = self.itemsDatabase.get(key)
            self.comboItems.addItem(displayName)
            self.comboItems.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.tab2Consumer.listInternalItems.append(key)
            count += 1

        count = 0
        for count in range(25):
            increased, decreased = self.tab2Consumer.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1

        for i in range(6):
            self.finalStats[i].setEnabled(False)

        return

    ########## Signal Definitions  #########################

    def startBattle(self):
        self.tab1Consumer.battleObject.setTeams(self.tab2Consumer.player1Team, self.tab2Consumer.player2Team)
        self.player1B_Widgets[6] = self.tab1Consumer.battleObject.player1Team
        self.player2B_Widgets[6] = self.tab1Consumer.battleObject.player2Team

        self.pushSwitchPlayer1.setEnabled(True)
        self.listPokemon1_moves.setEnabled(True)

        self.pushStartBattle.setEnabled(False)
        self.listPokemon2_moves.setEnabled(False)

        self.txtBattleInfo.setAlignment(QtCore.Qt.AlignHCenter)
        self.txtBattleInfo.setText("Battle Start!")

        self.listPlayer1_team.setCurrentRow(0)
        self.listPlayer2_team.setCurrentRow(0)

        self.tab1Consumer.updateBattleInfo("===================================")
        self.tab1Consumer.updateBattleInfo("Player 1 sent out " + self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex].name)
        self.tab1Consumer.updateBattleInfo("Player 2 sent out " + self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex].name)

        # Get Entry Level Effects for Player1 and Player2
        self.tab1Consumer.executeEntryLevelEffects(self.player1B_Widgets, self.player2B_Widgets, self.tab1Consumer.battleObject.currPlayer1PokemonIndex, self.tab1Consumer.battleObject.currPlayer2PokemonIndex)
        self.tab1Consumer.executeEntryLevelEffects(self.player2B_Widgets, self.player1B_Widgets, self.tab1Consumer.battleObject.currPlayer2PokemonIndex, self.tab1Consumer.battleObject.currPlayer1PokemonIndex)
        self.tab1Consumer.showPokemonBattleInfo(self.player1B_Widgets, "switch")
        self.tab1Consumer.showPokemonBattleInfo(self.player2B_Widgets, "switchview")
        return

    ############### Common Helper Definitions #################
    def updateBattleInfo(self, textBattle):
        self.txtBattleInfo.append(textBattle)
        return

    def displayPokemon(self, viewPokemon, pokedexEntry):
        if (pokedexEntry != None):
            pokemonImageScene = QtWidgets.QGraphicsScene()
            pokemon = self.pokedex.get(pokedexEntry)
            pixmap = QtGui.QPixmap(pokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem = QtWidgets.QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, QtCore.Qt.KeepAspectRatio)
        else:
            scene = QtWidgets.QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()

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