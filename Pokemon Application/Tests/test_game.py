import sys
sys.path.append("../application")
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt
import unittest
from game import *

app = QtWidgets.QApplication(sys.argv)

class GameTest(unittest.TestCase):
    def setUp(self):
        self.form = battleConsumer()
        self.form.show()

    def setUpTeamsConfig(self, player1Config, player2Config):
        ########## THis function sets up the team configuration for both players  ######################
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
        app.exec_()

    def execMoves(self, player1Move, player2Move):
        ################ This function executes the move given by the two players ##############################
        if (player1Move[0] == "move"):
            self.form.listPokemon1_moves.setCurrentRow(player1Move[1])
            QTest.mouseClick(self.form.listPokemon1_moves.viewport(), Qt.LeftButton)
        else:
            pass

        if (player2Move[0] == "move"):
            self.form.listPokemon2_moves.setCurrentRow(player2Move[1])
            QTest.mouseClick(self.form.listPokemon2_moves.viewport(), Qt.LeftButton)
        else:
            pass


    def test_1(self):
        ################# This test sets up a 1v1 Battle, execute Moves for the two players and check their resulting action Object values

        # Setup : List of (POkedex Entry, Level, Gender, Happiness, Item, Nature, Ability, Moves, EVs, IVs) tuples
        player1Setup = [("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [],[])]
        player2Setup = [("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], [])]
        self.setUpTeamsConfig(player1Setup, player2Setup)

        # Start the battle
        QTest.mouseClick(self.form.pushStartBattle, Qt.LeftButton)

        # Execute Player Moves - Player Move: (move/swap, moveIndex/swapIndex)
        self.execMoves(("move", 0), ("move", 0))

        # Perform Checks
        self.assertNotEqual(self.form.battleObject.player1Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player1Action.action, "move")
        self.assertEqual(self.form.battleObject.player1Action.priority, 0)
        self.assertEqual(self.form.battleObject.player1Action.isFirst, False)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.internalMove, "TACKLE")
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currPower, 50)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currMoveAccuracy, 100)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetAttackStat, self.form.battleObject.player1Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetDefenseStat, self.form.battleObject.player2Team[0].finalStatsList[2])

        self.assertNotEqual(self.form.battleObject.player2Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player2Action.action, "move")
        self.assertEqual(self.form.battleObject.player2Action.priority, 0)
        self.assertEqual(self.form.battleObject.player2Action.isFirst, True)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.internalMove, "SCRATCH")
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currPower, 40)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currMoveAccuracy, 100)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetAttackStat, self.form.battleObject.player2Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetDefenseStat, self.form.battleObject.player1Team[0].finalStatsList[2])

    def test_2(self):
        ################# This test sets up a 1v1 Battle, execute Moves for the two players and check their resulting action Object valuee
        # Setup : List of (POkedex Entry, Level, Gender, Happiness, Item, Nature, Ability, Moves, EVs, IVs) tuples
        player1Setup = [("55", "50", "Male", "255", "Mystic Water", "Bold", "Damp", ["Aqua Jet"], [], [])]
        player2Setup = [("3", "50", "Male", "255", "Miracle Seed", "Bold", "Overgrow", ["Razor Leaf"], [], [])]
        self.setUpTeamsConfig(player1Setup, player2Setup)

        # Start the battle
        QTest.mouseClick(self.form.pushStartBattle, Qt.LeftButton)

        # Execute Player Moves
        self.execMoves(("move", 0), ("move", 0))

        # Perform Checks
        self.assertNotEqual(self.form.battleObject.player1Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player1Action.action, "move")
        self.assertEqual(self.form.battleObject.player1Action.priority, 1)
        self.assertEqual(self.form.battleObject.player1Action.isFirst, True)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.internalMove, "AQUAJET")
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currPower, int(40*1.2))
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currMoveAccuracy, 100)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetAttackStat, self.form.battleObject.player1Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetDefenseStat, self.form.battleObject.player2Team[0].finalStatsList[2])

        self.assertNotEqual(self.form.battleObject.player2Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player2Action.action, "move")
        self.assertEqual(self.form.battleObject.player2Action.priority, 0)
        self.assertEqual(self.form.battleObject.player2Action.isFirst, False)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.internalMove, "RAZORLEAF")
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currPower, int(55 * 1.2))
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currMoveAccuracy, 95)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetAttackStat, self.form.battleObject.player2Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetDefenseStat, self.form.battleObject.player1Team[0].finalStatsList[2])

    def test_3(self):
        ################# This test sets up a 3v3 Battle, execute Moves for the two players and check their resulting action Object values

        # Setup : List of (POkedex Entry, Level, Gender, Happiness, Item, Nature, Ability, Moves, EVs, IVs) tuples
        player1Setup = [("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [],[]),
                        ("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [], []),
                        ("3", "50", "Male", "255", "Grass Gem", "Bold", "Overgrow", ["Tackle"], [], [])]
        player2Setup = [("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], []),
                        ("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], []),
                        ("6", "50", "Male", "255", "Fire Gem", "Adamant", "Blaze", ["Scratch"], [], [])]
        self.form.comboBattleType.setCurrentIndex(1)
        self.setUpTeamsConfig(player1Setup, player2Setup)

        # Start the battle
        QTest.mouseClick(self.form.pushStartBattle, Qt.LeftButton)

        # Execute Player Moves - Player Move: (move/swap, moveIndex/swapIndex)
        self.execMoves(("move", 0), ("move", 0))

        # Perform Checks
        self.assertNotEqual(self.form.battleObject.player1Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player1Action.action, "move")
        self.assertEqual(self.form.battleObject.player1Action.priority, 0)
        self.assertEqual(self.form.battleObject.player1Action.isFirst, False)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.internalMove, "TACKLE")
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currPower, 50)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.currMoveAccuracy, 100)
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetAttackStat, self.form.battleObject.player1Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player1Action.moveObject.targetDefenseStat, self.form.battleObject.player2Team[0].finalStatsList[2])

        self.assertNotEqual(self.form.battleObject.player2Action.moveObject, None)
        self.assertEqual(self.form.battleObject.player2Action.action, "move")
        self.assertEqual(self.form.battleObject.player2Action.priority, 0)
        self.assertEqual(self.form.battleObject.player2Action.isFirst, True)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.internalMove, "SCRATCH")
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currPower, 40)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.currMoveAccuracy, 100)
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetAttackStat, self.form.battleObject.player2Team[0].finalStatsList[1])
        self.assertEqual(self.form.battleObject.player2Action.moveObject.targetDefenseStat, self.form.battleObject.player1Team[0].finalStatsList[2])


if __name__ == "__main__":
    unittest.main()