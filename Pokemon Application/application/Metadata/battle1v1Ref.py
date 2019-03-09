class Battle1v1Reference(object):
    def __init__(self, lbl_hpPokemon1, lbl_hpPokemon2, lbl_statusCond1, lbl_statusCond2, hpBar_Pokemon1, hpBar_Pokemon2, viewPokemon1, viewPokemon2, listPokemon1_moves, listPokemon2_moves,
                 listPlayer1_team, listPlayer2_team, pushSwitchPlayer1, pushSwitchPlayer2):
        self.lbl_hpPokemon1 = lbl_hpPokemon1
        self.lbl_hpPokemon2 = lbl_hpPokemon2
        self.lbl_statusCond1 = lbl_statusCond1
        self.lbl_statusCond2 = lbl_statusCond2
        self.hpBar_Pokemon1 = lbl_hpPokemon1
        self.hpBar_Pokemon2 = lbl_hpPokemon2
        self.viewPokemon1 = viewPokemon1
        self.viewPokemon2 = viewPokemon2
        self.listPokemon1_moves = listPokemon1_moves
        self.listPokemon2_moves = listPokemon2_moves
        self.listPlayer1_team = listPlayer1_team
        self.listPlayer2_team = listPlayer2_team
        self.pushSwitchPlayer1 = pushSwitchPlayer1
        self.pushSwitchPlayer2 = pushSwitchPlayer2
        self.player1B_Widgets = [self.listPokemon1_moves, self.listPlayer1_team, self.hpBar_Pokemon1, self.viewPokemon1, self.txtPokemon1_Level, self.pushSwitchPlayer1, self.tab1Consumer.battleObject.player1Team, self.lbl_hpPokemon1, self.lbl_statusCond1, 1]
        self.player2B_Widgets = [self.listPokemon2_moves, self.listPlayer2_team, self.hpBar_Pokemon2, self.viewPokemon2,
                                 self.txtPokemon2_Level, self.pushSwitchPlayer2, self.tab1Consumer.battleObject.player2Team, self.lbl_hpPokemon2, self.lbl_statusCond2, 2]