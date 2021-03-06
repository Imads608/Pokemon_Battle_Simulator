import sys
sys.path.append("../automation_scripts")
sys.path.append("../user_interface")
from PyQt5 import QtCore, QtGui, QtWidgets
from battle_simulator import Ui_MainWindow
import subprocess
import random
import math
import createDatabase
from multiprocessing import Process
from classes import *
from functionCodeEffects import *
import copy

class battleConsumer(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        super(battleConsumer, self).__init__(parent)
        self.setupUi(self)

        # Create BattleField Effects Object
        self.battleFieldObject = BattleField()

        # Create Battle Object
        self.battleObject = Battle()

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

        # Additional Variables
        # Tab 2
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.listInternalItems = []
        self.chosenMovesetMap = {}
        self.natureEffects = [("None", "None"), ("Def", "Att"), ("SpAtt", "Att"), ("SpDef", "Att"), ("Spd", "Att"),
                         ("Att", "Def"), ("None", "None"), ("SpAtt", "Def"),("SpDef", "Def"), ("Spd", "Def"),
                         ("Att", "SpAtt"), ("Def", "SpAtt"), ("None", "None"), ("SpDef", "SpAtt"), ("SpAtt", "SpDef"),
                         ("Spd", "SpA"), ("Att", "SpDef"), ("Def", "SpDef"), ("None", "None"), ("Spd", "SpDef"), ("Att", "Spd"),
                         ("Def", "Spd"), ("SpAtt", "Spd"), ("SpDef", "Spd"), ("None", "None")]
        self.player1Team = []
        self.player2Team = []

        # Tab 1
        self.criticalHitStages = [16, 8, 4, 3, 2]
        self.statsStageMultipliers = [2/8, 2/7, 2/6, 2/5, 2/4, 2/3, 2/2, 3/2, 4/2, 5/2, 6/2, 7/2, 8/2]
        self.stage0Index = 6
        self.accuracy_evasionMultipliers = [3/9, 3/8, 3/7, 3/6, 3/5, 3/4, 3/3, 4/3, 5/3, 6/3, 7/3, 8/3, 9/3]
        self.accuracy_evasionStage0Index = 6
        self.nonVolatileStatusConditions = ["Healthy", "Poisoned", "Badly Poisoned", "Paralyzed", "Asleep", "Frozen", "Burn", "Fainted"]
        self.volatileStatusConditions = ["Drowsy", "Confused", "Infatuated"]

        # Widget Shortcuts
        self.evsList = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        self.ivsList = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        self.finalStatsList = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, self.battleObject.player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1, 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2, self.txtPokemon2_Level, self.pushSwitchPlayer2, self.battleObject.player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2, 2]

        # Hover Information
        self.txtPokedexEntry.setToolTip("Enter the Pokedex Number here")
        self.txtChosenLevel.setToolTip("Enter the Level of the Pokemon (1-100)")

        # Tab 1 Signals
        self.listPlayer1_team.doubleClicked.connect(lambda:self.showPokemonBattleInfo(self.player1B_Widgets, "view"))
        self.listPlayer2_team.doubleClicked.connect(lambda:self.showPokemonBattleInfo(self.player2B_Widgets, "view"))
        self.pushStartBattle.clicked.connect(self.startBattle)
        self.pushSwitchPlayer1.clicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "switch"))
        self.pushSwitchPlayer2.clicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "switch"))
        self.listPokemon1_moves.clicked.connect(lambda: self.playerTurnComplete(self.player1B_Widgets, "move")) # Testing Purposes
        self.listPokemon2_moves.clicked.connect(lambda: self.playerTurnComplete(self.player2B_Widgets, "move")) # Testing Purposes
        #self.listPokemon1_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player1B_Widgets, "move"))   # Use this in the end
        #self.listPokemon2_moves.doubleClicked.connect(lambda:self.playerTurnComplete(self.player2B_Widgets, "move"))   @ use this in the end


        # Tab 2 Signals
        self.txtPokedexEntry.textChanged.connect(self.updatePokemonEntry)
        self.txtChosenLevel.textChanged.connect(self.checkPokemonLevel)
        self.pushAddMove.clicked.connect(self.updateMoveSet)
        self.pushRandomizeEVs.clicked.connect(self.randomizeEVStats)
        self.pushRandomizeIVs.clicked.connect(self.randomizeIVStats)
        self.comboNatures.currentIndexChanged.connect(self.updateStats)
        self.txtEV_HP.textChanged.connect(self.updateEVs)
        self.txtEV_Attack.textChanged.connect(self.updateEVs)
        self.txtEV_Defense.textChanged.connect(self.updateEVs)
        self.txtEV_SpAttack.textChanged.connect(self.updateEVs)
        self.txtEV_SpDefense.textChanged.connect(self.updateEVs)
        self.txtEV_Speed.textChanged.connect(self.updateEVs)
        self.txtIV_HP.textChanged.connect(self.updateIVs)
        self.txtIV_Attack.textChanged.connect(self.updateIVs)
        self.txtIV_Defense.textChanged.connect(self.updateIVs)
        self.txtIV_SpAttack.textChanged.connect(self.updateIVs)
        self.txtIV_SpDefense.textChanged.connect(self.updateIVs)
        self.txtIV_Speed.textChanged.connect(self.updateIVs)
        self.txtHappinessVal.textChanged.connect(self.finalizePokemon)
        self.pushFinished.clicked.connect(self.savePokemon)
        self.listCurr_p1Team.doubleClicked.connect(lambda:self.restorePokemonDetails(self.listCurr_p1Team, self.player1Team))
        self.listCurr_p2Team.doubleClicked.connect(lambda:self.restorePokemonDetails(self.listCurr_p2Team, self.player2Team))
        self.pushClearP1.clicked.connect(lambda:self.clearPokemon(self.listCurr_p1Team, self.player1Team))
        self.pushClearP2.clicked.connect(lambda:self.clearPokemon(self.listCurr_p2Team, self.player2Team))
        self.comboBattleType.currentIndexChanged.connect(self.checkPlayerTeams)
        self.pushDone.clicked.connect(self.creationDone)

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
        self.abilitiesEffectsMap = createDatabase.getAbilitiesMapping("../database/abilityTypes.csv")

    def initializeWidgets(self):

        # Tab 1
        self.txtBattleInfo.setReadOnly(True)
        #self.txtBattleInfo.setVerticalScrollBar(self.verticalScrollBar)
        #elf.txtBattleInfo.setHorizontalScrollBar(self.horizontalScrollBar)

        self.txtPokemon1_Level.setEnabled(False)
        #self.txtPokemon1_Ability.setEnabled(False)
        #self.txtPokemon1_Nature.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)
       #self.txtPokemon2_Ability.setEnabled(False)
       #self.txtPokemon2_Nature.setEnabled(False)

        self.pushStartBattle.setEnabled(False)
        self.pushRestart.setEnabled(False)
        self.pushDifferentTeam.setEnabled(False)
        self.pushSwitchPlayer1.setEnabled(False)
        self.pushSwitchPlayer2.setEnabled(False)


        # Tab 2
        self.disableDetails()

        itemKeys = list(self.itemsDatabase.keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            displayName, _, description, _, _, _, _ = self.itemsDatabase.get(key)
            self.comboItems.addItem(displayName)
            self.comboItems.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalItems.append(key)
            count += 1


        count = 0
        for count in range(25):
            increased, decreased = self.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1


        for i in range(6):
            self.finalStatsList[i].setEnabled(False)



        return

######################### Tab 1 Signal Definitions #####################################################################

    def startBattle(self):
        self.battleObject.setTeams(self.player1Team, self.player2Team)
        self.player1B_Widgets[6] = self.battleObject.player1Team
        self.player2B_Widgets[6] = self.battleObject.player2Team

        self.pushSwitchPlayer1.setEnabled(True)
        self.listPokemon1_moves.setEnabled(True)

        self.pushStartBattle.setEnabled(False)
        self.listPokemon2_moves.setEnabled(False)

        self.txtBattleInfo.setAlignment(QtCore.Qt.AlignHCenter)
        self.txtBattleInfo.setText("Battle Start!")

        self.listPlayer1_team.setCurrentRow(0)
        self.listPlayer2_team.setCurrentRow(0)

        self.updateBattleInfo("===================================")
        self.updateBattleInfo("Player 1 sent out " + self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex].name)
        self.updateBattleInfo("Player 2 sent out " + self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex].name)

        # Get Entry Level Effects
        self.executeEntryLevelEffects(self.player1B_Widgets, self.player2B_Widgets, self.battleObject.currPlayer1PokemonIndex, self.battleObject.currPlayer2PokemonIndex)
        self.executeEntryLevelEffects(self.player2B_Widgets, self.player1B_Widgets, self.battleObject.currPlayer2PokemonIndex, self.battleObject.currPlayer1PokemonIndex)
        '''
        self.determinePokemonEntryAbilityEffects(self.player1B_Widgets, self.player2B_Widgets, self.battleObject.currPlayer1PokemonIndex, self.battleObject.currPlayer2PokemonIndex)
        self.determinePokemonEntryAbilityEffects(self.player2B_Widgets, self.player1B_Widgets, self.battleObject.currPlayer2PokemonIndex, self.battleObject.currPlayer1PokemonIndex)
        message1 = self.determinePokemonEntryItemEffects(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex])
        message2 = self.determinePokemonEntryItemEffects(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex])

        self.updateBattleInfo(message1)
        self.updateBattleInfo(message2)
        '''
        self.showPokemonBattleInfo(self.player1B_Widgets, "switch")
        self.showPokemonBattleInfo(self.player2B_Widgets, "switchview")

        return

    def playerTurnComplete(self, playerWidgets, moveMade):

        # Determine move made and set up tuple object for player
        if (moveMade == "switch"):
            index = playerWidgets[1].currentRow()
            if (self.battleObject.playerTurn == 1):
                if (index == self.battleObject.currPlayer1PokemonIndex):
                    QtWidgets.QMessageBox.about(self, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.battleObject.setPlayer1MoveTuple((moveMade, index, 7))
            else:
                if (index == self.battleObject.currPlayer2PokemonIndex):
                    QtWidgets.QMessageBox.about(self, "Cannot switch", "Pokemon is currently in Battle!")
                    return
                self.battleObject.setPlayer2MoveTuple((moveMade, index, 7))
        else:
            index = playerWidgets[0].currentRow()
            if (self.battleObject.playerTurn == 1):
                priority = self.getMovePriority(index, self.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex)
                if (priority == None):
                    QtWidgets.QMessageBox.about(self, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    QtWidgets.QMessageBox.about(self, "Invalid Move", result[1])
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.battleObject.setPlayer1MoveTuple((moveMade, 4, 0)) # Struggle
                else:
                    self.battleObject.setPlayer1MoveTuple((moveMade, index, priority))
            else:
                priority = self.getMovePriority(index, self.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex)
                if (priority == None):
                    QtWidgets.QMessageBox.about(self, "Invalid Move", "Please select a valid move")
                    return
                result = self.isMoveValid(index, self.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex)
                if (result[0] == False and result[1] != "All moves unavailable"):
                    QtWidgets.QMessageBox.about(self, "Invalid Move", result[1])
                    return
                elif (result[0] == False and result[1] == "All moves unavailable"):
                    self.battleObject.setPlayer2MoveTuple((moveMade, 4, 0)) # Struggle
                else:
                    self.battleObject.setPlayer2MoveTuple((moveMade, index, priority))

        # Increment turns until both have chosen actions
        self.battleObject.updateTurnsDone()

        # Update player number that goes nexft
        self.battleObject.updatePlayerTurn()

        # Clear widget selected for cheating purposes
        playerWidgets[0].clearSelection()
        playerWidgets[1].clearSelection()

        # Check which player goes first based on move priority and pokemon speed
        if (self.battleObject.playerActionsComplete == True):
            self.battleObject.updateTurnsDone()
            actionFirst, actionSecond = self.decideMoveExecutionOrder()
            self.battleObject.setPlayer1MoveTuple(tuple())
            self.battleObject.setPlayer2MoveTuple(tuple())
            #self.battleObject.setPlayer1Action(Action())
            #self.battleObject.setPlayer2Action(Action())

        # Disable widgets based on player turn
        if (self.battleObject.playerTurn == 2):
            self.listPokemon1_moves.setEnabled(False)
            self.pushSwitchPlayer1.setEnabled(False)
            self.listPokemon2_moves.setEnabled(True)
            self.pushSwitchPlayer2.setEnabled(True)
        elif (self.battleObject.playerTurn == 1):
            self.pushSwitchPlayer1.setEnabled(True)
            self.listPokemon1_moves.setEnabled(True)
            self.pushSwitchPlayer2.setEnabled(False)
            self.listPokemon2_moves.setEnabled(False)

        return

    def showPokemonBattleInfo(self, playerWidgets, taskString):
        listPlayerTeam = playerWidgets[1]
        playerTeam = playerWidgets[6]
        viewPokemon = playerWidgets[3]
        hpBar_Pokemon = playerWidgets[2]
        txtPokemon_Level = playerWidgets[4]
        lbl_hpPokemon = playerWidgets[7]
        listPokemonMoves = playerWidgets[0]
        switchPokemon = playerWidgets[5]
        lbl_statusCond = playerWidgets[8]

        index = listPlayerTeam.currentRow()
        pokemonB = playerTeam[index]

        if (taskString == "view" and listPlayerTeam.item(index).foreground() == QtCore.Qt.blue and playerWidgets[9] == self.battleObject.playerTurn):
            taskString = "switch"

        if (taskString == "switch" or taskString == "switchview"):
            for i in range(listPlayerTeam.count()):
                if (i != index):
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
                else:
                    listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        self.displayPokemon(viewPokemon, pokemonB.pokedexEntry)
        hpBar_Pokemon.setRange(0, int(pokemonB.finalStatsList[0]))
        hpBar_Pokemon.setValue(int(pokemonB.battleStats[0]))
        hpBar_Pokemon.setToolTip(str(pokemonB.battleStats[0]) + "/" + str(pokemonB.finalStatsList[0]))

        # HP Color Code
        lbl_hpPokemon.setStyleSheet("color: rgb(0, 255, 0);")
        if (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStatsList[0])/2) and int(pokemonB.battleStats[0]) >= int(int(pokemonB.finalStatsList[0])/5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.battleStats[0]) <= int(int(pokemonB.finalStatsList[0])/5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

        # Status Condition Color Codes
        statusIndex = pokemonB.statusConditionIndex
        lbl_statusCond.setText(self.nonVolatileStatusConditions[statusIndex])
        if (statusIndex == 0):
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 0);")
        elif (statusIndex == 1):
            lbl_statusCond.setStyleSheet("color: rgb(148, 0, 211);")
        elif (statusIndex == 2):
            lbl_statusCond.setStyleSheet("color: rgb(128, 0, 128);")
        elif (statusIndex == 3):
            lbl_statusCond.setStyleSheet("color: rgb(255, 255, 0);")
        elif (statusIndex == 4):
            lbl_statusCond.setStyleSheet("color: rgb(128, 128, 128);")
        elif (statusIndex == 5):
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 255);")
        elif (statusIndex == 6):
            lbl_statusCond.setStyleSheet("color: rgb(255, 0, 0);")
        elif (statusIndex == 7):
            lbl_statusCond.setStyleSheet("color: rgb(220, 20, 60);")

        txtPokemon_Level.setText(pokemonB.level)

        listPokemonMoves.clear()
        listPokemonMoves.addItem("Move 1: ")
        listPokemonMoves.addItem("Move 2: ")
        listPokemonMoves.addItem("Move 3: ")
        listPokemonMoves.addItem("Move 4: ")


        if (taskString == "view" or taskString == "switchview"):
            listPokemonMoves.setEnabled(False)
            switchPokemon.setEnabled(False)
        elif (taskString == "switch"):
            switchPokemon.setEnabled(True)
            listPokemonMoves.setEnabled(True)



        for i in range(5):
            if (pokemonB.internalMovesMap.get(i) != None):
                internalMoveName, index, currPP = pokemonB.internalMovesMap.get(i)
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(internalMoveName)
                _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
                listPokemonMoves.currentItem().setText("Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip("Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)


        listPokemonMoves.clearSelection()
        listPlayerTeam.clearSelection()

        return


