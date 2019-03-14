from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
import sys
from pokemonBattleMetadata import *

class AbilityEffects(object):
    def __init__(self, gameUI, battle, battleField):
        self.gameUI = gameUI
        self.battle = battle
        self.battleField = battleField

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

        # Generic Variables
        self.message = ""

        # Priority Effects Variables
        self.currSpeed = None
        self.moveTurn = None

        # Move Execution Opponent Variables
        self.executeFlag = True

    def updateFields(self, playerNum, stateInBattle):
        self.message = ""
        self.executeFlag = True

        if (stateInBattle == "Entry"):
            self.updateEntryFields(playerNum)
        elif (stateInBattle == "Priority"):
            self.updatePriorityFields(playerNum)
        elif ("Move Effect" in stateInBattle):
            self.updateMoveEffectsFields(playerNum)
        elif ("Move Execution" in stateInBattle):
            self.updateMoveExecutionFields(playerNum)
        elif (stateInBattle == "End of Turn"):
            self.updateEoTFields(playerNum)
        elif (stateInBattle == "Switch out"):
            self.updateEntryFields(playerNum)

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

    def updateEoTFields(self, playerNum):
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
        if (stateInBattle == "Move Effect Opponent" and self.currPokemonTemp.currInternalAbility in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
            return

        if (ability == "DOWNLOAD"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.battleInfo.battleStats[2] < self.opponentPokemon.battleInfo.battleStats[4]):
                    self.currPokemon.battleInfo.battleStats[1] = int(self.currPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.currPokemon.battleInfo.statsStages[1] += 1
                    self.tab1Consumer.updateBattleInfo(currPokemon.name + "\'s Download raised its Attack")
                else:
                    self.currPokemon.battleInfo.battleStats[3] = int(self.currPokemon.battleInfo.battleStats[3] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.currPokemon.battleInfo.statsStages[3] += 1
                    self.tab1Consumer.updateBattleInfo(currPokemon.name + "\'s Download raised its Special Attack")
        elif (ability == "INTIMIDATE"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.internalAbility == "CONTRARY" and self.opponentPokemon.battleInfo.statsStages[1] != 6):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.opponentPokemon.battleInfo.statsStages[1] += 1
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Intimidate increased " + self.opponentPokemon.name + "\'s Attack")
                elif (self.opponentPokemon.internalAbility == "SIMPLE" and self.opponentPokemon.battleInfo.statsStages[1] > -5):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 2])
                    self.opponentPokemon.battleInfo.statsStages[1] -= 2
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Intimidate sharply decreased " + self.opponentPokemon.name + "\'s Attack")
                elif (self.opponentPokemon.battleInfo.effects.substituteTuple[0] == True):
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s Substitute prevented Intimidate from activating")
                elif (self.opponentPokemon.internalAbility == "CLEARBODY" or self.opponentPokemon.internalAbility == "HYPERCUTTER" or self.opponentPokemon.internalAbility == "WHITESMOKE"):
                    self.tab1Consumer.updateBattleInfo(self.opponentPokemon.name + "\'s " + self.opponentPokemon.internalAbility + " prevented " + self.currPokemon.name + "\'s Intimiade from activating.")
                elif (self.opponentPokemon.battleInfo.statsStages[1] != -6):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
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
                self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Sand Stream brewed a Sandstorm")
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
            if (stateInBattle == "End of Turn"):
                if (self.currPokemon.battleInfo.turnsPlayed > 0 and self.currPokemon.battleInfo.statsStages[5] != 6):
                    self.currPokemon.battleInfo.statsStages[5] += 1
                    self.currPokemon.battleInfo.battleStats[5] += int(self.currPokemon.battleInfo.battleStats[5] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + " \'s Speed Boost increased its speed")
        elif (ability == "MOODY"):
            if (stateInBattle == "End of Turn"):
                arrStats = ["Health", self.currPokemon.battleStats.statsStages[1], self.currPokemon.battleStats.statsStages[2], self.currPokemon.battleStats.statsStages[3], self.currPokemon.battleStats.statsStages[4], self.currPokemon.battleStats.statsStages[5], self.currPokemon.battleStats.accuracyStage, self.currPokemon.battleStats.evasionStage]
                statsNames = ["Health", "Attack", "Special Attack", "Defense", "Special Defense", "Speed", "Accuracy", "Evasion"]
                repeatFlag = True
                while (repeatFlag == True):
                    randomInc = random.randint(1, 7)
                    randomDec = random.randint(1, 7)
                    if (randomInc == randomDec):
                        continue
                    elif (arrStats == ["Health",6,6,6,6,6,6,6]):
                        repeatFlag = False
                        if (randomDec == 6):
                            self.currPokemon.battleInfo.accuracyStage -= 1
                            self.currPokemon.battleInfo.accuracy = int(self.currPokemon.battleInfo.accuracy * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage-1])
                        elif (randomDec == 7):
                            self.currPokemon.battleInfo.evasionStage -= 1
                            self.currPokemon.battleInfo.evasion = int(self.currPokemon.battleInfo.evasion * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage - 1])
                        else:
                            self.currPokemon.battleInfo.statsStages[randomDec] -= 1
                            self.currPokemon.battleInfo.battleStats[randomDec] -= int(self.currPokemon.battleInfo.battleStats[randomDec] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
                        self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Moody decreased its " + statsNames[randomDec])
                    elif (arrStats == ["Health", -6,-6,-6,-6,-6,-6,-6]):
                        repeatFlag = False
                        if (randomInc == 6):
                            self.currPokemon.battleInfo.accuracyStage += 2
                            self.currPokemon.battleInfo.accuracy = int(self.currPokemon.battleInfo.accuracy * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage+2])
                        elif (randomInc == 7):
                            self.currPokemon.battleInfo.evasionStage += 2
                            self.currPokemon.battleInfo.evasion = int(self.currPokemon.battleInfo.evasion * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage + 2])
                        else:
                            self.currPokemon.battleInfo.statsStages[randomInc] += 2
                            self.currPokemon.battleInfo.battleStats[randomInc] += int(self.currPokemon.battleInfo.battleStats[randomInc] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2])
                        self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Moody sharply raised its " + statsNames[randomInc])
                    elif (arrStats[randomInc] != 6 and arrStats[randomDec] == -6):
                        repeatFlag = False
                        if (arrStats[randomInc] == 5):
                            incNum = 1
                            self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Moody raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        else:
                            incNum = 2
                            self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Moody sharply raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        if (randomInc == 6):
                            self.currPokemon.battleInfo.accuracyStage += incNum
                            self.currPokemon.battleInfo.accuracy = int(self.currPokemon.battleInfo.accuracy * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage + incNum])
                        elif (randomInc == 7):
                            self.currPokemon.battleInfo.evasionStage += incNum
                            self.currPokemon.battleInfo.evasion = int(self.currPokemon.battleInfo.evasion * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage + incNum])
                        else:
                            self.currPokemon.battleInfo.statsStages[randomInc] += incNum
                            self.currPokemon.battleInfo.battleStats[randomInc] += int(self.currPokemon.battleInfo.battleStats[randomInc] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + incNum])
                        if (randomDec == 6):
                            self.currPokemon.battleInfo.accuracyStage -= 1
                            self.currPokemon.battleInfo.accuracy = int(self.currPokemon.battleInfo.accuracy * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage-1])
                        elif (randomDec == 7):
                            self.currPokemon.battleInfo.evasionStage -= 1
                            self.currPokemon.battleInfo.evasion = int(self.currPokemon.battleInfo.evasion * self.tab1Consumer.accuracy_evasionMultipliers[self.tab1Consumer.accuracy_evasionStage - 1])
                        else:
                            self.currPokemon.battleInfo.statsStages[randomDec] -= 1
                            self.currPokemon.battleInfo.battleStats[randomDec] -= int(self.currPokemon.battleInfo.battleStats[randomDec] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
        elif (ability == "SHEDSKIN"):
            if (stateInBattle == "End of Turn"):
                randNum = random.randint(1,100)
                if (self.currPokemon.battleStats.nonVolatileIndex != 0 and randNum <= 30):
                    self.currPokemon.battleStats.nonVolatileIndex = 0
                    self.tab1Consumer.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Shed Skin cured its status condition")
        elif (ability == "HEALER"):
            # Useful in double and triple battles
            pass
        elif (ability == "BADDREAMS"):
            if (stateInBattle == "End of Turn"):
                if (self.opponentPokemon.internalAbility != "HYDRATION"):
                    damage = int(self.opponentPokemon.finalStats[0] * 1/8)
                    self.tab1Consumer.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + " \'s Bad Dreams hurt " + self.opponentPokemon.name)
        elif (ability == "HYDRATION"):
            if (stateInBattle == "End of Turn"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Raining"):
                    self.currPokemon.battleStats.nonVolatileIndex = 0
                    self.tab1Consumer.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Hydration cured its status condition")
        elif (ability == "DRYSKIN"):
            if (stateInBattle == "Move Effect Opponent"):    # Delete
                if (self.currPlayerAction.moveObject.typeMove == "FIRE" and self.currPlayerAction.moveObject.damageCategory != "Status"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.25))
                    #self.battleUI.calculateDamage(self.currPlayerAction, self.currPokemon)
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.typeMove == "WATER"):
                    self.currPlayerAction.moveObject.setEffectiveness(0)
                    healAmt = int(0.25 * self.opponentPokemon.finalStats[0])
                    if (healAmt + self.opponentPokemon.battleInfo.battleStats[0] > self.opponentPokemon.finalStats[0]):
                        self.currPlayerAction.moveObject.setHealAmount(self.opponentPokemon.finalStats[0] - self.opponentPokemon.battleInfo.battleStats[0])
                    else:
                        self.currPlayerAction.moveObject.setHealAmount(healAmt)
                    self.battleUI.showHealHealthAnimation(self.opponentPokemon, healAmt, self.opponentPlayerWidgets[2])
                    self.message = self.opponentPokemon.name + "\'s Dry Skin absorbed the move and restored some HP"
                    self.executeFlag = False
            elif (stateInBattle == "End of Turn"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny"):
                    damage = int(self.currPokemon.finalStats[0] * 1/8)
                    self.tab1Consumer.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Dry Skin hurt it because of the Weather")
                elif (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Raining"):
                    healAmt = int(self.currPokemon.finalStats[0] * 1/8)
                    self.tab1Consumer.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Dry Skin gained some HP due to the Weather")
        elif (ability == "RAINDISH"):
            if (stateInBattle == "End of Turn"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Raining"):
                    healAmt = int(self.currPokemon.finalStats[0] * 1/16)
                    self.tab1Consumer.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Rain DIsh gained it some HP")
        elif (ability == "ICEBODY"):
            if (stateInBattle == "End of Turn"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Hail"):
                    healAmt = int(self.currPokemon.finalStats[0] *1/16)
                    self.tab1Consumer.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Ice Body gained it some HP")
        elif (ability == "PICKUP"):
            if (stateInBattle == "End of Turn"):
                #TODO: Implement Later
                pass
        elif (ability == "HARVEST"):
            if (stateInBattle == "End of Turn"):
                #TODO: Implement Later
                pass
        elif (ability == "ANGERPOINT"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.criticalHit == True and self.opponentPokemon.battleInfo.battleStats[0] - self.currPlayerAction.moveObject.currDamage > 0):
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.finalStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 6])
                    self.opponentPokemon.battleInfo.statsStages[1] = 6
                    self.messaage = self.opponentPokemon.name + "\'s Anger Point maximized its Attack"
        elif (ability == "DEFIANT"):
            if (stateInBattle == "Move Execution Opponent"):
                statsLowered = 0
                statsChangesTuple = self.currPlayerAction.moveObject.opponentTemp.statsChangesTuple
                for i in range(1, 6):
                    if (statsChangesTuple[i][0] < 0 and statsChangesTuple[i][1] == "opponent"):
                        statsLowered += 1
                stageIncrease = statsLowered * 2
                if (opponentPokemon.battleInfo.statsStages[1] + stageIncrease > 6):
                    self.opponentPokemon.battleInfo.statsStages[1] = 6
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.finalStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 6])
                else:
                    self.opponentPokemon.battleInfo.statsStages[1] += stageIncrease
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.finalStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + self.opponentPokemon.battleInfo.statsStages[1]])
                self.message = self.opponentPokemon.name + "\'s Defiant raised its Attack"
        elif (ability == "STEADFAST"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.flinch == True):
                    if (self.opponentPokemon.battleInfo.statsStages[5] != 6):
                        self.opponentPokemon.battleInfo.statsStages[5] += 1
                        self.opponentPokemon.battleInfo.battleStats[5] = int(self.opponentPokemon.battleInfo.battleStats[5] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                        self.message = self.opponentPokemon.name + "\'s Steadfast raised its Speed"
        elif (ability == "WEAKARMOR"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    defLowered = False
                    speedIncreased = False
                    if (self.opponentPokemon.battleInfo.statsStages[2] != -6):
                        self.opponentPokemon.battleInfo.statsStages[2] -= 1
                        self.opponentPokemon.battleInfo.battleStats[2] = int(self.opponentPokemon.battleInfo.battleStats[2] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index - 1])
                        defLowered = True
                    if (self.opponentPokemon.battleInfo.statsStages[5] != 6):
                        self.opponentPokemon.battleInfo.statsStages[5] += 1
                        self.opponentPokemon.battleInfo.battleStats[5] = int(self.opponentPokemon.battleInfo.battleStats[5] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                        speedIncreased = True
                    if (defLowered and speedIncreased):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor lowered its Defense but increased its Speed"
                    elif (defLowered):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor lowered its Defense"
                    elif (speedIncreased):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor increased its Speed"
        elif (ability == "JUSTIFIED"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.typeMove == "DARK" and self.currPlayerAction.moveObject.damageCategory != "Status" and self.opponentPokemon.battleInfo.statsStages[1] != 6):
                    self.opponentPokemon.battleInfo.statsStages[1] += 1
                    self.opponentPokemon.battleInfo.battleStats[1] = int(self.opponentPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.message = self.opponentPokemon.name + "\'s Justified raised its Attack"
        elif (ability == "RATTLED"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.typeMove in ["DARK", "BUG", "GHOST"] and self.currPlayerAction.moveObject.damageCategory != "Status" and self.opponentPokemon.battleInfo.statsStages[5] != 6):
                    self.opponentPokemon.battleInfo.statsStages[5] += 1
                    self.opponentPokemon.battleInfo.battleStats[5] = int(self.opponentPokemon.battleInfo.battleStats[5] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.message = self.opponentPokemon.name + "\'s Rattled increased its Attack"
        elif (ability == "MOXIE"):
            if (stateInBattle == "Move Execution Attacker"):
                if (opponentPokemon.battleInfo.battleStats[0] - action.moveObject.currDamage == 0):
                    self.currPokemon.battleInfo.battleStats[1] = int(self.currPokemon.battleInfo.battleStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1])
                    self.currPokemon.battleInfo.statsStages[1] += 1
                    self.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moxie raised its Attack")
        elif (ability == "CURSEDBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory != "Status"):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPokemon.battleInfo.effects.addMovesBlocked(self.currPlayerAction.moveObject.internalMove, 4)
                        self.message = self.opponentPokemon.name + "\'s Cursed Body blocked " + self.currPlayerAction.moveObject.internalMove
        elif (ability == "CUTECHARM"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemon.gender != "Genderless" and self.opponentPokemon.gender != "Genderless" and self.currPokemon.gender != self.opponentPokemon.gender):
                    randNum = random.randint(1,100)
                    if (randNum <= 30 and 9 not in self.currPokemon.battleInfo.volatileConditionIndices):
                        self.currPokemon.battleInfo.volatileConditionIndices.append(9)
                        self.message = self.currPokemon.name + " became infatuated"
        elif (ability == "POISONPOINT"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPlayerAction.battleInfo.nonVolatileConditionIndex == 0):
                    if (randNum <= 30):
                        self.currPokemon.battleInfo.nonVolatileConditionIndex = 1
                        self.message = self.opponentPokemon.name + "\'s Poison Point poisoned " + self.currPokemon.name
        elif (ability == "STATIC"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemon.battleInfo.nonVolatileConditionIndex == 0):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPokemon.battleInfo.nonVolatileConditionIndex = 3
                        self.message = self.opponentPokemon.name + "\'s Static paralyzed " + self.currPokemon.name
        elif (ability == "EFFECTSPORE"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemon.battleInfo.nonVolatileConditionIndex == 0):
                    randNum = random.randint(1,100)
                    randNum2 = random.randint(1,100)
                    if (randNum <= 30):
                        randNum2 = random.randint(1, 30)
                        if (randNum2 <= 9):
                            self.currPokemon.battleInfo.nonVolatileConditionIndex = 1
                            self.message = self.opponentPokemon.name + "\'s Effect Spore poisoned " + self.currPokemon.name
                        elif (randNum2 <= 19):
                            self.currPokemon.battleInfo.nonVolatileConditionIndex = 3
                            self.message = self.opponentPokemon.name + "\'s Effect Spore paralyzed " + self.currPokemon.name
                        else:
                            self.currPokemon.battleInfo.nonVolatileConditionIndex = 4
                            self.message = self.opponentPokemon.name + "\'s Effect spore made " + self.currPokemon.name + " fall asleep"
        elif (ability == "FLAMEBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemon.battleInfo.nonVolatileConditionIndex == 0):
                    if (randNum <= 30):
                        self.currPokemon.battleInfo.nonVolatileConditionIndex = 6
                        self.message = self.opponentPokemon.name + "\'s Flame Body burned " + self.currPokemon.name
        elif (ability == "ROUGHSKIN"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    damage = int(self.currPokemon.battleInfo.battleStats[0] - (self.currPokemon.finalStats[0] / 16))
                    if (self.currPokemon.battleInfo.battleStats[0] - damage < 0):
                        self.currPokemon.battleInfo.battleStats[0] = 0
                        self.currPokemon.battleInfo.isFainted = True
                        self.message = self.opponentPokemon.name + "\'s Rough Skin hurt " + self.currPokemon.name + "\n" + self.currPokemon.name + " fainted"
                    else:
                        self.currPokemon.battleInfo.battleStats[0] -= damage
                        self.message = self.opponentPokemon.name + "\'s Rough Skin hurt " + self.currPokemon.name
        elif (ability == "IRONBARBS"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    damage = int(self.currPokemon.battleInfo.battleStats[0] - (self.currPokemon.finalStats[0] / 8))
                    if (self.currPokemon.battleInfo.battleStats[0] - damage < 0):
                        self.currPokemon.battleInfo.battleStats[0] = 0
                        self.currPokemon.battleInfo.isFainted = True
                        self.message = self.opponentPokemon.name + "\'s Iron Barbs hurt " + self.currPokemon.name + "\n" + self.currPokemon.name + " fainted"
                    else:
                        self.currPokemon.battleInfo.battleStats[0] -= damage
                        self.message = self.opponentPokemon.name + "\'s Iron Barbs hurt " + self.currPokemon.name
        elif (ability == "PICKPOCKET"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.opponentPokemon.internalItem == None and self.opponentPokemon.battleInfo.battleStats[0] - self.currPlayerAction.moveObject.currDamage > 0):
                    # TODO: Must check at very end of determineMoveDetails function. (Move will not work if pokemon dies)
                    self.opponentPokemon.internalItem = self.currPokemon.internalItem
                    self.currPokemon.internalItem = None
                    self.message = self.opponentPokemon.name + "\'s Pickpocket stole " + self.opponentPokemon.internalItem + " from " + self.currPokemon.name
        elif (ability == "MUMMY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.action.moveObject.damageCategory == "Physical" and self.currPokemon.internalAbility != "MUMMY"):
                    self.currPokemon.internalAbility = "MUMMY"
                    self.message = self.opponentPokemon.name + "\'s Mummy chaanged " + self.currPokemon.name + "\'s ability to be Mummy as well"
        elif (ability == "STENCH"):
            if (stateInBattle == "Move Execution Attacker"):
                if (self.currPokemon.internalAbility == "STENCH"):
                    randNum = random.randint(0, 100)
                    if (randNum <= 10):
                        self.currPlayerAction.moveObject.setFlinchValid()
        elif (ability == "POISONTOUCH"):
            if (stateInBattle == "Move Execution Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(self.currPlayerAction.moveObject.internalMove)
                if ("a" in flag):
                    randNum = random.randint(0, 100)
                    if (randNum <= 30 and self.currPlayerAction.moveObject.nonVolatileCondition == None and self.opponentPokemon.nonVolatileConditionIndex == None):
                        self.currPlayerAction.moveObject.setNonVolatileCondition(1)
        elif (ability == "SYNCHRONIZE"):
            if (stateInBattle == "Move Execution Opponent"):
                pass
        elif (ability == "AFTERMATH"):
            if (stateInBattle == "Move Execution Opponent"):
                pass
            # TODO: Check Ability at very end of determineMoveDetails function (MOve will work if pokemon dies)
        elif (ability == "COLORCHANGE"):
            pass
        elif (ability == "FLAREBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.damageCategory == "Special" and self.currPokemonTemp.currStatusCondition == 6):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "GUTS"):
            if (stateInBattle == "Move Effect Attacker"):
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
                if ((self.currPokemonTemp.currStatusCondition == 1 or self.currPokemonTemp.currStatusCondition == 2) and self.currPokemonTemp.currStatsStages[1] != 6):
                    self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "TANGLEDFEET"):
            if (stateInBattle == "Move Effect Opponent"):
                if (8 in self.opponentPokemonTemp.currTempConditions):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 0.5))
        elif (ability == "HUSTLE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    if (self.currPokemonTemp.currStatsStages[1] != 6):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPokemonTemp.currStats[1] * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 0.8))
        elif (ability == "PUREPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                    if (currPokemon.currStatsStages[1] < 5):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2]))
                    else:
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "HUGEPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                    if (currPokemon.currStatsStages[1] < 5):
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 2]))
                    else:
                        self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "COMPOUNDEYES"):
            if (stateInBattle == "Move Effect Attacker"):
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
                action.moveObject.setTargetAttackStat(int(action.moveObject.targetAttackStat * 0.5))
        elif (ability == "DEFEATIST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 2)):
                    action.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 0.5))
        elif (ability == "VICTORYSTAR"):
            if (stateInBattle == "Move Effect Attacker"):
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
            if (stateInBattle == "End of Turn"):
                # Just needs checking if it gets hurt in sandstorm which is already checked in another area of code
                pass
        elif (ability == "SOLARPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.moveObject.damageCategory == "Special"):
                    self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 1.5))
            elif (stateInBattle == "End of Turn"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.moveObject.damageCategory == "Special"):
                    damage = int(self.currPokemon.finalStats[0] * 1/8)
                    self.tab1Consumer.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.tab1Consumer.updateBattleInfo(self.currPokemon.name + "\'s Solar Power reduced some of its HP")
        elif (ability == "SANDVEIL"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "SNOWCLOAK"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Hail"):
                    self.currPlayerAction.moveObject.setMoveAccuracy(int(self.currPlayerAction.moveObject.currMoveAccuracy * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "FLOWERGIFT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.moveObject.damageCategory == "Physical"):
                    self.currPlayerAction.moveObject.setTargetAttackStat(int(self.currPlayerAction.moveObject.targetAttackStat * 1.5))
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.damageCategory == "Special" and self.opponentPokemonTemp.currStatsStages[4] != 6 and self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sunny"):
                    self.currPlayerAction.moveObject.setTargetDefenseStat(int(self.currPlayerAction.moveObject.setTargetDefenseStat * self.tab1Consumer.statsStageMultipliers[self.tab1Consumer.stage0Index + 1]))
        elif (ability == "BLAZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "FIRE"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "OVERGROW"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "GRASS"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "TORRENT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "WATER"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "SWARM"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.moveObject.damageCategory != "Status" and self.currPlayerAction.moveObject.typeMove == "BUG"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "SANDFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if ((self.currPlayerAction.moveObject.typeMove == "ROCK" or self.currPlayerAction.moveObject.typeMove == "GROUND" or self.currPlayerAction.moveObject.typeMove == "STEEL") and self.currPlayerAction.moveObject.damageCategory != "Status" and self.tab1Consumer.battleFieldObject.weatherEffect != None and self.tab1Consumer.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.3))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already handled
                pass
        elif (ability == "IRONFIST"):
            if (stateInBattle == "Move Effect Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleUI.movesDatabase.get(self.currPlayerAction.moveObject.internalMove)
                if ("j" in flag):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.2))
        elif (ability == "RECKLESS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.functionCode == "0FA" or self.currPlayerAction.moveObject.functionCode == "0FB" or self.currPlayerAction.moveObject.functionCode == "0FC" or self.currPlayerAction.moveObject.functionCode == "0FD" or self.currPlayerAction.moveObject.functionCode == "0FE" or self.currPlayerAction.moveObject.internalMove == "JUMPKICK" or self.currPlayerAction.moveObject.internalMove == "HIGHJUMPKICK"):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.2))
        elif (ability == "RIVALRY"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemon.gender != "Genderless" and self.opponentPokemon.gender != "Genderless"):
                    if (self.currPokemon.gender == self.opponentPokemon.gender):
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.25))
                    else:
                        self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 0.75))
        elif (ability == "SHEERFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.currAddEffect != 0):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.3))
                    self.currPlayerAction.moveObject.setAddEffect(0)
        elif (ability == "TECHNICIAN"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.currPower <= 60):
                    self.currPlayerAction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 1.5))
        elif (ability == "TINTEDLENS"):
            if (stateInBattle == "Move Effect Attacker"):
                pokemonPokedex = self.battleUI.pokedex.get(self.opponentPokemon.pokedexEntry)
                if (self.battleUI.checkTypeEffectivenessExists(self.currPlayerAction.moveObject.typeMove, pokemonPokedex.resistances) == True):
                    self.currPlayerActionaction.moveObject.setMovePower(int(self.currPlayerAction.moveObject.currPower * 2))
        elif (ability == "SNIPER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.moveObject.criticalHit == True):
                    pass # Handled in Critical Hit Determine Function
        elif (ability == "ANALYTIC"):
            if (stateInBattle == "Move Effect Attacker"):
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
            elif (stateInBattle == "End of Turn"):
                # Just needs to half burn damage which is already handled
                pass
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
            # Haandled in other areas in code
            pass
        elif (ability == "SIMPLE"):
            pass
        elif (ability == "POISONHEAL"):
            pass
        elif (ability == "EARLYBIRD"):
            pass
        elif (ability == "LIQUIDOOZE"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.moveObject.functionCode in ["0DC", "0DD", "0DE"]):
                    self.currPlayerAction.setRecoil(self.currPlayerAction.healAmount)
                    self.currPlayerAction.setHealAmount(0)
        elif (ability == "AIRLOCK"):
            if (stateInBattle == "Entry Effect"):
                self.tab1Consumer.battleFieldObject.setWeatherInEffect(False)
            elif (stateInBattle == "Switched Out"):
                self.tab1Consumer.battleFieldObject.setWeatherInEffect(True)
            elif (stateInBattle == "End of Turn"):
                # Handled already elsewhere
                pass
        elif (ability == "CLOUDNINE"):
            if (stateInBattle == "Entry Effect"):
                self.tab1Consumer.battleFieldObject.setWeatherInEffect(False)
            elif (stateInBattle == "Switched Out"):
                self.tab1Consumer.battleFieldObject.setWeatherInEffect(True)
            elif (stateInBattle == "End of Turn"):
                # Handled already elsewhere
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
                self.currPlayerAction.moveObject.setAddEffect(self.currPlayerAction.moveObject.currAddEffect * 2)
        elif (ability == "SHIELDDUST"):
            if (stateInBattle == "Move Effect Opponent"):
                self.currPlayerAction.moveObject.setAddEffect(0)
        elif (ability == "SKILLINK"):
            pass
        elif (ability == "SUPERLUCK"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.moveObject.setCriticalHitStage(self.currPlayerAction.moveObject.criticalHitStage + 1)
        elif (ability == "DAMP"):
            pass
        elif (ability == "ADAPTABILITY"):
            pass
        elif (ability == "NOGUARD"):
            pass
        elif (ability == "NORMALIZE"):
            if (stateInBattle == "Move Effect Attacker"):
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
                self.currPokemonTemp.currWeight *= 2
        elif (ability == "LIGHTMETAL"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPokemonTemp.currWeight *= 0.5
        elif (ability == "FORECAST"):
            pass
        elif (ability == "MULTITYPE"):
            pass
        elif (ability == "ZENMODE"):
            pass