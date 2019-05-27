class PlayerBattler(object):
    def __init__(self, playerNum, pokemonTeam, widgets):
        self.playerNum = playerNum
        self.team = pokemonTeam
        self.playerWidgets = widgets
        self.currPokemon = None
        self.turnPlayed = False
        self.actionTuple = None
        self.actionPerformed = None

    def getPlayerNumber(self):
        return self.playerNum

    def setPlayerNum(self, num):
        self.playerNum = num

    def getPokemonTeam(self):
        return self.team

    def setPokemonTeam(self, team):
        self.team = team

    def getPlayerWidgetShortcuts(self):
        return self.playerWidgets

    def setPlayerWidgetShortcuts(self, widgets):
        self.playerWidgets = widgets

    def getCurrentPokemon(self):
        return self.currPokemon

    def setCurrentPokemon(self, curr):
        self.currPokemon = curr

    def getTurnPlayed(self):
        return self.turnPlayed

    def setTurnPlayed(self, boolVal):
        self.turnPlayed = boolVal

    def getActionTuple(self):
        return self.actionTuple

    def setActionTuple(self, tupleVals):
        self.actionTuple = tupleVals

    def getActionPerformed(self):
        return self.actionPerformed

    def setActionPerformed(self, action):
        self.actionPerformed = action