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
import math

class battleConsumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(battleConsumer, self).__init__(parent)
        self.setupUi(self)

        # Variables Used
        # Get pokedex Data
        self.pokedex = pokemon_database.getPokemonDetails()
        self.types = pokemon_database.getTypes("types.csv")
        self.natures = pokemon_database.getNatures("natures.csv")
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

        # Update Moveset
        self.listChosenMoves.clicked.connect(self.updateMoveSet)

        #Update Nature
        self.comboNatures.currentIndexChanged.connect(lambda:self.getPokemonStats(self.txtPokedexEntry.displayText()))

    def updateMoveSet(self):
        widgetItem = self.listChosenMoves.currentItem()
        matchMoveName = r'[^ ]+'
        listMatches = re.findall(matchMoveName, self.comboAvailableMoves.currentText())
        print(listMatches)
        #print(widgetItem.text())
        print(self.listChosenMoves.currentRow())
        if (self.listChosenMoves.currentRow() == 0):
            widgetItem.setText("Move 1: " + listMatches[1])
        elif (self.listChosenMoves.currentRow() == 1):
            widgetItem.setText("Move 2: " + listMatches[1])
        elif (self.listChosenMoves.currentRow() == 2):
            widgetItem.setText("Move 3: " + listMatches[1])
        elif (self.listChosenMoves.currentRow() == 3):
            widgetItem.setText("Move 4: " + listMatches[1])
        #widgetItem.setText(widgetItem.text() + " " + listMatches[1])
        #print(self.comboAvailableMoves.currentText())

    def randomizeIVs(self):

        self.txtIV_HP.setText(str(random.randrange(0, 32)))

        self.txtIV_Attack.setText(str(random.randrange(0, 32)))

        self.txtIV_Defense.setText(str(random.randrange(0, 32)))

        self.txtIV_SpAttack.setText(str(random.randrange(0, 32)))

        self.txtIV_SpDefense.setText(str(random.randrange(0, 32)))

        self.txtIV_Speed.setText(str(random.randrange(0, 32)))

        self.getPokemonStats(self.txtPokedexEntry.displayText())

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
        self.getPokemonStats(self.txtPokedexEntry.displayText())

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
        self.getPokemonStats(self.txtPokedexEntry.displayText())

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

        self.getPokemonStats(self.txtPokedexEntry.displayText())


    def updateLevel(self):
        try:
            levelVal = int(self.txtChosenLevel.displayText())
            if (levelVal > 0 and levelVal <= 100):
                self.labelLevelCheck.setText("")
            else:
                self.labelLevelCheck.setText("Range: 1 - 100")
        except:
            self.labelLevelCheck.setText("Must be a number!")
        self.getPokemonStats(self.txtPokedexEntry.displayText())

    def updateBattleType(self):
        print(self.comboBattleType.currentText())

    def updateEntry(self):
        entryNum = self.txtPokedexEntry.displayText()
        try:
            int(entryNum)
            self.labelEntryCheck.setText("")
            self.chosenPokemon = entryNum
            self.displayPokemon(self.viewCurrentPokemon)
            self.getPokemonMoves(entryNum)
            self.getPokemonAbilities(entryNum)
            self.getPokemonStats(entryNum)
        except:
            self.labelEntryCheck.setText("Must be a number!")
            self.chosenPokemon = ""
            self.displayPokemon(self.viewCurrentPokemon)
            self.comboAvailableMoves.clear()
            self.comboAvailableAbilities.clear()

    def getPokemonStats(self, pokedexNum):
        pokemon = self.pokedex.get(pokedexNum)
        print("dsadasdas")
        statIDMap = {"1":"HP", "2":"Attack", "3":"Defense", "4":"Special Attack", "5":"Special Defense", "6":"Speed"}
        statChangesMap = {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1}
        finalHP = 0
        finalAttack = 0
        finalDefense = 0
        finalSpAtack = 0
        finalSpDefense = 0
        finalSpeed = 0
        #print(type(self.comboNatures.currentIndex()))
        nature_name,decreased_stat_id,increased_stat_id,_,_,_ = self.natures.get(str(self.comboNatures.currentIndex() + 1))
        #print(nature_name)
        if (decreased_stat_id != increased_stat_id):
            statChangesMap.update({decreased_stat_id:0.9})
            statChangesMap.update({increased_stat_id:1.1})

        try:
            # Test if IVs and EVs are fully filled
            total = int(self.txtEV_HP.displayText()) + int(self.txtEV_Attack.displayText()) + int(self.txtEV_Defense.displayText())\
                    + int(self.txtEV_SpAttack.displayText()) + int(self.txtEV_SpDefense.displayText()) + int(self.txtEV_Speed.displayText())

            total = int(self.txtIV_HP.displayText()) + int(self.txtIV_Attack.displayText()) + int(self.txtIV_Defense.displayText())\
                    + int(self.txtIV_SpAttack.displayText()) + int(self.txtIV_SpDefense.displayText()) + int(self.txtIV_Speed.displayText())

            finalHP = int(math.floor(((2*float(pokemon.stats.get("HP")) + float(self.txtIV_HP.displayText()) +
                                   float(self.txtEV_HP)/4)*float(self.txtChosenLevel))/100 + float(self.txtChosenLevel) + 10))
            finalAttack = int(math.floor((((2*float(pokemon.stats.get("Attack")) + float(self.txtIV_Attack.displayText()) +
                                   float(self.txtEV_Attack)/4)*float(self.txtChosenLevel))/100 + 5) * statChangesMap.get("2")))
            finalDefense = int(math.floor((((2*float(pokemon.stats.get("Defense")) + float(self.txtIV_Defense.displayText()) +
                                   float(self.txtEV_Defense)/4)*float(self.txtChosenLevel))/100 + 5) * statChangesMap.get("3")))
            finalSpAttack = int(math.floor((((2*float(pokemon.stats.get("Special Attack")) + float(self.txtIV_SpAttack.displayText()) +
                                   float(self.txtEV_SpAttack)/4)*float(self.txtChosenLevel))/100 + 5) * statChangesMap.get("4")))
            finalSpDefense = int(math.floor((((2*float(pokemon.stats.get("Special Defense")) + float(self.txtIV_SpDefense.displayText()) +
                                   float(self.txtEV_SpDefense)/4)*float(self.txtChosenLevel))/100 + 5) * statChangesMap.get("5")))
            finalSpeed = int(math.floor((((2*float(pokemon.stats.get("Speed")) + float(self.txtIV_Speed.displayText()) +
                                   float(self.txtEV_Speed)/4)*float(self.txtChosenLevel))/100 + 5) * statChangesMap.get("6")))

            print("Im here")
        except:
            finalHP = pokemon.stats.get("HP")
            finalAttack = pokemon.stats.get("Attack")
            finalDefense = pokemon.stats.get("Defense")
            finalSpAtack = pokemon.stats.get("Special Attack")
            finalSpDefense = pokemon.stats.get("Special Defense")
            finalSpeed = pokemon.stats.get("Speed")

        print(finalHP)
        self.txtFinal_HP.setText(str(finalHP))
        self.txtFinal_Attack.setText(str(finalAttack))
        self.txtFinal_Defense.setText(str(finalDefense))
        self.txtFinal_SpAttack.setText(str(finalSpAtack))
        self.txtFinal_SpDefense.setText(str(finalSpDefense))
        self.txtFinal_Speed.setText(str(finalSpeed))


    def getPokemonMoves(self, pokedexNum):
        pokemon = self.pokedex.get(pokedexNum)
        knownMovesMap = pokemon.moves
        listMove_ids = list(knownMovesMap.keys())
        listMove_ids.sort()
        self.comboAvailableMoves.clear()
        for move_id in listMove_ids:
            move_name,_,type_id,power,pp,_,_,_,_,_,_,_,_,_ = knownMovesMap.get(move_id)
            type_name,generation_id,damage_class_id = self.types.get(type_id)
            self.comboAvailableMoves.addItem("Move: " + move_name + "   Type: " + type_name + "   Power: " + power + "  PP: " + pp)
        return

    def getPokemonAbilities(self, pokedexNum):
        pokemon = self.pokedex.get(pokedexNum)
        listAbilityIds = list(pokemon.abilities.keys())
        listAbilityIds.sort()
        self.comboAvailableAbilities.clear()
        for ability_id in listAbilityIds:
            abilityName = pokemon.abilities.get(ability_id)
            self.comboAvailableAbilities.addItem(abilityName)

        return

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
