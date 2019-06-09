from PyQt5 import QtCore, QtGui, QtWidgets
import time
from pubsub import pub

class BattleObserver(object):
    def __init__(self, widgets, pokemonMetadata, battleProperties):
        self.battleWidgets = widgets
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties
        pub.subscribe(self.updateBattleInfoListener, battleProperties.getUpdateBattleInfoTopic())
        pub.subscribe(self.showPokemonDamageListener, battleProperties.getShowDamageTopic())
        pub.subscribe(self.showPokemonHealingListener, battleProperties.getShowHealingTopic())
        pub.subscribe(self.showPokemonStatusConditionListener, battleProperties.getShowStatusConditionTopic())
        pub.subscribe(self.alertPlayerListener, battleProperties.getAlertPlayerTopic())
        pub.subscribe(self.displayPokemonInfoListener, battleProperties.getDisplayPokemonInfoTopic())

    ######### Helpers ##############
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


    ########### Listeners #############
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

    def showPokemonStatusConditionListener(self, playerNum, pokemonBattler):
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

    def alertPlayerListener(self, header, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(header)
        msg.setInformativeText(body)
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("Pokemon Fainted")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    def displayPokemonInfoListener(self, playerBattler):
        playerWidgets = playerBattler.getPlayerWidgetShortcuts()
        listPlayerTeam = playerWidgets[1]
        playerTeam = playerWidgets[6]
        viewPokemon = self.battleWidgets.getPokemonView(playerBattler.getPlayerNumber())
        hpBar_Pokemon = playerWidgets[2]
        txtPokemon_Level = playerWidgets[4]
        lbl_hpPokemon = playerWidgets[7]
        listPokemonMoves = playerWidgets[0]
        switchPokemon = playerWidgets[5]
        lbl_statusCond = playerWidgets[8]

        index = listPlayerTeam.currentRow()
        pokemonBattler = playerTeam[index]

        for i in range(listPlayerTeam.count()):
            if (i != index):
                listPlayerTeam.item(i).setForeground(QtCore.Qt.black)
            else:
                listPlayerTeam.item(i).setForeground(QtCore.Qt.blue)
        
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
        
        listPokemonMoves.setEnabled(False)
    
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