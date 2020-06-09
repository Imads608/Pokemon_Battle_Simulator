from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats

from PyQt5 import QtCore, QtGui, QtWidgets
import time
from pubsub import pub

class SinglesBattleObserver(object):
    def __init__(self, widgets, pokemonDAL, battleProperties):
        self.battleWidgets = widgets
        self.pokemonDAL = pokemonDAL
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
        if (int(pokemonB.getBattleStat(Stats.HP)) <= int(int(pokemonB.getGivenStat(Stats.HP)) / 2) and int(
                pokemonB.getBattleStat(Stats.HP)) >= int(int(pokemonB.getGivenStat(Stats.HP)) / 5)):
            lbl_hpPokemon.setStyleSheet("color: rgb(255, 255, 0);")
        elif (int(pokemonB.getBattleStat(Stats.HP)) <= int(int(pokemonB.getGivenStat(Stats.HP)) / 5)):
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

    def displayPokemonInfoHandler(self, playerBattler, pokemonIndex=None):
        self.battleProperties.getLockMutex().lock()
        self.displayPokemonInfoListener(playerBattler, pokemonIndex)
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

        if (pokemonBattler.getBattleStat(Stats.HP) - amount < 0):
            targetPokemonHP = 0
        else:
            targetPokemonHP = pokemonBattler.getBattleStat(Stats.HP) - amount

        QtCore.QCoreApplication.processEvents()
        while (pokemonBattler.getBattleStat(Stats.HP) > targetPokemonHP):
            time.sleep(0.1)
            QtCore.QCoreApplication.processEvents()
            pokemonBattler.setBattleStat(Stats.HP, pokemonBattler.getBattleStat(Stats.HP) - 1)
            hpWidget.setValue(pokemonBattler.getBattleStat(Stats.HP))
            hpWidget.setToolTip(str(pokemonBattler.getBattleStat(Stats.HP)) + "/" + str(pokemonBattler.getGivenStat(Stats.HP)))
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
        targetHP = pokemonBattler.getBattleStat(Stats.HP) + amount
        hpWidget = self.battleWidgets.getPokemonHPBar(playerNum)
        lblPokemonHP = self.battleWidgets.getPokemonHPLabel(playerNum)

        if (pokemonBattler.getBattleStat(Stats.HP) + amount > pokemonBattler.getGivenStat(Stats.HP)):
            targetHP = pokemonBattler.getGivenStat(Stats.HP)

        while (pokemonBattler.getBattleStat(Stats.HP) != targetHP):
            pokemonBattler.getBattleStats()[Stats.HP] += 0.0000001
            hpWidget.setValue(pokemonBattler.getBattleStat(Stats.HP))
            self.showPlayerPokemonHP(pokemonBattler, lblPokemonHP)
        if (message != None):
            self.updateBattleInfoListener(message)

    def showPokemonStatusConditionListener(self, playerNum, pokemonBattler, message=None):
        # Status Condition Color Codes
        lbl_statusCond = self.battleWidgets.getStatusConditionLabel(playerNum)
        statusCondition = pokemonBattler.getNonVolatileStatusCondition()
        #lbl_statusCond.setText(self.battleProperties.getStatusConditions()[statusIndex])
        if(pokemonBattler.getIsFainted() == True):
            lbl_statusCond.setText("Fainted")
            lbl_statusCond.setStyleSheet("color: rgb(220, 20, 60);")
        if (statusCondition == NonVolatileStatusConditions.HEALTHY):
            lbl_statusCond.setText("Healthy")
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 0);")
        elif (statusCondition == NonVolatileStatusConditions.POISONED):
            lbl_statusCond.setText("Poisoned")
            lbl_statusCond.setStyleSheet("color: rgb(148, 0, 211);")
        elif (statusCondition == NonVolatileStatusConditions.BADLY_POISONED):
            lbl_statusCond.setText("Badly Poisoned")
            lbl_statusCond.setStyleSheet("color: rgb(128, 0, 128);")
        elif (statusCondition == NonVolatileStatusConditions.PARALYZED):
            lbl_statusCond.setText("Paralyzed")
            lbl_statusCond.setStyleSheet("color: rgb(255, 255, 0);")
        elif (statusCondition == NonVolatileStatusConditions.ASLEEP):
            lbl_statusCond.setText("Asleep")
            lbl_statusCond.setStyleSheet("color: rgb(128, 128, 128);")
        elif (statusCondition == NonVolatileStatusConditions.FROZEN):
            lbl_statusCond.setText("Frozen")
            lbl_statusCond.setStyleSheet("color: rgb(0, 255, 255);")
        elif (statusCondition == NonVolatileStatusConditions.BURN):
            lbl_statusCond.setText("Burned")
            lbl_statusCond.setStyleSheet("color: rgb(255, 0, 0);")

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
        #switchPokemon = self.battleWidgets.getSwitchPlayerPokemonPushButton(playerBattler.getPlayerNumber())
        #lbl_statusCond = self.battleWidgets.getStatusConditionLabel(playerBattler.getPlayerNumber())

        #if (self.battleProperties.getIsFirstTurn() == True):
        #    self.showPokemonImage(viewPokemon, None, None)
        #    return
        if (pokemonIndex == None):
            index = listPlayerTeam.currentRow()
        else:
            index = pokemonIndex
        pokemonBattler = playerTeam[index]

        self.showPokemonImage(viewPokemon, pokemonBattler.getPokedexEntry(), self.pokemonDAL.getPokedex())
        hpBar_Pokemon.setRange(0, int(pokemonBattler.getGivenStat(Stats.HP)))
        hpBar_Pokemon.setValue(int(pokemonBattler.getBattleStat(Stats.HP)))
        hpBar_Pokemon.setToolTip(str(pokemonBattler.getBattleStat(Stats.HP)) + "/" + str(pokemonBattler.getGivenStat(Stats.HP)))

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
        elif (playerBattler.getCurrentPokemon() == None):
            listPokemonMoves.setEnabled(False)
        elif (pokemonBattler.getIsFainted() == False):
            listPokemonMoves.setEnabled(True)
        #listPokemonMoves.setEnabled(False)
    
        for i in range(5):
            if (pokemonBattler.getInternalMovesMap().get(i) != None):
                pokemonMove = pokemonBattler.getInternalMovesMap()[i]
                listPokemonMoves.setCurrentRow(i - 1)
                moveDefinition = self.pokemonDAL.getMoveDefinitionForInternalName(pokemonMove.internalName)
                listPokemonMoves.currentItem().setText("Move " + str(i) + ": " + pokemonMove.name + "\t\tPP: " + str(pokemonMove.ppLeft) + "/" + str(pokemonMove.totalPP))
                listPokemonMoves.currentItem().setToolTip("Power: " + str(pokemonMove.power) + "\t" + "PP: " + str(pokemonMove.totalPP) + "\t" + "Type: " + pokemonMove.type + "\tDamage Category: " +
                                                          self.battleProperties.getDamageCategoryStringFromEnum(pokemonMove.damageCategory) +
                                                          "\t" + "Accuracy: " + str(moveDefinition.accuracy) + "\n" + str(moveDefinition.accuracy))

        listPokemonMoves.clearSelection()
        listPlayerTeam.clearSelection()
        return

    def addPokemonToTeamListener(self, playerNumber, pokemon, placementIndex):
        pokemonName = self.pokemonDAL.getPokedexEntryForNumber(pokemon.getPokedexEntry()).pokemonName
        self.battleWidgets.getPlayerTeamListBox(playerNumber).addItem(pokemonName)
        abilityDefinition = self.pokemonDAL.getAbilityDefinitionForInternalName(pokemon.getInternalAbility())
        itemDefinition = self.pokemonDAL.getItemDefinitionForInternalName(pokemon.getInternalItem())
        self.battleWidgets.getPlayerTeamListBox(playerNumber).item(placementIndex).setToolTip("Ability:\t\t" + abilityDefinition.name + "\n" +
                                                                         "Nature:\t\t" + pokemon.getNature() + "\n" +
                                                                         "Item:\t\t" + itemDefinition.name + "\n\n" +
                                                                         "HP:\t\t" + str(pokemon.getGivenStat(Stats.HP)) + "\n" +
                                                                         "Attack:\t\t" + str(pokemon.getGivenStat(Stats.ATTACK)) + "\n" +
                                                                         "Defense:\t" + str(pokemon.getGivenStat(Stats.DEFENSE)) + "\n" +
                                                                         "SpAttack:\t" + str(pokemon.getGivenStat(Stats.SPATTACK)) + "\n" +
                                                                         "SpDefense:\t" + str(pokemon.getGivenStat(Stats.SPDEFENSE)) + "\n" +
                                                                         "Speed:\t\t" + str(pokemon.getGivenStat(Stats.SPEED)))
        
    def togglePokemonSwitchListener(self, playerNum, toggleVal):
        self.battleWidgets.getSwitchPlayerPokemonPushButton(playerNum).setEnabled(toggleVal)
    
    def toggleStartBattleListener(self, toggleVal):
        self.battleWidgets.getStartBattlePushButton().setEnabled(toggleVal)
    
    def togglePokemonMovesSelectionListener(self, playerNum, toggleVal):
        self.battleWidgets.getPokemonMovesListBox(playerNum).setEnabled(toggleVal)
    
    def togglePokemonSelectionListener(self, playerNum, toggleVal):
        self.battleWidgets.getPlayerTeamListBox(playerNum).setEnabled(toggleVal)
    
    def setCurrentPokemonListener(self, pokemonIndex, playerBattler):
        pokemonBattlerChosen = playerBattler.getPokemon(pokemonIndex)
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
            switch.setCurrentPokemonSpeed(switch.getPlayerBattler().getPokemon(index).getBattleStat(Stats.SPEED))
            switch.getPlayerBattler().setCurrentPokemon(switch.getPlayerBattler().getPokemon(index))
            self.showPokemonImage(self.battleWidgets.getPokemonView(playerNum), None, None)
        return

    def pokemonMoveSelectedListener(self, pokemonBattler, move):
        index = self.battleWidgets.getPokemonMovesListBox(pokemonBattler.getPlayerNum()).currentRow()
        if (pokemonBattler.getInternalMovesMap().get(index+1) != None):
            pokemonMove = pokemonBattler.getInternalMovesMap().get(index+1)
            move.setMoveInternalName(pokemonMove.internalName)
            move.setMoveIndex(index)
        return

    def moveSelectedListener(self, pokemonBattler, playerNum):
        moveIndex = self.battleProperties.getPokemonMovesListBox(playerNum).currentRow()
        pokemonBattler.getInternalMovesMap().update({"chosen_index":moveIndex})
