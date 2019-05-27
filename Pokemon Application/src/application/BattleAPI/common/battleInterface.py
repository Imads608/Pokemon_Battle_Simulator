class BattleInterface(object):
    def __init__(self, pokemonDB, player1, player2, typeBattle, battleWidgets):
        self.player1Battler = player1
        self.player2Battler = player2        
        self.battleFinished = False

        # Pokemon Database
        self.pokemonDB = pokemonDB

        # Battle Observer
        self.battleObserver = BattleObserver(battleWidgets)

        # Common Battle Properties
        self.battleProperties = BattleProperties()

        # BattleField Manager
        self.battleFieldManager = BattleFieldManager(pokemonDB, self.battleProperties)

        # Abilities Manager
        self.abilitiesManager = AbilitiesManager(pokemonDB, typeBattle, self.battleProperties)