######################################### Tab 2 Signal Definitions #####################################################

    def creationDone(self):
        QtWidgets.QMessageBox.about(self, "Play Game","Set up is finished! Go to Tab 1 to play game.")
        self.clearGUI()
        self.disableDetails()
        self.txtPokedexEntry.setEnabled(False)
        self.txtChosenLevel.setEnabled(False)
        self.pushClearP1.setEnabled(False)
        self.pushClearP2.setEnabled(False)
        self.listCurr_p1Team.setEnabled(False)
        self.listCurr_p2Team.setEnabled(False)
        self.pushDone.setEnabled(False)
        self.txtHappinessVal.setEnabled(False)

        self.setupGame()
        return

    def clearPokemon(self, listCurrTeam, playerTeam):
        if (listCurrTeam.currentItem() != None):
            row = listCurrTeam.currentRow()
            listCurrTeam.takeItem(row)
            playerTeam.pop(row)

        return

    def checkPlayerTeams(self):

        if (self.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (len(self.player1Team) == maxPokemon and len(self.player2Team) == maxPokemon):
            self.pushDone.setEnabled(True)
        else:
            self.pushDone.setEnabled(False)

        return

    def restorePokemonDetails(self, listCurrTeam, playerTeam):
        self.clearGUI()
        print(listCurrTeam.currentRow())
        pokemonB = playerTeam[listCurrTeam.currentRow()]

        self.txtPokedexEntry.setText(pokemonB.pokedexEntry)
        self.updatePokemonEntry()

        self.txtChosenLevel.setText(pokemonB.level)
        self.checkPokemonLevel()

        self.txtHappinessVal.setText(pokemonB.happiness)
        self.finalizePokemon()
        print(pokemonB.evList[0])
        for count in range(6):
            self.evsList[count].setText(str(pokemonB.evList[count]))
            self.ivsList[count].setText(str(pokemonB.ivList[count]))
            self.finalStatsList[count].setText(str(pokemonB.finalStatsList[count]))
        self.finalizePokemon()

        abilityIndex = self.listInternalAbilities.index(pokemonB.internalAbility)
        self.comboAvailableAbilities.setCurrentIndex(abilityIndex)

        itemIndex = self.listInternalItems.index(pokemonB.internalItem)
        self.comboItems.setCurrentIndex(itemIndex)

        natureIndex = self.comboNatures.findText(pokemonB.nature)
        self.comboNatures.setCurrentIndex(natureIndex)

        self.chosenMovesetMap = copy.copy(pokemonB.internalMovesMap)

        for i in range(5):
            if (self.chosenMovesetMap.get(i) != None):
                internalMoveName, moveIndex, currPP = self.chosenMovesetMap.get(i)
                self.comboAvailableMoves.setCurrentIndex(moveIndex)
                self.listChosenMoves.setCurrentRow(i-1)
                self.updateMoveSet()

        for i in range(self.comboGenders.count()):
            if (self.comboGenders.itemText(i) == pokemonB.gender):
                self.comboGenders.setCurrentIndex(i)
                break


        self.finalizePokemon()

        return

    def savePokemon(self):
        pokedexEntry = self.txtPokedexEntry.displayText()
        level = self.txtChosenLevel.displayText()
        happinessVal = self.txtHappinessVal.displayText()
        pokemonObject = self.pokedex.get(pokedexEntry)
        pokemonImage = pokemonObject.image
        types = pokemonObject.pokemonTypes
        pokemonName = pokemonObject.pokemonName
        evList = []
        ivList = []
        finalStatsList = []
        nature = self.comboNatures.currentText()
        internalAbility = self.listInternalAbilities[self.comboAvailableAbilities.currentIndex()]
        chosenMovesWidget = self.listChosenMoves
        chosenInternalMovesMap = self.chosenMovesetMap
        internalItem = self.listInternalItems[self.comboItems.currentIndex()]
        chosenGender = self.comboGenders.currentText()

        for i in range(6):
            evList.append(int(self.evsList[i].displayText()))
            ivList.append(int(self.ivsList[i].displayText()))
            finalStatsList.append(int(self.finalStatsList[i].displayText()))

        if (self.comboPlayerNumber.currentText() == "Player 1"):
            playerNum = 1
            listCurrTeam = self.listCurr_p1Team
            playerTeam = self.player1Team
        else:
            playerNum = 2
            listCurrTeam = self.listCurr_p2Team
            playerTeam = self.player2Team

        pokemonB = Pokemon_Setup(playerNum, pokemonName, pokedexEntry, level, happinessVal, pokemonImage, evList, ivList, finalStatsList, nature, internalAbility, chosenMovesWidget, chosenInternalMovesMap, internalItem, types, chosenGender, pokemonObject.weight, pokemonObject.height)

        if (self.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() == None):
            QtWidgets.QMessageBox.about(self, "Warning", "You have reached the max Pokemon Limit. Please select a pokemon to replace")
        elif (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() != None):
            listCurrTeam.currentItem().setText(self.pokedex.get(pokedexEntry).pokemonName)
            playerTeam[listCurrTeam.currentRow()] = pokemonB
            self.clearGUI()
        else:
            listCurrTeam.addItem(self.pokedex.get(pokedexEntry).pokemonName)
            playerTeam.append(pokemonB)
            self.clearGUI()


        self.checkPlayerTeams()

        return

    def updateEVs(self):
        for evWidget in self.evsList:
            try:
                value = int(evWidget.displayText())
                if (value > 255 or value < 0):
                    self.pushFinished.setEnabled(False)
            except:
                self.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()
        return

    def updateIVs(self):

        for ivWidget in self.ivsList:
            try:
                value = int(ivWidget.displayText())
                if (value > 31 or value < 0):
                    self.pushFinished.setEnabled(False)
            except:
                self.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()

        return

    def updatePokemonEntry(self):
        self.resetDetails()
        pokedexEntry = self.pokedex.get(self.txtPokedexEntry.displayText())
        if (pokedexEntry == None):
            self.displayPokemon(self.viewCurrentPokemon, pokedexEntry=None)
            self.disableDetails()
        else:
            self.displayPokemon(self.viewCurrentPokemon, self.txtPokedexEntry.displayText())
            self.updateAbilities()
            self.updatePokemonMoves()
            self.checkPokemonLevel()
            self.updateStats()
            self.updateGenders()

        self.finalizePokemon()
        return

    def checkPokemonLevel(self):
        invalidFlag = 0

        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            invalidFlag = 1

        try:
            levelNum = int(self.txtChosenLevel.displayText())
            if (levelNum <= 0 or levelNum > 100):
                invalidFlag = 1
        except:
            invalidFlag = 1

        if (invalidFlag == 1):
            self.disableDetails()
        else:
            self.enableDetails()

        self.updateStats()
        self.finalizePokemon()
        return

    def updateMoveSet(self):
        if (self.listChosenMoves.currentItem() != None):
            selectedListRow = self.listChosenMoves.currentRow()
            selectedIndex = self.comboAvailableMoves.currentIndex()
            internalMoveName = self.listInternalMoves[selectedIndex]

            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(internalMoveName)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.listChosenMoves.currentItem().setText("Move " + str(selectedListRow+1) + ": " + moveName)
            self.listChosenMoves.currentItem().setToolTip("Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
            self.chosenMovesetMap.update({selectedListRow+1:(internalMoveName, selectedIndex, int(totalPP))})
            self.finalizePokemon()
        return

    def randomizeEVStats(self):
        total = 0

        while (total != 510):
            total = 0
            self.txtEV_HP.setText(str(random.randrange(0, 256)))
            total += int(self.txtEV_HP.displayText())
            # print(total)

            self.txtEV_Attack.setText(str(random.randrange(0, 256)))
            total += (int(self.txtEV_Attack.displayText()))
            # print(total)

            self.txtEV_Defense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_Defense.displayText()))
            # print(total)

            self.txtEV_SpAttack.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_SpAttack.displayText()))
            # print(total)

            self.txtEV_SpDefense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_SpDefense.displayText()))
            # print(total)

            self.txtEV_Speed.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.txtEV_Speed.displayText()))

        self.updateStats()
        self.finalizePokemon()

        return

    def randomizeIVStats(self):

        self.txtIV_HP.setText(str(random.randrange(0, 32)))

        self.txtIV_Attack.setText(str(random.randrange(0, 32)))

        self.txtIV_Defense.setText(str(random.randrange(0, 32)))

        self.txtIV_SpAttack.setText(str(random.randrange(0, 32)))

        self.txtIV_SpDefense.setText(str(random.randrange(0, 32)))

        self.txtIV_Speed.setText(str(random.randrange(0, 32)))

        self.updateStats()

        self.finalizePokemon()
        return

####################################### Helper Functions ###############################################################

