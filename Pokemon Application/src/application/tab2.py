from PyQt5 import QtCore, QtGui, QtWidgets
import random
import math
import copy
from pokemonBattleMetadata import *

class Tab2(object):
    def __init__(self, battleUI):
        self.battleUI = battleUI
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.listInternalItems = []
        self.chosenMovesetMap = {}
        self.natureEffects = [("None", "None"), ("Def", "Att"), ("SpAtt", "Att"), ("SpDef", "Att"), ("Spd", "Att"),
                              ("Att", "Def"), ("None", "None"), ("SpAtt", "Def"), ("SpDef", "Def"), ("Spd", "Def"),
                              ("Att", "SpAtt"), ("Def", "SpAtt"), ("None", "None"), ("SpDef", "SpAtt"),
                              ("SpAtt", "SpDef"),
                              ("Spd", "SpA"), ("Att", "SpDef"), ("Def", "SpDef"), ("None", "None"), ("Spd", "SpDef"),
                              ("Att", "Spd"),
                              ("Def", "Spd"), ("SpAtt", "Spd"), ("SpDef", "Spd"), ("None", "None")]
        self.player1Team = []
        self.player2Team = []

    ############################ Signnal Definitions ####################################
    def creationDone(self):
        QtWidgets.QMessageBox.about(self.battleUI, "Play Game", "Set up is finished! Go to Tab 1 to play game.")
        self.clearGUI()
        self.disableDetails()
        self.battleUI.txtPokedexEntry.setEnabled(False)
        self.battleUI.txtChosenLevel.setEnabled(False)
        self.battleUI.pushClearP1.setEnabled(False)
        self.battleUI.pushClearP2.setEnabled(False)
        self.battleUI.listCurr_p1Team.setEnabled(False)
        self.battleUI.listCurr_p2Team.setEnabled(False)
        self.battleUI.pushDone.setEnabled(False)
        self.battleUI.txtHappinessVal.setEnabled(False)

        self.setupGame()
        return

    def clearPokemon(self, listCurrTeam, playerTeam):
        if (listCurrTeam.currentItem() != None):
            row = listCurrTeam.currentRow()
            listCurrTeam.takeItem(row)
            playerTeam.pop(row)

        return

    def checkPlayerTeams(self):

        if (self.battleUI.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.battleUI.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.battleUI.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (len(self.player1Team) == maxPokemon and len(self.player2Team) == maxPokemon):
            self.battleUI.pushDone.setEnabled(True)
        else:
            self.battleUI.pushDone.setEnabled(False)

        return

    def restorePokemonDetails(self, listCurrTeam, playerTeam):
        self.clearGUI()
        pokemonB = playerTeam[listCurrTeam.currentRow()]

        self.battleUI.txtPokedexEntry.setText(pokemonB.pokedexEntry)
        self.updatePokemonEntry()

        self.battleUI.txtChosenLevel.setText(pokemonB.level)
        self.checkPokemonLevel()

        self.battleUI.txtHappinessVal.setText(pokemonB.happiness)
        self.finalizePokemon()

        for count in range(6):
            self.battleUI.evsList[count].setText(str(pokemonB.evList[count]))
            self.battleUI.ivsList[count].setText(str(pokemonB.ivList[count]))
            self.battleUI.finalStats[count].setText(str(pokemonB.finalStats[count]))
        self.finalizePokemon()

        abilityIndex = self.listInternalAbilities.index(pokemonB.internalAbility)
        self.battleUI.comboAvailableAbilities.setCurrentIndex(abilityIndex)

        itemIndex = self.listInternalItems.index(pokemonB.internalItem)
        self.battleUI.comboItems.setCurrentIndex(itemIndex)

        natureIndex = self.battleUI.comboNatures.findText(pokemonB.nature)
        self.battleUI.comboNatures.setCurrentIndex(natureIndex)

        self.chosenMovesetMap = copy.copy(pokemonB.internalMovesMap)

        for i in range(5):
            if (self.chosenMovesetMap.get(i) != None):
                internalMoveName, moveIndex, currPP = self.chosenMovesetMap.get(i)
                self.battleUI.comboAvailableMoves.setCurrentIndex(moveIndex)
                self.battleUI.listChosenMoves.setCurrentRow(i - 1)
                self.updateMoveSet()

        for i in range(self.battleUI.comboGenders.count()):
            if (self.battleUI.comboGenders.itemText(i) == pokemonB.gender):
                self.battleUI.comboGenders.setCurrentIndex(i)
                break

        self.finalizePokemon()

        return

    def savePokemon(self):
        pokedexEntry = self.battleUI.txtPokedexEntry.displayText()
        level = self.battleUI.txtChosenLevel.displayText()
        happinessVal = self.battleUI.txtHappinessVal.displayText()
        pokemonObject = self.battleUI.pokedex.get(pokedexEntry)
        pokemonImage = pokemonObject.image
        types = pokemonObject.pokemonTypes
        pokemonName = pokemonObject.pokemonName
        evList = []
        ivList = []
        finalStatsList = []
        nature = self.battleUI.comboNatures.currentText()
        internalAbility = self.listInternalAbilities[self.battleUI.comboAvailableAbilities.currentIndex()]
        chosenMovesWidget = self.battleUI.listChosenMoves
        chosenInternalMovesMap = self.chosenMovesetMap
        internalItem = self.listInternalItems[self.battleUI.comboItems.currentIndex()]
        chosenGender = self.battleUI.comboGenders.currentText()

        for i in range(6):
            evList.append(int(self.battleUI.evsList[i].displayText()))
            ivList.append(int(self.battleUI.ivsList[i].displayText()))
            finalStatsList.append(int(self.battleUI.finalStats[i].displayText()))

        if (self.battleUI.comboPlayerNumber.currentText() == "Player 1"):
            playerNum = 1
            listCurrTeam = self.battleUI.listCurr_p1Team
            playerTeam = self.player1Team
        else:
            playerNum = 2
            listCurrTeam = self.battleUI.listCurr_p2Team
            playerTeam = self.player2Team

        pokemonB = PokemonSetup(playerNum, pokemonName, pokedexEntry, level, happinessVal, pokemonImage, evList, ivList,
                                finalStatsList, nature, internalAbility, chosenMovesWidget, chosenInternalMovesMap,
                                internalItem, types, chosenGender, pokemonObject.weight, pokemonObject.height)

        if (self.battleUI.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.battleUI.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.battleUI.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() == None):
            QtWidgets.QMessageBox.about(self.battleUI, "Warning",
                                        "You have reached the max Pokemon Limit. Please select a pokemon to replace")
        elif (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() != None):
            listCurrTeam.currentItem().setText(self.battleUI.pokedex.get(pokedexEntry).pokemonName)
            playerTeam[listCurrTeam.currentRow()] = pokemonB
            self.clearGUI()
        else:
            listCurrTeam.addItem(self.battleUI.pokedex.get(pokedexEntry).pokemonName)
            playerTeam.append(pokemonB)
            self.clearGUI()

        self.checkPlayerTeams()

        return

    def updateEVs(self):
        for evWidget in self.battleUI.evsList:
            try:
                value = int(evWidget.displayText())
                if (value > 255 or value < 0):
                    self.battleUI.pushFinished.setEnabled(False)
            except:
                self.battleUI.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()
        return

    def updateIVs(self):

        for ivWidget in self.battleUI.ivsList:
            try:
                value = int(ivWidget.displayText())
                if (value > 31 or value < 0):
                    self.battleUI.pushFinished.setEnabled(False)
            except:
                self.battleUI.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()

        return

    def updatePokemonEntry(self):
        self.resetDetails()
        pokedexEntry = self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText())
        if (pokedexEntry == None):
            self.battleUI.displayPokemon(self.battleUI.viewCurrentPokemon, pokedexEntry=None)
            self.disableDetails()
        else:
            self.battleUI.displayPokemon(self.battleUI.viewCurrentPokemon, self.battleUI.txtPokedexEntry.displayText())
            self.updateAbilities()
            self.updatePokemonMoves()
            self.checkPokemonLevel()
            self.updateStats()
            self.updateGenders()

        self.finalizePokemon()
        return

    def checkPokemonLevel(self):
        invalidFlag = 0

        if (self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText()) == None):
            invalidFlag = 1

        try:
            levelNum = int(self.battleUI.txtChosenLevel.displayText())
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
        if (self.battleUI.listChosenMoves.currentItem() != None):
            selectedListRow = self.battleUI.listChosenMoves.currentRow()
            selectedIndex = self.battleUI.comboAvailableMoves.currentIndex()
            internalMoveName = self.listInternalMoves[selectedIndex]

            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.battleUI.movesDatabase.get(
                internalMoveName)
            _, typeName, _, _, _ = self.battleUI.typesDatabase.get(typeMove)
            self.battleUI.listChosenMoves.currentItem().setText("Move " + str(selectedListRow + 1) + ": " + moveName)
            self.battleUI.listChosenMoves.currentItem().setToolTip(
                "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
            self.chosenMovesetMap.update({selectedListRow + 1: (internalMoveName, selectedIndex, int(totalPP))})
            self.finalizePokemon()
        return

    def randomizeEVStats(self):
        total = 0

        while (total != 510):
            total = 0
            self.battleUI.txtEV_HP.setText(str(random.randrange(0, 256)))
            total += int(self.battleUI.txtEV_HP.displayText())

            self.battleUI.txtEV_Attack.setText(str(random.randrange(0, 256)))
            total += (int(self.battleUI.txtEV_Attack.displayText()))

            self.battleUI.txtEV_Defense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.battleUI.txtEV_Defense.displayText()))

            self.battleUI.txtEV_SpAttack.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.battleUI.txtEV_SpAttack.displayText()))

            self.battleUI.txtEV_SpDefense.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.battleUI.txtEV_SpDefense.displayText()))

            self.battleUI.txtEV_Speed.setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.battleUI.txtEV_Speed.displayText()))

        self.updateStats()
        self.finalizePokemon()

        return

    def randomizeIVStats(self):
        self.battleUI.txtIV_HP.setText(str(random.randrange(0, 32)))
        self.battleUI.txtIV_Attack.setText(str(random.randrange(0, 32)))
        self.battleUI.txtIV_Defense.setText(str(random.randrange(0, 32)))
        self.battleUI.txtIV_SpAttack.setText(str(random.randrange(0, 32)))
        self.battleUI.txtIV_SpDefense.setText(str(random.randrange(0, 32)))
        self.battleUI.txtIV_Speed.setText(str(random.randrange(0, 32)))

        self.updateStats()
        self.finalizePokemon()
        return


    #################################### Helper Functions #################################

    def setupGame(self):
        self.battleUI.pushStartBattle.setEnabled(True)
        self.battleUI.pushRestart.setEnabled(True)
        self.battleUI.pushDifferentTeam.setEnabled(True)
        # self.pushSwitchPlayer1.setEnabled(True)
        # self.pushSwitchPlayer2.setEnabled(True)

        i = 0
        for pokemon in self.player1Team:
            pokemonFullName = self.battleUI.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.battleUI.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.battleUI.itemsDatabase.get(pokemon.internalItem)
            self.battleUI.listPlayer1_team.addItem(pokemonFullName)
            # self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.battleUI.listPlayer1_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + str(pokemon.finalStats[0]) + "\n" +
                                                     "Attack:\t\t" + str(pokemon.finalStats[1]) + "\n" +
                                                     "Defense:\t" + str(pokemon.finalStats[2]) + "\n" +
                                                     "SpAttack:\t" + str(pokemon.finalStats[3]) + "\n" +
                                                     "SpDefense:\t" + str(pokemon.finalStats[4]) + "\n" +
                                                     "Speed:\t\t" + str(pokemon.finalStats[5]))
            i += 1

        i = 0
        for pokemon in self.player2Team:
            pokemonFullName = self.battleUI.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.battleUI.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.battleUI.itemsDatabase.get(pokemon.internalItem)
            self.battleUI.listPlayer2_team.addItem(pokemonFullName)
            self.battleUI.listPlayer2_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                     "Nature:\t\t" + pokemon.nature + "\n" +
                                                     "Item:\t\t" + itemName + "\n\n" +
                                                     "HP:\t\t" + str(pokemon.finalStats[0]) + "\n" +
                                                     "Attack:\t\t" + str(pokemon.finalStats[1]) + "\n" +
                                                     "Defense:\t" + str(pokemon.finalStats[2]) + "\n" +
                                                     "SpAttack:\t" + str(pokemon.finalStats[3]) + "\n" +
                                                     "SpDefense:\t" + str(pokemon.finalStats[4]) + "\n" +
                                                     "Speed:\t\t" + str(pokemon.finalStats[5]))
            i += 1

        return

    def finalizePokemon(self):
        enableFlag = 1
        if (self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText()) == None):
            enableFlag = 0

        evTotal = 0
        try:
            levelNum = int(self.battleUI.txtChosenLevel.displayText())
            happinessVal = int(self.battleUI.txtHappinessVal.displayText())

            if (happinessVal < 0 or happinessVal > 255):
                enableFlag = 0

            if (levelNum < 1 or levelNum > 100):
                enableFlag = 0

            for i in range(6):
                evValue = int(self.battleUI.evsList[i].displayText())
                ivValue = int(self.battleUI.ivsList[i].displayText())

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
            self.battleUI.pushFinished.setEnabled(True)
        else:
            self.battleUI.pushFinished.setEnabled(False)

        self.checkPlayerTeams()

        return

    def updateStats(self):
        if (self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText()) == None):
            return
        pokemon = self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText())
        # if (self.txtFinal_HP.isEnabled() == False):
        #   return

        natureIndex = self.battleUI.comboNatures.currentIndex()
        increasedStat, decreasedStat = self.natureEffects[natureIndex]
        # level = int(self.txtChosenLevel.displayText())

        for i in range(6):
            statChange = 1

            try:
                ivValue = int(self.battleUI.ivsList[i].displayText())
                evValue = int(self.battleUI.evsList[i].displayText())
                level = int(self.battleUI.txtChosenLevel.displayText())
                if (i == 0):
                    self.battleUI.finalStats[i].setText(str(math.floor(math.floor(((2 * int(pokemon.baseStats[i]) + ivValue + (
                        math.floor(evValue / 4))) * level) / 100) + level + 10)))
                else:
                    if (i == 1 and increasedStat == "Att"):
                        statChange = 1.1  # self.finalStats[i] = (((((2*pokemon.baseStats[i] + ivValue + (evValue/4)) * level)/100)) + 5) * 1.1
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
                    self.battleUI.finalStats[i].setText(str(math.floor(((math.floor(((2 * int(
                        pokemon.baseStats[i]) + ivValue + math.floor(evValue / 4)) * level) / 100)) + 5) * statChange)))
            except:
                self.battleUI.finalStats[i].setText(str(pokemon.baseStats[i]))

    def resetDetails(self):
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.chosenMovesetMap = {}

        self.battleUI.listChosenMoves.clear()
        self.battleUI.comboAvailableMoves.clear()
        self.battleUI.comboAvailableAbilities.clear()
        self.battleUI.comboGenders.clear()

        self.battleUI.listChosenMoves.addItem("Move 1:")
        self.battleUI.listChosenMoves.addItem("Move 2:")
        self.battleUI.listChosenMoves.addItem("Move 3:")
        self.battleUI.listChosenMoves.addItem("Move 4:")

        for i in range(6):
            self.battleUI.finalStats[i].setText("")

        return

    def clearGUI(self):
        # Clear Details
        self.resetDetails()
        self.battleUI.txtPokedexEntry.setText("")
        self.battleUI.txtChosenLevel.setText("")
        self.battleUI.txtHappinessVal.setText("")

        for i in range(6):
            self.battleUI.evsList[i].setText("")
            self.battleUI.ivsList[i].setText("")

        return

    def updateAbilities(self):
        pokemon = self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText())
        self.battleUI.comboAvailableAbilities.clear()

        count = 0
        for ability in pokemon.abilities:
            idNum, displayName, description = self.battleUI.abilitiesDatabase.get(ability)
            self.battleUI.comboAvailableAbilities.addItem(displayName)
            self.battleUI.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(ability)
            count += 1

        if (pokemon.hiddenAbility != ""):
            idNum, displayName, description = self.battleUI.abilitiesDatabase.get(pokemon.hiddenAbility)
            self.battleUI.comboAvailableAbilities.addItem(displayName)  # ("HA: " + displayName)
            self.battleUI.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(pokemon.hiddenAbility)

        return

    def updatePokemonMoves(self):
        pokemon = self.battleUI.pokedex.get(self.battleUI.txtPokedexEntry.displayText())
        self.battleUI.comboAvailableMoves.clear()

        count = 0
        for move in pokemon.moves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.battleUI.movesDatabase.get(
                move)
            _, typeName, _, _, _ = self.battleUI.typesDatabase.get(typeMove)
            self.battleUI.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.battleUI.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + " " + "Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        for move in pokemon.eggMoves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.battleUI.movesDatabase.get(
                move)
            _, typeName, _, _, _ = self.battleUI.typesDatabase.get(typeMove)
            self.battleUI.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.battleUI.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + "\t" + "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        return

    def updateGenders(self):
        pokedexEntry = self.battleUI.txtPokedexEntry.displayText()
        pokemonObject = self.battleUI.pokedex.get(pokedexEntry)
        self.battleUI.comboGenders.clear()
        if (len(pokemonObject.genders) != 0):
            if ("MALE" in pokemonObject.genders):
                self.battleUI.comboGenders.addItem("Male")
            if ("FEMALE" in pokemonObject.genders):
                self.battleUI.comboGenders.addItem("Female")
        else:
            self.battleUI.comboGenders.addItem("Genderless")

 

    def disableDetails(self):
        self.battleUI.pushFinished.setEnabled(False)

        for i in range(6):
            self.battleUI.evsList[i].setEnabled(False)
            self.battleUI.ivsList[i].setEnabled(False)

        self.battleUI.pushRandomizeEVs.setEnabled(False)
        self.battleUI.pushRandomizeIVs.setEnabled(False)

        self.battleUI.pushAddMove.setEnabled(False)

        return

    def enableDetails(self):
        # self.pushFinished.setEnabled(True)

        for i in range(6):
            self.battleUI.evsList[i].setEnabled(True)
            self.battleUI.ivsList[i].setEnabled(True)

        self.battleUI.pushRandomizeEVs.setEnabled(True)
        self.battleUI.pushRandomizeIVs.setEnabled(True)

        self.battleUI.pushAddMove.setEnabled(True)
        return

