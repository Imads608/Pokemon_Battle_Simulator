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
from pokemonBattleMetadata import *
import functionCodeEffects
import copy
import threading
import time
from tab2 import *
from tab1 import *

# TODO: After mechanics are completed and working, think about features to stand out from the crowd
# Possibly add Pokemon Fusion

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
        # self.txtBattleInfo.setVerticalScrollBar(self.verticalScrollBar)
        # elf.txtBattleInfo.setHorizontalScrollBar(self.horizontalScrollBar)

        self.txtPokemon1_Level.setEnabled(False)
        # self.txtPokemon1_Ability.setEnabled(False)
        # self.txtPokemon1_Nature.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)
        # self.txtPokemon2_Ability.setEnabled(False)
        # self.txtPokemon2_Nature.setEnabled(False)

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

    ######### Item Effects ##########
    # TODO: Revise Function Definitions
    '''
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
    '''

    '''
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
    '''


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