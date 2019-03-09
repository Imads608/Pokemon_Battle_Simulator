class BattleTeams(object):
    def __init__(self):
        self.player1Team = []
        self.player2Team = []
        self.currPlayer1PokemonIndex = 0
        self.currPlayer2PokemonIndex = 0
        self.playerTurn = 1
        self.player1MoveTuple = tuple()
        self.player2MoveTuple = tuple()
        self.player1Action = Action()
        self.player2Action = Action()
        self.playerActionsComplete = False
        self.playerTurnsDone = 0
        self.battleOver = False

    def setTeams(self, player1Team, player2Team):
        self.player1Team = player1Team
        self.player2Team = player2Team

    def setPlayer1CurrentPokemonIndex(self, index):
        self.currPlayer1PokemonIndex = index

    def setPlayer2CurrentPokemonIndex(self, index):
        self.currPlayer2PokemonIndex = index

    def setPlayer1MoveTuple(self, moveTuple):
        self.player1MoveTuple = moveTuple

    def setPlayer2MoveTuple(self, moveTuple):
        self.player2MoveTuple = moveTuple

    def updatePlayer1Action(self, action):
        self.player1Action = action

    def updatePlayer2Action(self, action):
        self.player2Action = action

    def updatePlayerTurn(self):
        if (self.playerTurn == 1):
            self.playerTurn = 2
        else:
            self.playerTurn = 1

    def setPlayerTurn(self, playerNum):
        self.playerTurn = playerNum

    def updateTurnsDone(self):
        if (self.playerTurnsDone == 2):
            self.playerTurnsDone = 0
        else:
            self.playerTurnsDone += 1

        if (self.playerTurnsDone == 2):
            self.playerActionsComplete = True
        else:
            self.playerActionsComplete = False

        return

    def setBattleOver(self):
        self.battleOver = True

    def unsetBattleOver(self):
        self.battleOver = False