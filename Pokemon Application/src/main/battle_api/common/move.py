class Move(object):
    def __init__(self, playerBattler, opponentBattler, moveProperties, moveInternalName, moveIndex, pokemonIndex):
        self.playerBattler = playerBattler
        self.opponentBattler = opponentBattler
        self.moveProperties = moveProperties
        self.moveInternalName = moveInternalName
        self.pokemonIndex = pokemonIndex
        self.moveIndex = moveIndex
        self.pokemonBattler = self.playerBattler.getPokemonTeam()[self.playerBattler.getCurrentPokemon()]
        self.opponentPokemonBattler = self.opponentBattler.getPokemonTeam()[self.opponentBattler.getCurrentPokemon()]
        self.pokemonTemporaryProperties = PokemonTemporaryProperties(self.pokemonBattler)
        self.opponentPokemonTemporaryProperties = PokemonTemporaryProperties(self.opponentPokemonBattler)

