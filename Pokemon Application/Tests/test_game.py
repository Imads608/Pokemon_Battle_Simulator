import sys
sys.path.append("../application")
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import unittest
from game import *

app = QtWidgets.QApplication(sys.argv)

class GameTest(unittest.TestCase):
    def setUp(self):
        self.form = battleConsumer()
        self.form.show()

    def setUpTeamsConfig(self, player1Config, player2Config):
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

        #app.exec_()
        QTest.mouseClick(self.form.pushDone, Qt.LeftButton)
        app.exec_()

    def test_1v1BattleTurn(self):
        # Setup : List of (POkedex Entry, Level, Gender, Happiness, Item, Nature, Ability, Moves, EVs, IVs) tuples
        player1Setup = [("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [],[])]
        player2Setup = [("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], [])]
        self.setUpTeamsConfig(player1Setup, player2Setup)

        # Start the battle
        self.form.pushStartBattle()

        # Choose Player 1 Move

        self.assertEqual(self.form.comboGenders.currentText(), "")


if __name__ == "__main__":
    unittest.main()