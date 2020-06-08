import sys
sys.path.append("../main")
sys.path.append("../main/battle_api")
sys.path.append("../main/user_interface")
sys.path.append("../main/automation_scripts")
sys.path.append("../main/team_builder")
sys.path.append("../main/battle_api/common")
sys.path.append("../main/battle_api/singles")
sys.path.append("../main/battle_api/doubles")

#from PokemonTemporaryEffectsQueue import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt
import unittest
from gameController import *

app = QtWidgets.QApplication(sys.argv)

class SwitchTest(unittest.TestCase):
    def setUp(self):
        self.form = GameController()
        self.form.show()

    def setupTeamsConfiguration(self, battleTypeIndex, player1Config, player2Config):
        ########## THis function sets up the team configuration for both players  ######################
        self.form.comboBattleType.setCurrentIndex(battleTypeIndex)
        players = [player1Config, player2Config]
        for playerConfig in players:
            for pokemonConfig in playerConfig:
                dexNum, level, gender, happiness, item, nature, ability, moves, evs, ivs = pokemonConfig
                self.form.txtPokedexEntry.setText(dexNum)
                self.form.txtChosenLevel.setText(level)
                indexGender = self.form.comboGenders.findText(gender)
                self.form.comboGenders.setCurrentIndex(indexGender)
                self.form.txtHappinessVal.setText(happiness)
                indexItem = self.form.comboItems.findText(item)
                self.form.comboItems.setCurrentIndex(indexItem)
                indexNature = self.form.comboNatures.findText(nature)
                self.form.comboNatures.setCurrentIndex(indexNature)
                indexAbility = self.form.comboAvailableAbilities.findText(ability)
                self.form.comboAvailableAbilities.setCurrentIndex(indexAbility)
                i = 0
                for move in moves:
                    indexMove = self.form.comboAvailableMoves.findText("Move: " + move)
                    self.form.comboAvailableMoves.setCurrentIndex(indexMove)
                    self.form.listChosenMoves.setCurrentRow(i)
                    QTest.mouseClick(self.form.pushAddMove, Qt.LeftButton)
                if (len(evs) == 0):
                    QTest.mouseClick(self.form.pushRandomizeEVs, Qt.LeftButton)
                else:
                    for i in range(0, len(evs)):
                        self.form.evsList[i].setText(evs[i])
                if (len(ivs) == 0):
                    QTest.mouseClick(self.form.pushRandomizeIVs, Qt.LeftButton)
                else:
                    for i in range(0, len(ivs)):
                        self.form.ivsList[i].setText(ivs[i])
                QTest.mouseClick(self.form.pushFinished, Qt.LeftButton)
            self.form.comboPlayerNumber.setCurrentIndex(1)

        # Used to close pop ups
        QTest.mouseClick(self.form.pushDone, Qt.LeftButton)
        qMessageBox = app.activeModalWidget()
        if (qMessageBox):
            qMessageBox.close()
        #app.exec_() ### Uncomment this to bring up main gui

    def execMoves(self, player1Move, player2Move):
        ################ This function executes the move given by the two players ##############################
        if (player1Move[0] == "move"):
            self.form.listPokemon1_moves.setCurrentRow(player1Move[1])
            QTest.mouseClick(self.form.listPokemon1_moves.viewport(), Qt.LeftButton)
        else:
            self.form.listPlayer1_team.setCurrentRow(player1Move[1])
            QTest.mouseClick(self.form.pushSwitchPlayer1, Qt.LeftButton)

        if (player2Move[0] == "move"):
            self.form.listPokemon2_moves.setCurrentRow(player2Move[1])
            QTest.mouseClick(self.form.pushSwitchPlayer2.viewport(), Qt.LeftButton)
        else:
            self.form.listPlayer2_team.setCurrentRow(player2Move[1])
            QTest.mouseClick(self.form.pushSwitchPlayer2, Qt.LeftButton)

    ############### This test sets up a 3v3 Battle and tests players switching pokemon #################
    def test_switch(self):
        # Setup : List of (POkedex Entry, Level, Gender, Happiness, Item, Nature, Ability, Moves, EVs, IVs) tuples
        player1Setup = [("248", "50", "Male", "255", "Grass Gem", "Adamant", "Sand Stream", ["Dragon Claw"], [], []),
                        ("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [], []),
                        ("9", "50", "Male", "255", "Grass Gem", "Adamant", "Torrent", ["Aqua Jet"], [], [])]
        player2Setup = [("149", "50", "Male", "255", "Fire Gem", "Adamant", "Inner Focus", ["Dragon Claw"], [], []),
                        ("59", "50", "Male", "255", "Fire Gem", "Adamant", "Intimidate", ["Strength"], [], []),
                        ("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], [])]

        self.setupTeamsConfiguration(1, player1Setup, player2Setup)

        # Start the battle
        QTest.mouseClick(self.form.pushStartBattle, Qt.LeftButton)

        # Execute Player Moves - Player Move: (move/swap, moveIndex/swapIndex)
        self.execMoves(("switch", 0), ("switch", 2))

        # Perform Checks
        self.assertEqual(self.form.battleFacade.singlesBattleAdapter.player1Battler.getCurrentPokemon().getName(), "Tyranitar")
        self.assertEqual(self.form.battleFacade.singlesBattleAdapter.player2Battler.getCurrentPokemon().getName(), "Charizard")
        self.assertEqual(self.form.battleFacade.singlesBattleAdapter.battleFieldManager.getWeather(), "sandstorm")

if __name__ == "__main__":
    unittest.main()