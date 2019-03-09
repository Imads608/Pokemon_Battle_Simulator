class Switch(Action):
    def __init__(self, actionType):
        super.__init__(self, actionType)
        self.currPlayer = None
        self.currPokemonIndex = None
        self.switchPokemonIndex = None

    def initializeSwitch(self, currPlayer, currPokemonIndex, switchPokemonIndex):
        self.currPlayer = currPlayer
        self.currPokemonIndex = currPokemonIndex
        self.switchPokemonIndex = switchPokemonIndex
