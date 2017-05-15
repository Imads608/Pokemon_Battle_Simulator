import sys
from PySide.QtGui import *
from battle_simulator import Ui_MainWindow
import scipy as sp
from scipy import misc
import base64
import re
import random
import pokemon_database
import createPokemon
import PySide.QtCore
import random

class battleConsumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(battleConsumer, self).__init__(parent)
        self.setupUi(self)

        # Variables Used
        # Get pokedex Data
        self.pokedex = pokemon_database.getPokemonDetails()
        self.chosenPokemon = None
        self.EVsDone = 0
        self.EVsTotal = 0
        self.maxEVs = 0

        # Disable text boxes of the GUI
        # Tab 1
        # Pokemon 1
        self.txtPokemon1_Level.setEnabled(False)
        self.txtPokemon1_Nature.setEnabled(False)
        self.txtPokemon1_Ability.setEnabled(False)
        self.txtPokemon1_HP.setEnabled(False)

        # Pokemon 2
        self.txtPokemon2_Level.setEnabled(False)
        self.txtPokemon2_Nature.setEnabled(False)
        self.txtPokemon2_Ability.setEnabled(False)
        self.txtPokemon2_HP.setEnabled(False)

        # Other info
        self.txtBattleInfo.setEnabled(False)

        # Battle Type Changed
        #print(self.comboBattleType.currentText())
        self.comboBattleType.currentIndexChanged.connect(self.updateBattleType)

        # Entry Updated
        self.txtPokedexEntry.textChanged.connect(self.updateEntry)

        # Level Updated
        self.txtChosenLevel.textChanged.connect(self.updateLevel)

        # EVs updated
        self.txtEV_HP.textChanged.connect(lambda:self.updateEVs("HP", self.txtEV_HP.displayText()))
        self.txtEV_Attack.textChanged.connect(lambda:self.updateEVs("Attack", self.txtEV_Attack.displayText()))
        self.txtEV_Defense.textChanged.connect(lambda:self.updateEVs("Defense", self.txtEV_Defense.displayText()))
        self.txtEV_SpAttack.textChanged.connect(lambda:self.updateEVs("SpAttack", self.txtEV_SpAttack.displayText()))
        self.txtEV_SpDefense.textChanged.connect(lambda:self.updateEVs("SpDefense", self.txtEV_SpDefense.displayText()))
        self.txtEV_Speed.textChanged.connect(lambda:self.updateEVs("Speed", self.txtEV_Speed.displayText()))

        # Randomize EVs
        self.pushRandomizeEVs.clicked.connect(self.randomizeEVs)

        # IVs updated
        self.txtIV_HP.textChanged.connect(lambda:self.updateIVs("HP", self.txtIV_HP.displayText()))
        self.txtIV_Attack.textChanged.connect(lambda:self.updateIVs("Attack", self.txtIV_Attack.displayText()))
        self.txtIV_Defense.textChanged.connect(lambda:self.updateIVs("Defense", self.txtIV_Defense.displayText()))
        self.txtIV_SpAttack.textChanged.connect(lambda:self.updateIVs("SpAttack", self.txtIV_SpAttack.displayText()))
        self.txtIV_SpDefense.textChanged.connect(lambda:self.updateIVs("SpDefense", self.txtIV_SpDefense.displayText()))
        self.txtIV_Speed.textChanged.connect(lambda:self.updateIVs("Speed", self.txtIV_Speed.displayText()))

        # Randomize IVs
        self.pushRandomizeIVs.clicked.connect(self.randomizeIVs)

    def randomizeIVs(self):

        self.txtIV_HP.setText(str(random.randrange(0, 32)))

        self.txtIV_Attack.setText(str(random.randrange(0, 32)))

        self.txtIV_Defense.setText(str(random.randrange(0, 32)))

        self.txtIV_SpAttack.setText(str(random.randrange(0, 32)))

        self.txtIV_SpDefense.setText(str(random.randrange(0, 32)))

        self.txtIV_Speed.setText(str(random.randrange(0, 32)))

    def updateIVs(self, stat, value):
        exception1 = 0
        try:
            statVal = int(value)
            if (statVal > 31):
                if (stat == "HP"):
                    self.txtIV_HP.setText("31")
                elif (stat == "Attack"):
                    self.txtIV_Attack.setText("31")
                elif (stat == "Defense"):
                    self.txtIV_Defense.setText("31")
                elif (stat == "SpAttack"):
                    self.txtIV_SpAttack.setText("31")
                elif (stat == "SpDefense"):
                    self.txtIV_SpDefense.setText("31")
                else:
                    self.txtIV_Speed.setText("31")
            self.labelEVCheck.setText("")
        except:
            exception1 = 1
            self.labelEVCheck.setText("Must be a number!")

        try:
            total = int(self.txtIV_HP.displayText()) + int(self.txtIV_Attack.displayText()) + int(self.txtIV_Defense.displayText())\
                    + int(self.txtIV_SpAttack.displayText()) + int(self.txtIV_SpDefense.displayText()) + int(self.txtIV_Speed.displayText())
            if (total > 31*6):
                self.labelIVCheck.setText("Total must be within 186")
            else:
                self.labelIVCheck.setText("")
        except:
            self.labelIVCheck.setText("Must be a number!")


    def randomizeEVs(self):
        total = 0

        while (total != 510):
            total = 0
            self.txtEV_HP.setText(str(random.randrange(0, 256)))
            total += int(self.txtEV_HP.displayText())
            #print(total)

            self.txtEV_Attack.setText(str(random.randrange(0, 256)))
            total += (int(self.txtEV_Attack.displayText()))
            #print(total)

            self.txtEV_Defense.setText(str(random.randrange(0, min(256,510 - total + 1))))
            total += (int(self.txtEV_Defense.displayText()))
            #print(total)

            self.txtEV_SpAttack.setText(str(random.randrange(0, min(256,510 - total + 1))))
            total += (int(self.txtEV_SpAttack.displayText()))
            #print(total)

            self.txtEV_SpDefense.setText(str(random.randrange(0, min(256,510 - total + 1))))
            total += (int(self.txtEV_SpDefense.displayText()))
            #print(total)

            self.txtEV_Speed.setText(str(random.randrange(0, min(256,510 - total + 1))))
            total += (int(self.txtEV_Speed.displayText()))


    def updateEVs(self, stat, value):
        exception1 = 0
        try:
            statVal = int(value)
            self.labelEVCheck.setText("")
        except:
            exception1 = 1
            self.labelEVCheck.setText("Must be a number!")

        try:
            total = int(self.txtEV_HP.displayText()) + int(self.txtEV_Attack.displayText()) + int(self.txtEV_Defense.displayText())\
                    + int(self.txtEV_SpAttack.displayText()) + int(self.txtEV_SpDefense.displayText()) + int(self.txtEV_Speed.displayText())
            if (total != 510):
                self.labelEVCheck.setText("Total must be 510")
            else:
                self.labelEVCheck.setText("")
        except:
            self.labelEVCheck.setText("Must be a number!")


    def updateLevel(self):
        try:
            levelVal = int(self.txtChosenLevel.displayText())
            if (levelVal > 0 and levelVal <= 100):
                self.labelLevelCheck.setText("")
            else:
                self.labelLevelCheck.setText("Range: 1 - 100")
        except:
            self.labelLevelCheck.setText("Must be a number!")


    def updateBattleType(self):
        print(self.comboBattleType.currentText())

    def updateEntry(self):
        entryNum = self.txtPokedexEntry.displayText()
        try:
            int(entryNum)
            self.labelEntryCheck.setText("")
            self.chosenPokemon = entryNum
            self.displayPokemon(self.viewCurrentPokemon)
        except:
            self.labelEntryCheck.setText("Must be a number!")
            self.chosenPokemon = ""
            self.displayPokemon(self.viewCurrentPokemon)

    def displayPokemon(self, viewPokemon):
        pokemonImageScene = QGraphicsScene()

        chosenPokemon = self.pokedex.get(self.chosenPokemon)
        if (chosenPokemon != None):
            pixmap = QPixmap(chosenPokemon.image)
            pokemonImageScene.addPixmap(pixmap)
            pixItem = QGraphicsPixmapItem(pixmap)
            viewPokemon.setScene(pokemonImageScene)
            viewPokemon.fitInView(pixItem, PySide.QtCore.Qt.KeepAspectRatio)
        else:
            scene = QGraphicsScene()
            viewPokemon.setScene(scene)
            viewPokemon.show()
        return

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = battleConsumer()

    currentForm.show()
    currentApp.exec_()
