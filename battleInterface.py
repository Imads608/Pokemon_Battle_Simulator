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
        self.movesSet = [0, 0, 0, 0]
        self.listMovesID = []
        self.movesChosen = ["", "", "", ""]
        self.player1Team = []
        self.player2Team = []
        self.CPUTeam = []

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

        # Finished Editing
        self.pushFinished.clicked.connect(self.savePokemon)

        # Show Pokemon Details
        self.listCurr_p1Team.doubleClicked.connect(lambda: self.restoreDetails("player 1"))
        self.listCurr_p2Team.doubleClicked.connect(lambda: self.restoreDetails("player 2"))

    def restoreDetails(self, player):
        if (player == "player 1"):
            currPlayerTeam = self.player1Team
        else:
            currPlayerTeam = self.player2Team

        for pokemon in currPlayerTeam:
            if (player == "player 1"):
                item = self.listCurr_p1Team.currentItem()
            else:
                item = self.listCurr_p2Team.currentItem()
            print(type(pokemon))
            if (pokemon.name == item.text()):
                pokemon_details = pokemon

        self.txtPokedexEntry.setText(pokemon_details.entry)
        self.txtChosenLevel.setText(pokemon_details.level)
        evSet = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        ivSet = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        finalStats = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]
        pokemonEVs = pokemon_details.evs
        pokemonIVs = pokemon_details.ivs
        pokemonFinalStats = pokemon_details.finalStats

        for i in range(len(evSet)):
            ev = evSet[i]
            iv = ivSet[i]
            final = finalStats[i]
            ev.setText(pokemonEVs[i])
            iv.setText(pokemonIVs[i])
            final.setText(pokemonFinalStats[i])

        moves = pokemon_details.moves
        print(moves)

        self.getPokemonMoves(pokemon_details.entry)
        self.getPokemonAbilities(pokemon_details.entry)
        self.listChosenMoves.clear()
        self.listChosenMoves.addItem(moves[0])
        self.listChosenMoves.addItem(moves[1])
        self.listChosenMoves.addItem(moves[2])
        self.listChosenMoves.addItem(moves[3])



    def savePokemon(self):
        isValid = self.checkPokemon()

        if (isValid == False):
            self.labelCheckFinalized.setText("ERROR")
        else:
            self.labelCheckFinalized.setText("")

        pokedexEntry = self.txtPokedexEntry.displayText()
        level = self.txtChosenLevel.displayText()
        image = self.pokedex.get(self.chosenPokemon).image
        evSet = [self.txtEV_HP.displayText(), self.txtEV_Attack.displayText(), self.txtEV_Defense.displayText(), self.txtEV_SpAttack.displayText(), self.txtEV_SpDefense.displayText(), self.txtEV_Speed.displayText()]
        ivSet = [self.txtIV_HP.displayText(), self.txtIV_Attack.displayText(), self.txtIV_Defense.displayText(), self.txtIV_SpAttack.displayText(), self.txtIV_SpDefense.displayText(), self.txtIV_Speed.displayText()]
        movesChosen = self.movesChosen
        print(movesChosen[0])
        moveIds = self.movesSet
        finalStats = [self.txtFinal_HP.displayText(), self.txtFinal_Attack.displayText(), self.txtFinal_Defense.displayText(), self.txtFinal_SpAttack.displayText(), self.txtFinal_SpDefense.displayText(), self.txtFinal_Speed.displayText()]
        player = self.comboPlayerNumber.currentText()
        pokemon = self.pokedex.get(self.chosenPokemon).name
        savePokemon = PokemonSave(pokedexEntry, pokemon, level, image, evSet, ivSet, movesChosen, moveIds, finalStats)

        if (player == "Player 1"):
            self.player1Team.append(savePokemon)
            self.listCurr_p1Team.addItem(pokemon)
        elif (player == "Player 2"):
            self.player2Team.append(savePokemon)
            self.listCurr_p2Team.addItem(pokemon)
        else:
            self.CPUTeam.append(savePokemon)
            self.listCurr_p2Team.addItem(pokemon)

        self.detailsClear()
        return

    def detailsClear(self):
        self.txtPokedexEntry.setText("")
        self.txtChosenLevel.setText("")
        scene = QGraphicsScene()
        self.viewCurrentPokemon.setScene(scene)
        self.viewCurrentPokemon.show()
        currEVSet = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        currIVSet = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        currFinalSet = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]

        for index in range(0, len(currEVSet)):
            ev = currEVSet[index]
            iv = currIVSet[index]
            final = currFinalSet[index]
            ev.setText("")
            iv.setText("")
            final.setText("")

        self.comboAvailableMoves.destroy()
        self.comboAvailableAbilities.destroy()
        self.listChosenMoves.clear()
        self.listChosenMoves.addItem("Move 1:")
        self.listChosenMoves.addItem("Move 2:")
        self.listChosenMoves.addItem("Move 3:")
        self.listChosenMoves.addItem("Move 4:")

        self.chosenPokemon = None
        self.EVsDone = 0
        self.EVsTotal = 0
        self.maxEVs = 0
        self.movesSet = [0, 0, 0, 0]
        self.listMovesID = []
        self.movesChosen = ["", "", "", ""]
        self.player1Team = []
        self.player2Team = []
        self.CPUTeam = []


    def checkPokemon(self):
        invalid = 0

        if (self.txtPokedexEntry.displayText() == ""):
            return False
        if (self.labelEntryCheck.text() != ""):
            return False

        if (self.txtChosenLevel.text() == ""):
            return False

        levelValue = int(self.txtChosenLevel.displayText())
        if (levelValue <= 0 or levelValue > 100):
            return False

        if (self.labelEVCheck.text() != ""):
            return False

        try:
            evHP = int(self.txtEV_HP.displayText())
            evAttack = int(self.txtEV_Attack.displayText())
            evDefense = int(self.txtEV_Defense.displayText())
            evSpAttack = int(self.txtEV_SpAttack.displayText())
            evSpDefense = int(self.txtEV_SpDefense.displayText())
            evSpeed = int(self.txtEV_Speed.displayText())
        except:
            invalid = 1

        if (invalid == 1):
            return False

        evCheck  = [evHP, evAttack, evDefense, evSpAttack, evSpDefense, evSpeed]

        for ev in evCheck:
            if (ev < 0 or ev > 255):
                return False

        if (self.labelIVCheck.text() != ""):
            return False

        try:
            ivHP = int(self.txtIV_HP.displayText())
            ivAttack = int(self.txtIV_Attack.displayText())
            ivDefense = int(self.txtIV_Defense.displayText())
            ivSpAttack = int(self.txtIV_SpAttack.displayText())
            ivSpDefense = int(self.txtIV_SpDefense.displayText())
            ivSpeed = int(self.txtIV_Speed.displayText())
        except:
            invalid = 1

        if (invalid == 1):
            return False

        ivCheck = [ivHP, ivAttack, ivDefense, ivSpAttack, ivSpDefense, ivSpeed]

        for iv in ivCheck:
            if (iv < 0 or iv > 31):
                return False

        if (0 in self.movesSet):
            return False

        return True

    def updateMoveSet(self):
        widgetItem = self.listChosenMoves.currentItem()
        matchMoveName = r'[^ ]+'
        listMatches = re.findall(matchMoveName, self.comboAvailableMoves.currentText())

        if (self.listChosenMoves.currentRow() == 0):
            widgetItem.setText("Move 1: " + listMatches[1])
            self.movesSet[0] = self.listMovesID[self.comboAvailableMoves.currentIndex()]
            self.movesChosen[0] = "Move 1: " + listMatches[1]
        elif (self.listChosenMoves.currentRow() == 1):
            widgetItem.setText("Move 2: " + listMatches[1])
            self.movesSet[1] = self.listMovesID[self.comboAvailableMoves.currentIndex()]
            self.movesChosen[1] = "Move 2: " + listMatches[1]
        elif (self.listChosenMoves.currentRow() == 2):
            widgetItem.setText("Move 3: " + listMatches[1])
            self.movesSet[2] = self.listMovesID[self.comboAvailableMoves.currentIndex()]
            self.movesChosen[2] = "Move 3: " + listMatches[1]
        elif (self.listChosenMoves.currentRow() == 3):
            widgetItem.setText("Move 4: " + listMatches[1])
            self.movesSet[3] = self.listMovesID[self.comboAvailableMoves.currentIndex()]
            self.movesChosen[3] = "Move 4: " + listMatches[1]


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
        if (pokemon == None):
            return
        #print("dsadasdas")
        statIDMap = {"1":"HP", "2":"Attack", "3":"Defense", "4":"Special Attack", "5":"Special Defense", "6":"Speed"}
        statChangesMap = {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1}
        finalHP = 0
        finalAttack = 0
        finalDefense = 0
        finalSpAttack = 0
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
                                   float(self.txtEV_HP.displayText())/4)*float(self.txtChosenLevel.displayText()))/100 + float(self.txtChosenLevel.displayText()) + 10))

            finalAttack = math.floor((math.floor(((2*float(pokemon.stats.get("Attack")) + float(self.txtIV_Attack.displayText()) +
                                                  math.floor(float(self.txtEV_Attack.displayText())/4))
                                                  *float(self.txtChosenLevel.displayText()))/100)+5)*statChangesMap.get("2"))

            finalDefense = math.floor((math.floor(((2*float(pokemon.stats.get("Defense")) + float(self.txtIV_Defense.displayText()) +
                                                  math.floor(float(self.txtEV_Defense.displayText())/4))
                                                  *float(self.txtChosenLevel.displayText()))/100)+5)*statChangesMap.get("3"))

            finalSpAttack = math.floor((math.floor(((2*float(pokemon.stats.get("Special Attack")) + float(self.txtIV_SpAttack.displayText()) +
                                                  math.floor(float(self.txtEV_SpAttack.displayText())/4))
                                                  *float(self.txtChosenLevel.displayText()))/100)+5)*statChangesMap.get("4"))

            finalSpDefense = math.floor((math.floor(((2*float(pokemon.stats.get("Special Defense")) + float(self.txtIV_SpDefense.displayText()) +
                                                  math.floor(float(self.txtEV_SpDefense.displayText())/4))
                                                  *float(self.txtChosenLevel.displayText()))/100)+5)*statChangesMap.get("5"))

            finalSpeed = math.floor((math.floor(((2*float(pokemon.stats.get("Speed")) + float(self.txtIV_Speed.displayText()) +
                                                  math.floor(float(self.txtEV_Speed.displayText())/4))
                                                  *float(self.txtChosenLevel.displayText()))/100)+5)*statChangesMap.get("6"))
        except:
            finalHP = pokemon.stats.get("HP")
            finalAttack = pokemon.stats.get("Attack")
            finalDefense = pokemon.stats.get("Defense")
            finalSpAttack = pokemon.stats.get("Special Attack")
            finalSpDefense = pokemon.stats.get("Special Defense")
            finalSpeed = pokemon.stats.get("Speed")

        #print(finalHP)
        self.txtFinal_HP.setText(str(finalHP))
        self.txtFinal_Attack.setText(str(finalAttack))
        self.txtFinal_Defense.setText(str(finalDefense))
        self.txtFinal_SpAttack.setText(str(finalSpAttack))
        self.txtFinal_SpDefense.setText(str(finalSpDefense))
        self.txtFinal_Speed.setText(str(finalSpeed))


    def getPokemonMoves(self, pokedexNum):
        pokemon = self.pokedex.get(pokedexNum)
        knownMovesMap = pokemon.moves
        listMove_ids = list(knownMovesMap.keys())
        listMove_ids.sort()
        self.listMovesID = listMove_ids
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

class PokemonSave():
    def __init__(self, pokedexEntry, name, level, image, evSet, ivSet, movesChosen, moveIds, finalStats):
        self.entry = pokedexEntry
        self.name = name
        self.level = level
        self.image = image
        self.evs = evSet
        self.ivs = ivSet
        self.moves = movesChosen
        self.moveIds = moveIds
        self.finalStats = finalStats

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = battleConsumer()

    currentForm.show()
    currentApp.exec_()
