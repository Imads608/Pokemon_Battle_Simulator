from battleObserver import BattleObserver
from battleProperties import BattleProperties
from battleFieldManager import BattleFieldManager
from abilitiesManagerFacade import AbilitiesManagerFacade
from actionExecutorFacade import ActionExecutorFacade

class BattleInterface(object):
    def __init__(self, pokemonMetadata, player1, player2, typeBattle, battleWidgets):
        self.player1Battler = player1
        self.player2Battler = player2        
        self.battleFinished = False

        # Pokemon Metadata
        self.pokemonMetadata = pokemonMetadata

        # Common Battle Properties
        self.battleProperties = BattleProperties()

        # Battle Observer
        self.battleObserver = BattleObserver(battleWidgets, pokemonMetadata, self.battleProperties)

        # BattleField Manager
        self.battleFieldManager = BattleFieldManager(pokemonMetadata, self.battleProperties)

        # Abilities Manager
        self.abilitiesManagerFacade = AbilitiesManagerFacade(pokemonMetadata, typeBattle, self.battleProperties)

        # Action Executor
        self.actionExecutorFacade = ActionExecutorFacade(typeBattle, self.battleProperties)

    ########### Getters and Setters #############
    def getPlayerBattler(self, playerNum):
        if (playerNum == 1):
            return self.player1Battler
        return self.player2Battler

    def getBattleFinished(self):
        return self.battleFinished

    def setBattleFinished(self, boolVal):
        self.battleFinished = boolVal

    def getPokemonMetadata(self):
        return self.pokemonMetadata

    def getBattleObserver(self):
        return self.battleObserver

    def getBattleProperties(self):
        return self.battleProperties

    def getBattleFieldManager(self):
        return self.battleFieldManager

    def getAbilitiesManagerFacade(self):
        return self.abilitiesManagerFacade

    def getActionExecutorFacade(self):
        return self.actionExecutorFacade

