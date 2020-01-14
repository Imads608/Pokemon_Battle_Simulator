import sys
#sys.path.append("battle_api/common")
from PyQt5 import QtCore, QtGui, QtWidgets
from battle_api.common.pokemonBattler import PokemonBattler
import random
import math
import copy
from pubsub import pub


class TeamBuilder(object):
    def __init__(self, TBWidgets, pokemonDB, controllerTopic):

        # Widgets of Team Builder Interface
        self.tbUI = TBWidgets

        # Set Publisher/Subscriber Topic
        self.controllerTopic = controllerTopic

        # Get Pokemon Database
        self.pokemonMetadata = pokemonDB

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

    ####### Getters ################
    def getTeamBuilderWidgets(self):
        return self.tbUI

    def getControllerTopic(self):
        return self.tbUI

    def getControllerTopic(self):
        return self.controllerTopic

    def getPokemonMetadata(self):
        return self.pokemonMetadata

    def getListInternalMoves(self):
        return self.listInternalMoves

    def getChosenMovessetMap(self):
        return self.chosenMovesetMap

    def getNatureEffects(self):
        return self.natureEffects

    def getPlayerTeamList(self, playerNum):
        if (playerNum == 1):
            return self.player1Team
        return self.player2Team


    ############################ Signnal Definitions ####################################
    def creationDone(self):
        self.tbUI.displayMessageBox("Play Game", "Set up is finished! Go to Tab 1 to play game")
        self.clearGUI()
        self.disableDetails()
        self.tbUI.getPokedexEntryTextBox().setEnabled(False)
        self.tbUI.getChosenLevelTextBox().setEnabled(False)
        self.tbUI.getClearPlayerTeamPushButton(1).setEnabled(False)
        self.tbUI.getClearPlayerTeamPushButton(2).setEnabled(False)
        self.tbUI.getCurrentPlayerTeam(1).setEnabled(False)
        self.tbUI.getCurrentPlayerTeam(2).setEnabled(False)
        self.tbUI.getTeamBuilderDonePushButton().setEnabled(False)
        self.tbUI.getHappinessValueTextBox().setEnabled(False)
        pub.sendMessage(self.controllerTopic, battleTypeChosen="singles")
        self.setupGame()
        return

    def clearPokemon(self, listCurrTeam, playerTeam):
        if (listCurrTeam.currentItem() != None):
            row = listCurrTeam.currentRow()
            listCurrTeam.takeItem(row)
            playerTeam.pop(row)

        return

    def checkPlayerTeams(self):

        if (self.tbUI.getBattleTypeCombinationBox().currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.tbUI.getBattleTypeCombinationBox().currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.tbUI.getBattleTypeCombinationBox().currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (len(self.player1Team) == maxPokemon and len(self.player2Team) == maxPokemon):
            self.tbUI.getTeamBuilderDonePushButton().setEnabled(True)
        else:
            self.tbUI.getTeamBuilderDonePushButton().setEnabled(False)

        return

    def restorePokemonDetails(self, listCurrTeam, playerTeam):
        self.clearGUI()
        pokemonB = playerTeam[listCurrTeam.currentRow()]

        self.tbUI.getPokedexEntryTextBox().setText(pokemonB.getPokedexEntry())
        self.updatePokemonEntry()

        self.tbUI.getChosenLevelTextBox().setText(pokemonB.getLevel())
        self.checkPokemonLevel()

        self.tbUI.getHappinessValueTextBox().setText(pokemonB.getHappiness())
        self.finalizePokemon()

        for count in range(6):
            self.tbUI.getEvsList()[count].setText(str(pokemonB.getEvsList()[count]))
            self.tbUI.getIvsList()[count].setText(str(pokemonB.getIvsList()[count]))
            self.tbUI.getFinalStats()[count].setText(str(pokemonB.getFinalStats()[count]))
        self.finalizePokemon()

        abilityIndex = self.listInternalAbilities.index(pokemonB.internalAbility)
        self.tbUI.getAvailableAbilitiesCombinationBox().setCurrentIndex(abilityIndex)

        itemIndex = self.listInternalItems.index(pokemonB.internalItem)
        self.tbUI.getItemsCombinationBox().setCurrentIndex(itemIndex)

        natureIndex = self.tbUI.getNaturesCombinationBox().findText(pokemonB.getNature())
        self.tbUI.getNaturesCombinationBox().setCurrentIndex(natureIndex)

        self.chosenMovesetMap = copy.copy(pokemonB.getInternalMovesMap())

        for i in range(5):
            if (self.chosenMovesetMap.get(i) != None):
                internalMoveName, moveIndex, currPP = self.chosenMovesetMap.get(i)
                self.tbUI.getAvailableMovesCombinationBox().setCurrentIndex(moveIndex)
                self.tbUI.getChosenMovesListBox().setCurrentRow(i - 1)
                self.updateMoveSet()

        for i in range(self.tbUI.comboGenders.count()):
            if (self.tbUI.getGendersCombinationBox().itemText(i) == pokemonB.getGender()):
                self.tbUI.getGendersCombinationBox().setCurrentIndex(i)
                break

        self.finalizePokemon()

        return

    def savePokemon(self):
        pokedexEntry = self.tbUI.getPokedexEntryTextBox().displayText()
        level = self.tbUI.getChosenLevelTextBox().displayText()
        happinessVal = self.tbUI.getHappinessValueTextBox().displayText()
        pokemonObject = self.pokemonMetadata.getPokedex().get(pokedexEntry)
        pokemonImage = pokemonObject.image
        types = pokemonObject.pokemonTypes
        pokemonName = pokemonObject.pokemonName
        evList = []
        ivList = []
        finalStatsList = []
        nature = self.tbUI.getNaturesCombinationBox().currentText()
        internalAbility = self.listInternalAbilities[self.tbUI.comboAvailableAbilities.currentIndex()]
        chosenMovesWidget = self.tbUI.getChosenMovesListBox
        chosenInternalMovesMap = self.chosenMovesetMap
        internalItem = self.listInternalItems[self.tbUI.comboItems.currentIndex()]
        chosenGender = self.tbUI.getGendersCombinationBox().currentText()

        for i in range(6):
            evList.append(int(self.tbUI.getEvsList()[i].displayText()))
            ivList.append(int(self.tbUI.getIvsList()[i].displayText()))
            finalStatsList.append(int(self.tbUI.getFinalStats()[i].displayText()))

        if (self.tbUI.comboPlayerNumber.currentText() == "Player 1"):
            playerNum = 1
            listCurrTeam = self.tbUI.getCurrentPlayerTeam(1)
            playerTeam = self.player1Team
        else:
            playerNum = 2
            listCurrTeam = self.tbUI.getCurrentPlayerTeam(2)
            playerTeam = self.player2Team

        pokemonB = PokemonBattler(playerNum, pokemonName, pokedexEntry, level, happinessVal, pokemonImage, evList, ivList,
                                finalStatsList, nature, internalAbility, chosenMovesWidget, chosenInternalMovesMap,
                                internalItem, types, chosenGender, pokemonObject.weight, pokemonObject.height)

        if (self.tbUI.getBattleTypeCombinationBox().currentText() == "1v1 Battle"):
            maxPokemon = 1
        elif (self.tbUI.getBattleTypeCombinationBox().currentText() == "3v3 Battle"):
            maxPokemon = 3
        elif (self.tbUI.getBattleTypeCombinationBox().currentText() == "6v6 Battle"):
            maxPokemon = 6

        if (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() == None):
            QtWidgets.QMessageBox.about(self.tbUI, "Warning",
                                        "You have reached the max Pokemon Limit. Please select a pokemon to replace")
        elif (listCurrTeam.count() >= maxPokemon and listCurrTeam.currentItem() != None):
            listCurrTeam.currentItem().setText(self.pokemonMetadata.getPokedex().get(pokedexEntry).pokemonName)
            playerTeam[listCurrTeam.currentRow()] = pokemonB
            self.clearGUI()
        else:
            listCurrTeam.addItem(self.pokemonMetadata.getPokedex().get(pokedexEntry).pokemonName)
            playerTeam.append(pokemonB)
            self.clearGUI()

        self.checkPlayerTeams()

        return

    def updateEVs(self):
        for evWidget in self.tbUI.evsList:
            try:
                value = int(evWidget.displayText())
                if (value > 255 or value < 0):
                    self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(False)
            except:
                self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(False)

        self.updateStats()
        self.finalizePokemon()
        return

    def updateIVs(self):

        for ivWidget in self.tbUI.ivsList:
            try:
                value = int(ivWidget.displayText())
                if (value > 31 or value < 0):
                    self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(False)
            except:
                self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(False)

        self.updateStats()
        self.finalizePokemon()

        return

    def updatePokemonEntry(self):
        self.resetDetails()
        pokedexEntry = self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText())
        if (pokedexEntry == None):
            self.tbUI.displayPokemon(self.tbUI.getCurrentPokemonView(), pokedexEntry, self.pokemonMetadata.getPokedex())
            self.disableDetails()
        else:
            self.tbUI.displayPokemon(self.tbUI.getCurrentPokemonView(), self.tbUI.getPokedexEntryTextBox().displayText(), self.pokemonMetadata.getPokedex())
            self.updateAbilities()
            self.updatePokemonMoves()
            self.checkPokemonLevel()
            self.updateStats()
            self.updateGenders()

        self.finalizePokemon()
        return

    def checkPokemonLevel(self):
        invalidFlag = 0

        if (self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText()) == None):
            invalidFlag = 1

        try:
            levelNum = int(self.tbUI.getChosenLevelTextBox().displayText())
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
            selectedListRow = self.tbUI.getChosenMovesListBox().currentRow()
            selectedIndex = self.tbUI.getAvailableMovesCombinationBox().currentIndex()
            internalMoveName = self.listInternalMoves[selectedIndex]

            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(
                internalMoveName)
            _, typeName, _, _, _ = self.pokemonMetadata.getTypesMetadata().get(typeMove)
            self.tbUI.getChosenMovesListBox().currentItem().setText("Move " + str(selectedListRow + 1) + ": " + moveName)
            self.tbUI.getChosenMovesListBox().currentItem().setToolTip(
                "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)
            self.chosenMovesetMap.update({selectedListRow + 1: (internalMoveName, selectedIndex, int(totalPP))})
            self.finalizePokemon()
        return

    def randomizeEVStats(self):
        total = 0

        while (total != 510):
            total = 0
            self.tbUI.getEvsList()[0].setText(str(random.randrange(0, 256)))
            total += int(self.tbUI.getEvsList()[0].displayText())

            self.tbUI.getEvsList()[1].setText(str(random.randrange(0, 256)))
            total += (int(self.tbUI.getEvsList()[1].displayText()))

            self.tbUI.getEvsList()[2].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.getEvsList()[2].displayText()))

            self.tbUI.getEvsList()[3].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.getEvsList()[3].displayText()))

            self.tbUI.getEvsList()[4].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.getEvsList()[4].displayText()))

            self.tbUI.getEvsList()[5].setText(str(random.randrange(0, min(256, 510 - total + 1))))
            total += (int(self.tbUI.getEvsList()[5].displayText()))

        self.updateStats()
        self.finalizePokemon()

        return

    def randomizeIVStats(self):
        self.tbUI.getIvsList()[0].setText(str(random.randrange(0, 32)))
        self.tbUI.getIvsList()[1].setText(str(random.randrange(0, 32)))
        self.tbUI.getIvsList()[2].setText(str(random.randrange(0, 32)))
        self.tbUI.getIvsList()[3].setText(str(random.randrange(0, 32)))
        self.tbUI.getIvsList()[4].setText(str(random.randrange(0, 32)))
        self.tbUI.getIvsList()[5].setText(str(random.randrange(0, 32)))

        self.updateStats()
        self.finalizePokemon()
        return


    #################################### Helper Functions #################################

    def setupGame(self):
        self.tbUI.getStartBattlePushButton().setEnabled(True)
        self.tbUI.getRestartBattlePushButton().setEnabled(True)
        self.tbUI.getDifferentTeamsPushButton().setEnabled(True)
        # self.pushSwitchPlayer1.setEnabled(True)
        # self.pushSwitchPlayer2.setEnabled(True)
        return

    def finalizePokemon(self):
        enableFlag = 1
        if (self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText()) == None):
            enableFlag = 0

        evTotal = 0
        try:
            levelNum = int(self.tbUI.getChosenLevelTextBox().displayText())
            happinessVal = int(self.tbUI.getHappinessValueTextBox().displayText())

            if (happinessVal < 0 or happinessVal > 255):
                enableFlag = 0

            if (levelNum < 1 or levelNum > 100):
                enableFlag = 0

            for i in range(6):
                evValue = int(self.tbUI.getEvsList()[i].displayText())
                ivValue = int(self.tbUI.getIvsList()[i].displayText())

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
            self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(True)
        else:
            self.tbUI.getPokemonSetupFinishedPushButton().setEnabled(False)

        self.checkPlayerTeams()

        return

    def updateStats(self):
        if (self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText()) == None):
            return
        pokemon = self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText())
        # if (self.txtFinal_HP.isEnabled() == False):
        #   return

        natureIndex = self.tbUI.getNaturesCombinationBox().currentIndex()
        increasedStat, decreasedStat = self.natureEffects[natureIndex]
        # level = int(self.txtChosenLevel.displayText())

        for i in range(6):
            statChange = 1

            try:
                ivValue = int(self.tbUI.getIvsList()[i].displayText())
                evValue = int(self.tbUI.getEvsList()[i].displayText())
                level = int(self.tbUI.getChosenLevelTextBox().displayText())
                if (i == 0):
                    self.tbUI.getFinalStats()[i].setText(str(math.floor(math.floor(((2 * int(pokemon.baseStats[i]) + ivValue + (
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
                    self.tbUI.getFinalStats()[i].setText(str(math.floor(((math.floor(((2 * int(
                        pokemon.baseStats[i]) + ivValue + math.floor(evValue / 4)) * level) / 100)) + 5) * statChange)))
            except:
                self.tbUI.getFinalStats()[i].setText(str(pokemon.baseStats[i]))

    def resetDetails(self):
        self.listInternalMoves = []
        self.listInternalAbilities = []
        self.chosenMovesetMap = {}

        self.tbUI.getChosenMovesListBox().clear()
        self.tbUI.getAvailableMovesCombinationBox().clear()
        self.tbUI.getAvailableAbilitiesCombinationBox().clear()
        self.tbUI.getGendersCombinationBox().clear()

        self.tbUI.getChosenMovesListBox().addItem("Move 1:")
        self.tbUI.getChosenMovesListBox().addItem("Move 2:")
        self.tbUI.getChosenMovesListBox().addItem("Move 3:")
        self.tbUI.getChosenMovesListBox().addItem("Move 4:")

        for i in range(6):
            self.tbUI.getFinalStats()[i].setText("")

        return

    def clearGUI(self):
        # Clear Details
        self.resetDetails()
        self.tbUI.getPokedexEntryTextBox().setText("")
        self.tbUI.getChosenLevelTextBox().setText("")
        self.tbUI.getHappinessValueTextBox().setText("")

        for i in range(6):
            self.tbUI.getEvsList()[i].setText("")
            self.tbUI.getIvsList()[i].setText("")

        return

    def updateAbilities(self):
        pokemon = self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText())
        self.tbUI.comboAvailableAbilities.clear()

        count = 0
        for ability in pokemon.abilities:
            idNum, displayName, description = self.pokemonMetadata.getAbilitiesMetadata().get(ability)
            self.tbUI.getAvailableAbilitiesCombinationBox().addItem(displayName)
            self.tbUI.getAvailableAbilitiesCombinationBox().setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(ability)
            count += 1

        if (pokemon.hiddenAbility != ""):
            idNum, displayName, description = self.pokemonMetadata.getAbilitiesMetadata().get(pokemon.hiddenAbility)
            self.tbUI.getAvailableAbilitiesCombinationBox().addItem(displayName)  # ("HA: " + displayName)
            self.tbUI.getAvailableAbilitiesCombinationBox().setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalAbilities.append(pokemon.hiddenAbility)

        return

    def updatePokemonMoves(self):
        pokemon = self.pokemonMetadata.getPokedex().get(self.tbUI.getPokedexEntryTextBox().displayText())
        self.tbUI.getAvailableMovesCombinationBox().clear()

        count = 0
        for move in pokemon.moves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(
                move)
            _, typeName, _, _, _ = self.pokemonMetadata.getTypesMetadata().get(typeMove)
            self.tbUI.getAvailableMovesCombinationBox().addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.tbUI.getAvailableMovesCombinationBox().setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + " " + "Power: " + basePower + "\t" +  "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        for move in pokemon.eggMoves:
            _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(
                move)
            _, typeName, _, _, _ = self.pokemonMetadata.getTypesMetadata().get(typeMove)
            self.tbUI.getAvailableMovesCombinationBox().addItem("Move: " + moveName)
            stringToolTip = "Base Power: " + basePower + "\nPP: " + totalPP + "\nType: " + typeMove + "\nDamage Category: " + damageCategory + "\nAccuracy: " + accuracy + "\nDescription: " + description
            self.tbUI.getAvailableMovesCombinationBox().setItemData(count, stringToolTip, QtCore.Qt.ToolTipRole)
            # self.comboAvailableMoves.addItem("Move: " + moveName + "\t" + "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\t" + "Damage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy)
            # self.comboAvailableMoves.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.listInternalMoves.append(move)
            count += 1

        return

    def updateGenders(self):
        pokedexEntry = self.tbUI.getPokedexEntryTextBox().displayText()
        pokemonObject = self.pokemonMetadata.getPokedex().get(pokedexEntry)
        self.tbUI.getGendersCombinationBox().clear()
        if (len(pokemonObject.genders) != 0):
            if ("MALE" in pokemonObject.genders):
                self.tbUI.getGendersCombinationBox().addItem("Male")
            if ("FEMALE" in pokemonObject.genders):
                self.tbUI.getGendersCombinationBox().addItem("Female")
        else:
            self.tbUI.getGendersCombinationBox().addItem("Genderless")

 

    def disableDetails(self):
        self.tbUI.pushFinished.setEnabled(False)

        for i in range(6):
            self.tbUI.getEvsList()[i].setEnabled(False)
            self.tbUI.getIvsList()[i].setEnabled(False)

        self.tbUI.getRandomizeEVsPushButton().setEnabled(False)
        self.tbUI.getRandomizeIVsPushButton().setEnabled(False)

        self.tbUI.getAddMovePushButton().setEnabled(False)

        return

    def enableDetails(self):
        # self.pushFinished.setEnabled(True)

        for i in range(6):
            self.tbUI.getEvsList()[i].setEnabled(True)
            self.tbUI.getIvsList()[i].setEnabled(True)

        self.tbUI.getRandomizeEVsPushButton().setEnabled(True)
        self.tbUI.getRandomizeIVsPushButton().setEnabled(True)

        self.tbUI.getAddMovePushButton().setEnabled(True)
        return

