class PlayerBattler(object):
    def __init__(self, playerNum, pokemonTeam):
        self.playerNum = playerNum
        self.team = pokemonTeam
        self.currPokemon = None
        self.turnPlayed = False
        self.actionPerformed = None

    def getPlayerNumber(self):
        return self.playerNum

    def setPlayerNum(self, num):
        self.playerNum = num

    def getPokemonTeam(self):
        return self.team

    def setPokemonTeam(self, team):
        self.team = team

    def getCurrentPokemon(self):
        return self.currPokemon

    def setCurrentPokemon(self, currPokemon):
        self.currPokemon = currPokemon

    def getTurnPlayed(self):
        return self.turnPlayed

    def setTurnPlayed(self, boolVal):
        self.turnPlayed = boolVal

    def getActionPerformed(self):
        return self.actionPerformed

    def setActionPerformed(self, action):
        self.actionPerformed = action