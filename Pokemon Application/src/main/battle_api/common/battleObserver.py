from PyQt5 import QtCore, QtGui, QtWidgets
import time
from pubsub import pub

class BattleObserver(object):
    def __init__(self, widgets, pokemonMetadata, battleProperties):
        self.battleWidgets = widgets
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None

        widgets.getBattleInfoTextBox().setAlignment(QtCore.Qt.AlignHCenter)
        self.startListeners()

    ######### Helpers ##############
    def startListeners(self):
        pub.subscribe(self.battleWidgetsSignaslBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())
        pub.subscribe(self.updateBattleInfoListener, self.battleProperties.getUpdateBattleInfoTopic())
        pub.subscribe(self.showPokemonDamageListener, self.battleProperties.getShowDamageTopic())
        pub.subscribe(self.showPokemonHealingListener, self.battleProperties.getShowHealingTopic())
        pub.subscribe(self.showPokemonStatusConditionListener, self.battleProperties.getShowStatusConditionTopic())
        pub.subscribe(self.alertPlayerListener, self.battleProperties.getAlertPlayerTopic())
        pub.subscribe(self.displayPokemonInfoListener, self.battleProperties.getDisplayPokemonInfoTopic())
        pub.subscribe(self.addPokemonToTeamListener, self.battleProperties.getAddPokemonToTeamTopic())
        pub.subscribe(self.togglePokemonSwitchListener, self.battleProperties.getToggleSwitchPokemonTopic())
        pub.subscribe(self.toggleStartBattleListener, self.battleProperties.getToggleStartBattleTopic())
        pub.subscribe(self.togglePokemonMovesSelectionListener, self.battleProperties.getTogglePokemonMovesSelectionTopic())
        pub.subscribe(self.togglePokemonSelectionListener, self.battleProperties.getTogglePokemonSelectionTopic())
        pub.subscribe(self.setCurrentPokemonListener, self.battleProperties.getSetCurrentPokemonTopic())
        pub.subscribe(self.pokemonSwitchSelectedListener, self.battleProperties.getPokemonSwitchTopic())
        pub.subscribe(self.pokemonMoveSelectedListener, self.battleProperties.getPokemonMoveSelectedTopic())

    def showPlayerPokemonHP(self, pokemonB, lbl_hpPokemon):
        lbl_hpPokemon.setStyleSheet("color: rgb(0, 255, 0);")
        if (int(pokemonB.getBattleStats()[0]) <= int(int(pokemonB.getFinalStats()[0]) / 2) and int(
                pokemonB.getBattleStats()[0]) >= int(int(pokemonB.getFinalStats()[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.getBattleStats()[0]) <= int(int(pokemonB.getFinalStats()[0]) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 0, 0);")

    def showPokemonImage(self, viewPokemon, pokedexEntry, pokedex):
        if (pokedexEntry != None):
            pokemonImageScene = QtWidgets.QGraphicsScene()
            pokemon = pokedex.get(pokedexEntry)
            pixmap = QtGui.QPixmap(pokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem = QtWidgets.QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, QtCore.Qt.KeepAspectRatio)
        else:
            scene = QtWidgets.QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()

    ########### Battle Widget Signals Connectors #################
    def setupBattleSignalsConnectors(self):
        self.battleWidgetsSignals.getPokemonHPDecreaseSignal().connect(self.pokemonHPDamageHandler)
        self.battleWidgetsSignals.getPokemonHPIncreaseSignal().connect(self.pokemonHPHealHandler)
        self.battleWidgetsSignals.getBattleMessageSignal().connect(self.battleInfoUpdateHandler)
        self.battleWidgetsSignals.getPokemonSwitchedSignal().connect(self.pokemonSwitchedHandler)
        self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().connect(self.pokemonStatusConditionHandler)
        self.battleWidgetsSignals.getTogglePokemonSelectionSignal().connect(self.togglePokemonSelectionHandler)
        self.battleWidgetsSignals.getTogglePokemonSwitchSignal().connect(self.togglePokemonSwitchHandler)
        self.battleWidgetsSignals.getTogglePokemonMovesSelectionSignal().connect(self.togglePokemonMovesSelectionHandler)
        self.battleWidgetsSignals.getDisplayPokemonInfoSignal().connect(self.displayPokemonInfoHandler)
        #self.battleWidgetsSignals.getPokemonFaintedSignal().connect(self.pokemonFaintedHandler)

    def pokemonHPDamageHandler(self, playerNum, pokemonBattler, amount, message):
        self.battleProperties.getLockMutex().lock()
        self.showPokemonDamageListener(playerNum, pokemonBattler, amount, message)
        self.battleProperties.getLockMutex().unlock()

    def pokemonHPHealHandler(self, playerNum, pokemonBattler, amount, message):
        self.battleProperties.getLockMutex().lock()
        self.showPokemonHealingListener(playerNum, pokemonBattler, amount, message)
        self.battleProperties.getLockMutex().unlock()

    def battleInfoUpdateHandler(self, message):
        self.battleProperties.getLockMutex().lock()
        self.updateBattleInfoListener(message)
        self.battleProperties.getLockMutex().unlock()

    def pokemonSwitchedHandler(self, switchedPokemonIndex, playerBattler, message):
        self.battleProperties.getLockMutex().lock()
        self.setCurrentPokemonListener(switchedPokemonIndex, playerBattler)
        self.displayPokemonInfoListener(playerBattler)
        self.battleWidgets.getPokemonMovesListBox(playerBattler.getPlayerNumber()).setEnabled(False)
        if (message != None):
            self.updateBattleInfoListener(message)
        self.battleProperties.getLockMutex().unlock()

    def pokemonStatusConditionHandler(self, playerNum, pokemonBattler, message):
        self.battleProperties.getLockMutex().lock()
        self.showPokemonStatusConditionListener(playerNum, pokemonBattler, message)
        self.battleProperties.getLockMutex().unlock()

    def togglePokemonSelectionHandler(self, playerNum, toggleVal):
        self.battleProperties.getLockMutex().lock()
        self.togglePokemonSelectionListener(playerNum, toggleVal)
        self.battleProperties.getLockMutex().unlock()

    def togglePokemonSwitchHandler(self, playerNum, toggleVal):
        self.battleProperties.getLockMutex().lock()
        self.togglePokemonSwitchListener(playerNum, toggleVal)
        self.battleProperties.getLockMutex().unlock()

    def togglePokemonMovesSelectionHandler(self, playerNum, toggleVal):
        self.battleProperties.getLockMutex().lock()
        self.togglePokemonMovesSelectionListener(playerNum, toggleVal)
        self.battleProperties.getLockMutex().unlock()

    def displayPokemonInfoHandler(self, playerBattler):
        self.battleProperties.getLockMutex().lock()
        self.displayPokemonInfoListener(playerBattler)
        self.battleProperties.getLockMutex().unlock()

    def pokemonFaintedHandler(self, playerNum):
        self.battleProperties.getLockMutex().lock()
        self.battleWidgets.getPlayerTeamListBox(playerNum).setEnabled(True)
        self.battleWidgets.getSwitchPlayerPokemonPushButton(playerNum).setEnabled(True)
        self.battleProperties.getLockMutex().unlock()

    ########### Listeners #############
    def battleWidgetsSignaslBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals
        self.setupBattleSignalsConnectors()

    def updateBattleInfoListener(self, message):
        self.battleWidgets.getBattleInfoTextBox().append(message)

    def showPokemonDamageListener(self, playerNum, pokemonBattler, amount, message=None):
        hpWidget = self.battleWidgets.getPokemonHPBar(playerNum)
        lblPokemonHP = self.battleWidgets.getPokemonHPLabel(playerNum)

        if (pokemonBattler.getBattleStats()[0] - amount < 0):
            damage = pokemonBattler.getBattleStats()[0]
            targetPokemonHP = 0
        else:
            damage = amount
            targetPokemonHP = pokemonBattler.getBattleStats()[0] - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemonBattler.getBattleStats()[0] > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemonBattler.getBattleStats()[0] -= 1
            hpWidget.setValue(pokemonBattler.getBattleStats()[0])
            hpWidget.setToolTip(str(pokemonBattler.getBattleStats()[0]) + "/" + str(pokemonBattler.getFinalStats()[0]))
            self.showPlayerPokemonHP(pokemonBattler, lblPokemonHP)

        if (targetPokemonHP == 0):
            pokemonBattler.setIsFainted(True)
        if (message != None):
            self.updateBattleInfoListener(message)
        if (pokemonBattler.getIsFainted() == True):
            self.updateBattleInfoListener(pokemonBattler.getName() + " fainted")
            # TODO: Check Item Effects
        return

    def showPokemonHealingListener(self, playerNum, pokemonBattler, amount, message=None):
        targetHP = pokemonBattler.getBattleStats()[0] + amount
        hpWidget = self.battleWidgets.getPokemonHPBar(playerNum)
        lblPokemonHP = self.battleWidgets.getPokemonHPLabel(playerNum)

        while (pokemonBattler.getBattleStats()[0] != targetHP):
            pokemonBattler.getBattleStats()[0] += 0.0000001
            hpWidget.setValue(pokemonBattler.getBattleStats()[0])
            self.showPlayerPokemonHP(pokemonBattler, lbl_hpPokemon)
        if (message != None):
            self.updateBattleInfoListener(message)

    def showPokemonStatusConditionListener(self, playerNum, pokemonBattler, message=None):
        # Status Condition Color Codes
        lbl_statusCond = self.battleWidgets.getStatusConditionLabel(playerNum)
        statusIndex = pokemonBattler.getNonVolatileStatusConditionIndex()
        lbl_statusCond.setText(self.battleProperties.getStatusConditions()[statusIndex])
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
        if (pokemonBattler.getIsFainted() == True):
            lbl_statusCond.setText("Fainted")

        if (message != None):
            self.updateBattleInfoListener(message)

    def alertPlayerListener(self, header, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(header)
        msg.setInformativeText(body)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #button = msg.button(QtWidgets.QMessageBox.Ok) ### Uncomment this for unit testing
        #QtCore.QTimer.singleShot(0, button.clicked)   ### Uncomment this for unit testing
        msg.exec_()

    def displayPokemonInfoListener(self, playerBattler, pokemonIndex=None):
        listPlayerTeam = self.battleWidgets.getPlayerTeamListBox(playerBattler.getPlayerNumber())
        playerTeam = playerBattler.getPokemonTeam()
        viewPokemon = self.battleWidgets.getPokemonView(playerBattler.getPlayerNumber())
        hpBar_Pokemon = self.battleWidgets.getPokemonHPBar(playerBattler.getPlayerNumber())
        txtPokemon_Level = self.battleWidgets.getPokemonLevelTextBox(playerBattler.getPlayerNumber())
        lbl_hpPokemon = self.battleWidgets.getPokemonHPLabel(playerBattler.getPlayerNumber())
        listPokemonMoves = self.battleWidgets.getPokemonMovesListBox(playerBattler.getPlayerNumber())
        switchPokemon = self.battleWidgets.getSwitchPlayerPokemonPushButton(playerBattler.getPlayerNumber())
        lbl_statusCond = self.battleWidgets.getStatusConditionLabel(playerBattler.getPlayerNumber())

        #if (self.battleProperties.getIsFirstTurn() == True):
        #    self.showPokemonImage(viewPokemon, None, None)
        #    return
        if (pokemonIndex == None):
            index = listPlayerTeam.currentRow()
        else:
            index = pokemonIndex
        pokemonBattler = playerTeam[index]

        self.showPokemonImage(viewPokemon, pokemonBattler.getPokedexEntry(), self.pokemonMetadata.getPokedex())
        hpBar_Pokemon.setRange(0, int(pokemonBattler.getFinalStats()[0]))
        hpBar_Pokemon.setValue(int(pokemonBattler.getBattleStats()[0]))
        hpBar_Pokemon.setToolTip(str(pokemonBattler.getBattleStats()[0]) + "/" + str(pokemonBattler.getFinalStats()[0]))

        # HP Color Code
        self.showPlayerPokemonHP(pokemonBattler, lbl_hpPokemon)

        # Status Condition Color Codes
        self.showPokemonStatusConditionListener(playerBattler.getPlayerNumber(), pokemonBattler)

        txtPokemon_Level.setText(pokemonBattler.level)

        listPokemonMoves.clear()
        listPokemonMoves.addItem("Move 1: ")
        listPokemonMoves.addItem("Move 2: ")
        listPokemonMoves.addItem("Move 3: ")
        listPokemonMoves.addItem("Move 4: ")

        if (listPlayerTeam.item(index).foreground() == QtCore.Qt.black):
            listPokemonMoves.setEnabled(False)
        elif (pokemonBattler.getIsFainted() == False):
            listPokemonMoves.setEnabled(True)
        #listPokemonMoves.setEnabled(False)
    
        for i in range(5):
            if (pokemonBattler.getInternalMovesMap().get(i) != None):
                internalMoveName, index, currPP = pokemonBattler.getInternalMovesMap().get(i)
                listPokemonMoves.setCurrentRow(i - 1)
                _, moveName, _, basePower, typeMove, damageCategory, accuracy, totalPP, description, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(
                    internalMoveName)
                _, typeName, _, _, _ = self.pokemonMetadata.getTypesMetadata().get(typeMove)
                listPokemonMoves.currentItem().setText(
                    "Move " + str(i) + ": " + moveName + "\t\tPP: " + str(currPP) + "/" + str(totalPP))
                listPokemonMoves.currentItem().setToolTip(
                    "Power: " + basePower + "\t" + "PP: " + totalPP + "\t" + "Type: " + typeName + "\tDamage Category: " + damageCategory + "\t" + "Accuracy: " + accuracy + "\n" + description)

        listPokemonMoves.clearSelection()
        listPlayerTeam.clearSelection()
        return

    def addPokemonToTeamListener(self, playerNumber, pokemon, placementIndex):
        pokemonName = self.pokemonMetadata.getPokedex().get(pokemon.getPokedexEntry()).pokemonName
        self.battleWidgets.getPlayerTeamListBox(playerNumber).addItem(pokemonName)
        _, abilityName, _ = self.pokemonMetadata.getAbilitiesMetadata().get(pokemon.getInternalAbility())
        itemName, _, _, _, _, _, _ = self.pokemonMetadata.getItemsMetadata().get(pokemon.getInternalItem())
        self.battleWidgets.getPlayerTeamListBox(playerNumber).item(placementIndex).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                                         "Nature:\t\t" + pokemon.getNature() + "\n" +
                                                                         "Item:\t\t" + itemName + "\n\n" +
                                                                         "HP:\t\t" + str(pokemon.getFinalStats()[0]) + "\n" +
                                                                         "Attack:\t\t" + str(pokemon.getFinalStats()[1]) + "\n" +
                                                                         "Defense:\t" + str(pokemon.getFinalStats()[2]) + "\n" +
                                                                         "SpAttack:\t" + str(pokemon.getFinalStats()[3]) + "\n" +
                                                                         "SpDefense:\t" + str(pokemon.getFinalStats()[4]) + "\n" +
                                                                         "Speed:\t\t" + str(pokemon.getFinalStats()[5]))
        
    def togglePokemonSwitchListener(self, playerNum, toggleVal):
        self.battleWidgets.getSwitchPlayerPokemonPushButton(playerNum).setEnabled(toggleVal)
    
    def toggleStartBattleListener(self, toggleVal):
        self.battleWidgets.getStartBattlePushButton().setEnabled(toggleVal)
    
    def togglePokemonMovesSelectionListener(self, playerNum, toggleVal):
        self.battleWidgets.getPokemonMovesListBox(playerNum).setEnabled(toggleVal)
    
    def togglePokemonSelectionListener(self, playerNum, toggleVal):
        self.battleWidgets.getPlayerTeamListBox(playerNum).setEnabled(toggleVal)
    
    def setCurrentPokemonListener(self, pokemonIndex, playerBattler):
        pokemonBattlerChosen = playerBattler.getPokemonTeam()[pokemonIndex]
        playerBattler.setCurrentPokemon(pokemonBattlerChosen)
        self.battleWidgets.getPlayerTeamListBox(playerBattler.getPlayerNumber()).setCurrentRow(pokemonIndex)
        listPlayerTeam = self.battleWidgets.getPlayerTeamListBox(playerBattler.getPlayerNumber())

        for i in range(listPlayerTeam.count()):
            if (i != pokemonIndex):
                listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
            else:
                listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)

        return

    def pokemonSwitchSelectedListener(self, playerNum, switch):
        index = self.battleWidgets.getPlayerTeamListBox(playerNum).currentRow()
        switch.setSwitchPokemonIndex(index)
        if (self.battleProperties.getIsFirstTurn() == True):
            switch.setCurrentPokemonIndex(index)
            switch.setCurrentPokemonSpeed(switch.getPlayerBattler().getPokemonTeam()[index].getBattleStats()[5])
            switch.getPlayerBattler().setCurrentPokemon(switch.getPlayerBattler().getPokemonTeam()[index])
            self.showPokemonImage(self.battleWidgets.getPokemonView(playerNum), None, None)
        return

    def pokemonMoveSelectedListener(self, pokemonBattler, move):
        index = self.battleWidgets.getPokemonMovesListBox(pokemonBattler.getPlayerNum()).currentRow()
        if (pokemonBattler.getInternalMovesMap().get(index+1) != None):
            internalMoveName, _, _ = pokemonBattler.getInternalMovesMap().get(index+1)
            move.setInternalMoveName(internalMoveName)
            move.setMoveIndex(index)
        return

    def moveSelectedListener(self, pokemonBattler, playerNum):
        moveIndex = self.battleProperties.getPokemonMovesListBox(playerNum).currentRow()
        pokemonBattler.getInternalMovesMap().update({"chosen_index":moveIndex})
