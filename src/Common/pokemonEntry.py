class PokemonEntry():
    def __init__(self, dexNumber, fullName, codeName, types, baseStats, baseExp, happinessVal, abilities, hiddenAbility, eggMoves, moves, weaknesses, resistances, immunities, pokemonImage, genders, height, weight, evolutions):
        self.weight = weight
        self.height = height
        self.genders = genders
        self.image = pokemonImage
        self.dexNum = dexNumber
        self.pokemonName = fullName
        self.codeName = codeName
        self.pokemonTypes = types
        self.baseStats = baseStats
        self.baseExp = baseExp
        self.happinessValue = happinessVal
        self.abilities = abilities
        self.hiddenAbility = hiddenAbility
        self.eggMoves = eggMoves
        self.moves = moves
        self.weaknesses = weaknesses
        self.resistances = resistances
        self.immunities = immunities
        self.evolutions = evolutions
        self.forms = {}