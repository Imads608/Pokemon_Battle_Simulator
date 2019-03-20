import sys
sys.path.append("Metadata")
from PyQt5 import QtCore, QtGui, QtWidgets
from pokemonDatabase import *
from pokemonSetup import *
import random
import math
import copy


class TeamBuilder(object):
    def __init__(self, TBWidgets, pokemonDB):

        # Widgets of Team Builder Interface
        self.tbUI = TBWidgets

        # Get Pokemon Database
        self.pokemonDB = pokemonDB

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
        QtWidgets.QMessageBox.about(self.tbUI, "Play Game", "Set up is finished! Go to Tab 1 to play game.")
        self.clearGUI()
        self.disableDetails()
        self.tbUI.txtPokedexEntry.setEnabled(False)
        self.tbUI.txtChosenLevel.setEnabled(False)
        self.tbUI.pushClearP1.setEnabled(False)
        self.tbUI.pushClearP2.setEnabled(False)
        self.tbUI.listCurr_p1Team.setEnabled(False)
        self.tbUI.listCurr_p2Team.setEnabled(False)
        self.tbUI.pushDone.setEnabled(False)
        self.tbUI.txtHappinessVal.setEnabled(False)

        self.setupGame()
        return

    def clearPokemon(self, listCurrTeam, playerTeam):
        if (listCurrTeam.currentItem() != None):
            row = listCurrTeam.currentRow()
            listCurrTeam.takeItem(row)
            playerTeam.pop(row)

        return

    def checkPlayerTeams(self):

        if (self.tbUI.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.tbUI.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.tbUI.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (len(self.player1Team) == maxPokemon and len(self.player2Team) == maxPokemon):
            self.tbUI.pushDone.setEnabled(True)
        else:
            self.tbUI.pushDone.setEnabled(False)

        return

    def restorePokemonDetails(self, listCurrTeam, playerTeam):
        self.clearGUI()
        pokemonB = playerTeam[listCurrTeam.currentRow()]

        self.tbUI.txtPokedexEntry.setText(pokemonB.pokedexEntry)
        self.updatePokemonEntry()

        self.tbUI.txtChosenLevel.setText(pokemonB.level)
        self.checkPokemonLevel()

        self.tbUI.txtHappinessVal.setText(pokemonB.happiness)
        self.finalizePokemon()

        for count in range(6):
            self.tbUI.evsList[count].setText(str(pokemonB.evList[count]))
            self.tbUI.ivsList[count].setText(str(pokemonB.ivList[count]))
            self.tbUI.finalStats[count].setText(str(pokemonB.finalStats[count]))
        self.finalizePokemon()

        abilityIndex = self.listInternalAbilities.index(pokemonB.internalAbility)
        self.tbUI.comboAvailableAbilities.setCurrentIndex(abilityIndex)

        itemIndex = self.listInternalItems.index(pokemonB.internalItem)
        self.tbUI.comboItems.setCurrentIndex(itemIndex)

        natureIndex = self.tbUI.comboNatures.findText(pokemonB.nature)
        self.tbUI.comboNatures.setCurrentIndex(natureIndex)

        self.chosenMovesetMap = copy.copy(pokemonB.internalMovesMap)

        for i in range(5):
            if (self.chosenMovesetMap.get(i) != None):
                internalMoveName, moveIndex, currPP = self.chosenMovesetMap.get(i)
                self.tbUI.comboAvailableMoves.setCurrentIndex(moveIndex)
                self.tbUI.listChosenMoves.setCurrentRow(i - 1)
                self.updateMoveSet()

        for i in range(self.tbUI.comboGenders.count()):
            if (self.tbUI.comboGenders.itemText(i) == pokemonB.gender):
                self.tbUI.comboGenders.setCurrentIndex(i)
                break

        self.finalizePokemon()

        return

    def savePokemon(self):
        pokedexEntry = self.tbUI.txtPokedexEntry.displayText()
        level = self.tbUI.txtChosenLevel.displayText()
        happinessVal = self.tbUI.txtHappinessVal.displayText()
        pokemonObject = self.pokemonDB.pokedex.get(pokedexEntry)
        pokemonImage = pokemonObject.image
        types = pokemonObject.pokemonTypes
        pokemonName = pokemonObject.pokemonName
        evList = []
        ivList = []
        finalStatsList = []
        nature = self.tbUI.comboNatures.currentText()
        internalAbility = self.listInternalAbilities[self.tbUI.comboAvailableAbilities.currentIndex()]
        chosenMovesWidget = self.tbUI.listChosenMoves
        chosenInternalMovesMap = self.chosenMovesetMap
        internalItem = self.listInternalItems[self.tbUI.comboItems.currentIndex()]
        chosenGender = self.tbUI.comboGenders.currentText()

        for i in range(6):
            evList.append(int(self.tbUI.evsList[i].displayText()))
            ivList.append(int(self.tbUI.ivsList[i].displayText()))
            finalStatsList.append(int(self.tbUI.finalStats[i].displayText()))

        if (self.tbUI.comboPlayerNumber.currentText() == "Player 1"):
            playerNum = 1
            listCurrTeam = self.tbUI.listCurr_p1Team
            playerTeam = self.player1Team
        else:
            playerNum = 2
            listCurrTeam = self.tbUI.listCurr_p2Team
            playerTeam = self.player2Team

        pokemonB = PokemonSetup(playerNum, pokemonName, pokedexEntry, level, happinessVal, pokemonImage, evList, ivList,
                                finalStatsList, nature, internalAbility, chosenMovesWidget, chosenInternalMovesMap,
                                internalItem, types, chosenGender, pokemonObject.weight, pokemonObject.height)

        if (self.tbUI.comboBattleType.currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.tbUI.comboBattleType.currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.tbUI.comboBattleType.currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() == None):
            QtWidgets.QMessageBox.about(self.tbUI, "Warning",
                                        "You have reached the max Pokemon Limit. Please select a pokemon to replace")
        elif (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() != None):
            listCurrTeam.currentItem().setText(self.pokemonDB.pokedex.get(pokedexEntry).pokemonName)
            playerTeam[listCurrTeam.currentRow()] = pokemonB
            self.clearGUI()
        else:
            listCurrTeam.addItem(self.pokemonDB.pokedex.get(pokedexEntry).pokemonName)
            playerTeam.append(pokemonB)
            self.clearGUI()

        self.checkPlayerTeams()

        return

    def updateEVs(self):
        for evWidget in self.tbUI.evsList:
            try:
                value = int(evWidget.displayText())
                if (value > 255 or value < 0):
                    self.tbUI.pushFinished.setEnabled(False)
            except:
                self.tbUI.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()
        return

    def updateIVs(self):

        for ivWidget in self.tbUI.ivsList:
            try:
                value = int(ivWidget.displayText())
                if (value > 31 or value < 0):
                    self.tbUI.pushFinished.setEnabled(False)
            except:
                self.tbUI.pushFinished.setEnabled(False)

        self.updateStats()
        self.finalizePokemon()

        return

    def updatePokemonEntry(self):
        self.resetDetails()
        pokedexEntry = self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText())
        if (pokedexEntry == None):
            self.tbUI.displayPokemon(self.tbUI.viewCurrentPokemon, pokedexEntry, self.pokemonDB.pokedex)
            self.disableDetails()
        else:
            self.tbUI.displayPokemon(self.tbUI.viewCurrentPokemon, self.tbUI.txtPokedexEntry.displayText(), self.pokemonDB.pokedex)
            self.updateAbilities()
            self.updatePokemonMoves()
            self.checkPokemonLevel()
            self.updateStats()
            self.updateGenders()

        self.finalizePokemon()
        return

    def checkPokemonLevel(self):
        invalidFlag = 0

        if (self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText()) == None):
            invalidFlag = 1

        try:
            levelNum = int(self.tbUI.txtChosenLevel.displayText())
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
        if (self.tbUI.listChosenMoves.currentItem() != None):
            selectedListRow = self.tbUI.listChosenMoves.currentRow()
            selectedIndex = self.tbUI.comboAvailableMoves.currentIndex()
            internalMoveName = self.listInternalMoves[selectedIndex]

            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonDB.movesDatabase.get(
                internalMoveName)
            _, typeName, _, _, _ = self.pokemonDB.typesDatabase.get(typeMove)
            self.tbUI.listChosenMoves.currentItem().setText("Move " + str(selectedListRow + 1) + ": " + moveName)
            self.tbUI.listChosenMoves.currentItem().setToolTip(
                "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
            self.chosenMovesetMap.update({selectedListRow + 1: (internalMoveName, selectedIndex, int(totalPP))})
            self.finalizePokemon()
        return

    def randomizeEVStats(self):
        total = 0

        while (total != 510):
            total = 0
            self.tbUI.evsList[0].setText(str(random.randrange(0, 256)))
            total += int(self.tbUI.evsList[0].displayText())

            self.tbUI.evsList[1].setText(str(random.randrange(0, 256)))
            total += (int(self.tbUI.evsList[1].displayText()))

            self.tbUI.evsList[2].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.evsList[2].displayText()))

            self.tbUI.evsList[3].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.evsList[3].displayText()))

            self.tbUI.evsList[4].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.evsList[4].displayText()))

            self.tbUI.evsList[5].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.evsList[5].displayText()))

        self.updateStats()
        self.finalizePokemon()

        return

    def randomizeIVStats(self):
        self.tbUI.ivsList[0].setText(str(random.randrange(0, 32)))
        self.tbUI.ivsList[1].setText(str(random.randrange(0, 32)))
        self.tbUI.ivsList[2].setText(str(random.randrange(0, 32)))
        self.tbUI.ivsList[3].setText(str(random.randrange(0, 32)))
        self.tbUI.ivsList[4].setText(str(random.randrange(0, 32)))
        self.tbUI.ivsList[5].setText(str(random.randrange(0, 32)))

        self.updateStats()
        self.finalizePokemon()
        return


    #################################### Helper Functions #################################

    def setupGame(self):
        self.tbUI.pushStartBattle.setEnabled(True)
        self.tbUI.pushRestart.setEnabled(True)
        self.tbUI.pushDifferentTeam.setEnabled(True)
        # self.pushSwitchPlayer1.setEnabled(True)
        # self.pushSwitchPlayer2.setEnabled(True)

        i = 0
        for pokemon in self.player1Team:
            pokemonFullName = self.pokemonDB.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.pokemonDB.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.pokemonDB.itemsDatabase.get(pokemon.internalItem)
            self.tbUI.listPlayer1_team.addItem(pokemonFullName)
            # self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
            self.tbUI.listPlayer1_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
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
            pokemonFullName = self.pokemonDB.pokedex.get(pokemon.pokedexEntry).pokemonName
            _, abilityName, _ = self.pokemonDB.abilitiesDatabase.get(pokemon.internalAbility)
            itemName, _, _, _, _, _, _ = self.pokemonDB.itemsDatabase.get(pokemon.internalItem)
            self.tbUI.listPlayer2_team.addItem(pokemonFullName)
            self.tbUI.listPlayer2_team.item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
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
        if (self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText()) == None):
            enableFlag = 0

        evTotal = 0
        try:
            levelNum = int(self.tbUI.txtChosenLevel.displayText())
            happinessVal = int(self.tbUI.txtHappinessVal.displayText())

            if (happinessVal < 0 or happinessVal > 255):
                enableFlag = 0

            if (levelNum < 1 or levelNum > 100):
                enableFlag = 0

            for i in range(6):
                evValue = int(self.tbUI.evsList[i].displayText())
                ivValue = int(self.tbUI.ivsList[i].displayText())

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
            self.tbUI.pushFinished.setEnabled(True)
        else:
            self.tbUI.pushFinished.setEnabled(False)

        self.checkPlayerTeams()

        return

    def updateStats(self):
        if (self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText()) == None):
            return
        pokemon = self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText())
        # if (self.txtFinal_HP.isEnabled() == False):
        #   return

        natureIndex = self.tbUI.comboNatures.currentIndex()
        increasedStat, decreasedStat = self.natureEffects[natureIndex]
        # level = int(self.txtChosenLevel.displayText())

        for i in range(6):
            statChange = 1

            try:
                ivValue = int(self.tbUI.ivsList[i].displayText())
                evValue = int(self.tbUI.evsList[i].displayText())
                level = int(self.tbUI.txtChosenLevel.displayText())
                if (i == 0):
                    self.tbUI.finalStats[i].setText(str(math.floor(math.floor(((2 * int(pokemon.baseStats[i]) + ivValue + (
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
                    self.tbUI.finalStats[i].setText(str(math.floor(((math.floor(((2 * int(
                        pokemon.baseStats[i]) + ivValue + math.floor(evValue / 4)) * level) / 100)) + 5) * statChange)))
            except:
                self.tbUI.finalStats[i].setText(str(pokemon.baseStats[i]))

    def resetDetails(self):
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.chosenMovesetMap = {}

        self.tbUI.listChosenMoves.clear()
        self.tbUI.comboAvailableMoves.clear()
        self.tbUI.comboAvailableAbilities.clear()
        self.tbUI.comboGenders.clear()

        self.tbUI.listChosenMoves.addItem("Move 1:")
        self.tbUI.listChosenMoves.addItem("Move 2:")
        self.tbUI.listChosenMoves.addItem("Move 3:")
        self.tbUI.listChosenMoves.addItem("Move 4:")

        for i in range(6):
            self.tbUI.finalStats[i].setText("")

        return

    def clearGUI(self):
        # Clear Details
        self.resetDetails()
        self.tbUI.txtPokedexEntry.setText("")
        self.tbUI.txtChosenLevel.setText("")
        self.tbUI.txtHappinessVal.setText("")

        for i in range(6):
            self.tbUI.evsList[i].setText("")
            self.tbUI.ivsList[i].setText("")

        return

    def updateAbilities(self):
        pokemon = self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText())
        self.tbUI.comboAvailableAbilities.clear()

        count = 0
        for ability in pokemon.abilities:
            idNum, displayName, description = self.pokemonDB.abilitiesDatabase.get(ability)
            self.tbUI.comboAvailableAbilities.addItem(displayName)
            self.tbUI.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(ability)
            count += 1

        if (pokemon.hiddenAbility != ""):
            idNum, displayName, description = self.pokemonDB.abilitiesDatabase.get(pokemon.hiddenAbility)
            self.tbUI.comboAvailableAbilities.addItem(displayName)  # ("HA: " + displayName)
            self.tbUI.comboAvailableAbilities.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(pokemon.hiddenAbility)

        return

    def updatePokemonMoves(self):
        pokemon = self.pokemonDB.pokedex.get(self.tbUI.txtPokedexEntry.displayText())
        self.tbUI.comboAvailableMoves.clear()

        count = 0
        for move in pokemon.moves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonDB.movesDatabase.get(
                move)
            _, typeName, _, _, _ = self.pokemonDB.typesDatabase.get(typeMove)
            self.tbUI.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.tbUI.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + " " + "Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        for move in pokemon.eggMoves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonDB.movesDatabase.get(
                move)
            _, typeName, _, _, _ = self.pokemonDB.typesDatabase.get(typeMove)
            self.tbUI.comboAvailableMoves.addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.tbUI.comboAvailableMoves.setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + "\t" + "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        return

    def updateGenders(self):
        pokedexEntry = self.tbUI.txtPokedexEntry.displayText()
        pokemonObject = self.pokemonDB.pokedex.get(pokedexEntry)
        self.tbUI.comboGenders.clear()
        if (len(pokemonObject.genders) != 0):
            if ("MALE" in pokemonObject.genders):
                self.tbUI.comboGenders.addItem("Male")
            if ("FEMALE" in pokemonObject.genders):
                self.tbUI.comboGenders.addItem("Female")
        else:
            self.tbUI.comboGenders.addItem("Genderless")

 

    def disableDetails(self):
        self.tbUI.pushFinished.setEnabled(False)

        for i in range(6):
            self.tbUI.evsList[i].setEnabled(False)
            self.tbUI.ivsList[i].setEnabled(False)

        self.tbUI.pushRandomizeEVs.setEnabled(False)
        self.tbUI.pushRandomizeIVs.setEnabled(False)

        self.tbUI.pushAddMove.setEnabled(False)

        return

    def enableDetails(self):
        # self.pushFinished.setEnabled(True)

        for i in range(6):
            self.tbUI.evsList[i].setEnabled(True)
            self.tbUI.ivsList[i].setEnabled(True)

        self.tbUI.pushRandomizeEVs.setEnabled(True)
        self.tbUI.pushRandomizeIVs.setEnabled(True)

        self.tbUI.pushAddMove.setEnabled(True)
        return

