from PyQt5 import QtCore, QtGui, QtWidgets

class SinglesBattleWidgets(object):
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

    def getPokemonHPLabel(self, playerNum):
        if (playerNum == 1):
            return self.lbl_hpPokemon1
        return self.lbl_hpPokemon2

    def setPokemonHPLabel(self, playerNum, widget):
        if (playerNum == 1):
            self.lbl_hpPokemon1 = widget
        else:
            self.lbl_hpPokemon2 = widget

    def getPokemonLevelTextBox(self, playerNum):
        if (playerNum == 1):
            return self.txtPokemon1_Level
        return self.txtPokemon2_Level

    def setPokemonLevelTextBox(self, playerNum, widget):
        if (playerNum == 1):
            self.txtPokemon1_Level = widget
        else:
            self.txtPokemon2_Level = widget

    def getStatusConditionLabel(self, playerNum):
        if (playerNum == 1):
            return self.lbl_statusCond1
        return self.lbl_statusCond2

    def setStatusConditionLabel(self, playerNum, widget):
        if (playerNum == 1):
            self.lbl_statusCond1 = widget
        else:
            self.lbl_statusCond2 = widget

    def getPokemonHPBar(self, playerNum):
        if (playerNum == 1):
            return self.hpBar_Pokemon1
        return self.hpBar_Pokemon2

    def setPokemonHPBar(self, playerNum, widget):
        if (playerNum == 1):
            self.hpBar_Pokemon1 = widget
        else:
            self.hpBar_Pokemon2 = widget

    def getPokemonView(self, playerNum):
        if (playerNum == 1):
            return self.viewPokemon1
        return self.viewPokemon2

    def setPokemonView(self, playerNum, widget):
        if (playerNum == 1):
            self.viewPokemon1 = widget
        else:
            self.viewPokemon2 = widget

    def getPokemonMovesListBox(self, playerNum):
        if (playerNum == 1):
            return self.listPokemon1_moves
        return self.listPokemon2_moves

    def setPokemonMovesListBox(self, playerNum, widget):
        if (playerNum == 1):
            self.listPokemon1_moves = widget
        else:
            self.listPokemon2_moves = widget

    def getPlayerTeamListBox(self, playerNum):
        if (playerNum == 1):
            return self.listPlayer1_team
        return self.listPlayer2_team

    def setPlayerTeamListBox(self, playerNum, widget):
        if (playerNum == 1):
            self.listPlayer1_team = widget
        else:
            self.listPlayer2_team = widget

    def getSwitchPlayerPokemonPushButton(self, playerNum):
        if (playerNum == 1):
            return self.pushSwitchPlayer1
        return self.pushSwitchPlayer2

    def setSwitchPlayerPokemonPushButton(self, playerNum, widget):
        if (playerNum == 1):
            self.pushSwitchPlayer1 = widget
        else:
            self.pushSwitchPlayer2 = widget

    def getStartBattlePushButton(self):
        return self.pushStartBattle

    def setStartBattlePushButton(self, widget):
        self.pushStartBattle = widget

    def getBattleInfoTextBox(self):
        return self.txtBattleInfo

    def setBattleInfoTextBox(self, widget):
        self.txtBattleInfo = widget

    def getPlayerBattleWidgets(self, playerNum):
        if (playerNum == 1):
            return self.player1B_Widgets
        return self.player2B_Widgets

    def setPlayerBattleWidgets(self, playerNum, widgets):
        if (playerNum == 1):
            self.player1B_Widgets = widgets
        else:
            self.player2B_Widgets = widgets

    def setPlayerWidgetShortcuts(self, player1Team, player2Team):
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1, 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2, self.txtPokemon2_Level, self.pushSwitchPlayer2, player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2, 2]

    def geCurrentPokemonIndex(self, playerNum):
        if (playerNum == 1):
            return self.listPlayer1_team.currentRow()
        else:
            return self.listPlayer2_team.currentRow()

    def getChosenMoveIndex(self, playerNum):
        if (playerNum == 1):
            return self.listPokemon1_moves.currentRow()
        else:
            return self.listPokemon2_moves.currentRow()