##################################### Tab 1 Helper Functions ###########################################################
    def executeEntryLevelEffects(self, currPlayerWidgets, opponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex):
        currPlayerTeam = currPlayerWidgets[6]
        opponentPlayerTeam = opponentPlayerWidgets[6]

        self.determinePokemonEntryAbilityEffects(currPlayerWidgets, opponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex)
        message = self.determinePokemonEntryItemEffects(currPlayerTeam[currPokemonIndex], opponentPlayerTeam[opponentPokemonIndex])
        self.updateBattleInfo(message)
        return

    def checkTypeEffectivenessExists(self, typeMove, effectivenessList):
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                return True
        return False

    def getTypeEffectiveness(self, typeMove, effectivenessList):
        numEffectiveness = 1
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                numEffectiveness = float(effectiveness[1:])
                break
        return numEffectiveness

    def checkPP(self, pokemon, moveIndex):
        movesSetMap = pokemon.internalMovesMap
        internalName, _, currPP = movesSetMap.get(moveIndex+1)
        if (currPP > 0):
            return "Available"

        ppAvailableFlag = False
        for moveIndex in movesSetMap:
            _,_,currPP = movesSetMap.get(moveIndex+1)
            if (currPP > 0):
                ppAvailableFlag = True

        if (ppAvailableFlag == True):
            return "Other Moves Available"
        return "All Moves Over"

    def updateBattleInfo(self, addedText):
        self.txtBattleInfo.append(addedText)
        return

    def getMovePriority(self, moveIndex, playerWidgets, currPokemonIndex):
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]
        movesSetMap = pokemonObject.internalMovesMap
        if (movesSetMap.get(moveIndex+1) == None):
            return None
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.movesDatabase.get(internalMoveName)
        return int(priority)

    def isMoveValid(self, moveIndex, playerWidgets, currPokemonIndex):
        # TODO: Figure out when a move is valid and invalid
        playerTeam = playerWidgets[6]
        pokemonObject = playerTeam[currPokemonIndex]

        # Get Move Internal Name
        movesSetMap = pokemonObject.internalMovesMap
        internalMoveName, _, _ = movesSetMap.get(moveIndex + 1)

        # Check wether PP is available
        result = self.checkPP(pokemonObject, moveIndex)
        if (result == "Other Moves Available"):
            return (False, "Move is out of PP")
        elif (result == "All Moves Over"):
            return (False, "All Moves Over")

        # Check if move is blocked
        for i in range(0, len(pokemonObject.effects.movesBlocked)):
            moveInternalBlocked, numTurns = pokemonObject.effects.movesBlocked[i]
            if (moveInternalBlocked == internalMoveName):
                return (False, "Move is Blocked")

        return (True, None)

    def decideMoveExecutionOrder(self):
        first = 1
        # Intially check any changes to move priority based on items, ability, etc...
        resultA1 = self.determinePriorityAbilityEffects(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1MoveTuple)
        resultA2 = self.determinePriorityAbilityEffects(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2MoveTuple)
        resultI1 = self.determinePriorityItemEffects(self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1MoveTuple)
        resultI2 = self.determinePriorityItemEffects(self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex], self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex], self.battleObject.player2MoveTuple)

        # Decide Execution order based on priority
        if (self.battleObject.player1MoveTuple[2] > self.battleObject.player2MoveTuple[2]):
            first = 1
        elif (self.battleObject.player1MoveTuple[2] < self.battleObject.player2MoveTuple[2]):
            first = 2
        elif ((resultI1 == "first" or (resultA1 == "first" and resultI1 != "last")) and resultI2 != "first" and resultA2 != "first"):
            first = 1
        elif ((resultI1 == "last" or (resultA1 == "last" and resultI1 != "first")) and resultI2 != "last" and resultA2 != "last"):
            first = 2
        else:
            pokemonP1 = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
            pokemonP2 = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
            if (int(pokemonP1.battleStats[5]) > int(pokemonP2.battleStats[5])):
                first = 1
            elif (int(pokemonP1.battleStats[5]) < int(pokemonP2.battleStats[5])):
                first = 2
            else:
                randomNum = random.randint(1, 2)
                if (randomNum == 1):
                    first = 1
                else:
                    first = 2

        if (first == 1):
            actionFirst = self.getAction(self.player1B_Widgets, self.player2B_Widgets, self.battleObject.player1MoveTuple, True)
            self.battleObject.updatePlayer1Action(actionFirst)
            self.executeMove(actionFirst, self.player1B_Widgets, self.player2B_Widgets)
            #actionSecond = self.getAction(self.player2B_Widgets, self.player1B_Widgets, self.battleObject.player2MoveTuple, False)
            #self.battleObject.updatePlayer2Action(actionSecond)
            #self.executeMove(actionSecond, self.player2B_Widgets, self.player1B_Widgets)
        else:
            actionFirst = self.getAction(self.player2B_Widgets, self.player1B_Widgets, self.battleObject.player2MoveTuple, True)
            self.battleObject.updatePlayer2Action(actionFirst)
            self.executeMove(actionFirst, self.player2B_Widgets, self.player1B_Widgets)
            #actionSecond = self.getAction(self.player1B_Widgets, self.player2B_Widgets, self.battleObject.player1MoveTuple, False)
            #self.battleObject.updatePlayer1Action(actionSecond)
            #self.executeMove(actionSecond, self.player1B_Widgets, self.player2B_Widgets)

        return (actionFirst, actionSecond)

    def executeMove(self, action, currPlayerWidgets, opponentPlayerWidgets):
        self.updateBattleInfo("==================================")
        if (action.action == "swap"):
            if (action.swapObject.currPlayer == 1):
                self.battleObject.setPlayer1CurrentPokemonIndex(action.swapObject.swapPokemonIndex)
                self.updateBattleInfo(action.battleMessage)
                #self.showPokemonBattleInfo(currPlayerWidgets, "switch")
                if (self.battleObject.player2MoveTuple[0] == "switch" and action.isFirst == False):
                    self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets, self.battleObject.currPlayer1PokemonIndex, self.battleObject.currPlayer2PokemonIndex)
                    self.executeEntryLevelEffects(opponentPlayerWidgets, currPlayerWidgets, self.battleObject.currPlayer2PokemonIndex, self.battleObject.currPlayer1PokemonIndex)
                elif (self.battleObject.player2MoveTuple[0] != "switch"):
                    self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets, self.battleObject.currPlayer1PokemonIndex, self.battleObject.currPlayer2PokemonIndex)
                self.showPokemonBattleInfo(currPlayerWidgets, "switch")
            else:
                self.battleObject.setPlayer2CurrentPokemonIndex(action.swapObject.swapPokemonIndex)
                self.updateBattleInfo(action.battleMessage)
                #self.showPokemonBattleInfo(currPlayerWidgets, "switch")
                if (self.battleObject.player1MoveTuple[0] == "switch" and action.isFirst == False):
                    self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets, self.battleObject.currPlayer2PokemonIndex, self.battleObject.currPlayer1PokemonIndex)
                    self.executeEntryLevelEffects(opponentPlayerWidgets, currPlayerWidgets, self.battleObject.currPlayer1PokemonIndex, self.battleObject.currPlayer2PokemonIndex)
                elif (self.battleObject.player1MoveTuple[0] != "switch"):
                    self.executeEntryLevelEffects(currPlayerWidgets, opponentPlayerWidgets, self.battleObject.currPlayer2PokemonIndex, self.battleObject.currPlayer1PokemonIndex)
                self.showPokemonBattleInfo(currPlayerWidgets, "switch")
        else:
            if (action.moveObject.moveMiss == True):
                self.updateBattleInfo(action.battleMessage)
                return
            if (action.moveObject.playerAttacker == 1):
                self.determineMoveExecutionAbilityEffects(self.battleObject.player1Action, self.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex, self.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex)
            else:
                self.determineMoveExecutionAbilityEffects(self.battleObject.player2Action, self.player2B_Widgets, self.battleObject.currPlayer2PokemonIndex, self.player1B_Widgets, self.battleObject.currPlayer1PokemonIndex)

    def getAction(self, playerAttackerWidgets, playerOpponentWidgets, playerMoveTuple, isFirst):
        moveMade, index, priority = playerMoveTuple
        attackerPlayerTeam = playerAttackerWidgets[6]
        opponentPlayerTeam = playerOpponentWidgets[6]

        # Set up action object
        action = Action()

        # Create Switch Object if action made was switch
        if (moveMade == "switch"):
            switchedPokemon = attackerPlayerTeam[index]
            if (playerAttackerWidgets[9] == 1):
                action.createSwitchObject(playerMoveTuple[2], playerAttackerWidgets[9], self.battleObject.currPlayer1PokemonIndex, index, isFirst)
                action.setBattleMessage("Player 1 switched Pokemon\nPlayer 1 sent out " + switchedPokemon.name)
            else:
                action.createSwitchObject(playerMoveTuple[2], playerAttackerWidgets[9], self.battleObject.currPlayer2PokemonIndex, index, isFirst)
                action.setBattleMessage("Player 2 switched Pokemon\nPlayer 2 sent out " + switchedPokemon.name)
            return action

        # Get Attacker Pokemon and the Opposition Pokemon
        if (playerAttackerWidgets[9] == 1):
            currPokemonIndex = self.battleObject.currPlayer1PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.battleObject.currPlayer1PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.battleObject.currPlayer2PokemonIndex]
        else:
            currPokemonIndex = self.battleObject.currPlayer2PokemonIndex
            pokemonAttacker = attackerPlayerTeam[self.battleObject.currPlayer2PokemonIndex]
            pokemonOpponent = opponentPlayerTeam[self.battleObject.currPlayer1PokemonIndex]

        # Get internal move name from database
        movesSetMap = pokemonAttacker.internalMovesMap
        if (index == 4):
            internalMoveName = "STRUGGLE"
        else:
            internalMoveName, _, _ = movesSetMap.get(index + 1)

        # Create Move Object
        action.createMoveObject(playerAttackerWidgets[9], currPokemonIndex, internalMoveName, priority, isFirst)
        
        # Create Temp Pokemon
        action.moveObject.setAttackerObject(Pokemon_Temp(playerAttackerWidgets[9], pokemonAttacker.name, pokemonAttacker.level, pokemonAttacker.internalMovesMap, pokemonAttacker.internalAbility,
                                                      pokemonAttacker.battleStats, pokemonAttacker.statsStages, pokemonAttacker.currStatChangesList, pokemonAttacker.accuracy, pokemonAttacker.accuracyStage,
                                                      pokemonAttacker.evasion, pokemonAttacker.evasionStage, pokemonAttacker.weight, pokemonAttacker.height, pokemonAttacker.types, 
                                                      pokemonAttacker.effects, pokemonAttacker.statusConditionIndex, pokemonAttacker.tempConditionIndices, pokemonAttacker.internalItem, pokemonAttacker.wasHoldingItem))
        action.moveObject.setOpponentObject(Pokemon_Temp(playerOpponentWidgets[9], pokemonOpponent.name,pokemonOpponent.level, pokemonOpponent.internalMovesMap, pokemonOpponent.internalAbility,
                                                      pokemonOpponent.battleStats, pokemonOpponent.statsStages, pokemonOpponent.currStatChangesList, pokemonOpponent.accuracy, pokemonOpponent.accuracyStage,
                                                      pokemonOpponent.evasion, pokemonOpponent.evasionStage, pokemonOpponent.weight, pokemonOpponent.height,
                                                      pokemonOpponent.types, pokemonOpponent.effects, pokemonOpponent.statusConditionIndex, pokemonOpponent.tempConditionIndices, pokemonOpponent.internalItem, pokemonOpponent.wasHoldingItem))

        # Determine Move details - Damage, stat effects, weather effects, etc...
        self.determineMoveDetails(action.moveObject.attackerTemp, action.moveObject.opponentTemp, internalMoveName, action)
        return action

    def determineMoveDetails(self, attackerPokemon, opponentPokemon, internalMove, action):
        identifierNum, fullName, functionCode, basePower, typeMove, damageCategory, accuracy, totalPP, description, addEffect, targetCode, priority, flag = self.movesDatabase.get(internalMove)

        # Initialization
        action.setBattleMessage("Player " + action.moveObject.playerAttacker + " used " + fullName)
        baseDamage = 0
        action.moveObject.setMovePower(int(basePower))
        action.moveObject.setMoveAccuracy(int(accuracy))
        action.moveObject.setTypeMove(typeMove)
        action.moveObject.setDamageCategory(damageCategory)
        if (damageCategory == "Physical"):
            action.moveObject.setTargetAttackStat(attackerPokemon.currStats[1])
            action.moveObject.setTargetDefenseStat(opponentPokemon.currStats[2])
        elif (damageCategory == "Special"):
            action.moveObject.setTargetAttackStat(attackerPokemon.currStats[3])
            action.moveObject.setTargetDefenseStat(opponentPokemon.currStats[4])

        # Determine Function Code Effects
        determineFunctionCodeEffects(functionCode, internalMove, action, attackerPokemon, opponentPokemon, self.movesDatabase, self.functionCodesMap, self.battleFieldObject)

        # Determine Item Effects
        self.determineItemMoveEffects(attackerPokemon, opponentPokemon, internalMove, action)

        # Determine Modifiers
        self.getModifiers(attackerPokemon, opponentPokemon, internalMove, typeMove, action)

        # Determine Ability Effects
        self.determineAbilityMoveMultiplierEffects(action, internalMove, attackerPokemon, opponentPokemon)

        # Calculate Damage
        if (damageCategory != "Status"):
            damage = self.calculateDamage(action, attackerPokemon)
        action.moveObject.setDamage(damage*action.moveObject.currModifier)

        # Check if move will miss or hit
        threshold = 1
        if (action.moveObject.currMoveAccuracy != 0):
            threshold *= action.moveObject.currMoveAccuracy
        threshold *= (attackerPokemon.accuracyStage - opponentPokemon.evasionStage)
        randomNum = random.randint(1,100)
        if (randomNum > threshold):
            action.moveObject.setMoveMiss()
            action.setBattleMessage("Its attack missed")

        return

    def calculateDamage(self, action, attackerPokemon):
        baseDamage = ((((2 * int(attackerPokemon.level)) / 5 + 2) * action.moveObject.currPower * action.moveObject.targetAttackStat) / action.moveObject.targetDefenseStat) / 50 + 2
        return baseDamage

    def getModifiers(self, pokemonAttacker, pokemonOpponent, internalMove, typeAttack, action):
        identifierNum, fullName, functionCode, basePower, typeMove, damageCategory, accuracy, totalPP, description, addEffect, targetCode, priority, flag = self.movesDatabase.get(internalMove)
        
        # Get Read-ONLY metadata of pokemon attacker and opponent
        if (pokemonAttacker.playerNum == 1):
            pokemonAttackerRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
            pokemonOpponentRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
        else:
            pokemonAttackerRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
            pokemonOpponentRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]

        # Check Weather
        if (self.battleFieldObject.weatherEffect == "Rain" and typeMove == "WATER"):
            action.moveObject.multModifier(1.5)
        elif (self.battleFieldObject.weatherEffect == "Rain" and typeMove == "FIRE"):
            action.moveObject.multModifier(0.5)
        elif (self.battleFieldObject.weatherEffect == "Sunny" and typeMove == "FIRE"):
            action.moveObject.multModifier(1.5)
        elif (self.battleFieldObject.weatherEffect == "Sunny" and typeMove == "WATER"):
            action.moveObject.multModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(action, pokemonAttacker, pokemonOpponent, flag)
        action.moveObject.multModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        action.moveObject.multModifier(randomNum/100)

        # STAB
        if (typeMove in pokemonAttacker.currTypes):
            action.moveObject.multModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (pokemonAttacker.name == "GENESECT" and pokemonAttacker.internalItem == "DOUSEDRIVE" and internalMove == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.internalItem == "SHOCKDRIVE" and internalMove == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.internalItem == "BURNDRIVE" and internalMove == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (pokemonAttacker.name == "GENESECT" and pokemonAttacker.internalItem == "CHILLDRIVE" and internalMove == "TECHNOBLAST"):
            typeMove = "ICE"

        pokemonPokedex = self.pokedex.get(pokemonOpponentRead.pokedexEntry)
        if (self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True):
            action.moveObject.multModifier(self.getTypeEffectiveness(typeMove, pokemonPokedex.weaknesses))
        elif (self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == True):
            action.moveObject.multModifier(0)
        elif (self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.resistances) == True):
            action.moveObject.multModifier(self.getTypeEffectiveness(typeMove, pokemonPokedex.resistances))

        # Burn
        if (pokemonOpponent.internalAbility != "GUTS" and damageCategory == "Physical"):
            action.moveObject.multModifier(0.5)
        return

    def determineCriticalHitChance(self, action, pokemonAttacker, pokemonOpponent, flag):
        modifier = 1
        if (pokemonAttacker.playerNum == 1):
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP2
        else:
            fieldHazardsOpponent = self.battleFieldObject.fieldHazardsP1
        if (pokemonOpponent.internalAbility == "BATTLEARMOR" or pokemonOpponent.internalAbility == "SHELLARMOR" or "Lucky Chant" in fieldHazardsOpponent):
            action.moveObject.unsetCriticalHit()
            return 1
        elif (action.moveObject.criticalHit == True):
            #action.moveObject.setCriticalHit()
            return 2

        stageDenominator = self.criticalHitStages[action.moveObject.criticalHitStage]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1):
            action.moveObject.setCriticalHit()
            return 2
        return 1

    ######### Item Effects ##########
    def determinePriorityItemEffects(self, currPokemon, opponentPokemon, moveTuple):
        _, _, description, _, _, _, _ = self.itemsDatabase.get(currPokemon.internalItem)
        if (moveTuple[0] == "swap"):
            return
        if ("held" in description or "holding" in description or "holder" in description):
            if (currPokemon.internalItem == "LAGGINGTAIL"):
                return "last"
            elif (currPokemon.internalItem == "QUICKCLAW"):
                randomNum = random.randint(1,256)
                if (randomNum <= 51):
                    return "first"
            elif (currPokemon.internalItem == "FULLINCENSE"):
                return "last"
            elif (currPokemon.internalItem == "CUSTAPBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] * (1/3))):
                currPokemon.internalItem = None
                return "first"
        return

    def determineItemMoveEffects(self, attackerPokemon, opponentPokemon, internalMove, action):
        _,_,description,_,_,_,_ = self.itemsDatabase.get(attackerPokemon.currInternalItem)
        _, _, functionCode, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.movesDatabase.get(internalMove)
        if (attackerPokemon.playerNum == 1):
            attackerPokemonRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
        else:
            attackerPokemonRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]

        if ("held" in description or "holding" in description or "holder" in description):
            if (attackerPokemon.currInternalItem == "AIRBALLOON" and typeMove == "GROUND"):
                action.moveObject.multModifier(0)
                action.setBattleMessage(attackerPokemon.name + "\'s Air Balloon makes it immune to Ground type moves")
            elif ((attackerPokemon.currInternalItem == "CHOICEBAND" or attackerPokemon.currInternalItem == "CHOICESPECS" or attackerPokemon.currInternalItem == "CHOICESCARF") and attackerPokemon.currInternalItem not in attackerPokemon.currStatChangesList):
                attackerPokemon.currStatChangesList.append(internalItem)
                for moveIndex in attackerPokemon.internalMovesMap:
                    tupleData = attackerPokemon.internalMovesMap.get(moveIndex)
                    if (internalMove != tupleData[0]):
                        attackerPokemon.effects.addMoveBlocked(tupleData[0], sys.maxsize)
            elif (attackerPokemon.currInternalItem == "HEATROCK" and internalMove == "SUNNYDAY"):
                self.battleFieldObject.addWeatherEffect("Sunny", 8)
            elif (attackerPokemon.currInternalItem == "DAMPROCK" and internalMove == "RAINDANCE"):
                self.battleFieldObject.addWeatherEffect("Rain", 8)
            elif (attackerPokemon.currInternalItem == "SMOOTHROCK" and internalMove == "SANDSTORM"):
                self.battleFieldObject.addWeatherEffect("Sandstorm", 8)
            elif (attackerPokemon.currInternalItem == "ICYROCK" and internalMove == "ICYROCK"):
                self.battleFieldObject.addWeatherEffect("Hail", 8)
            elif (attackerPokemon.currInternalItem == "LIGHTCLAY" and (internalMove == "LIGHTSCREEN" or internalMove == "REFLECT")):
                index = self.battleFieldObject.fieldHazardsP1.index((internalMove, 5))
                self.battleFieldObject.fieldHazardsP1[index] = (internalMove, 8)
            elif (attackerPokemon.currInternalItem == "GRIPCLAW" and functionCode == "0CF"):
                for i in range(0, len(opponentPokemon.effects.multiTurnMoveDamage)):
                    if (opponentPokemon.effects.multiTurnMoveDamage[i][0] == internalMove):
                        opponentPokemon.effects.multiTurnMoveDamage[i] = (internalMove, 1/16, 7)
            elif (attackerPokemon.currInternalItem == "BINDINGBAND" and functionCode == "0CF"):
                for i in range(0, len(opponentPokemon.effects.multiTurnMoveDamage)):
                    if (opponentPokemon.effects.multiTurnMoveDamage[i][0] == internalMove):
                        opponentPokemon.effects.multiTurnMoveDamage[i] = (internalMove, 1/8, opponentPokemon.effects.multiTurnMoveDamage[i][2])
            elif (attackerPokemon.currInternalItem == "BIGROOT" and functionCode == "0DD"):
                action.moveObject.healAmount = int(action.moveObject.healAmount + (action.moveObject.damage * 30/100))
            elif (attackerPokemon.currInternalItem == "POWERHERB" and (functionCode == "0CC" or functionCode == "0CA" or functionCode == "OCB"
                or functionCode == "0C9" or functionCode == "0C5" or functionCode == "0C6" or functionCode == "0C3" or functionCode == "0C8"
                or functionCode == "0C7" or functionCode == "0C4")):
                attackerPokemon.currInternalItem = None
                action.moveObject.setTurnsStall(0)
            elif (attackerPokemon.currInternalItem == "LIFEORB"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.3))
                action.moveObject.setRecoil(int(attackerPokemon.finalStats[0] * (10/100)))
            elif (attackerPokemon.currInternalItem == "EXPERTBELT"):
                pokemonPokedex = self.pokedex.get(opponentPokemon.pokedexEntry)
                if (self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True):
                    action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "METRONOME"):
                numMoves = attackerPokemon.getNumSuccessiveMoves(internalMove)
                action.moveObject.currPower = int(action.moveObject.currPower + (action.moveObject.currPower*(numMoves*10/100)))
            elif (attackerPokemon.currInternalItem == "MUSCLEBAND"):
                if (damageCategory == "Physical"):
                    action.moveObject.currPower = int(action.moveObject.currPower*1.1)
            elif (attackerPokemon.currInternalItem == "WISEGLASSES"):
                if (damageCategory == "Special"):
                    action.moveObject.currPower = int(action.moveObject.currPower*1.1)
            elif (attackerPokemon.currInternalItem == "RAZORCLAW" or attackerPokemon.currInternalItem == "SCOPELENS"):
                action.moveObject.setCriticalHitStage(action.moveObject.criticalHitStage+1)
            elif (attackerPokemon.currInternalItem == "WIDELENS" and action.moveObject.currMoveAccuracy != 0 and action.isFirst == False):
                action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy*1.1))
            elif ((attackerPokemon.currInternalItem == "KINGSROCK" or attackerPokemon.currInternalItem == "RAZORFANG") and damageCategory != "Status"):
                randNumber = random.randint(1,100)
                if (randNumber <= 10):
                    action.moveObject.setFlinchValid()
            elif ((attackerPokemon.currInternalItem == "SEAINCENSE" or attackerPokemon.currInternalItem == "WAVEINCENSE" or attackerPokemon.currInternalItem == "MYSTICWATER" or attackerPokemon.currInternalItem == "SPLASHPLATE") and typeMove == "WATER"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "ROSEINCENSE" or attackerPokemon.currInternalItem == "MIRACLESEED" or attackerPokemon.currInternalItem == "MEADOWPLATE") and typeMove == "GRASS"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "ODDINCENSE" or attackerPokemon.currInternalItem == "TWISTEDSPOON" or attackerPokemon.currInternalItem == "MINDPLATE") and typeMove == "PSYCHIC"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "ROCKINCENSE" or attackerPokemon.currInternalItem == "HARDSTONE" or attackerPokemon.currInternalItem == "STONEPLATE") and typeMove == "ROCK"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "CHARCOAL" or attackerPokemon.currInternalItem == "FLAMEPLATE") and typeMove == "FIRE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "MAGNET" or attackerPokemon.currInternalItem == "ZAPPLATE") and typeMove == "ELECTRIC"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "NEVERMELTICE" or attackerPokemon.currInternalItem == "ICICLEPLATE") and typeMove == "ICE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "BLACKBELT" or attackerPokemon.currInternalItem == "FISTPLATE") and typeMove == "FIGHTING"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "POISONBARB" or attackerPokemon.currInternalItem == "TOXICPLATE") and typeMove == "POISON"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "SOFTSAND" or attackerPokemon.currInternalItem == "EARTHPLATE") and typeMove == "GROUND"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "SHARPBEAK" or attackerPokemon.currInternalItem == "SKYPLATE") and typeMove == "FLYING"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "SILVERPOWDER" or attackerPokemon.currInternalItem == "INSECTPLATE") and typeMove == "BUG"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "SPELLTAG" or attackerPokemon.currInternalItem == "SPOOKYPLATE") and typeMove == "GHOST"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "DRAGONFANG" or attackerPokemon.currInternalItem == "DRACOPLATE") and typeMove == "DRAGON"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "BLACKGLASSES" or attackerPokemon.currInternalItem == "DREADPLATE") and typeMove == "DARK"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif ((attackerPokemon.currInternalItem == "METALCOAT" or attackerPokemon.currInternalItem == "IRONPLATE") and typeMove == "STEEL"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "SILKSCARF" and typeMove == "NORMAL"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "FIREGEM" and typeMove == "FIRE" and internalMove != "FIREPLEDGE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "WATERGEM" and typeMove == "WATER" and internalMove != "WATERPLEDGE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "ELECTRICGEM" and typeMove == "ELECTRIC"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "GRASSGEM" and typeMove == "GRASS" and internalMove != "GRASSPLEDGE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "ICEGEM" and typeMove == "ICE"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "FIGHTINGGEM" and typeMove == "FIGHTING"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "POISONGEM" and typeMove == "POISON"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "GROUNDGEM" and typeMove == "GROUND"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "FLYINGGEM" and typeMove == "FLYING"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "PSYCHICGEM" and typeMove == "PSYCHIC"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "BUGGEM" and typeMove == "BUG"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "BUGGEM" and typeMove == "BUG"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "GHOSTGEM" and typeMove == "GHOST"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "DRAGONGEM" and typeMove == "DRAGON"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "DARKGEM" and typeMove == "DARK"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "STEELGEM" and typeMove == "STEEL"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "NORMALGEM" and typeMove == "NORMAL"):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.5))
            elif (attackerPokemon.currInternalItem == "LUCKYPUNCH" and attackerPokemon.name == "Chansey"):
                action.moveObject.setCriticalHitStage(action.moveObject.criticalHitStage+2)
            elif (attackerPokemon.currInternalItem == "ADAMANTORB" and attackerPokemon.name == "Dialga" and (typeMove == "STEEL" or typeMove == "DRAGON")):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "LUSTROUSORB" and attackerPokemon.name == "Palkia" and (typeMove == "WATER" or typeMove == "DRAGON")):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "GRISEOUSORB" and attackerPokemon.name == "Giratina" and (typeMove == "GHOST" or typeMove == "DRAGON")):
                action.moveObject.setMovePower(int(action.moveObject.currPower*1.2))
            elif (attackerPokemon.currInternalItem == "LANSATBERRY" and attackerPokemon.battleStats[0] < int(attackerPokemonRead.finalStats[0] *(1/3))):
                attackerPokemon.currInternalItem = None
                action.moveObject.setCriticalHitStage(action.moveObject.criticalHitStage+2)
                action.setBattleMessage(attackerPokemon.name + "\'s Lansat Berry sharply increased its Critical Hit Ratio!")
            elif (attackerPokemon.currInternalItem == "MICLEBERRY" and attackerPokemon.battleStats[0] < int(attackerPokemonRead.finalStats[0] *(1/3))):
                attackerPokemon.currInternalItem = None
                action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy*1.2))
                action.setBattleMessage(attackerPokemon.name + "\'s Micle Berry raised its accuracy")
        return

    def determinePokemonEntryItemEffects(self, currPokemon, opponentPokemon):
        _, _, description, _, _, _, _ = self.itemsDatabase.get(currPokemon.internalItem)
        message = ""

        if ("held" in description or "holding" in description or "holder" in description):
            if (currPokemon.internalItem == "BRIGHTPOWDER" and opponentPokemon.accuracyStage != -6):
                opponentPokemon.accuracy = int(opponentPokemon.accuracy * self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index-1])
                opponentPokemon.accuracyStage -= 1
            elif (currPokemon.internalItem == "EVIOLITE"):
                if (currPokemon.statsStages[2] != 6):
                    currPokemon.battleStats[2] = int(currPokemon.battleStats[2] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[2] += 1
                if (currPokemon.statsStages[4] != 6):
                    currPokemon.battleStats[4] = int(currPokemon.battleStats[4] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[4] += 1
            elif (currPokemon.internalItem == "FLOATSTONE"):
                currPokmeon.weight = int(currPokemon.weight/2)
            elif (currPokemon.internalItem == "CHOICEBAND" and currPokemon.statsStages[1] != 6):
                currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[1] += 1
            elif (currPokemon.internalItem == "CHOICESPECS" and currPokemon.statsStages[3] != 6):
                currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[3] += 1
            elif (currPokemon.internalItem == "CHOICESCARF" and currPokemon.statsStages[5] != 6):
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[5] += 1
            elif ((currPokemon.internalItem == "IRONBALL" or currPokemon.internalItem == "MACHOBRACE" or currPokemon.internalItem == "POWERWEIGHT"
                   or currPokemon.internalItem == "POWERBRACER" or currPokemon.internalItem == "POWERBELT" or currPokemon.internalItem == "POWERLENS"
                   or currPokemon.internalItem == "POWERBAND" or currPokemon.internalItem == "POWERANKLET") and currPokemon.statsStages[5] != -6):
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index-1])
                currPokemon.statsStages[5] -= 1
            elif (currPokemon.internalItem == "LIGHTBALL" and currPokemon.name == "Pikachu"):
                if (currPokemon.statsStages[1] != 6):
                    currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[1] += 1
                if (currPokemon.statsStages[3] != 6):
                    currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[3] += 1
            elif (currPokemon.internalItem == "METALPOWDER" and currPokemon.name == "Ditto" and currPokemon.statsStages[2] != 6):
                currPokemon.battleStats[2] = int(currPokemon.battleStats[2] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[2] += 1
            elif (currPokemon.internalItem == "QUICKPOWDER" and currPokemon.name == "Ditto" and currPokemon.statsStages[5] != 6):
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[5] += 1
            elif (currPokemon.internalItem == "THICKCLUB" and (currPokemon.name == "Marowak" or currPokemon.name == "Cubone") and currPokemon.statsStages[1] != 6):
                currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[1] += 1
            elif (currPokemon.internalItem == "SOULDEW" and (currPokemon.name == "Latios" or currPokemon.name == "Latias")):
                if (currPokemon.statsStages[3] != 6):
                    currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[3] += 1
                if (currPokemon.statsStages[4] != 6):
                    currPokemon.battleStats[4] = int(currPokemon.battleStats[4] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[4] += 1
            elif (currPokemon.internalItem == "DEEPSEATOOTH" and currPokemon.name == "Clamperl" and currPokemon.statsStages[3] != 6):
                currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[3] += 1
            elif (currPokemon.internalItem == "DEEPSEASCALE" and currPokemon.name == "Clamperl" and currPokemon.statsStages[4] != 6):
                currPokemon.battleStats[4] = int(currPokemon.battleStats[4] * self.statsStageMultipliers[self.stage0Index + 1])
                currPokemon.statsStages[4] += 1
            elif (currPokemon.internalItem == "LEPPABERRY" and currPokemon.finalStats[0]-currPokemon.battleStats[0] >= 10):
                currPokemon.battleStats[0] += 10
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Leppa Berry restored some HP"
            elif (currPokemon.internalItem == "SITRUSBERRY" and currPokemon.battleStats[0] < int(currPokemon.finalStats[0]/2)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] * (25/100)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Sitrus Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
            elif (currPokemon.internalItem == "FIGYBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0]/3)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] *(1/8)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Figy Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
                if (currPokemon.nature == "Modest" or currPokemon.nature == "Timid" or currPokemon.nature == "Calm" or currPokemon.nature == "Bold"):
                    currPokemon.tempConditionIndices.append(9)
                    message = message + "\n" + currPokemon.name + " became confused"
            elif (currPokemon.internalItem == "WIKIBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] * (1 / 8)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Wiki Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
                if (currPokemon.nature == "Adamant" or currPokemon.nature == "Jolly" or currPokemon.nature == "Careful" or currPokemon.nature == "Impish"):
                    currPokemon.tempConditionIndices.append(9)
                    message = message + "\n" + currPokemon.name + " became confused"
            elif (currPokemon.internalItem == "MAGOBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] * (1 / 8)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Mago Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
                if (currPokemon.nature == "Brave" or currPokemon.nature == "Quiet" or currPokemon.nature == "Sassy" or currPokemon.nature == "Relaxed"):
                    currPokemon.tempConditionIndices.append(9)
                    message = message + "\n" + currPokemon.name + " became confused"
            elif (currPokemon.internalItem == "AGUAVBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] * (1 / 8)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Aguav Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
                if (currPokemon.nature == "Naughty" or currPokemon.nature == "Rash" or currPokemon.nature == "Naive" or currPokemon.nature == "Lax"):
                    currPokemon.tempConditionIndices.append(9)
                    message = message + "\n" + currPokemon.name + " became confused"
            elif (currPokemon.internalItem == "IAPAPABERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3)):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] + (currPokemon.finalStats[0] * (1 / 8)))
                currPokemon.internalItem = None
                message = currPokemon.name + "\'s Iapapa Berry restored some HP"
                if (currPokemon.battleStats[0] > currPokemon.finalStats[0]):
                    currPokemon.battleStats[0] = currPokemon.finalStats[0]
                if (currPokemon.nature == "Lonely" or currPokemon.nature == "Mild" or currPokemon.nature == "Gentle" or currPokemon.nature == "Hasty"):
                    currPokemon.tempConditionIndices.append(9)
                    message = message + "\n" + currPokemon.name + " became confused"
            elif (currPokemon.internalItem == "LIECHIBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3) and currPokemon.statsStages[1] != 6):
                currPokemon.internalItem = None
                currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[1] += 1
                message = currPokemon.name + "\'s Liechi Berry raised its Attack"
            elif (currPokemon.internalItem == "GANLONBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3) and currPokemon.statsStages[2] != 6):
                currPokemon.internalItem = None
                currPokemon.battleStats[2] = int(currPokemon.battleStats[2] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[2] += 1
                message = currPokemon.name + "\'s Ganlon Berry raised its Defense"
            elif (currPokemon.internalItem == "SALACBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3) and currPokemon.statsStages[5] != 6):
                currPokemon.internalItem = None
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[5] += 1
                message = currPokemon.name + "\'s Salac Berry raised its Speed"
            elif (currPokemon.internalItem == "PETAYABERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3) and currPokemon.statsStages[3] != 6):
                currPokemon.internalItem = None
                currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[3] += 1
                message = currPokemon.name + "\'s Petaya Berry raised its Special Attack"
            elif (currPokemon.internalItem == "APICOTBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3) and currPokemon.statsStages[4] != 6):
                currPokemon.internalItem = None
                currPokemon.battleStats[4] = int(currPokemon.battleStats[4] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[4] += 1
                message = currPokemon.name + "\'s Apicot Berry raised its Special Defense"
            elif (currPokemon.internalItem == "STARFBERRY" and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0] / 3)):
                randomNum = random.randint(1,5)
                if (currPokemon.statsStages[randomNum] != 6):
                    currPokemon.internalItem = None
                    currPokemon.battleStats[randomNum] = int(currPokemon.battleStats[randomNum] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[randomNum] += 1
                    if (randomNum == 1):
                        message = currPokemon.name + "\'s Starf Berry raised its Attack"
                    elif (randomNum == 2):
                        message = currPokemon.name + "\'s Starf Berry raised its Defense"
                    elif (randomNum == 3):
                        message = currPokemon.name + "\'s Starf Berry raised its Special Attack"
                    elif (randomNum == 4):
                        message = currPokemon.name + "\'s Starf Berry raised its Special Defense"
                    else:
                        message = currPokemon.name + "\'s Starf Berry raised its Speed"
            return message

    ######### Ability Effects ##########
    def determineImmunityResistanceAbilityEffects(self, attackerPlayerAction, attackerPlayerWidgets, attackerPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex):
        attackerPokemon = attackerPlayerAction.moveObject.attackerTempObject
        opponentPokemon = attackerPlayerAction.moveObject.opponentTempObject
        attackerTeam = attackerPlayerWidgets[6]
        attackerPokemonRead = attackerTeam[attackerPokemonIndex]
        opponentTeam = opponentPlayerWidgets[6]
        opponentPokemonRead = opponentTeam[opponentPokemonIndex]

        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.movesDatabase.get(attackerPlayerAction.moveObject.internalMove)

        description = self.abilitiesEffectsMap.get(opponentPokemon.currInternalAbility)
        if (description == "Immunity or resistance to moves"):
            if (opponentPokemon.currInternalAbility == "FLASHFIRE" and attackerPlayerAction.moveObject.typeMove == "FIRE" and opponentPokemon.currInternalAbility not in opponentPokemon.currStatChangesList):
                attackerPlayerAction.moveObject.setDamage(0)
                opponentPokemon.currEffects.addMoveTypePowered("FIRE", 1.5)
                if (attackerPlayerAction.moveObject.inflictStatusCondition == 6):
                    attackerPlayerAction.moveObject.inflictStatusCondition = 0
                message = opponentPokemon.name + "\'s Flash Fire boosted its Fire type moves"
            elif (opponentPokemon.currInternalAbility == "STORMDRAIN" and attackerPlayerAction.moveObject.typeMove == "WATER" and opponentPokemon.currInternalAbility not in opponentPokemon.currStatChangesList):
                attackerPlayerAction.moveObject.setDamage(0)
                if (opponentPokemon.currStatsStages[3] < 6):
                    opponentPokemon.currStats[3] = int(opponentPokemon.currStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                    opponentPokemon.currStatsStages[3] += 1
                    message = opponentPokemon.name + "\'s Storm Drain raised its Special Attack"
            elif (opponentPokemon.currInternalAbility == "WATERABSORB" and attackerPlayerAction.moveObject.typeMove == "WATER"):
                attackerPlayerAction.moveObject.setDamage(0)
                opponentPokemon.currStats[0] = int(opponentPokemon.currStats[0] + (opponentPokemonRead.finalStats[0] * (1/4)))
                if (opponentPokemon.currStats[0] > opponentPokemonRead.finalStats[0]):
                    opponentPokemon.currStats[0] = opponentPokemon.finalStats[0]
                message = opponentPokemon.name + "\'s Water Absorb restored some of its HP"
            elif (opponentPokemon.currInternalAbility == "LIGHTNINGROD" and attackerPlayerAction.moveObject.typeMove == "ELECTRIC"):
                attackerPlayerAction.moveObject.setDamage(0)
                if (opponentPokemon.currStatsStages[3] < 6):
                    opponentPokemon.currStats[3] = int(opponentPokemon.currStats[3] * self.statsStageMultipliers[self.stage0Index+1])
                    opponentPokemon.currStatsStages[3] += 1
                    message = opponentPokemon.name + "\'s Lightning Rod raised its Special Attack"
            elif (opponentPokemon.currInternalAbility == "MOTORDRIVE" and attackerPlayerAction.moveObject.typeMove == "ELECTRIC"):
                attackerPlayerAction.moveObject.setDamage(0)
                if (opponentPokemon.currStatsStages[5] < 6):
                    opponentPokemon.currStats[5] = int(opponentPokemon.currStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                    opponentPokemon.currStatsStages[5] += 1
                    message = opponentPokemon.name + "\'s Motor Drive raised its Speed"
            elif (opponentPokemon.currInternalAbility == "VOLTABSORB" and attackerPlayerAction.moveObject.typeMove == "ELECTRIC"):
                attackerPlayerAction.moveObject.setDamage(0)
                opponentPokemon.currStats[0] = int(opponentPokemon.currStats[0] + (opponentPokemonRead.finalStats[0] * (1/4)))
                if (opponentPokemon.currStats[0] > opponentPokemonRead.finalStats[0]):
                    opponentPokemon.currStats[0] = opponentPokemonRead.finalStats[0]
                message = opponentPokemon.name + "\'s Volt Absorb restored some of its HP"
            elif (opponentPokemon.currInternalAbility == "SAPSIPPER" and attackerPlayerAction.moveObject.typeMove == "GRASS"):
                attackerPlayerAction.moveObject.setDamage(0)
                if (opponentPokemon.currStatsStages[1] < 6):
                    opponentPokemon.currStats[1] = int(opponentPokemon.currStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                    opponentPokemon.currStatsStages[1] += 1
                    message = opponentPokemon.name + "\'s Sap Sipper raised its Attack"
            elif (opponentPokemon.currInternalAbility == "LEVITATE" and (attackerPlayerAction.moveObject.typeMove == "GROUND" or attackerPlayerAction.moveObject.internalMove == "SKYDROP")):
                attackerPlayerAction.moveObject.setDamage(0)
                message = opponentPokemon.name + "\'s Levitate made it immune to the move"
            elif (opponentPokemon.currInternalAbility == "SOUNDPROOF" and "k" in flag):
                attackerPlayerAction.moveObject.setDamage(0)
                message = opponentPokemon.name + "\'s Soundproof made it immune to sound based moves"
            elif (opponentPokemon.currInternalAbility == "BATTLEARMOR" or opponentPokemon.currInternalAbility == "SHELLARMOR"):
                attackerPlayerAction.moveObject.criticalHit = False
            elif (opponentPokemon.currInternalAbility == "STURDY"):
                if (attackerPlayerAction.moveObject.internalMove == "FISSURE" or attackerPlayerAction.moveObject.internalMove == "GUILLOTINE" or attackerPlayerAction.moveObject.internalMove == "SHEERCOLD" or attackerPlayerAction.moveObject.internalMove == "HORNDRILL"):
                    attackerPlayerAction.moveObject.setDamage(0)
                    message = opponentPokemon.name + "\'s Sturdy made it immune to OHKO moves"
                elif (attackerPlayerAction.moveObject.currDamage >= opponentPokemon.currStats[0] and opponentPokemon.currStats[0] == opponentPokemonRead.finalStats[0]):
                    opponentPokemon.currStats[0] = 1
                    message = opponentPokemon.name + " held on with Sturdy"
            elif (opponentPokemon.currInternalAbility == "WONDERGUARD" and attackerPlayerAction.moveObject.effectiveness <= 1):
                attackerPlayerAction.moveObject.setDamage(0)
                message = opponentPokemon.name + "\'s Wonder Guard made it immune to the move"
            elif (opponentPokemon.currInternalAbility == "HEATPROOF"):
                if (attackerPlayerAction.moveObject.typeMove == "FIRE" and attackerPlayerAction.moveObject.damageCategory != "Status"):
                    attackerPlayerAction.moveObject.setDamage(int(attackerPlayerAction.moveObject.currDamage/2))
                    message = opponentPokemon.name + "\'s Heatproof made the fire type attack weak"
                if (attackerPlayerAction.moveObject.inflictStatusCondition == 6):
                    pass
            elif (opponentPokemon.currInternalAbility == "THICKFAT" and attackerPlayerAction.moveObject.damageCategory != "Status" and (attackerPlayerAction.moveObject.typeMove == "FIRE" or attackerPlayerAction.moveObject.typeMove == "ICE")):
                attackerPlayerAction.moveObject.setDamage(int(attackerPlayerAction.moveObject.currDamage/2))
                message = opponentPokemon.name + "\'s Thick Fat reduced the power of the move"
            elif ((opponentPokemon.currInternalAbility == "SOLIDROCK" or opponentPokemon.currInternalAbility == "FILTER") and attackerPlayerAction.moveObject.effectiveness > 1):
                attackerPlayerAction.moveObject.setDamage(int(attackerPlayerAction.moveObject.currDamage - (attackerPlayerAction.moveObject.currDamage * (25/100))))
                message = opponentPokemon.name + "\'s Solid Rock reduced the power of the move"
            elif (opponentPokemon.currInternalAbility == "MULTISCALE" and opponentPokemon.currStats[0] == opponentPokemonRead.finalStats[0]):
                attackerPlayerAction.moveObject.setDamage(int(attackerPlayerAction.moveObject.currDamage/2))
                message = opponentPokemon.name + "\'s Multiscale reduced the power of the move"

        return message

    def determineStat_StatusResistances(self, attackerPlayerAction, attackerPlayerWidgets, attackerPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex):
        attackerPokemon = attackerPlayerAction.moveObject.attackerTempObject
        opponentPokemon = attackerPlayerAction.moveObject.opponentTempObject
        attackerTeam = attackerPlayerWidgets[6]
        attackerPokemonRead = attackerTeam[attackerPokemonIndex]
        opponentTeam = opponentPlayerWidgets[6]
        opponentPokemonRead = opponentTeam[opponentPokemonIndex]

        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.movesDatabase.get(attackerPlayerAction.moveObject.internalMove)
        description = self.abilitiesEffectsMap.get(opponentPokemon.currInternalAbility)
        message = ""

        if (description == "Resists stat changes or status problems"):
            if (opponentPokemon.currInternalAbility == "BIGPECKS" and opponentPokemon.currStatsStages[2] < opponentPokemonRead.statsStages[2] and attackerPlayerAction.moveObject.internalMove in opponentPokemon.currStatChangesList):
                opponentPokemon.currStatsStages[2] = opponentPokemonRead.statsStages[2]
                opponentPokemon.currStats[2] = opponentPokemonRead.battleStats[2]
                opponentPokemon.currStatChangesList.remove(attackerPlayerAction.moveObject.internalMove)
                message = opponentPokemon.name + "\'s Big Pecks prevented its Defense from being lowered"
            elif (opponentPokemon.currInternalAbility == "HYPERCUTTER" and opponentPokemon.currStatsStages[1] < opponentPokemon.statsStages[1] and attackerPlayerAction.moveObject.internalMove in opponentPokemon.currStatChangesList):
                opponentPokemon.currStatsStages[1] = opponentPokemonRead.statsStages[1]
                opponentPokemon.currStats[1] = opponentPokemonRead.battleStats[1]
                opponentPokemon.currStatChangesList.remove(attackerPlayerAction.moveObject.internalMove)
                message = opponentPokemon.name + "\'s Hyper Cutter prevented its Attack from being lowered"
            elif (opponentPokemon.currInternalAbility == "KEENEYE" and opponentPokemon.currAccuracyStage < opponentPokemonRead.accuracyStage and attackerPlayerAction.moveObject.internalMove in opponentPokemon.currStatChangesList):
                opponentPokemon.currAccuracy = opponentPokemonRead.accuracy
                opponentPokemon.currAccuracyStage = opponentPokemonRead.accuracyStage
                opponentPokemon.currStatChangesList.remove(attackerPlayerAction.moveObject.internalMove)
                message = opponentPokemon.name + "\'s Keen Eye prevented its Accuracy from being lowered"
            elif ((opponentPokemon.currInternalAbility == "CLEARBODY" or opponentPokemon.currInternalAbility == "WHITESMOKE") and attackerPlayerAction.moveObject.internalMove in opponentPokemon.currStatChangesList):
                flag = False
                for i in range(1, 6):
                    if (opponentPokemon.currStatsStages[i] < opponentPokemonRead.statsStages[i]):
                        flag = True
                        break
                if (opponentPokemon.currAccuracyStage < opponentPokemonRead.accuracyStage):
                    flag = True
                if (opponentPokemon.currEvasionStage < opponentPokemonRead.evasionStage):
                    flag = True
                if (flag == True):
                    opponentPokemon.currStats = opponentPokemonRead.battleStats
                    opponentPokemon.currStatsStages = opponentPokemonRead.statsStages
                    opponentPokemon.currStatChangesList.remove(attackerPlayerAction.moveObject.internalMove)
                    message = opponentPokemon.name + "\'s Clear Body prevented its stats from being lowered"
            elif (opponentPokemon.currInternalAbility == "IMMUNITY" and (attackerPlayerAction.moveObject.inflictStatusCondition == 1 or attackerPlayerAction.moveObject.inflictStatusCondition == 2)):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Immunity prevented it from being poisoned"
            elif (opponentPokemon.currInternalAbility == "MAGMAARMOR" and attackerPlayerAction.inflictStatusCondition == 5):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Magma Armor prevented it from being frozen"
            elif (opponentPokemon.currInternalAbility == "LIMBER" and attackerPlayerAction.inflictStatusCondition == 3):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Limber prevented it from being paralyzed"
            elif ((opponentPokemon.currInternalAbility == "INSOMNIA" or opponentPokemon.currInternalAbility == "VITALSPIRIT") and (attackerPlayerAction.moveObject.inflictStatusCondition == 4 or attackerPlayerAction.moveObject.inflictStatusCondition == 8)):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status" and attackerPlayerAction.moveObject.inflictStatusCondition == 4):
                    message = opponentPokemon.name + "\'s Insomnia prevented it from being drowsy"
                elif (attackerPlayerAction.moveObject.damageCategory == "Status" and attackerPlayerAction.moveObject.inflictStatusCondition == 8):
                    message = opponentPokemon.name + "\'s Insomnia prevented it from being asleep"
            elif (opponentPokemon.currInternalAbility == "WATERVEIL" and attackerPlayerAction.moveObject.inflictStatusCondition == 6):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Water Veil prevented from being burned"
            elif (opponentPokemon.currInternalAbility == "OWNTEMPO" and attackerPlayerAction.moveObject.inflictStatusCondition == 9):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Own Tempo prevented it from being confused"
            elif (opponentPokemon.currInternalAbility == "OBLIVIOUS" and attackerPlayerAction.moveObject.inflictStatusCondition == 10):
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Oblivious prevented from being infatuated"
            elif (opponentPokemon.currInternalAbility == "INNERFOCUS" and attackerPlayerAction.moveObject.flinch == True):
                attackerPlayerAction.moveObject.flinch = False
            elif (opponentPokemon.currInternalAbility == "LEAFGUARD" and self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sunny" and attackerPlayerAction.moveObject.inflictStatusCondition >= 1 and attackerPlayerAction.moveObject.inflictStatusCondition <= 7):
                if (attackerPlayerAction.moveObject.damageCategory == "Status"):
                    message = opponentPokemon.name + "\'s Leaf Guard prevented it from being " + str(self.nonVolatileStatusConditions[attackerPlayerAction.moveObject.inflictStatusCondition])
                attackerPlayerAction.moveObject.inflictStatusCondition = 0
        return message

    def determineMoveExecutionAbilityEffects(self, attackerPlayerAction, attackerPlayerWidgets, attackerPokemonIndex, opponentPlayerWidgets, opponentPokemonIndex):
        attackerPokemon = attackerPlayerAction.moveObject.attackerTempObject
        opponentPokemon = attackerPlayerAction.moveObject.opponentTempObject
        attackerTeam = attackerPlayerWidgets[6]
        attackerPokemonRead = attackerTeam[attackerPokemonIndex]
        opponentTeam = opponentPlayerWidgets[6]
        opponentPokemonRead = opponentTeam[opponentPokemonIndex]

        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.movesDatabase.get(attackerPlayerAction.moveObject.internalMove)
        description = self.abilitiesEffectsMap.get(opponentPokemon.currInternalAbility)
        message = ""
        if (description == "Occurs upon a move hitting"):
            if (opponentPokemon.currInternalAbility == "ANGERPOINT" and attackerPlayerAction.moveObject.criticalHit == True):
                opponentPokemon.currStats[1] = int(opponentPokemon.finalStats[1] * self.statsStageMultipliers[self.stage0Index+6])
                opponentPokemon.currStatsStages[1] = 6
                message = opponentPokemon.name + "\'s Anger Point maximized its Attack"
            elif (opponentPokemon.currInternalAbility == "DEFIANT"):
                flag = False
                for i in range(1, 6):
                    if (attackerPlayerAction.moveObject.currOpponentStats[i] < opponentPokemon.currStats[i]):
                        flag = True
                        break
                if (flag == True):
                    if (opponentPokemon.currStatsStages[1] < 5):
                        opponentPokemon.currStats[1] = int(opponentPokemon.currStats[1] * self.statsStageMultipliers[self.stage0Index+2])
                        opponentPokemon.currStatsStages += 2
                        message = opponentPokemon.name + "\'s Defiant sharply raised its Attack"
                    elif (opponentPokemon.currStatsStages[1] == 5):
                        opponentPokemon.currStats[1] = int(opponentPokemon.currStats[1] * self.statsStageMultipliers[self.stage0Index + 1])
                        opponentPokemon.currStatsStages += 1
                        message = opponentPokemon.name + "\'s Defiant sharply its Attack"
            elif (opponentPokemon.currInternalAbility == "STEADFAST" and attackerPlayerAction.moveObject.flinch == True and opponentPokemon.currStatsStages[5] != 6):
                opponentPokemon.currStats[5] = int(opponentPokemon.currStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                opponentPokemon.currStatsStages[5] += 1
                message = opponentPokemon.name + "\'s Steadfast raised its Speed"
            elif (opponentPokemon.currInternalAbility == "WEAKARMOR" and attackerPlayerAction.moveObject.damageCategory == "Physical"):
                flagDefense = False
                flagSpeed = False
                if (opponentPokemon.currStatsStages[2] != -6):
                    opponentPokemon.currStats[2] = int(opponentPokemon.currStats[2] * self.statsStageMultipliers[self.stage0Index-1])
                    opponentPokemon.currStatsStages[2] -= 1
                    flagDefense = True
                if (opponentPokemon.currStatsStages[5] != 6):
                    opponentPokemon.currStats[5] = int(opponentPokemon.currStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                    opponentPokemon.currStatsStages[5] += 1
                    flagSpeed = True
                if (flagDefense == True and flagSpeed == False):
                    message = opponentPokemon.name + "\'s Weak Armor lowered its Defense"
                elif (flagDefense == False and flagSpeed == True):
                    message = opponentPokemon.name + "\'s Weak Armor raised its Attack"
                elif (flagDefense == True and flagSpeed == True):
                    message = opponentPokemon.name + "\'s Weak Armor lowered its Defense but raised its Attack"
            elif (opponentPokemon.currInternalAbility == "JUSTIFIED" and attackerPlayerAction.moveObject.currModifier != 0 and attackerPlayerAction.moveObject.damageCategory != "Status" and attackerPlayerAction.moveObject.typeMove == "DARK" and opponentPokemon.currStatsStages[1] != 6):
                opponentPokemon.currStats[1] = int(opponentPokemon.currStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                opponentPokemon.currStatsStages[1] += 1
                message = opponentPokemon.name + "\'s Justified increased its Attack"
            elif (opponentPokemon.currInternalAbility == "RATTLED" and attackerPlayerAction.moveObject.damageCategory != "Status" and (attackerPlayerAction.moveObject.typeMove == "BUG" or attackerPlayerAction.moveObject.typeMove == "DARK" or attackerPlayerAction.moveObject.typeMove == "GHOST") and opponentPokemon.currStatsStages[5] != 6):
                opponentPokemon.currStats[5] = int(opponentPokemon.currStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                opponentPokemon.currStatsStages[5] += 1
                message = opponentPokemon.name + "\'s Rattled increased its Speed"
            elif (opponentPokemon.currInternalAbility == "CURSEDBODY" and attackerPlayerAction.moveObject.damageCategory != "Status"):
                randomNum = random.randint(1,100)
                if (randomNum <= 30):
                    attackerPokemon.effects.addMoveBlocked((attackerPlayerAction.moveObject.internalMove, 4))
                    message = opponentPokemon.name + "\'s Cursed Body blocked " + attackerPlayerAction.moveObject.internalMove + " of " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "CUTECHARM" and attackerPokemonRead.gender != opponentPokemonRead.gender and attackerPokemonRead.gender != "Genderless" and opponentPokemonRead.gender != "Genderless" and "a" in flag):
                randomNum = random.randint(1, 100)
                if (randomNum <= 30 and 10 not in attackerPokemon.currTempConditions):
                    attackerPokemon.currTempConditions.append(10)
                    message = opponentPokemon.name + "\'s Cute Charm infatuated " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "POISONPOINT" and "a" in flag):
                randomNum = random.randint(1,100)
                if (randomNum <= 30 and attackerPokemon.currStatusCondition == 0):
                    attackerPokemon.currStatusCondition = 1
                    message = opponentPokemon.name + "\'s Poison Point poisoned " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "STATIC" and "a" in flag):
                randomNum = random.randint(1,100)
                if (randomNum <= 30 and attackerPokemon.currStatusCondition == 0):
                    attackerPokemon.currStatusCondition = 1
                    message = opponentPokemon.name + "\'s"
            elif (opponentPokemon.currInternalAbility == "EFFECTSPORE" and "a" in flag):
                randomNum1 = random.randint(1,100)
                randomNum2 = random.randint(1,3)
                if (randomNum1 <= 30 and attackerPokemon.currStatusCondition == 0):
                    if (randomNum2 == 1):
                        attackerPokemon.currStatusCondition = 3
                        message = opponentPokemon.name + "\'s Effect Spore paralyzed " + attackerPokemon.name
                    elif (randomNum2 == 2):
                        attackerPokemon.currStatusCondition = 1
                        message = opponentPokemon.name + "\'s Effect Spore poisoned " + attackerPokemon.name
                    else:
                        attackerPokemon.currStatusCondition = 4
                        message = opponentPokemon.name + "\'s Effect spore made " + attackerPokemon.name + " fall asleep"
            elif (opponentPokemon.currInternalAbility == "FLAMEBODY" and "a" in flag):
                randomNum = random.randint(1,100)
                if (randomNum <= 30 and attackerPokemon.currStatusCondition == 0):
                    attackerPokemon.currStatusCondition = 6
                    message = opponentPokemon.name + "\'s Flame Body burned " + attackerPokemon.name
            elif ((opponentPokemon.currInternalAbility == "ROUGHSKIN" or opponentPokemon.currInternalAbility == "IRONBARBS") and "a" in flag):
                attackerPokemon.battleStats[0] = int(attackerPokemon.battleStats[0] - (attackerPokemonRead.finalStats[0] * (1/8)))
                if (attackerPokemon.battleStats[0] < 0):
                    attackerPokemon.battleStats[0] = 0
                if (opponentPokemon.currInternalAbility == "ROUGHSKIN"):
                    message = opponentPokemon.name + "\'s Rough Skin hurt " + attackerPokemon.name
                else:
                    message = opponentPokemon.name + "\'s Iron Barbs hurt " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "PICKPOCKET" and attackerPokemon.currInternalItem != None and "a" in flag):
                opponentPokemon.internalItem = attackerPokemon.currInternalItem
                attackerPokemon.currInternalItem = None
                message = opponentPokemon.name + "\'s Pick Pocket stole " + attackerPokemon.name + "\'s held item"
            elif (opponentPokemon.currInternalAbility == "MUMMY" and "a" in flag):
                attackerPokemon.currInternalAbility = "MUMMY"
                message = opponentPokemon.name + "\'s Mummy changed " + attackerPokemon.name + "\'s Ability to Mummy"
            elif (opponentPokemon.currInternalAbility == "SYNCHRONIZE" and (attackerPlayerAction.moveObject.inflictStatusCondition == 6 or (attackerPlayerAction.moveObject.inflictStatusCondition >= 1 and attackerPlayerAction.moveObject.inflictStatusCondition <= 3))):
                if (attackerPokemon.currStatusCondition == 0):
                    attackerPokemon.currStatusCondition = attackerPlayerAction.moveObject.inflictStatusCondition
                    if (attackerPlayerAction.moveObject.inflictStatusCondition == 1):
                        message = opponentPokemon.name + "\'s Synchronize poisoned " + attackerPokemon.name
                    elif (attackerPlayerAction.moveObject.inflictStatusCondition == 2):
                        message = opponentPokemon.name + "\'s Synchronize badly poisoned " + attackerPokemon.name
                    elif (attackerPlayerAction.moveObject.inflictStatusCondition == 3):
                        message = opponentPokemon.name + "\'s Synchronize paralyed " + attackerPokemon.name
                    elif (attackerPlayerAction.moveObject.inflictStatusCondition == 6):
                        message = opponentPokemon.name + "\'s Synchronize burned " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "AFTERMATH" and (opponentPokemon.currStats[0] - attackerPlayerAction.moveObject.currDamage <= 0)):
                attackerPokemon.currStats[0] = int(attackerPokemon.currStats[0] - (attackerPokemonRead.finalStats[0] * (1/4)))
                if (attackerPokemon.currStats[0] < 0):
                    attackerPokemon.currStats[0] = 0
                    message = opponentPokemon.name + "\'s After math hurt " + attackerPokemon.name
            elif (opponentPokemon.currInternalAbility == "COLORCHANGE" and attackerPlayerAction.moveObject.internalMove != "STRUGGLE"):
                opponentPokemon.currTypes = [attackerPlayerAction.moveObject.typeMove]
                message = opponentPokemon.name + "\'s Color Change changes its type to " + attackerPlayerAction.moveObject.typeMove
            elif (attackerPokemon.currInternalAbility == "POISONTOUCH" and "a" in flag and attackerPlayerAction.moveObject.inflictStatusCondition == None):
                randomNum = random.randint(1,100)
                if (randomNum <= 30 and opponentPokemon.currStatusCondition == 0):
                    opponentPokemon.currStatusCondition = 1
                    message = attackerPokemon.name + "\'s Poison Touch poisoned " + opponentPokemon.name
            elif (attackerPokemon.currInternalAbility == "MOXIE" and attackerPlayerAction.moveObject.damageCategory != "Status" and opponentPokemon.currStats[0] - attackerPlayerAction.moveObject.currDamage <= 0):
                opponentPokemon.currStats[0] = 0
                message = attackerPokemon.name + "\'s Moxie raised its Attack"
            elif (attackerPokemon.currInternalAbility == "STENCH" and attackerPlayerAction.moveObject.damageCategory != "Status" and attackerPlayerAction.moveObject.flinch == False):
                randomNum = random.randint(1,100)
                if (randomNum <= 10):
                    attackerPlayerAction.moveObject.flinch = True
                    message = attackerPokemon.name + "\'s Stench made " + opponentPokemon.name + " flinch"
        return message

    def determinePriorityAbilityEffects(self, currPokemon, opponentPokemon, moveTuple):
        if (moveTuple[0] == "switch"):
            return
        movesSetMap = currPokemon.internalMovesMap
        internalMoveName, _, _ = movesSetMap.get(moveTuple[1] + 1)
        _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.movesDatabase.get(internalMoveName)

        if (currPokemon.internalAbility == "STALL"):
            return "last"
        elif (currPokemon.internalAbility == "PRANKSTER" and damageCategory == "Status"):
            moveTuple[2] += 1

    def determineAbilityMoveMultiplierEffects(self, action, internalMove, attackerPokemon, opponentPokemon):
        typeAbility = self.abilitiesEffectsMap.get(attackerPokemon.currInternalAbility)
        _, _, functionCode, basePower, typeMove, damageCategory, _, _, _, addEffect, _, _, flag = self.movesDatabase.get(internalMove)
        fcDescription,_ = self.functionCodesMap.get(functionCode)
        if (attackerPokemon.playerNum == 1):
            attackerPokemonRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]
            opponentPokemonRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
        else:
            attackerPokemonRead = self.battleObject.player2Team[self.battleObject.currPlayer2PokemonIndex]
            opponentPokemonRead = self.battleObject.player1Team[self.battleObject.currPlayer1PokemonIndex]

        if (typeAbility == "Move power multipliers"):
            if (attackerPokemon.currInternalAbility == "BLAZE" and typeMove == "FIRE" and damageCategory != "Status" and attackerPokemon.currStats[0] <= int(attackerPokemonRead.finalStats[0] * (1/3))):
                action.moveObject.setMovePower(int(basePower * 1.5))
            elif (attackerPokemon.currInternalAbility == "OVERGROW" and typeMove == "GRASS" and damageCategory != "Status" and attackerPokemon.currStats[0] <= int(attackerPokemonRead.finalStats[0] * (1/3))):
                action.moveObject.setMovePower(int(basePower * 1.5))
            elif (attackerPokemon.currInternalAbility == "TORRENT" and typeMove == "WATER" and damageCategory != "Status" and attackerPokemon.currStats[0] <= int(attackerPokemonRead.finalStats[0] * (1/3))):
                action.moveObject.setMovePower(int(basePower * 1.5))
            elif (attackerPokemon.currInternalAbility == "SWARM" and typeMove == "BUG" and damageCategory != "Status" and attackerPokemon.currStats[0] <= int(attackerPokemonRead.finalStats[0] * (1/3))):
                action.moveObject.setMovePower(int(basePower * 1.5))
            elif (attackerPokemon.currInternalAbility == "SANDFORCE" and (typeMove == "ROCK" or typeMove == "GROUND" or typeMove == "STEEL") and damageCategory != "Status"):
                if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                    action.moveObject.setMovePower(int(basePower*1.3))
            elif (attackerPokemon.currInternalAbility == "IRONFIST" and "j" in flag):
                action.moveObject.setMovePower(int(basePower * 1.2))
            elif (attackerPokemon.currInternalAbility == "RECKLESS" and (fcDescription == "Attacks with recoil" or functionCode == "10B")):
                action.moveObject.setMovePower(int(basePower * 1.2))
            elif (attackerPokemon.currInternalAbility == "RIVALRY"):
                if (attackerPokemonRead.gender != "Genderless" and opponentPokemonRead.gender != "Genderless"):
                    if (attackerPokemonRead.gender == opponentPokemonRead.gender):
                        action.moveObject.setMovePower(int(basePower*1.25))
                    else:
                        action.moveObject.setMovePower(int(basePower*0.75))
            elif (attackerPokemon.currInternalAbility == "SHEERFORCE" and addEffect != 0):
                action.moveObject.setMovePower(int(basePower*1.3))
                action.moveObject.setRecoil(0)
            elif (attackerPokemon.currInternalAbility == "TECHNICIAN" and basePower <= 60):
                action.moveObject.setMovePower(int(basePower*1.5))
            elif (attackerPokemon.currInternalAbility == "TINTEDLENS"):
                pokemonPokedex = self.pokedex.get(opponentPokemonRead.pokedexEntry)
                if (typeMove in pokemonPokedex.resistances):
                    action.moveObject.setMovePower(int(basePower*2))
            elif (attackerPokemon.currInternalAbility == "SNIPER" and action.moveObject.criticalHit == True):
                action.moveObject.setMovePower(int(basePower*1.5))
            elif (attackerPokemon.currInternalAbility == "ANALYTIC" and action.isFirst == False):
                action.moveObject.setMovePower(int(basePower*1.3))
        elif (typeAbility == "Stat multipliers"):
            if (attackerPokemon.internalAbility == "HUSTLE" and damageCategory == "Physical"):
                action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy*0.8))
        return

    def checkAbilityStatMultipliers(self, currPokemon, opponentPokemon, internalAbility, turnString):
        message = ""
        if (internalAbility == "FLAREBOOST" and currPokemon.statusConditionIndex == 6 and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[3] != 6):
            currPokemon.battleStats[3] = int(currPokemon.battleStats[3]*self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[3] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Flare Boost raised its Special Attack"
        elif (internalAbility == "GUTS" and currPokemon.statusConditionIndex != 0 and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[1] != 6):
            currPokemon.batttleStats[1] = int(currPokemon.battleStats[1]*self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[1] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Guts raised its Attack"
        elif (internalAbility == "MARVELSCALE" and currPokemon.statusConditionIndex != 0 and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[2] != 6):
            currPokemon.battleStats[2] = int(currPokemon.battleStats[2] * self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[2] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Marvel Scale raised its Defense"
        elif (internalAbility == "QUICKFEET" and currPokemon.statusConditionIndex != 0 and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[5] != 6):
            currPokemon.battleStats[5] = int(currPokemon.battleStats[5]*self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[5] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Quick Feet raised its Speed"
        elif (internalAbility == "TOXICBOOST" and (currPokemon.statusConditionIndex == 1 or currPokemon.statusConditionIndex == 2) and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[1] != 6):
            currPokemon.battleStats[1] = int(currPokemon.battleStats[1]*self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[1] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Toxic Boost raised its Attack"
        elif (internalAbility == "TANGLEDFEET" and 9 in currPokemon.tempConditionIndices and internalAbility not in currPokemon.currStatChangesList and currPokemon.evasionStage != 6):
            currPokemon.evasion = int(currPokemon.evasion*self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+1])
            currPokemon.evasionStage += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Tangled Feet raised its Evasion"
        elif (internalAbility == "HUSTLE" and internalAbility not in currPokemon.currStatChangesList):
            currPokemon.currStatChangesList.append(internalAbility)
            if (currPokemon.statsStages[1] != 6):
                currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[1] += 1
                message = currPokemon.name + "\'s Hustle raised its Attack but lowered its Accuracy"
        elif ((internalAbility == "PUREPOWER" or internalAbility == "HUGEPOWER") and internalAbility not in currPokemon.currStatChangesList):
            currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
            currPokemon.statsStages[1] += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Pure Power raised its Attack"
        elif (internalAbility == "COMPOUNDEYES" and internalAbility not in currPokemon.currStatChangesList and currPokemon.accuracyStage != 6):
            currPokemon.accuracy = int(currPokemon.accuracy * self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+1])
            currPokemon.accuracyStage += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Compound Eyes raised its Accuracy"
        elif (internalAbility == "UNBURDEN" and internalAbility not in currPokemon.currStatChangesList and currPokemon.statsStages[5] != 6 and currPokemon.internalItem == None and currPokemon.wasHoldingItem == True):
            currPokemon.wasHoldingItem = False
            if (currPokemon.statsStages[5] < 5):
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5]*self.statsStageMultipliers[self.stage0Index+2])
                currPokemon.statsStages[5] += 2
                message = currPokemon.name + "\'s Unburden sharped rasied its Speed"
            else:
                currPokemon.battleStats[5] = int(currPokemon.battleStats[5]*self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[5] += 1
                message = currPokemon.name + "\'s Unburden raised its Speed"
            currPokemon.currStatChangesList.append(internalAbility)
        elif (internalAbility == "SLOWSTART" and internalAbility not in currPokemon.currStatChangesList):
            battleStats = copy.copy(currPokemon.battleStats)
            battleStats[1] = int(battleStats[1] * self.statsStageMultipliers[self.stage0Index-2])
            battleStats[5] = int(battleStats[5] * self.statsStageMultipliers[self.stage0Index-2])
            currPokemon.effectsQueue.insert(battleStats, "stats change", 5)
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Slow Start sharply lowered its Attack and Defense"
        elif (internalAbility == "DEFEATIST" and internalAbility not in currPokemon.currStatChangesList and currPokemon.battleStats[0] <= int(currPokemon.finalStats[0]/2)):
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Defeatist "
            message1 = ""
            message2 = ""
            if (currPokemon.statsStages[1] > -6):
                currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index-1])
                currPokemon.statsStagees[1] -= 1
                message1 = "lowered its Attack"
            if (currPokemon.statsStages[3] > -6):
                currPokemon.battleStats[3] = int(currPokemon.battleStats[3] * self.statsStageMultipliers[self.stage0Index - 1])
                currPokemon.statsStages[3] -= 1
                message2 = "lowered its Special Attack"
            if (message1 == "" and message2 == ""):
                message = ""
            elif (message1 != "" and message2 == ""):
                message += message1
            elif (message1 == "" and message2 != ""):
                message += message2
            else:
                message = message1 + " and " + message2
        elif (internalAbility == "VICTORYSTAR" and internalAbility not in currPokemon.currStatChangesList and currPokemon.accuracyStage != 6):
            currPokemon.accuracy = int(currPokemon.accuracy * self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+1])
            currPokemon.accuracyStage += 1
            currPokemon.currStatChangesList.append(internalAbility)
            message = currPokemon.name + "\'s Victory Start raised its Accuracy"
        elif (internalAbility == "CHLOROPHYLL" and internalAbility not in currPokemon.currStatChangesList and currPokemon.battleStats[5] != 6):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sunny"):
                currPokemon.currStatChangesList.append(internalAbility)
                if (currPokemon.statsStages[5] < 5):
                    currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+2])
                    currPokemon.statsStages[5] += 2
                    message = currPokemon.name + "\'s Chlorophyll sharply raised its Speed"
                else:
                    currPokemon.batttleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[5] += 1
                    message = currPokemon.name + "\'s Chlorophyll raised its Speed"
        elif (internalAbility == "SWIFTSWIM" and internalAbility not in currPokemon.currStatChangesList and currPokemon.battleStats[5] != 6):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Rain"):
                currPokemon.currStatChangesList.append(internalAbility)
                if (currPokemon.statsStages[5] < 5):
                    currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+2])
                    currPokemon.statsStages[5] += 2
                    message = currPokemon.name + "\'s Swift Swim sharply raised its Speed"
                else:
                    currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[5] += 1
                    message = currPokemon.name + "\'s Swift Swim raised its Speed"
        elif (internalAbility == "SANDRUSH" and internalAbility not in currPokemon.currStatChangesList and currPokemon.battleStats[5] != 6):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                currPokemon.currStatChangesList.append(internalAbility)
                if (currPokemon.statsStages[5] < 5):
                    currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+2])
                    currPokemon.statsStages[5] += 2
                    message = currPokemon.name + "\'s Sand Rush sharply raised its Speed"
                else:
                    currPokemon.battleStats[5] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.battleStats[5] += 1
                    message = currPokemon.name + "\'s Sand Rush raised its Speed"
        elif (internalAbility == "SOLARPOWER" and currPokemon.battleStats[3] != 6):
            raisedFlag = False
            if (internalAbility not in currPokemon.currStatChangesList):
                currPokemon.currStatChangesList.append(internalAbility)
                currPokemon.battleStats[3] = int(currPokemon.battleStats[5] * self.statsStageMultipliers[self.stage0Index+1])
                currPokemon.statsStages[3] += 1
                raisedFlag = True
            if (turnString == "End of turn"):
                currPokemon.battleStats[0] = int(currPokemon.battleStats[0] - (currPokemon.finalStats[0] * (1/8)))
                if (currPokemon.battleStats[0] < 0):
                    currPokemon.battleStats[0] = 0
                if (raisedFlag == True):
                    message = currPokemon.name + "\'s Solar Power raised its Special Attack\n"# + currPokemon.name + " lost some HP due to Sunny Weather"
                else:
                    message = currPokemon.name + " lost some HP due to Sunny Weather"
        elif (internalAbility == "SANDVEIL" and internalAbility not in currPokmeon.currStatChangesList and currPokemon.evasionStage != 6):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                currPokemon.currStatChangesList.append(internalAbility)
                currPokemon.evasion = int(currPokemon.evasion * self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+1])
                currPokemon.evasionStage += 1
                message = currPokemon.name + "\'s Sand Veil raised its Evasion"
        elif (internalAbility == "SNOWCLOAK" and internalAbility not in currPokemon.currStatChangesList and currPokemon.evasionStage != 6):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                currPokemon.currStatChangesList.append(internalAbility)
                currPokemon.evasion = int(currPokemon.evasion * self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+1])
                currPokemon.evasionStage += 1
                message = currPokemon.name + "\'s Snow Cloak raised its Evasion"
        elif (internalAbility == "FLOWERGIFT" and internalAbility not in currPokemon.currStatChangesList):
            if (self.battleFieldObject.weatherEffect != None and self.battleFieldObject.weatherEffect[0] == "Sunny"):
                if (currPokemon.statsStages[1] < 6 or currPokemon.statsStages[4] < 6):
                    currPokemon.currStatChangesList.append(internalAbility)
                    attRaised = False
                    spDefRaised = False
                    if (currPokemon.statsStages[1] < 6):
                        currPokemon.battleStats[1] = int(currPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index+1])
                        currPokemon.statsStages[1] += 1
                        attRaised = True
                    if (currPokemon.sttasStages[4] < 6):
                        currPokmeon.battleStats[4] = int(currPokemon.battleStats[4] * self.statsStageMultipliers[self.stage0Index+1])
                        currPokemon.statsStages[4] += 1
                        spDefRaised = True
                    if (attRaised == True and spDefRaised == False):
                        message = currPokemon.name + "\'s Flower Gift raised its Attack"
                    elif (attRaised == False and spDefRaised == True):
                        message = currPokemon.name + "\'s Flower Gift raised its Special Defense"
                    else:
                        message = currPokemon.name + "\'s Flower Gift raised its Attack and Special Defense"

        return message

    def determinePokemonEntryAbilityEffects(self, listCurrPlayerWidgets, listOpponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex):
        # Used for trace
        abilityChanged = False

        # Initialize Message
        message = ""

        # Get current Pokemon
        currPlayerTeam = listCurrPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]

        # Get opponent Pokemon
        opponentPlayerTeam = listOpponentPlayerWidgets[6]
        opponentPokemon = opponentPlayerTeam[opponentPokemonIndex]

        # Get type of ability
        typeAbility = self.abilitiesEffectsMap.get(currPokemon.internalAbility)

        if (typeAbility == "Occurs upon switching in/out"):
            if (currPokemon.internalAbility == "DOWNLOAD"):
                if (opponentPokemon.battleStats[2] < opponentPokemon.battleStats[4]):
                    currPokemon.battleStats[1] = int(currPokemon.battleStats[1]*self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[1] += 1
                    message = currPokemon.name + "\'s Attack rose"
                else:
                    currPokemon.battleStats[3] = int(currPokemon.battleStats[3]*self.statsStageMultipliers[self.stage0Index+1])
                    currPokemon.statsStages[3] += 1
                    message = currPokemon.name + "\'s Special Attack rose"
            elif (currPokemon.internalAbility == "INTIMIDATE"):
                if (opponentPokemon.statsStages[1] != -6):
                    opponentPokemon.battleStats[1] = int(opponentPokemon.battleStats[1] * self.statsStageMultipliers[self.stage0Index-1])
                    opponentPokemon.statsStages[1] -= 1
                    message = currPokemon.name + "\'s Intimidate activated\n" + opponentPokemon.name + "\'s Attack fell"
                else:
                    message = opponentPokemon.name + "\'s Attack won't go lower"
            elif (currPokemon.internalAbility == "DRIZZLE"):
                self.battleFieldObject.addWeatherEffect("Rain", sys.maxsize)
                message = "It started raining"
            elif (currPokemon.internalAbility == "DROUGHT"):
                self.battleFieldObject.addWeatherEffect("Sunny", sys.maxsize)
                message = "It became sunny"
            elif (currPokemon.internalAbility == "SANDSTREAM"):
                self.battleFieldObject.addWeatherEffect("Sandstorm", sys.maxsize)
                message = "A sandstorm started brewing"
            elif (currPokemon.internalAbility == "SNOWWEATHER"):
                self.battleFieldObhect.addWeatherEffect("Hail", sys.maxsize)
                message = "It started hailing"
            elif (currPokemon.internalAbility == "FRISK"):
                message = currPokemon.name + "\'s Frisk showed " + opponentPokemon.name + "\'s held item\n"
                tupleData = self.itemsDatabase.get(opponentPokemon.internalItem)
                if (tupleData == None):
                    message += opponentPokemon.name + " is not holding an item"
                else:
                    fullName, _, _, _, _ = tupleData
                    message += message + opponentPokemon.name + " is holding " + fullName
            elif (currPokemon.internalAbility == "ANTICIPATION"):
                pokemonPokedex = self.pokedex.get(currPokemon.pokedexEntry)
                for moveIndex in opponentPokemon.internalMovesMap:
                    internalMoveName,_,_ = opponentPokemon.internalMovesMap.get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.movesDatabase.get(internalMoveName)
                    if (self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        message = currPokemon.name + " shudders"
                    elif ((internalMoveName == "FISSURE" and self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        message = currPokemon.name + " shudders"
            elif (currPokemon.internalAbility == "FOREWARN"):
                maxPower = -1
                moveName = ""
                for moveIndex in opponentPokemon.internalMovesMap:
                    internalMoveName, _, _ = opponentPokemon.internalMovesMap.get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.movesDatabase.get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                message = currPokemon.name + "\'s Forewarn reveals " + opponentPokemon.name + "\'s strongest move to be " + moveName
            elif (currPokemon.internalAbility == "TRACE"):
                if (opponentPokemon.internalAbility != "FORECAST" and opponentPokemon.internalAbility != "FLOWERGIFT" and opponentPokemon.internalAbility != "MULTITYPE" and opponentPokemon.internalAbility != "ILLUSION" and opponentPokemon.internalAbility != "ZENMODE"):
                    currPokemon.internalAbility = opponentPokemon.internalAbility
                    _,fullName,_ = self.abilitiesDatabase.get(opponentPokemon.internalAbility)
                    message = currPokemon.name + "\'s Trace caused it to change ability to " + fullName
                    abilityChanged = True
                    #self.determinePokemonEntryAbilityEffects(listCurrPlayerWidgets, listOpponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex)
            elif (currPokemon.internalAbility == "IMPOSTER"):
                #TODO: Need to account for this
                currPokemon = opponentPokemon
                self.displayPokemon(listCurrPlayerWidgets[3], currPokemon.pokedexEntry)
                message = currPokemon.name + " transformed into " + opponentPokemon.name
            elif (currPokemon.internalAbility == "ILLUSION"):
                #TODO: Need to account for this
                pass
        elif (typeAbility == "Stat multipliers"):
            message = self.checkAbilityStatMultipliers(currPokemon, opponentPokemon, currPokemon.internalAbility, "Beginning of Turn")
        elif (typeAbility == "Form changing"):
            #TODO: Need to account for this
            pass

        self.updateBattleInfo(message)
        if (abilityChanged == True):
            self.determinePokemonEntryAbilityEffects(listCurrPlayerWidgets, listOpponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex)
        return

#################################### Tab 2 Helper Functions ############################################################
    def setupGame(self):
        self.pushStartBattle.setEnabled(True)
        self.pushRestart.setEnabled(True)
        self.pushDifferentTeam.setEnabled(True)
        #self.pushSwitchPlayer1.setEnabled(True)
        #self.pushSwitchPlayer2.setEnabled(True)

        i = 0
        for pokemon in self.player1Team:
            pokemonFullName = self.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.itemsDatabase.get(pokemon.internalItem)
            self.listPlayer1_team.addItem(pokemonFullName)
            #self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.listPlayer1_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + str(pokemon.finalStatsList[0]) + "\n" +
                                                     "Attack:\t\t" + str(pokemon.finalStatsList[1]) + "\n"+
                                                     "Defense:\t" + str(pokemon.finalStatsList[2]) + "\n"+
                                                     "SpAttack:\t" + str(pokemon.finalStatsList[3]) + "\n"+
                                                     "SpDefense:\t" + str(pokemon.finalStatsList[4]) + "\n"+
                                                     "Speed:\t\t" + str(pokemon.finalStatsList[5]))
            i += 1

        i = 0
        for pokemon in self.player2Team:
            pokemonFullName = self.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.itemsDatabase.get(pokemon.internalItem)
            self.listPlayer2_team.addItem(pokemonFullName)
            self.listPlayer2_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + str(pokemon.finalStatsList[0]) + "\n" +
                                                     "Attack:\t\t" + str(pokemon.finalStatsList[1]) + "\n" +
                                                     "Defense:\t" + str(pokemon.finalStatsList[2]) + "\n" +
                                                     "SpAttack:\t" + str(pokemon.finalStatsList[3]) + "\n" +
                                                     "SpDefense:\t" + str(pokemon.finalStatsList[4]) + "\n" +
                                                     "Speed:\t\t" + str(pokemon.finalStatsList[5]))
            i += 1

        return

    def finalizePokemon(self):
        enableFlag = 1
        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            enableFlag = 0

        evTotal = 0
        try:
            levelNum = int(self.txtChosenLevel.displayText())
            happinessVal = int(self.txtHappinessVal.displayText())

            if (happinessVal < 0 or happinessVal > 255):
                enableFlag = 0

            if (levelNum < 1 or levelNum > 100):
                enableFlag = 0

            for i in range(6):
                evValue = int(self.evsList[i].displayText())
                ivValue = int(self.ivsList[i].displayText())

                evTotal += evValue
                if (evValue > 255 or evValue < 0):
                    enableFlag = 0

                if (ivValue > 31 or ivValue < 0):
                    enableFlag = 0

            if (evTotal > 510):
                enableFlag = 0
        except:
            enableFlag = 0



        if (self.chosenMovesetMap == {}):
            enableFlag = 0

        if (enableFlag == 1):
            self.pushFinished.setEnabled(True)
        else:
            self.pushFinished.setEnabled(False)

        self.checkPlayerTeams()

        return

    def updateStats(self):
        if (self.pokedex.get(self.txtPokedexEntry.displayText()) == None):
            return
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        #if (self.txtFinal_HP.isEnabled() == False):
        #   return

        natureIndex = self.comboNatures.currentIndex()
        increasedStat, decreasedStat = self.natureEffects[natureIndex]
        #level = int(self.txtChosenLevel.displayText())

        for i in range(6):
            statChange = 1

            try:
                ivValue = int(self.ivsList[i].displayText())
                evValue = int(self.evsList[i].displayText())
                level = int(self.txtChosenLevel.displayText())
                if (i == 0):
                    self.finalStatsList[i].setText(str(math.floor(math.floor(((2*int(pokemon.baseStats[i]) + ivValue + (math.floor(evValue/4))) * level)/100) + level + 10)))
                else:
                    if (i == 1 and increasedStat == "Att"):
                        statChange = 1.1#self.finalStatsList[i] = (((((2*pokemon.baseStats[i] + ivValue + (evValue/4)) * level)/100)) + 5) * 1.1
                    elif (i == 1 and decreasedStat == "Att"):
                        statChange = 0.9
                    elif (i == 2 and increasedStat == "Def"):
                        statChange = 1.1
                    elif (i == 2 and decreasedStat == "Def"):
                        statChange = 0.9
                    elif (i == 3 and increasedStat == "SpAtt"):
                        statChange = 1.1
                    elif (i == 3 and decreasedStat == "SpAtt"):
                        statChange = 0.9
                    elif (i == 4 and increasedStat == "SpDef"):
                        statChange = 1.1
                    elif (i == 4 and decreasedStat == "SpDef"):
                        statChange = 0.9
                    elif (i == 5 and increasedStat == "Spd"):
                        statChange = 1.1
                    elif (i == 5 and decreasedStat == "Spd"):
                        statChange = 0.9
                    self.finalStatsList[i].setText(str(math.floor(((math.floor(((2 * int(pokemon.baseStats[i]) + ivValue + math.floor(evValue / 4)) * level) / 100)) + 5) * statChange)))
            except:
                self.finalStatsList[i].setText(str(pokemon.baseStats[i]))

    def resetDetails(self):
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.chosenMovesetMap = {}


        self.listChosenMoves.clear()
        self.comboAvailableMoves.clear()
        self.comboAvailableAbilities.clear()
        self.comboGenders.clear()

        self.listChosenMoves.addItem("Move 1:")
        self.listChosenMoves.addItem("Move 2:")
        self.listChosenMoves.addItem("Move 3:")
        self.listChosenMoves.addItem("Move 4:")

        for i in range(6):
            self.finalStatsList[i].setText("")

        return

    def clearGUI(self):
        # Clear Details
        self.resetDetails()
        self.txtPokedexEntry.setText("")
        self.txtChosenLevel.setText("")
        self.txtHappinessVal.setText("")

        for i in range(6):
            self.evsList[i].setText("")
            self.ivsList[i].setText("")

        return

    def updateAbilities(self):
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        self.comboAvailableAbilities.clear()

        count = 0
        for ability in pokemon.abilities:
            idNum, displayName, description = self.abilitiesDatabase.get(ability)
            self.comboAvailableAbilities.addItem(displayName)
            self.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(ability)
            count += 1

        if (pokemon.hiddenAbility != ""):
            idNum, displayName, description = self.abilitiesDatabase.get(pokemon.hiddenAbility)
            self.comboAvailableAbilities.addItem(displayName)#("HA: " + displayName)
            self.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(pokemon.hiddenAbility)

        return

    def updatePokemonMoves(self):
        pokemon = self.pokedex.get(self.txtPokedexEntry.displayText())
        self.comboAvailableMoves.clear()

        count = 0
        for move in pokemon.moves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(move)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            #self.comboAvailableMoves.addItem("Move: " + moveName + " " + "Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            #self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        for move in pokemon.eggMoves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.movesDatabase.get(move)
            _, typeName, _, _, _ = self.typesDatabase.get(typeMove)
            self.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            #self.comboAvailableMoves.addItem("Move: " + moveName + "\t" + "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            #self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        return

    def updateGenders(self):
        pokedexEntry = self.txtPokedexEntry.displayText()
        pokemonObject = self.pokedex.get(pokedexEntry)
        self.comboGenders.clear()
        if (len(pokemonObject.genders) != 0):
            if ("MALE" in pokemonObject.genders):
                self.comboGenders.addItem("Male")
            if ("FEMALE" in pokemonObject.genders):
                self.comboGenders.addItem("Female")
        else:
            self.comboGenders.addItem("Genderless")

    def displayPokemon(self, viewPokemon, pokedexEntry):
        if (pokedexEntry != None):
            pokemonImageScene = QtWidgets.QGraphicsScene()
            pokemon = self.pokedex.get(pokedexEntry)
            pixmap = QtGui.QPixmap(pokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem =QtWidgets.QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, QtCore.Qt.KeepAspectRatio)
        else:
            scene = QtWidgets.QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()

    def disableDetails(self):
        self.pushFinished.setEnabled(False)

        for i in range(6):
            self.evsList[i].setEnabled(False)
            self.ivsList[i].setEnabled(False)

        self.pushRandomizeEVs.setEnabled(False)
        self.pushRandomizeIVs.setEnabled(False)

        self.pushAddMove.setEnabled(False)

        return

    def enableDetails(self):
        #self.pushFinished.setEnabled(True)

        for i in range(6):
            self.evsList[i].setEnabled(True)
            self.ivsList[i].setEnabled(True)

        self.pushRandomizeEVs.setEnabled(True)
        self.pushRandomizeIVs.setEnabled(True)

        self.pushAddMove.setEnabled(True)

        return


def playMusic():
    subprocess.call("/Users/imadsheriff/Documents/Random\ Stuff/playDancing.sh", shell=True)
    return

def executeGUI():
    currentApp = QtWidgets.QApplication(sys.argv)
    currentForm = battleConsumer()
    currentForm.show()
    currentApp.exec_()

    return

if __name__ == "__main__":
    #p1 = Process(target=executeGUI)
    #p1.start()
    #p2 = Process(target=playMusic)
    #p2.start()

    executeGUI()

    #pool = Pool()
    #pool.map()
    #result1 = pool.apply_async(playMusic())
    #result2 = pool.apply_async(executeGUI())
    #answer1 = result1.get(timeout=10)
    #answer2 = result2.get(timeout=10)