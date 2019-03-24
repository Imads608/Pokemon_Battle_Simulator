from PyQt5 import QtCore, QtGui, QtWidgets

class BattleWidgets1v1(object):
    def __init__(self, lbl_hpPokemon1, lbl_hpPokemon2, txtPokemon1_Level, txtPokemon2_Level, lbl_statusCond1, lbl_statusCond2, hpBar_Pokemon1, hpBar_Pokemon2,
                 viewPokemon1, viewPokemon2, listPokemon1_moves, listPokemon2_moves,
                 listPlayer1_team, listPlayer2_team, pushSwitchPlayer1, pushSwitchPlayer2, pushStartBattle, txtBattleInfo):
        self.lbl_hpPokemon1 = lbl_hpPokemon1
        self.lbl_hpPokemon2 = lbl_hpPokemon2
        self.txtPokemon1_Level = txtPokemon1_Level
        self.txtPokemon2_Level = txtPokemon2_Level
        self.lbl_statusCond1 = lbl_statusCond1
        self.lbl_statusCond2 = lbl_statusCond2
        self.hpBar_Pokemon1 = hpBar_Pokemon1
        self.hpBar_Pokemon2 = hpBar_Pokemon2
        self.viewPokemon1 = viewPokemon1
        self.viewPokemon2 = viewPokemon2
        self.listPokemon1_moves = listPokemon1_moves
        self.listPokemon2_moves = listPokemon2_moves
        self.listPlayer1_team = listPlayer1_team
        self.listPlayer2_team = listPlayer2_team
        self.pushSwitchPlayer1 = pushSwitchPlayer1
        self.pushSwitchPlayer2 = pushSwitchPlayer2
        self.pushStartBattle = pushStartBattle
        self.txtBattleInfo = txtBattleInfo
        self.player1B_Widgets = None #[self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, self.tab1Consumer.battleObject.player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1, 1]
        self.player2B_Widgets = None #[self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2, self.txtPokemon2_Level, self.pushSwitchPlayer2, self.tab1Consumer.battleObject.player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2, 2]

    def setPlayerWidgetShortcuts(self, player1Team, player2Team):
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1,
                                 self.txtPokemon1_Level, self.pushSwitchPlayer1,
                                 player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1,
                                 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2,
                                 self.txtPokemon2_Level, self.pushSwitchPlayer2,
                                 player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2,
                                 2]
    def displayPokemon(self, viewPokemon, pokedexEntry, pokedex):
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

    def displayMessageBox(self, header, body):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(header)
        msg.setInformativeText(body)
        # msg.setWindowTitle("MessageBox demo")
        # msg.setDetailedText("Pokemon Fainted")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    def updateBattleInfo(self, addedText):
        self.txtBattleInfo.append(addedText)
        return