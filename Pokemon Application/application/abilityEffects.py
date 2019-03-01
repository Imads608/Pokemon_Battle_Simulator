from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
from pokemonBattleMetadata import *

class AbilityEffects(object):
    def __init__(self, battleUI, tab1Consumer):
        self.battleUI = battleUI
        self.tab1Consumer = tab1Consumer

        # Current Pokemon and Opponent Pokemon Variables
        self.currPokemon = None
        self.currPokemonTemp = None
        self.currPlayerTeam = None
        self.currPlayerWidgets = None
        self.currPlayerAction = None
        self.currPlayerMoveTuple = None

        self.opponentPokemon = None
        self.opponentPokemonTemp = None
        self.opponentPlayerTeam = None
        self.opponentPlayerWidgets = None
        self.opponentPlayerAction = None
        self.opponentPlayerMoveTuple = None

        # Priority Effects Variables
        self.currSpeed = None
        self.moveTurn = None

    def updateFields(self, playerNum, stateInBattle):
        if (stateInBattle == "Entry"):
            self.updateEntryFields(playerNum)
        elif (stateInBattle == "Priority"):
            self.updatePriorityEffectsFields(playerNum)
        elif ("Move Effect" in stateInBattle):
            self.updateMoveEffectsFields(playerNum)
        elif ("Move Execution" in stateInBattle):
            self.updateMoveExecutionFields(playerNum)
        elif (stateInBattle == "End of Turn"):
            self.updateEoTFields(playerNum)
        elif (stateInBattle == "Priority"):
            self.updatePriorityFields(playerNum)

    def updateEntryFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.currPlayerWidgets = self.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.opponentPlayerWidgets = self.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.currPlayerWidgets = self.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.opponentPlayerWidgets = self.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateMoveEffectsFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.currPokemonTemp = self.tab1Consumer.battleObject.player1Action.moveObject.attackerTempObject
            self.currPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.currPlayerWidgets = self.battleUI.player1B_Widgets
            self.currPlayerAction = self.tab1Consumer.battleObject.player1Action
            self.opponentPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = self.tab1Consumer.battleObject.player1Action.moveObject.opponentTempObject
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.opponentPlayerWidgets = self.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.currPokemonTemp = self.tab1Consumer.battleObject.player2Action.moveObject.attackerTempObject
            self.currPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.currPlayerWidgets = self.battleUI.player2B_Widgets
            self.currPlayerAction = self.tab1Consumer.battleObject.player2Action
            self.opponentPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = self.tab1Consumer.battleObject.player2Action.moveObject.opponentTempObject
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.opponentPlayerWidgets = self.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateMoveExecutionFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.currPlayerWidgets = self.battleUI.player1B_Widgets
            self.currPlayerAction = self.tab1Consumer.battleObject.player1Action
            self.opponentPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.opponentPlayerWidgets = self.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.currPlayerWidgets = self.battleUI.player2B_Widgets
            self.currPlayerAction = self.tab1Consumer.battleObject.player2Action
            self.opponentPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.opponentPlayerWidgets = self.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateMoveEoTFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.currPlayerWidgets = self.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.opponentPlayerWidgets = self.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.currPlayerWidgets = self.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.opponentPlayerWidgets = self.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updatePriorityFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.currPlayerWidgets = self.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.opponentPlayerWidgets = self.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.tab1Consumer.battleObject.player2Team
            self.currPlayerWidgets = self.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.tab1Consumer.battleObject.player1Team
            self.opponentPlayerWidgets = self.battleUI.player1B_Widgets
            self.opponentPlayerAction = None
        self.currSpeed = self.currPokemon.battleInfo.battleStats[5]
        self.moveTurn = None

    def determineAbilityEffects(self, currPlayerNum, stateInBattle, ability):
        self.updateFields(currPlayerNum, stateInBattle)

        if (ability == "DOWNLOAD"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.battleInfo.battleStats[2] < self.opponentPokemon.battleInfo.battleStats[4]):
                    self.currPokemon.battleInfo.battleStats[1] = int(self.currPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                    self.currPokemon.battleInfo.statsStages[1] += 1
                    self.tab1Consumer.updateBattleInfo(currPokemon.name + "\'s Download raised its Attack")
                else:
                    self.currPokemon.battleInfo.battleStats[3] = int(self.currPokemon.battleInfo.battleStats[3] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                    self.currPokemon.battleInfo.statsStages[3] += 1
                    self.tab1Consumer.updateBattleInfo(currPokemon.name + "\'s Download raised its Special Attack")
        elif (ability == "INTIMIDATE"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.internalAbility == "CONTRARY" and self.opponentPokemon.battleInfo.statsStages[1] != 6):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                    self.opponentPokemon.battleInfo.statsStages[1] += 1
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Intimidate increased " + self.opponentPokemon.name + "\'s Attack")
                elif (self.opponentPokemon.internalAbility == "SIMPLE" and self.opponentPokemon.battleInfo.statsStages[1] > -5):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 2])
                    self.opponentPokemon.battleInfo.statsStages[1] -= 2
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Intimidate sharply decreased " + self.opponentPokemon.name + "\'s Attack")
                elif (opponentPokemon.effects.substituteTuple[0] == True):
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Substitute prevented Intimidate from activating")
                elif (self.opponentPokemon.internalAbility == "CLEARBODY" or self.opponentPokemon.internalAbility == "HYPERCUTTER" or self.opponentPokemon.internalAbility == "WHITESMOKE"):
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s " + self.opponentPokemon.internalAbility + " prevented " + self.currPokemon.name + "\'s Intimiade from activating.")
                elif (self.opponentPokemon.battleInfo.statsStages[1] != -6):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 1])
                    self.opponentPokemon.battleInfo.statsStages[1] -= 1
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Intimidate decreased " + self.opponentPokemon.name + "\'s Attack")
        elif (ability == "DRIZZLE"):
            if (stateInBattle == "Entry"):
                self.tab1Consumer.battleFieldObject.addWeatherEffect("Rain", sys.maxsize)
                self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Drizzle made it Rain")
        elif (ability == "DROUGHT"):
            if (stateInBattle == "Entry"):
                self.tab1Consumer.battleFieldObject.addWeatherEffect("Sunny", sys.maxsize)
                self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Drought made it Sunny")
        elif (ability == "SANDSTREAM"):
            if (stateInBattle == "Entry"):
                self.tab1Consumer.battleFieldObject.addWeatherEffect("Sandstorm", sys.maxsize)
                self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Sand Stream brewed a Sandstorm")
        elif (ability == "SNOWWARNING"):
            if (stateInBattle == "Entry"):
                self.tab1Consumer.battleFieldObject.addWeatherEffect("Hail", sys.maxsize)
                self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Snow Warning made it Hail")
        elif (ability == "FRISK"):
            if (stateInBattle == "Entry"):
                self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Frisk showed " + self.opponentPokemon.name + "\'s held item\n")
                tupleData = self.battleUI.itemsDatabase.get(self.opponentPokemon.internalItem)
                if (tupleData == None):
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + " is not holding an item")
                else:
                    fullName, _, _, _, _ = tupleData
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + " is holding " + fullName)
        elif (ability == "ANTICIPATION"):
            if (stateInBattle == "Entry"):
                pokemonPokedex = self.battleUI.pokedex.get(self.currPokemon.pokedexEntry)
                for moveIndex in self.opponentPokemon.internalMovesMap:
                    internalMoveName, _, _ = self.opponentPokemon.internalMovesMap.get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(internalMoveName)
                    if (self.battleUI.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        self.tab1Consumer.updateBattleInfo(self.currPokemon.name + " shudders")
                    elif ((internalMoveName == "FISSURE" and self.battleUI.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleUI.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleUI.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleUI.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        self.tab1Consumer.updateBattleInfo(self.currPokemon.name + " shudders")
        elif (ability == "FOREWARN"):
            if (stateInBattle == "Entry"):
                maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemon.internalMovesMap:
                    internalMoveName, _, _ = self.opponentPokemon.internalMovesMap.get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Forewarn reveals " + self.opponentPokemon.name + "\'s strongest move to be " + moveName)
        elif (ability == "TRACE"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.internalAbility != "FORECAST" and self.opponentPokemon.internalAbility != "FLOWERGIFT" and self.opponentPokemon.internalAbility != "MULTITYPE" and self.opponentPokemon.internalAbility != "ILLUSION" and self.opponentPokemon.internalAbility != "ZENMODE"):
                    self.currPokemon.internalAbility = self.opponentPokemon.internalAbility
                    _, fullName, _ = self.battleUI.abilitiesDatabase.get(self.opponentPokemon.internalAbility)
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Trace caused it to change ability to " + fullName)
                    abilityChanged = True
        elif (ability == "IMPOSTER"):
            pass
        elif (ability == "ILLUSION"):
            pass
        elif (ability == "REGENERATOR"):
            pass
        elif (ability == "NATURALCURE"):
            pass
        elif (ability == "SPEEDBOOST"):
            pass
        elif (ability == "MOODY"):
            pass
        elif (ability == "SHEDSKIN"):
            pass
        elif (ability == "HEALER"):
            pass
        elif (ability == "BADDREAMS"):
            pass
        elif (ability == "HYDRATION"):
            pass
        elif (ability == "DRYSKIN"):
            pass
        elif (ability == "RANDISH"):
            pass
        elif (ability == "ICEBODY"):
            pass
        elif (ability == "PICKUP"):
            pass
        elif (ability == "HARVEST"):
            pass
        elif (ability == "ANGERPOINT"):
            pass
        elif (ability == "DEFIANT"):
            pass
        elif (ability == "STEADFAST"):
            pass
        elif (ability == "WEAKARMOR"):
            pass
        elif (ability == "JUSTIFIED"):
            pass
        elif (ability == "RATTLED"):
            pass
        elif (ability == "MOXIE"):
            pass
        elif (ability == "CURSEDBODY"):
            pass
        elif (ability == "CUTECHARM"):
            pass
        elif (ability == "POISONPOINT"):
            pass
        elif (ability == "STATIC"):
            pass
        elif (ability == "EFFECTSPORE"):
            pass
        elif (ability == "FLAMEBODY"):
            pass
        elif (ability == "ROUGHSKIN"):
            pass
        elif (ability == "IRONBARBS"):
            pass
        elif (ability == "PICKPOCKET"):
            pass
        elif (ability == "MUMMY"):
            pass
        elif (ability == "STENCH"):
            pass
        elif (ability == "POISONTOUCH"):
            pass
        elif (ability == "SYNCHRONIZE"):
            pass
        elif (ability == "AFTERMATH"):
            pass
        elif (ability == "COLORCHANGE"):
            pass
        elif (ability == "FLAREBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.damageCategory == "Special" and self.currPokemonTemp.currStatusCondition == 6):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "GUTS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStatusCondition == 6 and self.currPokemonTemp.currStatsStages[1] != 6 and self.currPlayerAction.moveObject.damageCategory == "Physical"):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "MARVELSCALE"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.opponentPokemonTemp.currStatusCondtion != 0 and self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.moveObject.setTargetDefenseStat(int(self.currPlayerAction.moveObject.targetDefenseStat * 1.5))
        elif (ability == "QUICKFEET"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.battleInfo.statsStages[5] != 6):
                    self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index+1])
        elif (ability == "TOXICBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if ((self.currPokemonTemp.currStatusCondition == 1 or self.currPokemonTemp.currStatusCondition == 2) and self.currPokemonTemp.currStatsStages[1] != 6):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "TANGLEDFEET"):
            if (stateInBattle == "Move Effect Opponent"):
                if (8 in self.opponentPokemonTemp.currTempConditions):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 0.5))
        elif (ability == "HUSTLE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                        if (self.currPokemonTemp.currStatsStages[1] != 6):
                            self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPokemonTemp.currStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
                        self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 0.8))
        elif (ability == "PUREPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                        if (currPokemon.currStatsStages[1] < 5):
                            self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2]))
                        else:
                            self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "HUGEPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                        if (currPokemon.currStatsStages[1] < 5):
                            self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2]))
                        else:
                            self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "COMPOUNDEYES"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 1.3))
        elif (ability == "UNBURDEN"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.internalItem == None and self.currPokemon.battleInfo.wasHoldingItem == True and self.currPokemon.battleInfo.statsStages[5] < 6):
                    if (self.currPokemon.battleInfo.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
        elif (ability == "SLOWSTART"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.battleInfo.turnsPlayed < 5 and self.currPokemon.battleInfo.statsStages[5] != -6):
                    self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
            elif (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 0.5))
        elif (ability == "DEFEATIST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 2)):
                        action.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 0.5))
        elif (ability == "VICTORYSTAR"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 1.1))
        elif (ability == "PLUS"):
            pass
        elif (ability == "MINUS"):
            pass
        elif (ability == "CHLOROPHYLL"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.opponentPokemon.internalAbility != "AIRLOCK" and self.opponentPokemon.internalAbility != "CLOUDNINE" and self.currPokemon.battleInfo.statsStages[5] < 6):
                    if (self.currPokemon.battleInfo.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
        elif (ability == "SWIFTSWIM"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Rain" and self.opponentPokemon.internalAbility != "AIRLOCK" and self.opponentPokemon.internalAbility != "CLOUDNINE" and self.currPokemon.battleInfo.statsStages[5] < 6):
                    if (self.currPokemon.battleInfo.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
        elif (ability == "SANDRUSH"):
            pass
        elif (ability == "SOLARPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.moveObject.damageCategory == "Special"):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 1.5))
        elif (ability == "SANDVEIL"):
            pass
        elif (ability == "SNOWCLOAK"):
            pass
        elif (ability == "FLOWERGIFT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.moveObject.damageCategory == "Physical"):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 1.5))
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Special" and self.opponentPokemonTemp.currStatsStages[4] != 6 and self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny"):
                    self.currPlayerAction.moveObject.setTargetDefenseStat(int(self.currPlayerAction.moveObject.setTargetDefenseStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
        elif (ability == "BLAZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "FIRE"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "OVERGROW"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "GRASS"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "TORRENT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "WATER"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "SWARM"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "BUG"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "SANDFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if ((self.currPlayerAction.moveObject.typeMove == "ROCK" or self.currPlayerAction.moveObject.typeMove == "GROUND" or self.currPlayerAction.moveObject.typeMove == "STEEL") and self.currPlayerAction.moveObject.damageCategory != "Status" and self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.3))
        elif (ability == "IRONFIST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(self.currPlayerAction.moveObject.internalMove)
                    if ("j" in flag):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.2))
        elif (ability == "RECKLESS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.functionCode == "0FA" or self.currPlayerAction.moveObject.functionCode == "0FB" or self.currPlayerAction.moveObject.functionCode == "0FC" or self.currPlayerAction.moveObject.functionCode == "0FD" or self.currPlayerAction.moveObject.functionCode == "0FE" or self.currPlayerAction.moveObject.internalMove == "JUMPKICK" or self.currPlayerAction.moveObject.internalMove == "HIGHJUMPKICK"):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.2))
        elif (ability == "RIVALRY"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPokemon.gender != "Genderless" and self.opponentPokemon.gender != "Genderless"):
                        if (self.currPokemon.gender == self.opponentPokemon.gender):
                            self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.25))
                        else:
                            self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 0.75))
        elif (ability == "SHEERFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.currAddEffect != 0):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.3))
                        self.currPlayerAction.moveObject.setAddEffect(0)
        elif (ability == "TECHNICIAN"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.currPower <= 60):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "TINTEDLENS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    pokemonPokedex = self.battleUI.pokedex.get(self.opponentPokemon.pokedexEntry)
                    if (self.battleUI.checkTypeEffectivenessExists(self.currPlayerAction.moveObject.typeMove, pokemonPokedex.resistances) == True):
                        self.currPlayerActionaction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 2))
        elif (ability == "SNIPER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.criticalHit == True):
                        pass # Handled in Critical Hit Determine Function
        elif (ability == "ANALYTIC"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.isFirst == False):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.3))
        elif (ability == "BIGPECKS"):
            pass
        elif (ability == "HYPERCUTTER"):
            pass
        elif (ability == "KEENEYE"):
            pass
        elif (ability == "CLEARBODY"):
            pass
        elif (ability == "WHITESMOKE"):
            pass
        elif (ability == "IMMUNITY"):
            pass
        elif (ability == "MAGMAARMOR"):
            pass
        elif (ability == "LIMBER"):
            pass
        elif (ability == "INSOMNIA"):
            pass
        elif (ability == "VITALSPIRIT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.internalMove == "REST"):
                        self.currPlayerAction.setInvalid()
                        self.currPlayerAction.setBattleMessage("But it failed")
        elif (ability == "WATERVEIL"):
            pass
        elif (ability == "OWNTEMPO"):
            pass
        elif (ability == "OBLIVIOUS"):
            pass
        elif (ability == "INNERFOCUS"):
            pass
        elif (ability == "LEAFGUARD"):
            pass
        elif (ability == "FLASHFIRE"):
            pass
        elif (ability == "STORMDRAIN"):
            pass
        elif (ability == "WATERABSORB"):
            pass
        elif (ability == "LIGHTNINGROD"):
            pass
        elif (ability == "MOTORDRIVE"):
            pass
        elif (ability == "VOLTABSORB"):
            pass
        elif (ability == "SAPSIPPOR"):
            pass
        elif (ability == "LEVITATE"):
            pass
        elif (ability == "SOUNDPROOF"):
            if (stateInBattle == "Move Effect Opponent"):
                _, moveName, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(self.currPlayerAction.moveObject.internalMove)
                if (self.opponentPokemonTemp.currInternalAbility == "SOUNDPROOF" and "k" in flag):
                    self.currPlayerAction.setInvalid()
                    #action.setBattleMessage(opponentPokemon.name + " is immune to the move")
        elif (ability == "BATTLEARMOR"):
            pass
        elif (ability == "SHELLARMOR"):
            pass
        elif (ability == "ROCKHEAD"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPlayerAction.moveObject.setRecoil(0)
        elif (ability == "TELEPATHY"):
            pass
        elif (ability == "STURDY"):
            pass
        elif (ability == "WONDERGUARD"):
            pass
        elif (ability == "HEATPROOF"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.typeMove == "FIRE"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 0.5))
        elif (ability == "THICKFAT"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.typeMove in ["FIRE", "ICE"]):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 0.5))
        elif (ability == "SOLIDROCK"):
            pass
        elif (ability == "FILTER"):
            pass
        elif (ability == "MULTISCALE"):
            pass
        elif (ability == "FRIENDGUARD"):
            pass
        elif (ability == "MAGICGUARD"):
            pass
        elif (ability == "SIMPLE"):
            pass
        elif (ability == "POISONHEAL"):
            pass
        elif (ability == "EARLYBIRD"):
            pass
        elif (ability == "LIQUIDOOZE"):
            pass
        elif (ability == "AIRLOCK"):
            pass
        elif (ability == "CLOUDNINE"):
            pass
        elif (ability == "STICKYHOLD"):
            pass
        elif (ability == "GLUTTONY"):
            pass
        elif (ability == "UNNERVE"):
            pass
        elif (ability == "KLUTZ"):
            pass
        elif (ability == "RUNAWAY"):
            pass
        elif (ability == "SUCTIONCUPS"):
            pass
        elif (ability == "SHADOWTAG"):
            pass
        elif (ability == "ARENATRAP"):
            pass
        elif (ability == "MAGNETPULL"):
            pass
        elif (ability == "MOLDBREAKER"):
            pass
        elif (ability == "TERAVOLT"):
            pass
        elif (ability == "TURBOBLAZE"):
            pass
        elif (ability == "PRESSURE"):
            pass
        elif (ability == "TRUANT"):
            pass
        elif (ability == "STALL"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                self.moveTurn = "last"
        elif (ability == "UNAWARE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                        self.currPlayerAction.moveObject.setTargetDefenseStat(self.opponentPokemon.finalStats[2])
                    elif (self.currPlayerAction.moveObject.damageCategory == "Special"):
                        self.currPlayerAction.moveObject.setTargetDefenseStat(self.opponentPokemon.finalStats[4])
                    self.opponentPokemonTemp.currEvasion = 100
                    self.opponentPokemonTemp.currEvasionStage = 0
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    self.currPlayerAction.moveObject.setTargetAttackStat(self.currPokemon.finalStats[1])
                elif (self.currPlayerAction.moveObject.damageCategory == "Special"):
                    self.currPlayerAction.moveObject.setTargetAttackStat(self.currPokemon.finalStats[3])
                self.currPokemonTemp.currAccuracy = 100
                self.currPokemonTemp.currAccuracyStage = 0
        elif (ability == "CONTRARY"):
            pass
        elif (ability == "SCRAPPY"):
            pass
        elif (ability == "SERENEGRACE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPlayerAction.moveObject.setAddEffect(self.currPlayerAction.moveObject.currAddEffect * 2)
        elif (ability == "SHIELDDUST"):
            if (stateInBattle == "Move Effect Opponent"):
                self.currPlayerAction.moveObject.setAddEffect(0)
        elif (ability == "SKILLINK"):
            pass
        elif (ability == "SUPERLUCK"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPlayerAction.moveObject.setCriticalHitStage(self.currPlayerAction.moveObject.criticalHitStage + 1)
        elif (ability == "DAMP"):
            pass
        elif (ability == "ADAPTABILITY"):
            pass
        elif (ability == "NOGUARD"):
            pass
        elif (ability == "NORMALIZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    if (self.currPlayerAction.moveObject.internalMove not in ["HIDDENPOWER", "WEATHERBALL", "NATURALGIFT", "JUDGEMENT"]):
                        self.currPlayerAction.moveObject.setTypeMove("NORMAL")
        elif (ability == "WONDERSKIN"):
            pass
        elif (ability == "INFILTRATOR"):
            pass
        elif (ability == "PRANKSTER"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                movesSetMap = self.currPokemon.internalMovesMap
                internalMoveName, _, _ = movesSetMap.get(moveTuple[1] + 1)
                _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(internalMoveName)
                if (damageCategory == "Status"):
                    self.currPlayerMoveTuple[2] += 1
        elif (ability == "ILLUMINATE"):
            pass
        elif (ability == "HONEYGATHER"):
            pass
        elif (ability == "MAGICBOUNCE"):
            pass
        elif (ability == "HEAVYMETAL"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPokemonTemp.currWeight *= 2
        elif (ability == "LIGHTMETAL"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.opponentPokemonTemp.currInternalAbility not in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
                    self.currPokemonTemp.currWeight *= 0.5
        elif (ability == "FORECAST"):
            pass
        elif (ability == "MULTITYPE"):
            pass
        elif (ability == "ZENMODE"):
            pass



        
    def determineAbilityEntryEffects(self, listCurrPlayerWidgets, listOpponentPlayerWidgets, currPokemonIndex, opponentPokemonIndex):
        currPlayerTeam = listCurrPlayerWidgets[6]
        currPokemon = currPlayerTeam[currPokemonIndex]
        opponentPlayerTeam = listOpponentPlayerWidgets[6]
        opponentPokemon = opponentPlayerTeam[opponentPokemonIndex]

        abilityChanged = False
        message = ""

        if (currPokemon.internalAbility == "DOWNLOAD"):
            if (opponentPokemon.battleStats[2] < opponentPokemon.battleStats[4]):
                currPokemon.battleStats[1] = int(
                    currPokemon.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                currPokemon.statsStages[1] += 1
                message = currPokemon.name + "\'s Download raised its Attack"
            else:
                currPokemon.battleStats[3] = int(
                    currPokemon.battleStats[3] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                currPokemon.statsStages[3] += 1
                message = currPokemon.name + "\'s Download raised its Special Attack"
        elif (currPokemon.internalAbility == "INTIMIDATE" and opponentPokemon.statsStages[1] != -6):
            if (opponentPokemon.internalAbility == "CONTRARY" and opponentPokemon.statsStages[1] != 6):
                opponentPokemon.battleStats[1] = int(
                    opponentPokemon.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                opponentPokemon.statsStages[1] += 1
                message = currPokemon.name + "\'s Intimidate increased " + opponentPokemon.name + "\'s Attack"
            elif (opponentPokemon.internalAbility == "SIMPLE" and opponentPokemon.statsStages[1] > -5):
                opponentPokemon.battleStats[1] = int(
                    opponentPokemon.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 2])
                opponentPokemon.statsStages[1] -= 2
                message = currPokemon.name + "\'s Intimidate sharply decreased " + opponentPokemon.name + "\'s Attack"
            elif (opponentPokemon.effects.substituteTuple[0] == True):
                message = opponentPokemon.name + "\'s Substitute prevented Intimidate from activating"
            elif (
                    opponentPokemon.internalAbility == "CLEARBODY" or opponentPokemon.internalAbility == "HYPERCUTTER" or opponentPokemon.internalAbility == "WHITESMOKE"):
                message = opponentPokemon.name + "\'s " + opponentPokemon.internalAbility + " prevented " + currPokemon.name + "\'s Intimiade from activating."
            else:
                opponentPokemon.battleStats[1] = int(
                    opponentPokemon.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 1])
                opponentPokemon.statsStages[1] -= 1
                message = currPokemon.name + "\'s Intimidate decreased " + opponentPokemon.name + "\'s Attack"
        elif (currPokemon.internalAbility == "DRIZZLE"):
            self.tab1Consumer.battleFieldObject.addWeatherEffect("Rain", sys.maxsize)
            message = opponentPokemon.name + "\'s Drizzle made it Rain"
        elif (currPokemon.internalAbility == "DROUGHT"):
            self.tab1Consumer.battleFieldObject.addWeatherEffect("Sunny", sys.maxsize)
            message = opponentPokemon.name + "\'s Drought made it Sunny"
        elif (currPokemon.internalAbility == "SANDSTREAM"):
            self.tab1Consumer.battleFieldObject.addWeatherEffect("Sandstorm", sys.maxsize)
            message = opponentPokemon.name + "\'s Sand Stream brewed a Sandstorm"
        elif (currPokemon.internalAbility == "SNOWWARNING"):
            self.tab1Consumer.battleFieldObject.addWeatherEffect("Hail", sys.maxsize)
            message = opponentPokemon.name + "\'s Snow Warning made it Hail"
        elif (currPokemon.internalAbility == "FRISK"):
            message = currPokemon.name + "\'s Frisk showed " + opponentPokemon.name + "\'s held item\n"
            tupleData = self.battleUI.itemsDatabase.get(opponentPokemon.internalItem)
            if (tupleData == None):
                message += opponentPokemon.name + " is not holding an item"
            else:
                fullName, _, _, _, _ = tupleData
                message += message + opponentPokemon.name + " is holding " + fullName
        elif (currPokemon.internalAbility == "ANTICIPATION"):
            pokemonPokedex = self.battleUI.pokedex.get(currPokemon.pokedexEntry)
            for moveIndex in opponentPokemon.internalMovesMap:
                internalMoveName, _, _ = opponentPokemon.internalMovesMap.get(moveIndex)
                _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(internalMoveName)
                if (self.battleUI.checkTypeEffectivenessExists(typeMove,
                                                      pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                    message = currPokemon.name + " shudders"
                elif ((internalMoveName == "FISSURE" and self.battleUI.checkTypeEffectivenessExists(typeMove,
                                                                                           pokemonPokedex.immunities) == False) or (
                              internalMoveName == "SHEERCOLD" and self.battleUI.checkTypeEffectivenessExists(typeMove,
                                                                                                    pokemonPokedex.immunities) == False) or (
                              internalMoveName == "GUILLOTINE" and self.battleUI.checkTypeEffectivenessExists(typeMove,
                                                                                                     pokemonPokedex.immunities) == False) or (
                              internalMoveName == "HORNDRILL" and self.battleUI.checkTypeEffectivenessExists(typeMove,
                                                                                                    pokemonPokedex.immunities))):
                    message = currPokemon.name + " shudders"
        elif (currPokemon.internalAbility == "FOREWARN"):
            maxPower = -1
            moveName = ""
            for moveIndex in opponentPokemon.internalMovesMap:
                internalMoveName, _, _ = opponentPokemon.internalMovesMap.get(moveIndex)
                _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(
                    internalMoveName)
                if (basePower > maxPower):
                    maxPower = basePower
                    moveName = fullName
            if (moveName != ""):
                message = currPokemon.name + "\'s Forewarn reveals " + opponentPokemon.name + "\'s strongest move to be " + moveName
        elif (currPokemon.internalAbility == "TRACE"):
            if (
                    opponentPokemon.internalAbility != "FORECAST" and opponentPokemon.internalAbility != "FLOWERGIFT" and opponentPokemon.internalAbility != "MULTITYPE" and opponentPokemon.internalAbility != "ILLUSION" and opponentPokemon.internalAbility != "ZENMODE"):
                currPokemon.internalAbility = opponentPokemon.internalAbility
                _, fullName, _ = self.battleUI.abilitiesDatabase.get(opponentPokemon.internalAbility)
                message = currPokemon.name + "\'s Trace caused it to change ability to " + fullName
                abilityChanged = True
        elif (currPokemon.internalAbility == "VITALSPIRIT" and currPokemon.nonVolatileCondition == 4):
            currPokemon.nonVolatileCondition = 0
            self.battleUI.updateBattleInfo(currPokemon.name + "\'s Vital Spirit woke it up from its sleep")
        elif (currPokemon.internalAbility == "ILLUSION"):
            pass
        elif (currPokemon.internalAbility == "IMPOSTER"):
            pass
        elif (currPokemon.internalAbility == "CONTRARY"):
            pass
        elif (currPokemon.internalAbility == "FORECAST"):
            pass
        elif (currPokemon.internalAbility == "MULTITYPE"):
            pass
        elif (currPokemon.internalAbility == "ZENMODE"):
            pass

        return message

    def determineAbilityPriorityEffects(self, currPokemon, opponentPokemon, moveTuple):
        currSpeed = currPokemon.battleInfo.battleStats[5]
        moveTurn = None
        if (moveTuple[0] == "switch"):
            return (currSpeed, None)
        movesSetMap = currPokemon.internalMovesMap
        internalMoveName, _, _ = movesSetMap.get(moveTuple[1] + 1)
        _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.battleUI.movesDatabase.get(internalMoveName)

        # if (self.tab1Consumer.battleFieldObject.)
        if (currPokemon.battleInfo.nonVolatileConditionIndex == 3 and currPokemon.internalAbility != "QUICKFEET" and
                currPokemon.battleInfo.statsStages[5] != -6):
            currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 1])
        elif (currPokemon.internalAbility == "QUICKFEET" and currPokemon.battleInfo.statsStages[5] != 6):
            currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
        elif (
                currPokemon.internalAbility == "UNBURDEN" and currPokemon.internalItem == None and currPokemon.battleInfo.wasHoldingItem == True and
                currPokemon.battleInfo.statsStages[5] < 6):
            if (currPokemon.battleInfo.statsStages[5] < 5):
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 2])
            else:
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
        elif (currPokemon.internalAbility == "SLOWSTART" and currPokemon.battleInfo.turnsPlayed < 5 and
              currPokemon.battleInfo.statsStages[5] != -6):
            currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 1])
        elif (currPokemon.internalAbility == "CHLOROPHYLL" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[
                  0] == "Sunny" and opponentPokemon.internalAbility != "AIRLOCK" and opponentPokemon.internalAbility != "CLOUDNINE" and
              currPokemon.battleInfo.statsStages[5] < 6):
            if (currPokemon.battleInfo.statsStages[5] < 5):
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 2])
            else:
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
        elif (currPokemon.internalAbility == "SWIFTSWIM" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[
                  0] == "Rain" and opponentPokemon.internalAbility != "AIRLOCK" and opponentPokemon.internalAbility != "CLOUDNINE" and
              currPokemon.battleInfo.statsStages[5] < 6):
            if (currPokemon.battleInfo.statsStages[5] < 5):
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 2])
            else:
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
        elif (currPokemon.internalAbility == "CHLOROPHYLL" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[
                  0] == "Sandstorm" and opponentPokemon.internalAbility != "AIRLOCK" and opponentPokemon.internalAbility != "CLOUDNINE" and
              currPokemon.battleInfo.statsStages[5] < 6):
            if (currPokemon.battleInfo.statsStages[5] < 5):
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 2])
            else:
                currSpeed = int(currSpeed * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
        elif (currPokemon.internalAbility == "STALL"):
            moveTurn = "last"
        elif (currPokemon.internalAbility == "PRANKSTER" and damageCategory == "Status"):
            moveTuple[2] += 1

        return (currSpeed, moveTurn)

    def determineAttackerAbilityMoveEffects(self, currPokemon, opponentPokemon, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(action.moveObject.internalMove)

        if (
                opponentPokemon.currInternalAbility == "MOLDBREAKER" or opponentPokemon.currInternalAbility == "TERAVOLT" or opponentPokemon.currInternalAbility == "TURBOBLAZE"):
            return

        if (currPokemon.playerNum == 1):
            attackerPokemonRead = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            opponentPokemonRead = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
        else:
            attackerPokemonRead = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            opponentPokemonRead = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]

        return
        if (
                currPokemon.currInternalAbility == "FLAREBOOST" and action.moveObject.damageCategory == "Special" and currPokemon.currStatusCondition == 6):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "GUTS" and currPokemon.currStatusCondition == 6 and
              currPokemon.currStatsStages[1] != 6 and action.moveObject.damageCategory == "Physical"):
            action.moveObject.setTargetAttackStat(
                int(action.moveObject.targetAttackStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
        elif (currPokemon.currInternalAbility == "TOXICBOOST" and (
                currPokemon.currStatusCondition == 1 or currPokemon.currStatusCondition == 2) and
              currPokemon.currStatsStages[1] != 6):
            action.moveObject.setTargetAttackStat(
                int(action.moveObject.targetAttackStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
        elif (currPokemon.currInternalAbility == "HUSTLE" and action.moveObject.damageCategory == "Physical"):
            if (currPokemon.currStatsStages[1] != 6):
                action.moveObject.setTargetAttackStat(
                    int(currPokemon.currStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
            action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy * 0.8))
        elif ((
                      currPokemon.currInternalAbility == "PUREPOWER" or currPokemon.currInternalAbility == "HUGEPOWER") and action.moveObject.damageCategory == "Physical" and
              currPokemon.currStatsStages[1] != 6):
            if (currPokemon.currStatsStages[1] < 5):
                action.moveObject.setTargetAttackStat(
                    int(action.moveObject.targetAttackStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 2]))
            else:
                action.moveObject.setTargetAttackStat(
                    int(action.moveObject.targetAttackStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
        elif (currPokemon.currInternalAbility == "COMPOUNDEYES"):
            action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy * 1.3))
        elif (currPokemon.currInternalAbility == "SLOWSTART" and action.moveObject.damageCategory == "Physical"):
            action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 0.5))
        elif (currPokemon.currInternalAbility == "DEFEATIST" and currPokemon.currStats[0] <= int(
                attackerPokemonRead.finalStats[0] / 2)):
            action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 0.5))
        elif (currPokemon.currInternalAbility == "VICTORYSTAR"):
            action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy * 1.1))
        elif (currPokemon.currInternalAbility == "SOLARPOWER" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and action.moveObject.damageCategory == "Special"):
            action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 1.5))
        elif (currPokemon.currInternalAbility == "FLOWERGIFT" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and action.moveObject.damageCategory == "Physical"):
            action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 1.5))
        elif (currPokemon.currInternalAbility == "BLAZE" and currPokemon.currStats[0] <= int(
                attackerPokemonRead.finalStats[
                    0] / 3) and action.moveObject.damageCategory != "Status" and action.moveObject.typeMove == "FIRE"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "OVERGROW" and currPokemon.currStats[0] <= int(
                attackerPokemonRead.finalStats[
                    0] / 3) and action.moveObject.damageCategory != "Status" and action.moveObject.typeMove == "GRASS"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "TORRENT" and currPokemon.currStats[0] <= int(
                attackerPokemonRead.finalStats[
                    0] / 3) and action.moveObject.damageCategory != "Status" and action.moveObject.typeMove == "WATER"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "SWARM" and currPokemon.currStats[0] <= int(
                attackerPokemonRead.finalStats[
                    0] / 3) and action.moveObject.damageCategory != "Status" and action.moveObject.typeMove == "BUG"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "SANDFORCE" and (
                action.moveObject.typeMove == "ROCK" or action.moveObject.typeMove == "GROUND" or action.moveObject.typeMove == "STEEL") and action.moveObject.damageCategory != "Status" and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sandstorm"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.3))
        elif (currPokemon.currInternalAbility == "IRONFIST" and "j" in flag):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.2))
        elif (currPokemon.currInternalAbility == "RECKLESS" and (
                action.moveObject.functionCode == "0FA" or action.moveObject.functionCode == "0FB" or action.moveObject.functionCode == "0FC" or action.moveObject.functionCode == "0FD" or action.moveObject.functionCode == "0FE" or action.moveObject.internalMove == "JUMPKICK" or action.moveObject.internalMove == "HIGHJUMPKICK")):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.2))
        elif (
                currPokemon.currInternalAbility == "RIVALRY" and attackerPokemonRead.gender != "Genderless" and opponentPokemonRead.gender != "Genderless"):
            if (attackerPokemonRead.gender == opponentPokemonRead.gender):
                action.moveObject.setMovePower(int(action.moveObject.currPower * 1.25))
            else:
                action.moveObject.setMovePower(int(action.moveObject.currPower * 0.75))
        elif (currPokemon.currInternalAbility == "SHEERFORCE" and action.moveObject.currAddEffect != 0):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.3))
            action.moveObject.setAddEffect(0)
        elif (currPokemon.currInternalAbility == "TECHNICIAN" and action.moveObject.currPower <= 60):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.5))
        elif (currPokemon.currInternalAbility == "TINTEDLENS"):
            pokemonPokedex = self.battleUI.pokedex.get(opponentPokemonRead.pokedexEntry)
            if (self.battleUI.checkTypeEffectivenessExists(action.moveObject.typeMove, pokemonPokedex.resistances) == True):
                action.moveObject.setMovePower(int(action.moveObject.currPower * 2))
        elif (currPokemon.currInternalAbility == "SNIPER" and action.moveObject.criticalHit == True):
            # Handled in Critical Hit Determine Function
            pass
        elif (currPokemon.currInternalAbility == "ANALYTIC" and action.isFirst == False):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 1.3))
        elif (currPokemon.currInternalAbility == "VITALSPIRIT" and action.moveObject.internalMove == "REST"):
            action.setInvalid()
            action.setBattleMessage("But it failed")
        elif (currPokemon.currInternalAbility == "ROCKHEAD"):
            action.moveObject.setRecoil(0)
        elif (currPokemon.currInternalAbility == "UNAWARE"):
            if (action.moveObject.damageCategory == "Physical"):
                action.moveObject.setTargetDefenseStat(opponentPokemonRead.finalStats[2])
            elif (action.moveObject.damageCategory == "Special"):
                action.moveObject.setTargetDefenseStat(opponentPokemonRead.finalStats[4])
            opponentPokemon.currEvasion = 100
            opponentPokemon.currEvasionStage = 0
        elif (currPokemon.currInternalAbility == "SERENEGRACE"):
            action.moveObject.setAddEffect(action.moveObject.currAddEffect * 2)
        elif (currPokemon.currInternalAbility == "SUPERLUCK"):
            action.moveObject.setCriticalHitStage(action.moveObject.criticalHitStage + 1)
        elif (currPokemon.currInternalAbility == "NORMALIZE" and action.moveObject.internalMove != "HIDDENPOWER" and action.moveObject.internalMove != "WEATHERBALL" and action.moveObject.internalMove != "NATURALGIFT" and action.moveObject.internalMove != "JUDGEMENT"):
            action.moveObject.setTypeMove("NORMAL")
        elif (currPokemon.currInternalAbility == "HEAVYMETAL"):
            currPokemon.currWeight *= 2
        elif (currPokemon.currInternalAbility == "LIGHTMETAL"):
            currPokemon.currWeight *= 0.5

    def determineOpponentAbilityMoveEffects(self, currPokemon, opponentPokemon, action):
        # TODO: Check Ability 'Pick Up' and implement multi-strike move Ability effects such as Rattled

        _, moveName, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(action.moveObject.internalMove)
        if (currPokemon.playerNum == 1):
            attackerPokemonRead = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]
            opponentPokemonRead = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
        else:
            attackerPokemonRead = self.tab1Consumer.battleObject.player2Team[self.tab1Consumer.battleObject.currPlayer2PokemonIndex]
            opponentPokemonRead = self.tab1Consumer.battleObject.player1Team[self.tab1Consumer.battleObject.currPlayer1PokemonIndex]

        randNum = random.randint(1, 100)

        if (opponentPokemon.currInternalAbility == "MARVELSCALE" and opponentPokemon.currStatusCondtion != 0 and action.damageCategory == "Physical"):
            action.moveObject.setTargetDefenseStat(int(action.moveObject.targetDefenseStat * 1.5))
        elif (opponentPokemon.currInternalAbility == "TANGLEDFEET" and 8 in opponentPokemon.currTempConditions):  # and opponentPokemon.currEvasionStage != 6):
            action.moveObject.setMoveAccuracy(int(action.moveObject.currMoveAccuracy * 0.5))
            # opponentPokemon.currEvasion = int(opponentPokemon.currEvasion * self.battleUI.accuracy_evasionMultipliers[self.battleUI.accuracy_evasionStage0Index+1])
            # opponentPokemon.currEvasionStage += 1
        elif (opponentPokemon.currInternalAbility == "FLOWERGIFT" and action.moveObject.damageCategory == "Special" and
              opponentPokemon.currStatsStages[4] != 6 and self.tab1Consumer.battleFieldObject.weatherEffect != None and
              self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny"):
            action.moveObject.setTargetDefenseStat( int(action.moveObject.setTargetDefenseStat * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1]))
            # opponentPokemon.currStats[2] = int(opponentPokemon.currStats[2] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index+1])
            # opponentPokemon.currStatsStages[2] += 1
        elif (opponentPokemon.currInternalAbility == "SOUNDPROOF" and "k" in flag):
            action.setInvalid()
            action.setBattleMessage(opponentPokemon.name + " is immune to the move")
        elif ((opponentPokemon.currInternalAbility == "HEATPROOF" or opponentPokemon.currInternalAbility == "THICKFAT") and action.moveObject.typeMove == "FIRE"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 0.5))
        elif (opponentPokemon.currInternalAbility == "THICKFAT" and action.moveObject.typeMove == "ICE"):
            action.moveObject.setMovePower(int(action.moveObject.currPower * 0.5))
        elif (opponentPokemon.currInternalAbility == "UNAWARE"):
            if (action.moveObject.damageCategory == "Physical"):
                action.moveObject.setTargetAttackStat(attackerPokemonRead.finalStats[1])
            elif (action.moveObject.damageCategory == "Special"):
                action.moveObject.setTargetAttackStat(attackerPokemonRead.finalStats[3])
            currPokemon.currAccuracy = 100
            currPokemon.currAccuracyStage = 0
        elif (opponentPokemon.currInternalAbility == "SHIELDDUST"):
            action.moveObject.setAddEffect(0)
        elif (opponentPokemon.currInternalAbility == "WONDERSKIN" and action.moveObject.damageCategory == "Status" and currPokemon.currInternalAbility not in [
            "MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
            action.moveObject.setMoveAccuracy(50)
        elif (opponentPokemon.currInternalAbility == "HEAVYMETAL"):
            opponentPokemon.currWeight *= 2
        elif (opponentPokemon.currInternalAbility == "LIGHTMETAL"):
            opponentPokemon.currWeight *= 0.5
        return

    def determineAttackerAbilityMoveExecutionEffects(self, currPokemon, opponentPokemon, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(action.moveObject.internalMove)

        if (currPokemon.internalAbility == "MOXIE" and opponentPokemon.battleInfo.battleStats[
            0] - action.moveObject.currDamage == 0):
            currPokemon.battleInfo.battleStats[1] = int(currPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
            currPokemon.battleInfo.statsStages[1] += 1
            self.battleUI.updateBattleInfo(currPokemon.name + "\'s Moxie raised its Attack")
        elif (currPokemon.internalAbility == "STENCH"):
            randNum = random.randint(0, 100)
            if (randNum <= 10):
                action.moveObject.setFlinchValid()
        elif (currPokemon.internalAbility == "POISONTOUCH" and "a" in flag):
            randNum = random.randint(0, 100)
            if (randNum <= 30 and action.moveObject.nonVolatileCondition == None and opponentPokemon.nonVolatileConditionIndex == None):
                action.moveObject.setNonVolatileCondition(1)
        return

    def determineOpponentAbilityMoveExecutionEffects(self, currPokemon, currPlayerWidgets, opponentPokemon, opponentPlayerWidgets, action):
        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(action.moveObject.internalMove)
        executeFlag = True
        message = ""
        if (opponentPokemon.internalAbility == "DRYSKIN"):  # Remove
            if (action.moveObject.typeMove == "FIRE" and action.moveObject.damageCategory != "Status"):
                action.moveObject.setMovePower(int(action.moveObject.currPower * 1.25))
                self.battleUI.calculateDamage(action, currPokemon)
            if (action.moveObject.typeMove == "WATER"):
                action.moveObject.setEffectiveness(0)
                healAmt = int(0.25 * opponentPokemon.finalStats[0])
                if (healAmt + opponentPokemon.currStats[0] > opponentPokemonRead.finalStats[0]):
                    action.moveObject.setHealAmount(opponentPokemonRead.finalStats[0] - opponentPokemon.currStats[0])
                else:
                    action.moveObject.setHealAmount(healAmt)
                self.battleUI.showHealHealthAnimation(opponentPokemon, healAmt, opponentPlayerWidgets[2])
                message = opponentPokemon.name + "\'s Dry Skin absorbed the move and restored some HP"
                executeFlag = False
        elif (opponentPokemon.internalAbility == "ANGERPOINT" and action.moveObject.criticalHit == True and
              opponentPokemon.battleInfo.battleStats[0] - action.moveObject.currDamage > 0):
            opponentPokemon.battleInfo.battleStats[1] = int(
                opponentPokemon.finalStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 6])
            opponentPokemon.battleInfo.statsStages[1] = 6
            messaage = opponentPokemon.name + "\'s Anger Point maximized its Attack"
        elif (opponentPokemon.internalAbility == "DEFIANT"):
            statsLowered = 0
            statsChangesTuple = action.moveObject.opponentTemp.statsChangesTuple
            for i in range(1, 6):
                if (statsChangesTuple[i][0] < 0 and statsChangesTuple[i][1] == "opponent"):
                    statsLowered += 1
            stageIncrease = statsLowered * 2
            if (opponentPokemon.battleInfo.statsStages[1] + stageIncrease > 6):
                opponentPokemon.battleInfo.statsStages[1] = 6
                opponentPokemon.battleInfo.battleStats[1] = int(
                    opponentPokemon.finalStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 6])
            else:
                opponentPokemon.battleInfo.statsStages[1] += stageIncrease
                opponentPokemon.battleInfo.battleStats[1] = int(
                    opponentPokemon.finalStats[1] * self.battleUI.statsStageMultipliers[
                        self.battleUI.stage0Index + opponentPokemon.battleInfo.statsStages[1]])
            message = opponentPokemon.name + "\'s Defiant raised its Attack"
        elif (opponentPokemon.internalAbility == "STEADFAST" and action.moveObject.flinch == True):
            if (opponentPokemon.battleInfo.statsStages[5] != 6):
                opponentPokemon.battleInfo.statsStages[5] += 1
                opponentPokemon.battleInfo.battleStats[5] = int(
                    opponentPokemon.battleInfo.battleStats[5] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                message = opponentPokemon.name + "\'s Steadfast raised its Speed"
        elif (opponentPokemon.internalAbility == "WEAKARMOR" and action.moveObject.damageCategory == "Physical"):
            defLowered = False
            speedIncreased = False
            if (opponentPokemon.battleInfo.statsStages[2] != -6):
                opponentPokemon.battleInfo.statsStages[2] -= 1
                opponentPokemon.battleInfo.battleStats[2] = int(
                    opponentPokemon.battleInfo.battleStats[2] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index - 1])
                defLowered = True
            if (opponentPokemon.battleInfo.statsStages[5] != 6):
                opponentPokemon.battleInfo.statsStages[5] += 1
                opponentPokemon.battleInfo.battleStats[5] = int(
                    opponentPokemon.battleInfo.battleStats[5] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
                speedIncreased = True
            if (defLowered and speedIncreased):
                message = opponentPokemon.name + "\'s Weak Armor lowered its Defense but increased its Speed"
            elif (defLowered):
                message = opponentPokemon.name + "\'s Weak Armor lowered its Defense"
            elif (speedIncreased):
                message = opponentPokemon.name + "\'s Weak Armor increased its Speed"
        elif (
                opponentPokemon.internalAbility == "JUSTIFIED" and action.moveObject.typeMove == "DARK" and action.moveObject.damageCategory != "Status" and
                opponentPokemon.battleInfo.statsStages[1] != 6):
            opponentPokemon.battleInfo.statsStages[1] += 1
            opponentPokemon.battleInfo.battleStats[1] = int(
                opponentPokemon.battleInfo.battleStats[1] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
            message = opponentPokemon.name + "\'s Justified raised its Attack"
        elif (opponentPokemon.internalAbility == "RATTLED" and action.moveObject.typeMove in ["DARK", "BUG",
                                                                                              "GHOST"] and action.moveObject.damageCategory != "Status" and
              opponentPokemon.battleInfo.statsStages[5] != 6):
            opponentPokemon.battleInfo.statsStages[5] += 1
            opponentPokemon.battleInfo.battleStats[5] = int(
                opponentPokemon.battleInfo.battleStats[5] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index + 1])
            message = opponentPokemon.name + "\'s Rattled increased its Attack"
        elif (opponentPokemon.internalAbility == "CURSEDBODY" and action.moveObject.damageCategory != "Status"):
            if (randNum <= 30):
                currPokemon.battleInfo.effects.addMovesBlocked(action.moveObject.internalMove, 4)
                message = opponentPokemon.name + "\'s Cursed Body blocked " + moveName
        elif (
                opponentPokemon.internalAbility == "CUTECHARM" and action.moveObject.damageCategory == "Physical" and currPokemon.gender != "Genderless" and opponentPokemon.gender != "Genderless" and currPokemon.gender != opponentPokemon.gender):
            if (randNum <= 30 and 9 not in currPokemon.battleInfo.volatileConditionIndices):
                currPokemon.battleInfo.volatileConditionIndices.append(9)
                message = attackerPokemon.name + " became infatuated"
        elif (
                opponentPokemon.internalAbility == "POISONPOINT" and action.moveObject.damageCategory == "Physical" and currPokemon.battleInfo.nonVolatileConditionIndex == 0):
            if (randNum <= 30):
                currPokemon.battleInfo.nonVolatileConditionIndex = 1
                message = opponentPokemon.name + "\'s Poison Point poisoned " + currPokemon.name
        elif (
                opponentPokemon.internalAbility == "STATIC" and action.moveObject.damageCategory == "Physical" and currPokemon.battleInfo.nonVolatileConditionIndex == 0):
            if (randNum <= 30):
                currPokemon.battleInfo.nonVolatileConditionIndex = 3
                message = opponentPokemon.name + "\'s Static paralyzed " + currPokemon.name
        elif (
                opponentPokemon.internalAbility == "EFFECTSPORE" and action.moveObject.damageCategory == "Physical" and currPokemon.battleInfo.nonVolatileConditionIndex == 0):
            if (randNum <= 30):
                randNum2 = random.randint(1, 30)
                if (randNum2 <= 9):
                    currPokemon.battleInfo.nonVolatileConditionIndex = 1
                    message = opponentPokemon.name + "\'s Effect Spore poisoned " + currPokemon.name
                elif (randNum2 <= 19):
                    currPokemon.battleInfo.nonVolatileConditionIndex = 3
                    message = opponentPokemon.name + "\'s Effect Spore paralyzed " + currPokemon.name
                else:
                    currPokemon.battleInfo.nonVolatileConditionIndex = 4
                    message = opponentPokemon.name + "\'s Effect spore made " + currPokemon.name + " fall asleep"
        elif (
                opponentPokemon.internalAbility == "FLAMEBODY" and action.moveObject.damageCategory == "Physical" and currPokemon.battleInfo.nonVolatileConditionIndex == 0):
            if (randNum <= 30):
                currPokemon.battleInfo.nonVolatileConditionIndex = 6
                message = opponentPokemon.name + "\'s Flame Body burned " + currPokemon.name
        elif (opponentPokemon.internalAbility == "ROUGHSKIN" and action.moveObject.damageCategory == "Physical"):
            damage = int(currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] / 16))
            if (currPokemon.battleInfo.battleStats[0] - damage < 0):
                currPokemon.battleInfo.battleStats[0] = 0
                currPokemon.battleInfo.isFainted = True
                message = opponentPokemon.name + "\'s Rough Skin hurt " + currPokemon.name + "\n" + currPokemon.name + " fainted"
            else:
                currPokemon.battleInfo.battleStats[0] -= damage
                message = opponentPokemon.name + "\'s Rough Skin hurt " + currPokemon.name
        elif (opponentPokemon.internalAbility == "IRONBARBS" and action.moveObject.damageCategory == "Physical"):
            damage = int(currPokemon.battleInfo.battleStats[0] - (currPokemon.finalStats[0] / 8))
            if (currPokemon.battleInfo.battleStats[0] - damage < 0):
                currPokemon.battleInfo.battleStats[0] = 0
                currPokemon.battleInfo.isFainted = True
                message = opponentPokemon.name + "\'s Iron Barbs hurt " + currPokemon.name + "\n" + currPokemon.name + " fainted"
            else:
                currPokemon.battleInfo.battleStats[0] -= damage
                message = opponentPokemon.name + "\'s Iron Barbs hurt " + currPokemon.name
        elif (opponentPokemon.internalAbility == "PICKPOCKET" and opponentPokemon.internalItem == None and
              opponentPokemon.battleInfo.battleStats[0] - action.moveObject.currDamage > 0):
            # TODO: Must check at very end of determineMoveDetails function. (Move will not work if pokemon dies)
            opponentPokemon.internalItem = currPokemon.internalItem
            currPokemon.internalItem = None
            message = opponentPokemon.name + "\'s Pickpocket stole " + opponentPokemon.internalItem + " from " + currPokemon.name
        elif (
                opponentPokemon.internalAbility == "MUMMY" and action.moveObject.damageCategory == "Physical" and currPokemon.internalAbility != "MUMMY"):
            currPokemon.internalAbility = "MUMMY"
            message = opponentPokemon.name + "\'s Mummy chaanged " + currPokemon.name + "\'s ability to be Mummy as well"
        elif (opponentPokemon.internalAbility == "SYNCHRONIZE"):
            pass
        elif (opponentPokemon.internalAbility == "AFTERMATH"):
            # TODO: Check Ability at very end of determineMoveDetails function (MOve will work if pokemon dies)
            pass

        return (executeFlag, message)
        '''
        if (opponentPokemon.currInternalAbility == "DRYSKIN"):
            if (action.moveObject.typeMove == "FIRE" and action.moveObject.damageCategory != "Status"):
                action.moveObject.setDamage(int(action.moveObject.currDamage*1.25))
            elif (action.moveObject.typeMove == "WATER"):
                action.setInvalid()
                opponentPokemon.currStats[0] = int(opponentPokemon.currStats[0] + opponentPokemonRead.finalStats[0]/4)
                if (opponentPokemon.currStats[0] > opponentPokemonRead.finalStats[0]):
                    opponentPokemon.currStats[0] = opponentPokemonRead.finalStats[0]
                action.setBattleMessage(opponentPokemon.name + "\'s Dry Skin made it absorb Water Type Moves")
        elif (opponent.currInternalAbility == "ANGERPOINT" and action.moveObject.criticalHit == True):
            currPokemon.currStats[1] = currPokemonRead.finalStats[0] * self.battleUI.statsStageMultipliers[self.battleUI.stage0Index+6]
            currPokemon.currStatsStages[1] = 6
            currPokemon.permanentChanges.append("Attack")
            action.setBattleMessage(opponentPokemon.name + "\'s Anger Point caused it's Attack to be maximized")
        elif (opponentPokemon.currInternalAbility == "DEFIANT"):
            pass
        '''

    def determineEoTAbilityEffects(self, pokemon):
        if (pokemon.internalAbility == "SPEEDBOST"):
            if (pokemon.battleInfo.turnsPlayed > 0 and pokemon.battleInfo.statsStages[5] != 6):
                pokemon.battleInfo.statsStages[5] += 1
                pokemon.battleInfo.battleStats[5] += int(pokemon.battleInfo.battleStats[5] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index+1])
                self.tab1Consumer.updateBattleInfo(pokemon.name + " \'s Speed Boost increased its speed")
        elif (pokemon.internalAbility == "MOODY"):
            arrStats = ["HP", "Attack", "Special Attack", "Defense", "Special Defense", "Speed"]
            randomInc = random.randint(1, 5)
            randomDec = random.randint(1, 5)
            while (randomInc == randomDec):
                randomDec = random.randint(1,5)
            if (pokemon.battleInfo.battleStats[1] == 6 and pokemon.battleInfo.battleStats[2] == 6 and pokemon.battleInfo.battleStats[3] == 6 and pokemon.battleInfo.battleStats[4] == 6 and pokemon.battleInfo.battleStats[5] == 6):
                pokemon.battleInfo.statsStages[randomDec] -= 1
                pokemon.battleInfo.battleStats[randomDec] -= int(pokemon.battleInfo.battleStats[randomDec] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index-1])
                self.tab1Consumer.updateBattleInfo(pokemon.name + "\'s Moody decreased its " + arrStats[randomDec])
            elif (pokemon.battleInfo.battleStats[1] == -6 and pokemon.battleInfo.battleStats[2] == -6 and pokemon.battleInfo.battleStats[3] == -6 and pokemon.battleInfo.battleStats[4] == -6 and pokemon.battleInfo.battleStats[5] == -6):
                pokemon.battleInfo.statsStages[randomInc] += 2
                pokmeon.battleInfo.battleStats[randomInc] += int(pokemon.battleInfo.battleStats[randomInc] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index+2])
                self.tab1Consumer.updateBattleInfo(pokemon.name + "\'s Moody sharply raised its " + arrStats[randomInc])
            else:
                pokemon.battleInfo.statsStages[randomDec] -= 1
                pokemon.battleInfo.battleStats[randomDec] -= int(pokemon.battleInfo.battleStats[randomDec] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
                if (pokemon.battleInfo.statsStages[randomInc] < 5):
                    pass
        elif (pokemon.internalAbility == "SHEDSKIN"):
            pass
        elif (pokemon.internalAbility == "BADDREAMS"):
            pass
        elif (pokemon.internalAbility == "HYDRATION"):
            pass
        elif (pokemon.internalAbility == "DRYSKIN"):
            pass
        elif (pokemon.internalAbility == "RANDISH"):
            pass
        elif (pokemon.internalAbility == "ICEBODY"):
            pass
        elif (pokemon.internalAbility == "PICKUP"):
            pass
        elif (pokemon.internalAbility == "HARVEST"):
            pass
        elif (pokemon.internalAbility == "SANDRUSH"):
            pass
        elif (pokemon.internalAbility == "SOLARPOWER"):
            pass
        elif (pokemon.internalAbility == "SANDVEIL"):
            pass
        elif (pokemon.internalAbility == "SNOWCLOAK"):
            pass
        elif (pokemon.internalAbility == "SANDFORCE"):
            pass
        elif (pokemon.internalAbility == "HEATPROOF"):
            pass
        elif (pokemon.internalAbility == "MAGICGUARD"):
            pass
        elif (pokemon.internalAbility == "LIQUIDOOZE"):
            pass
        elif (pokemon.internalAbility == "AIRLOCK"):
            pass
        elif (pokemon.internalAbility == "CLOUDNINE"):
            pass
        elif (pokemon.internalAbility == "ZENMODE"):
            pass