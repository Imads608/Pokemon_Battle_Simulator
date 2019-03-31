from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
import sys

class AbilityEffects(object):
    def __init__(self, battleTab):
        self.battleTab = battleTab

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
            self.currPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player1Team
            self.currPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player2Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player2Team
            self.currPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player1Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateMoveEffectsFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.currPokemonTemp = self.battleTab.player1Action.attackerTempObject
            self.currPlayerTeam = self.battleTab.player1Team
            self.currPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.currPlayerAction = self.battleTab.player1Action
            self.opponentPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = self.battleTab.player1Action.opponentTempObject
            self.opponentPlayerTeam = self.battleTab.player2Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.currPokemonTemp = self.battleTab.player2Action.attackerTempObject
            self.currPlayerTeam = self.battleTab.player2Team
            self.currPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.currPlayerAction = self.battleTab.player2Action
            self.opponentPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = self.battleTab.player2Action.opponentTempObject
            self.opponentPlayerTeam = self.battleTab.player1Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateMoveExecutionFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player1Team
            self.currPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.currPlayerAction = self.battleTab.player1Action
            self.opponentPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player2Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player2Team
            self.currPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.currPlayerAction = self.battleTab.player2Action
            self.opponentPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player1Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updateEoTFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player1Team
            self.currPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player2Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player2Team
            self.currPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player1Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.opponentPlayerAction = None

    def updatePriorityFields(self, playerNum):
        if (playerNum == 1):
            self.currPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player1Team
            self.currPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player2Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.opponentPlayerAction = None
        else:
            self.currPokemon = self.battleTab.player2Team[self.battleTab.currPlayer2PokemonIndex]
            self.currPokemonTemp = None
            self.currPlayerTeam = self.battleTab.player2Team
            self.currPlayerWidgets = self.battleTab.battleUI.player2B_Widgets
            self.currPlayerAction = None
            self.opponentPokemon = self.battleTab.player1Team[self.battleTab.currPlayer1PokemonIndex]
            self.opponentPokemonTemp = None
            self.opponentPlayerTeam = self.battleTab.player1Team
            self.opponentPlayerWidgets = self.battleTab.battleUI.player1B_Widgets
            self.opponentPlayerAction = None
        self.currSpeed = self.currPokemon.battleStats[5]
        self.moveTurn = None

    def determineAbilityEffects(self, currPlayerNum, stateInBattle, ability):
        self.updateFields(currPlayerNum, stateInBattle)
        if (stateInBattle == "Move Effect Opponent" and self.currPokemonTemp.currInternalAbility in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
            return

        if (ability == "DOWNLOAD"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.battleStats[2] < self.opponentPokemon.battleStats[4]):
                    self.currPokemon.setBattleStat(1, int(self.currPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPokemon.setStatStage(1, self.currPokemon.statsStages[1]+1)
                    self.battleTab.battleUI.updateBattleInfo(currPokemon.name + "\'s Download raised its Attack")
                else:
                    self.currPokemon.setBattleStat(3, int(self.currPokemon.battleStats[3] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPokemon.setStatStage(3, self.currPokemon.statsStages[3]+1)
                    self.battleTab.battleUI.updateBattleInfo(currPokemon.name + "\'s Download raised its Special Attack")
        elif (ability == "INTIMIDATE"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.internalAbility == "CONTRARY" and self.opponentPokemon.statsStages[1] != 6):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1]+1)
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Intimidate increased " + self.opponentPokemon.name + "\'s Attack")
                elif (self.opponentPokemon.internalAbility == "SIMPLE" and self.opponentPokemon.statsStages[1] > -5):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 2]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1] - 2)
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Intimidate sharply decreased " + self.opponentPokemon.name + "\'s Attack")
                #TODO: elif (self.opponentPokemon.substituteTuple[0] == True):
                    #self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + "\'s Substitute prevented Intimidate from activating")
                elif (self.opponentPokemon.internalAbility == "CLEARBODY" or self.opponentPokemon.internalAbility == "HYPERCUTTER" or self.opponentPokemon.internalAbility == "WHITESMOKE"):
                    self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + "\'s " + self.opponentPokemon.internalAbility + " prevented " + self.currPokemon.name + "\'s Intimiade from activating.")
                elif (self.opponentPokemon.statsStages[1] != -6):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1] - 1)
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Intimidate decreased " + self.opponentPokemon.name + "\'s Attack")
        elif (ability == "DRIZZLE"):
            if (stateInBattle == "Entry"):
                self.battleTab.battleFieldObject.setWeatherEffect("Rain", sys.maxsize)
                self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + "\'s Drizzle made it Rain")
        elif (ability == "DROUGHT"):
            if (stateInBattle == "Entry"):
                self.battleTab.battleFieldObject.setWeatherEffect("Sunny", sys.maxsize)
                self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + "\'s Drought made it Sunny")
        elif (ability == "SANDSTREAM"):
            if (stateInBattle == "Entry"):
                self.battleTab.battleFieldObject.setWeatherEffect("Sandstorm", sys.maxsize)
                self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Sand Stream brewed a Sandstorm")
        elif (ability == "SNOWWARNING"):
            if (stateInBattle == "Entry"):
                self.battleTab.battleFieldObject.setWeatherEffect("Hail", sys.maxsize)
                self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + "\'s Snow Warning made it Hail")
        elif (ability == "FRISK"):
            if (stateInBattle == "Entry"):
                self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Frisk showed " + self.opponentPokemon.name + "\'s held item\n")
                tupleData = self.battleTab.itemsDatabase.get(self.opponentPokemon.internalItem)
                if (tupleData == None):
                    self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + " is not holding an item")
                else:
                    fullName, _, _, _, _ = tupleData
                    self.battleTab.battleUI.updateBattleInfo(self.opponentPokemon.name + " is holding " + fullName)
        elif (ability == "ANTICIPATION"):
            if (stateInBattle == "Entry"):
                pokemonPokedex = self.battleTab.pokemonDB.pokedex.get(self.currPokemon.pokedexEntry)
                for moveIndex in self.opponentPokemon.internalMovesMap:
                    internalMoveName, _, _ = self.opponentPokemon.internalMovesMap.get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleTab.pokemonDB.movesDatabase.get(internalMoveName)
                    if (self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + " shudders")
                    elif ((internalMoveName == "FISSURE" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + " shudders")
        elif (ability == "FOREWARN"):
            if (stateInBattle == "Entry"):
                maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemon.internalMovesMap:
                    internalMoveName, _, _ = self.opponentPokemon.internalMovesMap.get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleTab.pokemonDB.movesDatabase.get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Forewarn reveals " + self.opponentPokemon.name + "\'s strongest move to be " + moveName)
        elif (ability == "TRACE"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.internalAbility != "FORECAST" and self.opponentPokemon.internalAbility != "FLOWERGIFT" and self.opponentPokemon.internalAbility != "MULTITYPE" and self.opponentPokemon.internalAbility != "ILLUSION" and self.opponentPokemon.internalAbility != "ZENMODE"):
                    self.currPokemon.internalAbility = self.opponentPokemon.internalAbility
                    _, fullName, _ = self.battleTab.pokemonDB.abilitiesDatabase.get(self.opponentPokemon.internalAbility)
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Trace caused it to change ability to " + fullName)
                    abilityChanged = True
        elif (ability == "IMPOSTER"):
            if (stateInBattle == "Entry"):
                temporaryEffectsMap = self.opponentPokemon.temporaryEffects.seek()
                ignoreFlag = True
                if (temporaryEffectsMap.get("illusion") != None):
                    metadata = temporaryEffectsMap.get("illusion")
                    if (metadata[1] == True):
                        ignoreFlag = False
                elif (temporaryEffectsMap.get("substitute") != None):
                    metadata = temporaryEffectsMap.get("substitute")
                    if (metadata[1] == True):
                        ignoreFlag = False
                if (ignoreFlag == True):
                    pass#self.currPokemon.setBattleStats(copy.deepcopy(self.opponentPokemon.deep))
        elif (ability == "ILLUSION"):
            pass
        elif (ability == "REGENERATOR"):
            pass
        elif (ability == "NATURALCURE"):
            pass
        elif (ability == "SPEEDBOOST"):
            if (stateInBattle == "End of Turn"):
                if (self.currPokemon.turnsPlayed > 0 and self.currPokemon.statsStages[5] != 6):
                    self.currPokemon.setStatStage(5, self.currPokemon.statsStages[5] + 1)
                    self.currPokemon.setBattleStat(5, int(self.currPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + " \'s Speed Boost increased its speed")
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
                            self.currPokemon.accuracyStage -= 1
                            self.currPokemon.accuracy = int(self.currPokemon.accuracy * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage-1])
                        elif (randomDec == 7):
                            self.currPokemon.evasionStage -= 1
                            self.currPokemon.evasion = int(self.currPokemon.evasion * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage - 1])
                        else:
                            self.currPokemon.setStatStage(randomDec, self.currPokemon.statsStages[randomDec] - 1)
                            self.currPokemon.setBattleStat(randomDec, int(self.currPokemon.battleStats[randomDec] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1]))
                        self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moody decreased its " + statsNames[randomDec])
                    elif (arrStats == ["Health", -6,-6,-6,-6,-6,-6,-6]):
                        repeatFlag = False
                        if (randomInc == 6):
                            self.currPokemon.accuracyStage += 2
                            self.currPokemon.accuracy = int(self.currPokemon.accuracy * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage+2])
                        elif (randomInc == 7):
                            self.currPokemon.evasionStage += 2
                            self.currPokemon.evasion = int(self.currPokemon.evasion * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage + 2])
                        else:
                            self.currPokemon.setStatStage(randomInc, self.currPokemon.statsStages[randomInc] + 2)
                            self.currPokemon.setBattleStat(randomInc, int(self.currPokemon.battleStats[randomInc] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2]))
                        self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moody sharply raised its " + statsNames[randomInc])
                    elif (arrStats[randomInc] != 6 and arrStats[randomDec] == -6):
                        repeatFlag = False
                        if (arrStats[randomInc] == 5):
                            incNum = 1
                            self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moody raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        else:
                            incNum = 2
                            self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moody sharply raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        if (randomInc == 6):
                            self.currPokemon.accuracyStage += incNum
                            self.currPokemon.accuracy = int(self.currPokemon.accuracy * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage + incNum])
                        elif (randomInc == 7):
                            self.currPokemon.evasionStage += incNum
                            self.currPokemon.evasion = int(self.currPokemon.evasion * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage + incNum])
                        else:
                            self.currPokemon.setStatStage(randomInc, randomIncself.currPokemon.statsStages[randomInc] + incNum)
                            self.currPokemon.setBattleStat(randomInc, int(self.currPokemon.battleStats[randomInc] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + incNum]))
                        if (randomDec == 6):
                            self.currPokemon.accuracyStage -= 1
                            self.currPokemon.accuracy = int(self.currPokemon.accuracy * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage-1])
                        elif (randomDec == 7):
                            self.currPokemon.evasionStage -= 1
                            self.currPokemon.evasion = int(self.currPokemon.evasion * self.battleTab.accuracy_evasionMultipliers[self.battleTab.accuracy_evasionStage - 1])
                        else:
                            self.currPokemon.setStatStage(randomDec, self.currPokemon.statsStages[randomDec] - 1)
                            self.currPokemon.setBattleStat(randomDec, int(self.currPokemon.battleStats[randomDec] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1]))
        elif (ability == "SHEDSKIN"):
            if (stateInBattle == "End of Turn"):
                randNum = random.randint(1,100)
                if (self.currPokemon.battleStats.nonVolatileIndex != 0 and randNum <= 30):
                    self.currPokemon.battleStats.nonVolatileIndex = 0
                    self.battleTab.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Shed Skin cured its status condition")
        elif (ability == "HEALER"):
            # Useful in double and triple battles
            pass
        elif (ability == "BADDREAMS"):
            if (stateInBattle == "End of Turn"):
                if (self.opponentPokemon.internalAbility != "HYDRATION"):
                    damage = int(self.opponentPokemon.finalStats[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + " \'s Bad Dreams hurt " + self.opponentPokemon.name)
        elif (ability == "HYDRATION"):
            if (stateInBattle == "End of Turn"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Raining"):
                    self.currPokemon.battleStats.nonVolatileIndex = 0
                    self.battleTab.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Hydration cured its status condition")
        elif (ability == "DRYSKIN"):
            if (stateInBattle == "Move Effect Opponent"):    # Delete
                if (self.currPlayerAction.typeMove == "FIRE" and self.currPlayerAction.damageCategory != "Status"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.25))
                    #self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemon)
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.typeMove == "WATER"):
                    self.currPlayerAction.setEffectiveness(0)
                    healAmt = int(0.25 * self.opponentPokemon.finalStats[0])
                    if (healAmt + self.opponentPokemon.battleStats[0] > self.opponentPokemon.finalStats[0]):
                        self.currPlayerAction.setHealAmount(self.opponentPokemon.finalStats[0] - self.opponentPokemon.battleStats[0])
                    else:
                        self.currPlayerAction.setHealAmount(healAmt)
                    self.battleTab.showHealHealthAnimation(self.opponentPokemon, healAmt, self.opponentPlayerWidgets[2])
                    self.message = self.opponentPokemon.name + "\'s Dry Skin absorbed the move and restored some HP"
                    self.executeFlag = False
            elif (stateInBattle == "End of Turn"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny"):
                    damage = int(self.currPokemon.finalStats[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Dry Skin hurt it because of the Weather")
                elif (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Raining"):
                    healAmt = int(self.currPokemon.finalStats[0] * 1/8)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Dry Skin gained some HP due to the Weather")
        elif (ability == "RAINDISH"):
            if (stateInBattle == "End of Turn"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Raining"):
                    healAmt = int(self.currPokemon.finalStats[0] * 1/16)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Rain DIsh gained it some HP")
        elif (ability == "ICEBODY"):
            if (stateInBattle == "End of Turn"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Hail"):
                    healAmt = int(self.currPokemon.finalStats[0] *1/16)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Ice Body gained it some HP")
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
                if (self.currPlayerAction.criticalHit == True and self.opponentPokemon.battleStats[0] - self.currPlayerAction.currDamage > 0):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.finalStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 6]))
                    self.opponentPokemon.setStatStage(1, 6)
                    self.messaage = self.opponentPokemon.name + "\'s Anger Point maximized its Attack"
        elif (ability == "DEFIANT"):
            if (stateInBattle == "Move Execution Opponent"):
                statsLowered = 0
                statsChangesTuple = self.currPlayerAction.opponentTemp.statsChangesTuple
                for i in range(1, 6):
                    if (statsChangesTuple[i][0] < 0 and statsChangesTuple[i][1] == "opponent"):
                        statsLowered += 1
                stageIncrease = statsLowered * 2
                if (opponentPokemon.statsStages[1] + stageIncrease > 6):
                    self.opponentPokemon.setStatStage(1, 6)
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.finalStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 6]))
                else:
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1] + stageIncrease)
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.finalStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + self.opponentPokemon.statsStages[1]]))
                self.message = self.opponentPokemon.name + "\'s Defiant raised its Attack"
        elif (ability == "STEADFAST"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.flinch == True):
                    if (self.opponentPokemon.statsStages[5] != 6):
                        self.opponentPokemon.setStatStage(5, self.opponentPokemon.statsStages[5] + 1)
                        self.opponentPokemon.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                        self.message = self.opponentPokemon.name + "\'s Steadfast raised its Speed"
        elif (ability == "WEAKARMOR"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    defLowered = False
                    speedIncreased = False
                    if (self.opponentPokemon.statsStages[2] != -6):
                        self.opponentPokemon.setStatStage(2, self.opponentPokemon.statsStages[2] - 1)
                        self.opponentPokemon.setBattleStat(2, int(self.opponentPokemon.battleStats[2] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1]))
                        defLowered = True
                    if (self.opponentPokemon.statsStages[5] != 6):
                        self.opponentPokemon.setStatStage(5, self.opponentPokemon.statsStages[5] + 1)
                        self.opponentPokemon.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                        speedIncreased = True
                    if (defLowered and speedIncreased):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor lowered its Defense but increased its Speed"
                    elif (defLowered):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor lowered its Defense"
                    elif (speedIncreased):
                        self.message = self.opponentPokemon.name + "\'s Weak Armor increased its Speed"
        elif (ability == "JUSTIFIED"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.typeMove == "DARK" and self.currPlayerAction.damageCategory != "Status" and self.opponentPokemon.statsStages[1] != 6):
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1] + 1)
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.message = self.opponentPokemon.name + "\'s Justified raised its Attack"
        elif (ability == "RATTLED"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.typeMove in ["DARK", "BUG", "GHOST"] and self.currPlayerAction.damageCategory != "Status" and self.opponentPokemon.statsStages[5] != 6):
                    self.opponentPokemon.setStatStage(5, self.opponentPokemon.statsStages[5] + 1)
                    self.opponentPokemon.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.message = self.opponentPokemon.name + "\'s Rattled increased its Attack"
        elif (ability == "MOXIE"):
            if (stateInBattle == "Move Execution Attacker"):
                if (opponentPokemon.battleStats[0] - action.currDamage == 0):
                    self.currPokemon.setBattleStat(1, int(self.currPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPokemon.setStatStage(1, self.currPokemon.statsStages[1] + 1)
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Moxie raised its Attack")
        elif (ability == "CURSEDBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory != "Status"):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        # TODO: Change this
                        self.currPokemon.effects.addMovesBlocked(self.currPlayerAction.internalMove, 4)
                        self.message = self.opponentPokemon.name + "\'s Cursed Body blocked " + self.currPlayerAction.internalMove
        elif (ability == "CUTECHARM"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemon.gender != "Genderless" and self.opponentPokemon.gender != "Genderless" and self.currPokemon.gender != self.opponentPokemon.gender):
                    randNum = random.randint(1,100)
                    if (randNum <= 30 and 9 not in self.currPokemon.volatileConditionIndices):
                        self.currPokemon.volatileConditionIndices.append(9)
                        self.message = self.currPokemon.name + " became infatuated"
        elif (ability == "POISONPOINT"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPlayerAction.nonVolatileConditionIndex == 0):
                    if (randNum <= 30):
                        self.currPokemon.setNonVolatileConditionIndex(1)
                        self.message = self.opponentPokemon.name + "\'s Poison Point poisoned " + self.currPokemon.name
        elif (ability == "STATIC"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemon.nonVolatileConditionIndex == 0):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPokemon.setNonVolatileConditionIndex(3)
                        self.message = self.opponentPokemon.name + "\'s Static paralyzed " + self.currPokemon.name
        elif (ability == "EFFECTSPORE"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemon.nonVolatileConditionIndex == 0):
                    randNum = random.randint(1,100)
                    randNum2 = random.randint(1,100)
                    if (randNum <= 30):
                        randNum2 = random.randint(1, 30)
                        if (randNum2 <= 9):
                            self.currPokemon.setNonVolatileConditionIndex(1)
                            self.message = self.opponentPokemon.name + "\'s Effect Spore poisoned " + self.currPokemon.name
                        elif (randNum2 <= 19):
                            self.currPokemon.setNonVolatileConditionIndex(3)
                            self.message = self.opponentPokemon.name + "\'s Effect Spore paralyzed " + self.currPokemon.name
                        else:
                            self.currPokemon.setNonVolatileConditionIndex(4)
                            self.message = self.opponentPokemon.name + "\'s Effect spore made " + self.currPokemon.name + " fall asleep"
        elif (ability == "FLAMEBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemon.nonVolatileConditionIndex == 0):
                    if (randNum <= 30):
                        self.currPokemon.setNonVolatileConditionIndex(6)
                        self.message = self.opponentPokemon.name + "\'s Flame Body burned " + self.currPokemon.name
        elif (ability == "ROUGHSKIN"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    damage = int(self.currPokemon.battleStats[0] - (self.currPokemon.finalStats[0] / 16))
                    if (self.currPokemon.battleStats[0] - damage < 0):
                        self.currPokemon.setBattleStat(0,  0)
                        self.currPokemon.setIsFainted(True)
                        self.message = self.opponentPokemon.name + "\'s Rough Skin hurt " + self.currPokemon.name + "\n" + self.currPokemon.name + " fainted"
                    else:
                        self.currPokemon.setBattleStat(0, self.currPokemon.battleStats[0] - damage)
                        self.message = self.opponentPokemon.name + "\'s Rough Skin hurt " + self.currPokemon.name
        elif (ability == "IRONBARBS"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    damage = int(self.currPokemon.battleStats[0] - (self.currPokemon.finalStats[0] / 8))
                    if (self.currPokemon.battleStats[0] - damage < 0):
                        self.currPokemon.setBattleStat(0, 0)
                        self.currPokemon.setIsFainted(True)
                        self.message = self.opponentPokemon.name + "\'s Iron Barbs hurt " + self.currPokemon.name + "\n" + self.currPokemon.name + " fainted"
                    else:
                        self.currPokemon.setBattleStat(0, self.currPokemon.battleStats[0] - damage)
                        self.message = self.opponentPokemon.name + "\'s Iron Barbs hurt " + self.currPokemon.name
        elif (ability == "PICKPOCKET"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.opponentPokemon.internalItem == None and self.opponentPokemon.battleStats[0] - self.currPlayerAction.currDamage > 0):
                    # TODO: Must check at very end of determineMoveDetails function. (Move will not work if pokemon dies)
                    self.opponentPokemon.internalItem = self.currPokemon.internalItem
                    self.currPokemon.internalItem = None
                    self.message = self.opponentPokemon.name + "\'s Pickpocket stole " + self.opponentPokemon.internalItem + " from " + self.currPokemon.name
        elif (ability == "MUMMY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.action.damageCategory == "Physical" and self.currPokemon.internalAbility != "MUMMY"):
                    self.currPokemon.internalAbility = "MUMMY"
                    self.message = self.opponentPokemon.name + "\'s Mummy chaanged " + self.currPokemon.name + "\'s ability to be Mummy as well"
        elif (ability == "STENCH"):
            if (stateInBattle == "Move Execution Attacker"):
                if (self.currPokemon.internalAbility == "STENCH"):
                    randNum = random.randint(0, 100)
                    if (randNum <= 10):
                        self.currPlayerAction.setFlinchValid()
        elif (ability == "POISONTOUCH"):
            if (stateInBattle == "Move Execution Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleTab.pokemonDB.movesDatabase.get(self.currPlayerAction.internalMove)
                if ("a" in flag):
                    randNum = random.randint(0, 100)
                    if (randNum <= 30 and self.currPlayerAction.nonVolatileCondition == None and self.opponentPokemon.nonVolatileConditionIndex == None):
                        self.currPlayerAction.setNonVolatileCondition(1)
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
                if (self.currPlayerAction.damageCategory == "Special" and self.currPokemonTemp.currStatusCondition == 6):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "GUTS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStatusCondition == 6 and self.currPokemonTemp.currStatsStages[1] != 6 and self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
        elif (ability == "MARVELSCALE"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.opponentPokemonTemp.currStatusCondtion != 0 and self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.targetDefenseStat * 1.5))
        elif (ability == "QUICKFEET"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.statsStages[5] != 6):
                    self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index+1])
        elif (ability == "TOXICBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if ((self.currPokemonTemp.currStatusCondition == 1 or self.currPokemonTemp.currStatusCondition == 2) and self.currPokemonTemp.currStatsStages[1] != 6):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
        elif (ability == "TANGLEDFEET"):
            if (stateInBattle == "Move Effect Opponent"):
                if (8 in self.opponentPokemonTemp.currTempConditions):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 0.5))
        elif (ability == "HUSTLE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    if (self.currPokemonTemp.currStatsStages[1] != 6):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPokemonTemp.currStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 0.8))
        elif (ability == "PUREPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                    if (currPokemon.currStatsStages[1] < 5):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2]))
                    else:
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
        elif (ability == "HUGEPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.damageCategory == "Physical" and self.currPokemonTemp.currStatsStages[1] != 6):
                    if (currPokemon.currStatsStages[1] < 5):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2]))
                    else:
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
        elif (ability == "COMPOUNDEYES"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 1.3))
        elif (ability == "UNBURDEN"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.internalItem == None and self.currPokemon.wasHoldingItem == True and self.currPokemon.statsStages[5] < 6):
                    if (self.currPokemon.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1])
        elif (ability == "SLOWSTART"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.turnsPlayed < 5 and self.currPokemon.statsStages[5] != -6):
                    self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1])
            elif (stateInBattle == "Move Effect Attacker"):
                action.setTargetAttackStat(int(action.targetAttackStat * 0.5))
        elif (ability == "DEFEATIST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 2)):
                    action.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * 0.5))
        elif (ability == "VICTORYSTAR"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 1.1))
        elif (ability == "PLUS"):
            pass
        elif (ability == "MINUS"):
            pass
        elif (ability == "CHLOROPHYLL"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny" and self.opponentPokemon.internalAbility != "AIRLOCK" and self.opponentPokemon.internalAbility != "CLOUDNINE" and self.currPokemon.statsStages[5] < 6):
                    if (self.currPokemon.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1])
        elif (ability == "SWIFTSWIM"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Rain" and self.opponentPokemon.internalAbility != "AIRLOCK" and self.opponentPokemon.internalAbility != "CLOUDNINE" and self.currPokemon.statsStages[5] < 6):
                    if (self.currPokemon.statsStages[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1])
        elif (ability == "SANDRUSH"):
            if (stateInBattle == "End of Turn"):
                # Just needs checking if it gets hurt in sandstorm which is already checked in another area of code
                pass
        elif (ability == "SOLARPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.damageCategory == "Special"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * 1.5))
            elif (stateInBattle == "End of Turn"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.damageCategory == "Special"):
                    damage = int(self.currPokemon.finalStats[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "\'s Solar Power reduced some of its HP")
        elif (ability == "SANDVEIL"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "SNOWCLOAK"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Hail"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.currMoveAccuracy * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "FLOWERGIFT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny" and self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.targetAttackStat * 1.5))
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.damageCategory == "Special" and self.opponentPokemonTemp.currStatsStages[4] != 6 and self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sunny"):
                    self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.setTargetDefenseStat * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
        elif (ability == "BLAZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.damageCategory != "Status" and self.currPlayerAction.typeMove == "FIRE"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "OVERGROW"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.damageCategory != "Status" and self.currPlayerAction.typeMove == "GRASS"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "TORRENT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.damageCategory != "Status" and self.currPlayerAction.typeMove == "WATER"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "SWARM"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.currStats[0] <= int(self.currPokemon.finalStats[0] / 3) and self.currPlayerAction.damageCategory != "Status" and self.currPlayerAction.typeMove == "BUG"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "SANDFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if ((self.currPlayerAction.typeMove == "ROCK" or self.currPlayerAction.typeMove == "GROUND" or self.currPlayerAction.typeMove == "STEEL") and self.currPlayerAction.damageCategory != "Status" and self.battleTab.battleFieldObject.weatherEffect != None and self.battleTab.battleFieldObject.weatherEffect[0] == "Sandstorm"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.3))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already handled
                pass
        elif (ability == "IRONFIST"):
            if (stateInBattle == "Move Effect Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleTab.pokemonDB.movesDatabase.get(self.currPlayerAction.internalMove)
                if ("j" in flag):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.2))
        elif (ability == "RECKLESS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.functionCode == "0FA" or self.currPlayerAction.functionCode == "0FB" or self.currPlayerAction.functionCode == "0FC" or self.currPlayerAction.functionCode == "0FD" or self.currPlayerAction.functionCode == "0FE" or self.currPlayerAction.internalMove == "JUMPKICK" or self.currPlayerAction.internalMove == "HIGHJUMPKICK"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.2))
        elif (ability == "RIVALRY"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemon.gender != "Genderless" and self.opponentPokemon.gender != "Genderless"):
                    if (self.currPokemon.gender == self.opponentPokemon.gender):
                        self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.25))
                    else:
                        self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 0.75))
        elif (ability == "SHEERFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.currAddEffect != 0):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.3))
                    self.currPlayerAction.setAddEffect(0)
        elif (ability == "TECHNICIAN"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.currPower <= 60):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.5))
        elif (ability == "TINTEDLENS"):
            if (stateInBattle == "Move Effect Attacker"):
                pokemonPokedex = self.battleTab.pokemonDB.pokedex.get(self.opponentPokemon.pokedexEntry)
                if (self.battleTab.checkTypeEffectivenessExists(self.currPlayerAction.typeMove, pokemonPokedex.resistances) == True):
                    self.currPlayerActionaction.setMovePower(int(self.currPlayerAction.currPower * 2))
        elif (ability == "SNIPER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.criticalHit == True):
                    pass # Handled in Critical Hit Determine Function
        elif (ability == "ANALYTIC"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.isFirst == False):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 1.3))
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
                if (self.currPlayerAction.internalMove == "REST"):
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
                _, moveName, _, _, _, _, _, _, _, _, _, _, flag = self.battleTab.pokemonDB.movesDatabase.get(self.currPlayerAction.internalMove)
                if (self.opponentPokemonTemp.currInternalAbility == "SOUNDPROOF" and "k" in flag):
                    self.currPlayerAction.setInvalid()
                    #action.setBattleMessage(opponentPokemon.name + " is immune to the move")
        elif (ability == "BATTLEARMOR"):
            pass
        elif (ability == "SHELLARMOR"):
            pass
        elif (ability == "ROCKHEAD"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setRecoil(0)
        elif (ability == "TELEPATHY"):
            pass
        elif (ability == "STURDY"):
            pass
        elif (ability == "WONDERGUARD"):
            pass
        elif (ability == "HEATPROOF"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.typeMove == "FIRE"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 0.5))
            elif (stateInBattle == "End of Turn"):
                # Just needs to half burn damage which is already handled
                pass
        elif (ability == "THICKFAT"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.typeMove in ["FIRE", "ICE"]):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.currPower * 0.5))
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
                if (self.currPlayerAction.functionCode in ["0DC", "0DD", "0DE"]):
                    self.currPlayerAction.setRecoil(self.currPlayerAction.healAmount)
                    self.currPlayerAction.setHealAmount(0)
        elif (ability == "AIRLOCK"):
            if (stateInBattle == "Entry Effect"):
                self.battleTab.battleFieldObject.setWeatherInEffect(False)
            elif (stateInBattle == "Switched Out"):
                self.battleTab.battleFieldObject.setWeatherInEffect(True)
            elif (stateInBattle == "End of Turn"):
                # Handled already elsewhere
                pass
        elif (ability == "CLOUDNINE"):
            if (stateInBattle == "Entry Effect"):
                self.battleTab.battleFieldObject.setWeatherInEffect(False)
            elif (stateInBattle == "Switched Out"):
                self.battleTab.battleFieldObject.setWeatherInEffect(True)
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
                if (self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetDefenseStat(self.opponentPokemon.finalStats[2])
                elif (self.currPlayerAction.damageCategory == "Special"):
                    self.currPlayerAction.setTargetDefenseStat(self.opponentPokemon.finalStats[4])
                self.opponentPokemonTemp.currEvasion = 100
                self.opponentPokemonTemp.currEvasionStage = 0
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(self.currPokemon.finalStats[1])
                elif (self.currPlayerAction.damageCategory == "Special"):
                    self.currPlayerAction.setTargetAttackStat(self.currPokemon.finalStats[3])
                self.currPokemonTemp.currAccuracy = 100
                self.currPokemonTemp.currAccuracyStage = 0
        elif (ability == "CONTRARY"):
            pass
        elif (ability == "SCRAPPY"):
            pass
        elif (ability == "SERENEGRACE"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setAddEffect(self.currPlayerAction.currAddEffect * 2)
        elif (ability == "SHIELDDUST"):
            if (stateInBattle == "Move Effect Opponent"):
                self.currPlayerAction.setAddEffect(0)
        elif (ability == "SKILLINK"):
            pass
        elif (ability == "SUPERLUCK"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setCriticalHitStage(self.currPlayerAction.criticalHitStage + 1)
        elif (ability == "DAMP"):
            pass
        elif (ability == "ADAPTABILITY"):
            pass
        elif (ability == "NOGUARD"):
            pass
        elif (ability == "NORMALIZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.internalMove not in ["HIDDENPOWER", "WEATHERBALL", "NATURALGIFT", "JUDGEMENT"]):
                    self.currPlayerAction.setTypeMove("NORMAL")
        elif (ability == "WONDERSKIN"):
            pass
        elif (ability == "INFILTRATOR"):
            pass
        elif (ability == "PRANKSTER"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                movesSetMap = self.currPokemon.internalMovesMap
                internalMoveName, _, _ = movesSetMap.get(moveTuple[1] + 1)
                _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.battleTab.pokemonDB.movesDatabase.get(internalMoveName)
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