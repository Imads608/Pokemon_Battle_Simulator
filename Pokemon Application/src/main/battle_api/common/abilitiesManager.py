from PyQt5 import QtCore, QtGui, QtWidgets
from move import *
import random
import math
import copy
import sys

class AbilitiesManager(object):
    def __init__(self, pokemonMetadata, typeBattle, battleProperties):

        self.pokemonMetadata = pokemonMetadata
        self.typeBattle = typeBattle
        self.battleProperties = battleProperties

        # Current Pokemon and Opponent Pokemon Variables
        self.pokemonBattler = None
        self.opponentPokemonBattler = None
        self.pokemonBattlerTempProperties = None
        self.opponentPokemonBattlerTempProperties = None


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
        if (stateInBattle == "Move Effect Opponent" and self.currPokemonTemp.getCurrentInternalAbility() in ["MOLDBREAKER", "TERAVOLT", "TURBOBLAZE"]):
            return

        if (ability == "DOWNLOAD"):
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.getBattleStats()[2] < self.opponentPokemon.getBattleStats()[4]):
                    self.currPokemon.setBattleStat(1, int(self.currPokemon.getBattleStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.currPokemon.setStatStage(1, self.currPokemon.getStatsStages()[1]+1)
                    self.battleTab.getBattleUI().updateBattleInfo(currPokemon.getName() + "\'s Download raised its Attack")
                else:
                    self.currPokemon.setBattleStat(3, int(self.currPokemon.getBattleStats()[3] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.currPokemon.setStatStage(3, self.currPokemon.getStatsStages()[3]+1)
                    self.battleTab.getBattleUI().updateBattleInfo(currPokemon.getName() + "\'s Download raised its Special Attack")
        elif (ability == "INTIMIDATE"):
            if (stateInBattle == "Entry"):
                effectsMap = self.currPokemon.getTemporaryEffects().seek()
                if (effectsMap.get("substitute") != None and effectsMap.get("substitute")[1] == True):
                    self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + "'s Substitute prevented Intimidate from activating")
                if (self.opponentPokemon.getInternalAbility() == "CONTRARY" and self.opponentPokemon.getStatsStages()[1] != 6):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.getBattleStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.getStatsStages()[1]+1)
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Intimidate increased " + self.opponentPokemon.getName() + "\'s Attack")
                elif (self.opponentPokemon.getInternalAbility() == "SIMPLE" and self.opponentPokemon.getStatsStages()[1] > -5):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.getBattleStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() - 2]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.getStatsStages()[1] - 2)
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Intimidate sharply decreased " + self.opponentPokemon.getName() + "\'s Attack")
                elif (self.opponentPokemon.getInternalAbility() in ["CLEARBODY", "HYPERCUTTER", "WHITESMOKE"]):
                    self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + "\'s " + self.opponentPokemon.getInternalAbility() + " prevented " + self.currPokemon.getName() + "\'s Intimiade from activating.")
                elif (self.opponentPokemon.getStatsStages()[1] != -6):
                    self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.getBattleStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.stage0Index - 1]))
                    self.opponentPokemon.setStatStage(1, self.opponentPokemon.getStatsStages()[1] - 1)
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Intimidate decreased " + self.opponentPokemon.getName() + "\'s Attack")
        elif (ability == "DRIZZLE"):
            if (stateInBattle == "Entry"):
                self.battleTab.getBattleField().setWeatherEffect("Rain", sys.maxsize)
                self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + "\'s Drizzle made it Rain")
        elif (ability == "DROUGHT"):
            if (stateInBattle == "Entry"):
                self.battleTab.getBattleField().setWeatherEffect("Sunny", sys.maxsize)
                self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + "\'s Drought made it Sunny")
        elif (ability == "SANDSTREAM"):
            if (stateInBattle == "Entry"):
                self.battleTab.getBattleField().setWeatherEffect("Sandstorm", sys.maxsize)
                self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Sand Stream brewed a Sandstorm")
        elif (ability == "SNOWWARNING"):
            if (stateInBattle == "Entry"):
                self.battleTab.getBattleField().setWeatherEffect("Hail", sys.maxsize)
                self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + "\'s Snow Warning made it Hail")
        elif (ability == "FRISK"):
            if (stateInBattle == "Entry"):
                self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Frisk showed " + self.opponentPokemon.getName() + "\'s held item\n")
                tupleData = self.battleTab.getPokemonDB().getItemsDB().get(self.opponentPokemon.getInternalItem())
                if (tupleData == None):
                    self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + " is not holding an item")
                else:
                    fullName, _, _, _, _ = tupleData
                    self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemon.getName() + " is holding " + fullName)
        elif (ability == "ANTICIPATION"):
            if (stateInBattle == "Entry"):
                pokemonPokedex = self.battleTab.getPokemonDB().getPokedex().get(self.currPokemon.pokedexEntry)
                for moveIndex in self.opponentPokemon.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemon.getInternalMovesMap().get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleTab.getPokemonDB().getMovesDB().get(internalMoveName)
                    if (self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " shudders")
                    elif ((internalMoveName == "FISSURE" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleTab.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " shudders")
        elif (ability == "FOREWARN"):
            if (stateInBattle == "Entry"):
                maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemon.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemon.getInternalMovesMap().get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.battleTab.getPokemonDB().getMovesDB().get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Forewarn reveals " + self.opponentPokemon.getName() + "\'s strongest move to be " + moveName)
        elif (ability == "TRACE"):  #TODO: Skill swap move functionality
            if (stateInBattle == "Entry"):
                if (self.opponentPokemon.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
                    self.currPokemon.setInternalAbility(self.opponentPokemon.getInternalAbility())
                    _, fullName, _ = self.battleTab.getPokemonDB().getAbilitiesDB().get(self.opponentPokemon.getInternalName())
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Trace caused it to change ability to " + fullName)
                    abilityChanged = True
                self.currPokemon.getTemporaryEffects().enQueue("ability changed", [True, True, {"Trace Activated": True}], -1)

        elif (ability == "IMPOSTER"):
            if (stateInBattle == "Entry"):
                temporaryEffectsMap = self.opponentPokemon.getTemporaryEffects().seek()
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
                    self.currPokemon.getTemporaryEffects().enQueue("disguise", [True, True, {"illusion": [True, copy.deepcopy(self.currPokemon)]}])
                    battleStats = copy.deepcopy(self.opponentPokemon.getBattleStats())
                    battleStats[0] = self.currPokemon.getBattleStats()[0]
                    types = copy.deepcopy(self.opponentPokemon.getTypes())
                    internalMovesMap = copy.deepcopy(self.opponentPokemon.getInternalMovesMap())
                    for moveIndex in internalMovesMap.keys():
                        tupleMetadata = internalMovesMap.get(moveIndex)
                        newTupleMetadata = (tupleMetadata[0], tupleMetadata[1], 5)
                        internalMovesMap.update({moveIndex: newTupleMetadata})
                    self.currPokemon.setBattleStats(self.opponentPokemon.getBattleStats())
                    self.currPokemon.setImage(self.opponentPokemon.getImage())
                    self.currPokemon.setInternalMovesMap(internalMovesMap)
                    self.currPokemon.setInternalAbility(self.opponentPokemon.getInternalAbility())
                    self.currPokemon.setWeight(self.opponentPokemon.getWeight())
                    self.currPokemon.setTypes(types)
                    self.battleTab.showPokemonBattleInfo(self.currPlayerWidgets, "view")
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " transformed")
        elif (ability == "ILLUSION"):
            if (stateInBattle == "Switched In"):
                #TODO: Implement switching function call for this to work
                currPlayerTeam = self.currPlayerWidgets[6]
                if (currPlayerTeam[len(currPlayerTeam)-1].getName() != self.currPokemon.getName() and currPlayerTeam[len(currPlayerTeam)-1].getIsFainted() == False):
                    self.currPokemon.getTemporaryEffects().enQueue("disguise", [True, True,{"illusion": [True, copy.deepcopy(self.currPokemon)]}])
                    self.currPokemon.setImage(self.opponentPokemon.getImage())
                    self.currPokemon.setGender(self.opponentPokemon.getGender())
                    self.currPokemon.setTypes(self.opponentPokemon.getTypes())
                    self.currPokemon.setName(self.opponentPokemon.getName())
        elif (ability == "REGENERATOR"):
            if (stateInBattle == "Switched Out"):
                self.currPokemon.getBattleStats()[0] += int(self.currPokemon.getBattleStats()[0]*1/3)
                if (self.currPokemon.getBattleStats()[0] > self.currPokemon.getFinalStats()[0]):
                    self.currPokemon.setBattleStat(0, self.currPokemon.finalStats[0])
        elif (ability == "NATURALCURE"):
            if (stateInBattle == "Switched Out"):
                #TODO: Verify that Trace can also activate this when switched out
                temporaryEffectsMap = self.currPokemon.getTemporaryEffects()
                if (temporaryEffectsMap.get("ability supressed") == None and temporaryEffectsMap.get("ability supressed")[1] == True):
                    self.currPokemon.setVolatileStatusConditionIndices([])
                    self.currPokemon.setNonVolatileStatusConditionIndex(0)
        elif (ability == "SPEEDBOOST"):
            #TODO: Also triggers if this pokemon was switched in after prev pokmeon fainted. must implement
            if (stateInBattle == "End of Turn"):
                if (self.currPokemon.getTurnsPlayed() > 0 and self.currPokemon.getStatsStages()[5] != 6):
                    self.currPokemon.setStatStage(5, self.currPokemon.getStatsStages()[5] + 1)
                    self.currPokemon.setBattleStat(5, int(self.currPokemon.getBattleStats()[5] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " \'s Speed Boost increased its speed")
        elif (ability == "MOODY"):
            if (stateInBattle == "End of Turn"):
                arrStats = ["Health", self.currPokemon.getStatsStages()[1], self.currPokemon.getStatsStages()[2], self.currPokemon.getStatsStages()[3], self.currPokemon.getStatsStages()[4], self.currPokemon.getStatsStages()[5], self.currPokemon.getAccuracyStage(), self.currPokemon.getEvasionStage()]
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
                            self.currPokemon.setAccuracyStage(self.currPokemon.getAccuracyStage()-1)
                            self.currPokemon.setAccuracy(int(self.currPokemon.getAccuracy() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index()-1]))
                        elif (randomDec == 7):
                            self.currPokemon.setEvasionStage(self.currPokemon.getEvasionStage()-1)
                            self.currPokemon.setEvasion(int(self.currPokemon.getEvasion() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index() - 1]))
                        else:
                            self.currPokemon.setStatStage(randomDec, self.currPokemon.getStatsStages()[randomDec] - 1)
                            self.currPokemon.setBattleStat(randomDec, int(self.currPokemon.getBattleStats()[randomDec] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() - 1]))
                        self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Moody decreased its " + statsNames[randomDec])
                    elif (arrStats == ["Health", -6,-6,-6,-6,-6,-6,-6]):
                        repeatFlag = False
                        if (randomInc == 6):
                            self.currPokemon.setAccuracyStage(self.currPokemon.getAccuracyStage()+2)
                            self.currPokemon.setAccuracy(int(self.currPokemon.getAccuracy() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index()+2]))
                        elif (randomInc == 7):
                            self.currPokemon.setEvasionStage(self.currPokemon.getEvasionStage()+2)
                            self.currPokemon.setEvasion(int(self.currPokemon.getEvasion() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index()+2]))
                        else:
                            self.currPokemon.setStatStage(randomInc, self.currPokemon.getStatsStages()[randomInc] + 2)
                            self.currPokemon.setBattleStat(randomInc, int(self.currPokemon.getBattleStats()[randomInc] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2]))
                        self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Moody sharply raised its " + statsNames[randomInc])
                    elif (arrStats[randomInc] != 6 and arrStats[randomDec] == -6):
                        repeatFlag = False
                        if (arrStats[randomInc] == 5):
                            incNum = 1
                            self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Moody raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        else:
                            incNum = 2
                            self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Moody sharply raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        if (randomInc == 6):
                            self.currPokemon.setAccuracyStage(self.currPokemon.getAccuracyStage()+incNum)
                            self.currPokemon.setAccuracy(int(self.currPokemon.getAccuracy() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index() + incNum]))
                        elif (randomInc == 7):
                            self.currPokemon.setEvasionStage(self.currPokemon.getEvasionStage() + incNum)
                            self.currPokemon.setEvasion(int(self.currPokemon.getEvasion() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index() + incNum]))
                        else:
                            self.currPokemon.setStatStage(randomInc, self.currPokemon.getStatsStages()[randomInc] + incNum)
                            self.currPokemon.setBattleStat(randomInc, int(self.currPokemon.getBattleStats()[randomInc] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + incNum]))
                        if (randomDec == 6):
                            self.currPokemon.setAccuracyStage(self.currPokemon.getAccuracyStage()-1)
                            self.currPokemon.setAccuracy(int(self.currPokemon.getAccuracy() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index()-1]))
                        elif (randomDec == 7):
                            self.currPokemon.setEvasionStage(self.currPokemon.getEvasionStage()-1)
                            self.currPokemon.setEvasion(int(self.currPokemon.getEvasion() * self.battleTab.getAccuracyEvasionMultipliers()[self.battleTab.getAccuracyEvasionStage0Index()-1]))
                        else:
                            self.currPokemon.setStatStage(randomDec, self.currPokemon.getStatsStages()[randomDec] - 1)
                            self.currPokemon.setBattleStat(randomDec, int(self.currPokemon.getBattleStats()[randomDec] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() - 1]))
        elif (ability == "SHEDSKIN"):
            if (stateInBattle == "End of Turn"): #TODO: Make sure this happens before burn or poison damage takes effect
                randNum = random.randint(1,100)
                if (self.currPokemon.getNonVolatileStatusConditionIndex() != 0 and randNum <= 30):
                    self.currPokemon.setNonVolatileStatusConditionIndex(0)
                    self.battleTab.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Shed Skin cured its status condition")
        elif (ability == "HEALER"):
            # Useful in double and triple battles
            pass
        elif (ability == "BADDREAMS"):
            if (stateInBattle == "End of Turn"): #TODO: Make sure Shed Skin has chance to activate before checking for this
                if (self.opponentPokemon.getInternalAbility() != "HYDRATION"):
                    damage = int(self.opponentPokemon.getFinalStats()[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " \'s Bad Dreams hurt " + self.opponentPokemon.getName())
        elif (ability == "HYDRATION"):
            if (stateInBattle == "End of Turn"): #TODO: Check how Yawn works this case
                if (self.battleTab.getBattleField().getWeather() == "Raining"):
                    self.currPokemon.setNonVolatileStatusConditionIndex(0)
                    self.battleTab.showPokemonStatusCondition(self.currPokemon, self.currPlayerWidgets[7])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Hydration cured its status condition")
        elif (ability == "DRYSKIN"): #TODO: Won't work if pokemon is protected
            if (stateInBattle == "Move Exection Opponent"):
                if (self.currPlayerAction.getTypeMove() == "FIRE" and self.currPlayerAction.getDamageCategory() != "Status"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.25))
                    #self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemon)
                elif (self.currPlayerAction.getTypeMove() == "WATER"):
                    self.currPlayerAction.setEffectiveness(0)
                    healAmt = int(0.25 * self.opponentPokemon.getFinalStats()[0])
                    if (healAmt + self.opponentPokemon.getBattleStats()[0] > self.opponentPokemon.getFinalStats()[0]):
                        self.currPlayerAction.setHealAmount(self.opponentPokemon.getFinalStats()[0] - self.opponentPokemon.getBattleStats()[0])
                    else:
                        self.currPlayerAction.setHealAmount(healAmt)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Dry Skin absorbed the move and restored some HP")
                    #self.battleTab.showHealHealthAnimation(self.opponentPokemon, healAmt, self.opponentPlayerWidgets[2])
                    #self.message = self.opponentPokemon.getName() + "\'s Dry Skin absorbed the move and restored some HP"
                    #self.executeFlag = False
            elif (stateInBattle == "End of Turn"):
                if (self.battleTab.getBattleField().getWeather() == "Sunny"):
                    damage = int(self.currPokemon.getFinalStats()[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Dry Skin hurt it because of the Weather")
                elif (self.battleTab.getBattleField().getWeather() == "Raining"):
                    healAmt = int(self.currPokemon.getFinalStats()[0] * 1/8)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Dry Skin gained some HP due to the Weather")
        elif (ability == "RAINDISH"):
            if (stateInBattle == "End of Turn"):
                if (self.battleTab.getBattleField().getWeather() == "Raining"):
                    healAmt = int(self.currPokemon.getFinalStats()[0] * 1/16)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Rain Dish gained it some HP")
        elif (ability == "ICEBODY"):
            if (stateInBattle == "End of Turn"):
                if (self.battleTab.getBattleField().getWeather() == "Hail"):
                    healAmt = int(self.currPokemon.getFinalStats()[0] *1/16)
                    self.battleTab.showHealHealthAnimation(self.currPokemon, healAmt, self.currPlayerWidgets[2])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Ice Body gained it some HP")
        elif (ability == "PICKUP"): #TODO: Revise this
            #if (stateInBattle == "End of Turn"):
            #    if (self.currPokemon.getInternalItem() == None and self.opponentPokemon.getInternalItem() == None and self.opponentPokemon.getWasHoldingItem() == True):
             #       if (self.opponentPokemon.getName() == self.currPlayerAction.getCurrentOpponent().getName() and self.opponentPokemon.getName() == self.opponentPlayerAction.getCurrentAttacker().getName()):
              #          pass
            if (stateInBattle == "End of Turn"):
                #TODO: Revise and assign player actions for stateInBattle of End of Turn
                tempEffects = self.currPokemon.getTemporaryEffects().seek()
                values = tempEffects.get("ability effect")
                randomNum = rand.randint(0,1)
                if (self.currPokemon.getInternalItem() == None or values[1] == True and self.opponentPokemon.getInternalItem() == None and self.opponentPokemon.wasHoldingItem == True):
                    if (self.opponentPokemon.getInternalAbility() == ability and (self.currPokemon.getBattleStats()[5] < self.opponentPokemon.getBattleStats()[5] or (self.currPokemon.getBattleStats()[5] == self.opponentPokemon.getBattleStats()[5] and randomNum == 0))):
                        return
                    if (isinstance(self.currPlayerAction, Move) and self.currPlayerAction.getInternalMove() in ["Incinerate", "Bug Bite", "Pluck", "Knock Off"]):
                        return
                    if (self.opponentPokemon.getImmutableCopy().getInternalItem() == "Air Balloon"):
                        return
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "'s Pickup picked up" + self.opponentPokemon.getImmutableCopy().getInternalItem())
                    self.currPokemon.setInternalItem(self.opponentPokemon.getImmutableCopy().getInternalItem())
        elif (ability == "HARVEST"):
            if (stateInBattle == "End of Turn"):
                #TODO: Implement Later
                pass
        elif (ability == "ANGERPOINT"): #TODO: Make sure to ignore substitute
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getCriticalHit() == True):
                    self.opponentPokemonTemp.getStatsStagesChangesTuple()[1] = (6 - self.opponentPokemonTemp.getCurrentStatsStages()[1], "opponent")
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Anger Point maximized its Attack")
        elif (ability == "DEFIANT"):
            if (stateInBattle == "Move Execution Opponent"  and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                statsLowered = 0
                statsChangesTuple = self.opponentPokemonTemp.getStatsStagesChangesTuple()
                for i in range(1, 6):
                    if (statsChangesTuple[i][0] < 0 and statsChangesTuple[i][1] == "opponent"):
                        statsLowered += 1
                stageIncrease = statsLowered * 2
                if (stageIncrease + self.opponentPokemonTemp.getCurrentStatsStages()[1] > 6):
                    self.opponentPokemonTemp.getStatsStagesChangesTuple()[1] = (6-self.opponentPokemonTemp.getCurrentStatsStages()[1], "opponent")
                else:
                    self.opponentPokemonTemp.getStatsStagesChangesTuple()[1] = (stageIncrease, "opponent")
                self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Defiant raised its Attack")
        elif (ability == "STEADFAST"):
            if (stateInBattle == "Move Execution Opponent"  and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getFlinch() == True):
                    if (self.opponentPokemonTemp.getCurrentStatsStages()[5] != 6):
                        self.opponentPokemonTemp.getStatsStagesChangesTuple()[5] = (1, "opponent")
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "'s Steadfast raised its speed")
                        #self.opponentPokemonTemp.getCurrentStatsStages()[5] += 1
                        #self.opponentPokemonTemp.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                        #self.message = self.opponentPokemon.name + "\'s Steadfast raised its Speed"
        elif (ability == "WEAKARMOR"):
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    defLowered = False
                    speedIncreased = False
                    if (self.opponentPokemonTemp.getCurrentStatsStages()[2] != -6):
                        self.opponentPokemonTemp.getStatsStagesChangesTuple()[2] = (-1, "opponent")
                        #self.opponentPokemon.setStatStage(2, self.opponentPokemon.statsStages[2] - 1)
                        #self.opponentPokemon.setBattleStat(2, int(self.opponentPokemon.battleStats[2] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index - 1]))
                        defLowered = True
                    if (self.opponentPokemon.statsStages[5] != 6):
                        self.opponentPokemonTemp.getStatsStagesChangesTuple()[5] = (1, "opponent")
                        #self.opponentPokemon.setStatStage(5, self.opponentPokemon.statsStages[5] + 1)
                        #self.opponentPokemon.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                        speedIncreased = True
                    if (defLowered and speedIncreased):
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Weak Armor lowered its Defense but increased its Speed")
                    elif (defLowered):
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Weak Armor lowered its Defense")
                    elif (speedIncreased):
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Weak Armor increased its Speed")
        elif (ability == "JUSTIFIED"):
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getTypeMove() == "DARK" and self.currPlayerAction.getDamageCategory() != "Status" and self.opponentPokemonTemp.getCurrentStatsStages()[1] != 6):
                    self.opponentPokemonTemp.getStatsStagesChangesTuple()[1] = (1, "opponent")
                    #self.opponentPokemon.setStatStage(1, self.opponentPokemon.statsStages[1] + 1)
                    #self.opponentPokemon.setBattleStat(1, int(self.opponentPokemon.battleStats[1] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Justified raised its Attack")
        elif (ability == "RATTLED"):
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getTypeMove() in ["DARK", "BUG", "GHOST"] and self.currPlayerAction.getDamageCategory() != "Status" and self.opponentPokemonTemp.getCurrentStatsStages()[5] != 6):
                    self.opponentPokemonTemp.getStatsStagesChangesTuple()[5] = (1, "opponent")
                    #self.opponentPokemon.setStatStage(5, self.opponentPokemon.statsStages[5] + 1)
                    #self.opponentPokemon.setBattleStat(5, int(self.opponentPokemon.battleStats[5] * self.battleTab.statsStageMultipliers[self.battleTab.stage0Index + 1]))
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Rattled increased its Attack")
        elif (ability == "MOXIE"):
            if (stateInBattle == "Move Execution Attacker"):
                if (self.opponentPokemon.getIsFainted()):
                    self.currPokemon.setBattleStat(1, int(self.currPokemon.getBattleStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.currPokemon.setStatStage(1, self.currPokemon.getStatsStages()[1] + 1)
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Moxie raised its Attack")
        elif (ability == "CURSEDBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() != "Status"):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPokemonTemp.getTemporaryEffects().enQueue("move block", [False, True, {self.currPlayerAction.getInternalMove():True}], 4)
                        #self.currPokemon.effects.addMovesBlocked(self.currPlayerAction.internalMove, 4)
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Cursed Body blocked " + self.currPlayerAction.getInternalMove())
        elif (ability == "CUTECHARM"):
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.currPlayerAction.getDamageCategory() == "Physical" and self.currPokemon.getGender() != "Genderless" and self.opponentPokemon.getGender() != "Genderless" and self.currPokemon.getGender() != self.opponentPokemon.getGender()):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPlayerAction.setVolatileStatusConditionsByOpponent(9)
                        self.currPlayerAction.setInflictStatusConditionsByOpponent(True)
                        #self.currPokemon.volatileConditionIndices.append(9)
                        #self.message = self.currPokemon.name + " became infatuated"
        elif (ability == "POISONPOINT"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    if (randNum <= 30):
                        self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(1)
                        self.currPlayerAction.setInflictStatusConditionsByOpponent(True)
                        #self.currPokemon.setNonVolatileConditionIndex(1)
                        #self.message = self.opponentPokemon.name + "\'s Poison Point poisoned " + self.currPokemon.name
        elif (ability == "STATIC"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    randNum = random.randint(1,100)
                    if (randNum <= 30):
                        self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(3)
                        self.currPlayerAction.setInflictStatusConditionsByOpponent(True)
                        #self.currPokemon.setNonVolatileConditionIndex(3)
                        #self.message = self.opponentPokemon.name + "\'s Static paralyzed " + self.currPokemon.name
        elif (ability == "EFFECTSPORE"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    randNum = random.randint(1,100)
                    randNum2 = random.randint(1,100)
                    if (randNum <= 30):
                        randNum2 = random.randint(1, 30)
                        self.currPlayerAction.setInflictStatusConditionsByOpponent(True)
                        if (randNum2 <= 9):
                            self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(1)
                            #self.currPokemon.setNonVolatileConditionIndex(1)
                            #self.message = self.opponentPokemon.name + "\'s Effect Spore poisoned " + self.currPokemon.name
                        elif (randNum2 <= 19):
                            self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(3)
                            #self.currPokemon.setNonVolatileConditionIndex(3)
                            #self.message = self.opponentPokemon.name + "\'s Effect Spore paralyzed " + self.currPokemon.name
                        else:
                            self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(4)
                            #self.currPokemon.setNonVolatileConditionIndex(4)
                            #self.message = self.opponentPokemon.name + "\'s Effect spore made " + self.currPokemon.name + " fall asleep"
        elif (ability == "FLAMEBODY"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    if (randNum <= 30):
                        self.currPlayerAction.setNonVolatileStatusConditionsByOpponent(6)
                        self.currPlayerAction.setInflictStatusConditionsByOpponent(True)
                        #self.currPokemon.setNonVolatileConditionIndex(6)
                        #self.message = self.opponentPokemon.name + "\'s Flame Body burned " + self.currPokemon.name
        elif (ability == "ROUGHSKIN"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    damage = int(self.currPokemonTemp.getCurrentStats()[0] - (self.currPokemon.getFinalStats()[0] / 16))
                    if (self.currPokemonTemp.getCurrentStats()[0] - damage < 0):
                        self.currPlayerAction.setPhysicalContactDamage(self.currPokemon.getCurrentStats()[0])
                    else:
                        self.currPlayerAction.setPhysicalContactDamage(damage)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Rough Skin hurt " + self.currPokemon.getName())
        elif (ability == "IRONBARBS"):
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    damage = int(self.currPokemonTemp.getCurrentStats()[0] - (self.currPokemon.getFinalStats()[0] / 8))
                    if (self.currPokemonTemp.getCurrentStats()[0] - damage < 0):
                        self.currPlayerAction.setPhysicalContactDamage(self.currPokemon.getCurrentStats()[0])
                    else:
                        self.currPlayerAction.setPhysicalContactDamage(damage)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Iron Barbs hurt " + self.currPokemon.getName())
        elif (ability == "PICKPOCKET"):
            if (stateInBattle == "Move Execution Opponent" and self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemonTemp) < self.opponentPokemonTemp.getCurrentStats()[0]):
                if (self.opponentPokemonTemp.getCurrentInternalItem() == None and self.currPlayerAction.getDamageCategory() == "Physical"):
                    self.opponentPokemonTemp.setCurrentInternalItem(self.currPokemonTemp.getCurrentInternalItem())
                    self.currPokemonTemp.setCurrentInternalItem(None)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Pickpocket stole " + self.opponentPokemon.getInternalItem() + " from " + self.currPokemon.getName())
        elif (ability == "MUMMY"): #TODO: Make sure to set back recoil to positive value
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Physical" and self.currPokemonTemp.getCurrentInternalAbility() not in ["MULTITYPE", "ZENMODE", "MUMMY"]):
                    self.currPokemonTemp.setCurrentInternalAbility("MUMMY")
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Mummy chaanged " + self.currPokemon.getName() + "\'s ability to be Mummy as well")
        elif (ability == "STENCH"):
            if (stateInBattle == "Move Execution Attacker"):
                if (self.currPokemonTemp.getCurrentInternalAbility() == "STENCH" and self.currPlayerAction.getDamageCategory() != "Status"):
                    randNum = random.randint(0, 100)
                    if (randNum <= 10):
                        self.currPlayerAction.setFlinch(True)
        elif (ability == "POISONTOUCH"):
            if (stateInBattle == "Move Execution Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleTab.pokemonDB.movesDatabase.get(self.currPlayerAction.internalMove)
                if ("a" in flag):
                    randNum = random.randint(0, 100)
                    if (randNum <= 30):
                        self.currPlayerAction.inflictStatusConditionsByAttacker(True)
                        self.currPlayerAction.setNonVolatileConditionsByAttacker(1)
        elif (ability == "SYNCHRONIZE"): #TODO: Work on this later
            if (stateInBattle == "Move Execution Attacker"):
                pass
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPokemon.nonVolatileConditionIndex == 0):
                    if (self.opponentPokemon.nonVolatileConditionIndex in [1,2,3,6] and self.currPlayerAction.inflictStatusCondition == True):
                        self.battleTab.battleUI.updateBattleInfo(self.currPokemon.name + "'s Synchronize tried to inflict back")
                        if (self.battleTab.checkStatusConditionAffectPokemon(self.opponentPokemon.nonVolatileConditionIndex, self.currPokemon)):
                            pass
        elif (ability == "AFTERMATH"):
            pass # Done in showMoveExecutionEffects function
        elif (ability == "COLORCHANGE" and self.currPlayerAction.getDamage() < self.opponentPokemonTemp.getCurrentStats()[0]):
            #TODO: Must account for status condition too
            if (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getDamageCategory() != "Status" and self.currPlayerAction.getInternalMove() != "STRUGGLE"):
                    self.opponentPokemonTemp.setCurrentTypes(self.currPokemon.getTypes())
                    self.battleTab.getBattleUI().updateBattleInfo(self.opponentPokemonTemp.getName() + "'s Color Change caused its type to change to " + str(self.currPokemonTemp.getTypes()))
        elif (ability == "FLAREBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getDamageCategory() == "Special" and self.currPokemonTemp.getCurrentStatusCondition() == 6):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "GUTS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStatusCondition() == 6 and self.currPokemonTemp.getCurrentStatsStages()[1] != 6 and self.currPlayerAction.getDamageCategory() == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (ability == "MARVELSCALE"):
            if (stateInBattle == "Move Execution Opponent"): #Move Effect Opponent
                if (self.opponentPokemonTemp.getCurrentStatusCondition() != 0 and self.currPlayerAction.getDamageCategory() == "Physical"):
                    self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.getTargetDefenseStat() * 1.5))
        elif (ability == "QUICKFEET"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.getStatsStages()[5] != 6):
                    self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index()+1])
        elif (ability == "TOXICBOOST"):
            if (stateInBattle == "Move Effect Attacker"):
                if ((self.currPokemonTemp.getCurrentStatusCondition() in [1, 2]) and self.currPokemonTemp.getCurrentStatsStages()[1] != 6):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (ability == "TANGLEDFEET"):
            if (stateInBattle == "Move Execution Opponent"): #Move Effect Opponent
                if (8 in self.opponentPokemonTemp.getCurrentTemporaryConditions()):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 0.5))
        elif (ability == "HUSTLE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getDamageCategory() == "Physical"):
                    if (self.currPokemonTemp.getCurrentStatsStages()[1] != 6):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPokemonTemp.getCurrentStats()[1] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 0.8))
        elif (ability == "PUREPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getDamageCategory() == "Physical" and self.currPokemonTemp.getCurrentStatsStages()[1] != 6):
                    if (self.currPokemonTemp.getCurrentStatsStages()[1] < 5):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2]))
                    else:
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (ability == "HUGEPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getDamageCategory() == "Physical" and self.currPokemonTemp.getCurrentStatsStages()[1] != 6):
                    if (self.currPokemonTemp.getCurrentStatsStages()[1] < 5):
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2]))
                    else:
                        self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (ability == "COMPOUNDEYES"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 1.3))
        elif (ability == "UNBURDEN"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.getInternalItem() == None and self.currPokemon.getWasHoldingItem() == True and self.currPokemon.getStatsStages()[5] < 6):
                    if (self.currPokemon.getStatsStages()[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1])
        elif (ability == "SLOWSTART"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.currPokemon.getTurnsPlayed() < 5 and self.currPokemon.getStatsStages()[5] != -6):
                    self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() - 1])
            elif (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * 0.5))
        elif (ability == "DEFEATIST"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStats()[0] <= int(self.currPokemon.getFinalStats()[0] / 2)):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * 0.5))
        elif (ability == "VICTORYSTAR"):
            if (stateInBattle == "Move Effect Attacker"):
                self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 1.1))
        elif (ability == "PLUS"):
            pass # Not useful in single battles
        elif (ability == "MINUS"):
            pass # Not useful in single battles
        elif (ability == "CHLOROPHYLL"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.battleTab.getBattleField().getWeather() == "Sunny" and self.opponentPokemon.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.currPokemon.getStatsStages()[5] < 6):
                    if (self.currPokemon.getStatsStages()[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1])
        elif (ability == "SWIFTSWIM"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.battleTab.getBattleField().getWeather() == "Rain" and self.opponentPokemon.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.currPokemon.getStatsStages()[5] < 6):
                    if (self.currPokemon.getStatsStages()[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1])
        elif (ability == "SANDRUSH"):
            if (stateInBattle == "Priority" and self.currPlayerMoveTuple[0] != "switch"):
                if (self.battleTab.getBattleField().getWeather() == "Sandstorm" and self.currPokemon.getStatsStages()[5] < 6):
                    if (self.currPokemon.getStatsStages()[5] < 5):
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2])
                    else:
                        self.currSpeed = int(self.currSpeed * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1])
            if (stateInBattle == "End of Turn"):
                # Just needs checking if it gets hurt in sandstorm which is already checked in another area of code
                pass
        elif (ability == "SOLARPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.battleTab.getBattleField().getWeather() == "Sunny" and self.currPlayerAction.getDamageCategory() == "Special"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * 1.5))
            elif (stateInBattle == "End of Turn"):
                if (self.battleTab.getBattleField().getWeather() == "Sunny" and self.currPlayerAction.getDamageCategory() == "Special"):
                    damage = int(self.currPokemon.getFinalStats()[0] * 1/8)
                    self.battleTab.showDamageHealthAnimation(self.currPokemon, damage, self.currPlayerWidgets[2], self.currPlayerWidgets[7])
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "\'s Solar Power reduced some of its HP")
        elif (ability == "SANDVEIL"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.getBattleField().getWeather() == "Sandstorm"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "SNOWCLOAK"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.getBattleField().getWeather() == "Hail"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (ability == "FLOWERGIFT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.battleTab.getBattleField().getWeather() == "Sunny" and self.currPlayerAction.getDamageCategory() == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(int(self.currPlayerAction.getTargetAttackStat() * 1.5))
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Special" and self.opponentPokemonTemp.getCurrentStatsStages()[4] != 6 and self.battleTab.getBattleField().getWeather() == "Sunny"):
                    self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.getTargetDefenseStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (ability == "BLAZE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStats()[0] <= int(self.currPokemon.getFinalStats()[0] / 3) and self.currPlayerAction.getDamageCategory() != "Status" and self.currPlayerAction.getTypeMove() == "FIRE"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "OVERGROW"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStats()[0] <= int(self.currPokemon.getFinalStats()[0] / 3) and self.currPlayerAction.getDamageCategory() != "Status" and self.currPlayerAction.getTypeMove() == "GRASS"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "TORRENT"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStats()[0] <= int(self.currPokemon.getFinalStats()[0] / 3) and self.currPlayerAction.getDamageCategory() != "Status" and self.currPlayerAction.getTypeMove() == "WATER"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "SWARM"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemonTemp.getCurrentStats()[0] <= int(self.currPokemon.getFinalStats()[0] / 3) and self.currPlayerAction.getDamageCategory() != "Status" and self.currPlayerAction.getTypeMove() == "BUG"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "SANDFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if ((self.currPlayerAction.getTypeMove() in ["ROCK", "GROUND", "STEEL"]) and self.currPlayerAction.getDamageCategory() != "Status" and self.battleTab.getBattleField().getWeather() == "Sandstorm"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.3))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already handled
                pass
        elif (ability == "IRONFIST"):
            if (stateInBattle == "Move Effect Attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.battleTab.getPokemonDB().getMovesDB().get(self.currPlayerAction.getInternalMove())
                if ("j" in flag):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.2))
        elif (ability == "RECKLESS"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getFunctionCode() == "0FA" or self.currPlayerAction.getFunctionCode() in ["0FB", "0FC", "0FD", "0FE"] or self.currPlayerAction.getInternalMove() in ["JUMPKICK", "HIGHJUMPKICK"]):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.2))
        elif (ability == "RIVALRY"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPokemon.getGender() != "Genderless" and self.opponentPokemon.getGender() != "Genderless"):
                    if (self.currPokemon.getGender() == self.opponentPokemon.getGender()):
                        self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.25))
                    else:
                        self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 0.75))
        elif (ability == "SHEERFORCE"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getAddEffect() != 0):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.3))
                    self.currPlayerAction.setAddEffect(0)
        elif (ability == "TECHNICIAN"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getMovePower() <= 60):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.5))
        elif (ability == "TINTEDLENS"):
            if (stateInBattle == "Move Effect Attacker"):
                pokemonPokedex = self.battleTab.getPokemonDB().getPokedex().get(self.opponentPokemon.getPokedexEntry())
                if (self.battleTab.checkTypeEffectivenessExists(self.currPlayerAction.getTypeMove(), pokemonPokedex.resistances) == True):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 2))
        elif (ability == "SNIPER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getCriticalHit() == True):
                    pass # Handled in Critical Hit Determine Function
        elif (ability == "ANALYTIC"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getIsFirst() == False):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.3))
        elif (ability == "BIGPECKS"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.opponentPokemonTemp.getCurrentStatsStages()[2] < 0):
                    self.opponentPokemonTemp.getCurrentStatsStages()[2] = 0
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "'s Big Pecks prevented its defense from being lowered")
        elif (ability == "HYPERCUTTER"):
            # Entry Effects already handled in Attacker Pokemon Entry Effects
            if (stateInBattle == "Move Effect Opponent"):
                if (self.opponentPokemonTemp.getStatsStagesChangesTuples()[1][0] < 0 and self.opponentPokemonTemp.getStatsStagesChangesTuples()[1][1] == "opponent"):
                    self.opponentPokemonTemp.getStatsStagesChangesTuples()[1] = (0, None)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "'s Hyper Cutter prevented its attack from being lowered")
                #if (self.currPlayerAction.nonVolatileCondition != 6):
                #     if (self.opponentPokemonTemp.statsStagesChanges[1] < 0):
                #        self.opponentPokemonTemp.statsStagesChanges[1] = 0
                #        self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Hyper Cutter prevented its attack from being lowered")
        elif (ability == "KEENEYE"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.opponentPokemonTemp.getAccuracyEvasionStagesChangesTuples()[0][0] < 0):
                    self.opponentPokemonTemp.getAccuracyEvasionStagesChangesTuples()[0] = (0, None)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "'s Keen Eye prevented its accuracy from being lowered")
        elif (ability == "CLEARBODY"):
            # Entry Effects already handled in Attacker Pokemon Entry Effects
            if (stateInBattle == "Move Effect Opponent"):
                stats = self.opponentPokemonTemp.getStatsStagesChangesTuples().extend(self.opponentPokemonTemp.getAccuracyEvasionStagesChangesTuples())
                loweredFlag = False
                for index, stat in enumerate(stats):
                    if (stat[0][0] < 0):
                        if ((index == 1 and self.currPlayerAction.getNonVolatileStatusConditionByAttacker() == 6) or (index == 5 and self.currPlayerAction.getNonVolatileStatusConditionByAttacker() == 3)):
                            if (stat[0][0] < -1):
                                loweredFlag = True
                            statsIndex[index] = (-1, "opponent")
                        else:
                            loweredFlag = True
                            stats[index] = 0
                self.opponentPokemonTemp.setStatsStagesChangesTuples(stats[0:6])
                self.opponentPokemonTemp.setAccuracyEvasionStagesChangesTuples(stats[6:])
                if (loweredFlag):
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Clear Body prevented its stats from being lowered")
        elif (ability == "WHITESMOKE"):
            if (stateInBattle == "Move Effect Opponent"):
                stats = self.opponentPokemonTemp.getStatsStagesChangesTuples().extend(self.opponentPokemonTemp.getAccuracyEvasionStagesChangesTuples())
                loweredFlag = False
                for index, stat in enumerate(stats):
                    if (stat[0][0] < 0):
                        if ((index == 1 and self.currPlayerAction.getNonVolatileStatusConditionByAttacker() == 6) or (index == 5 and self.currPlayerAction.getNonVolatileStatusConditionByAttacker() == 3)):
                            if (stat[0][0] < -1):
                                loweredFlag = True
                            statsIndex[index] = (-1, "opponent")
                        else:
                            loweredFlag = True
                            stats[index] = 0
                self.opponentPokemonTemp.setStatsStagesChangesTuples(stats[0:6])
                self.opponentPokemonTemp.setAccuracyEvasionStagesChangesTuples(stats[6:])
                if (loweredFlag):
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Clear Body prevented its stats from being lowered")
        elif (ability == "IMMUNITY"):
            if (stateInBattle == "Entry Effect"):
               prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                   if (self.currPokemon.getNonVolatileStatusConditionIndex() in [1, 2]):
                       self.currPokemon.setNonVolatileStatusConditionIndex(None)
                       self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Immunity cured its poison")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() in [1,2]):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Immunity prevented it from being poisoned")
            if (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() in [1,2]):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
        elif (ability == "MAGMAARMOR"):
            if (stateInBattle == "Entry Effect"):
               prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                   if (self.currPokemon.getNonVolatileStatusConditionIndex() == 5):
                       self.currPokemon.setNonVolatileStatusConditionIndex(None)
                       self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Magma Armor unthawed itself")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 5):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Magma Armor prevented it from being frozen")
                elif (stateInBattle == "End of Turn"):
                    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 5):
                        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Magma Armor unthawed itself")
        elif (ability == "LIMBER"):
            if (stateInBattle == "Entry Effect"):
               prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                   if (self.currPokemon.getNonVolatileStatusConditionIndex() == 3):
                       self.currPokemon.setNonVolatileStatusConditionIndex(None)
                       self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Limber cured its paralysis")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 3):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Limber prevented it from being paralyzed")
            elif (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() == 3):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
                    self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Limber cured its paralysis")
        elif (ability == "INSOMNIA"):
            if (stateInBattle == "Entry Effect"):
                prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Insomnia cured its sleep")
            elif (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getInternalMove() == "REST"):
                    self.currPlayerAction.setInvalid(True)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Insomnia prevented it from sleeping")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 4 or self.currPlayerAction.getVolatileStatusConditionByAttacker() == 7):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Insomnia prevented it from sleeping")
            elif (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
                    self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Insomnia cured its sleep")
        elif (ability == "VITALSPIRIT"):
            if (stateInBattle == "Entry Effect"):
                prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Vital Spirit cured its sleep")
            elif (stateInBattle == "Move Effect Attacker"):
                if (self.currPlayerAction.getInternalMove() == "REST"):
                    self.currPlayerAction.setInvalid(True)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Vital Spirit prevented it from sleeping")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 4 or self.currPlayerAction.getVolatileStatusConditionByAttacker() == 7):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Vital Spirit prevented it from sleeping")
            elif (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
                    self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Vital Spirit cured its sleep")
        elif (ability == "WATERVEIL"):
            if (stateInBattle == "Entry Effect"):
                prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
                        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 6):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Water Veil prevented it from burned")
            elif (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
                    self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
        elif (ability == "OWNTEMPO"):
            if (stateInBattle == "Entry Effect"):
                prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
                        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
            elif (stateInBattle == "Move Retaliate"):
                if (self.currPlayerAction.getVolatileStatusConditionByOpponent() == 8):
                    self.currPlayerAction.setVolatileConditionByOpponent(None)
                    self.currPlayerAction.getInflicted
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 6):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Water Veil prevented it from burned")
            elif (stateInBattle == "End of Turn"):
                if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
                    self.currPokemon.setNonVolatileStatusConditionIndex(None)
                    self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
        elif (ability == "OBLIVIOUS"):
            pass
        elif (ability == "INNERFOCUS"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.flinch == True):
                    self.currPlayerAction.setFlinch(False)
        elif (ability == "LEAFGUARD"):
            # TODO: Items trigger this ability
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.battleFieldObject.getWeather() == "Sunny"):
                    if (self.currPlayerAction.nonVolatileCondition in [1,2,3,4,5,6]):
                        self.currPlayerAction.setNonVolatileStatusCondition(None)
                    if (self.currPlayerAction.volatileCondition == 7):
                        self.currPlayerAction.setVolatileStatusCondition(None)
        elif (ability == "FLASHFIRE"):
            # Fire types move powered up handled in determineMoveDetails Function
            if (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.typeMove == "FIRE"):
                    self.currPlayerAction.setEffectiveness(0)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Flash Fire made it immune to Fire type moves")
                    self.currPlayerAction.temporaryEffects.enQueue("type move powered", [True, True,{"Fire":[True, 1.5]}], -1)
        elif (ability == "STORMDRAIN"):
            if (stateInBattle == "Move Effect Opponent"):
                #TODO: Check for opponent in semi-invulnerable state or is protected
                if (self.currPlayerAction.typeMove == "WATER"):
                    self.currPlayerAction.setEffectiveness(0)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain made it immune to Water type moves")
                    if (self.opponentPokemonTemp.currStatsStages[3] != 6):
                        self.opponentPokemonTemp.statsStagesChanges[3] += 1
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain also increased its Special Attack")
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
                self.opponentPokemonTemp.acc_evasStagesChanges[1] = 0
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.damageCategory == "Physical"):
                    self.currPlayerAction.setTargetAttackStat(self.currPokemon.finalStats[1])
                elif (self.currPlayerAction.damageCategory == "Special"):
                    self.currPlayerAction.setTargetAttackStat(self.currPokemon.finalStats[3])
                self.currPokemonTemp.currAccuracy = 100
                self.currPokemonTemp.acc_evasStagesChanges[0] = 0
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
