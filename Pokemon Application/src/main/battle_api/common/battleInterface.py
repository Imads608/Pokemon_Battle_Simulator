from battleObserver import BattleObserver
from battleProperties import BattleProperties
from battleFieldManager import BattleFieldManager
from abilityEffectsExecutor import AbilityEffectsExecutor
from actionExecutorFacade import ActionExecutorFacade

class BattleInterface(object):
    def __init__(self, pokemonDataSource, player1, player2, typeBattle, battleWidgets):
        self.player1Battler = player1
        self.player2Battler = player2        
        self.battleFinished = False

        # Pokemon Metadata
        self.pokemonDataSource = pokemonDataSource

        # Common Battle Properties
        self.battleProperties = BattleProperties()

        # Battle Observer
        self.battleObserver = BattleObserver(battleWidgets, pokemonDataSource, self.battleProperties)

        # BattleField Manager
        self.battleFieldManager = BattleFieldManager(pokemonDataSource, self.battleProperties)

        # Abilities Manager
        self.abilityEffectsExecutor = AbilityEffectsExecutor(typeBattle, self.battleProperties, pokemonDataSource)

        # Action Executor
        self.actionExecutorFacade = ActionExecutorFacade(typeBattle, pokemonDataSource, self.battleProperties)

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
        return self.pokemonDataSource

    def getBattleObserver(self):
        return self.battleObserver

    def getBattleProperties(self):
        return self.battleProperties

    def getBattleFieldManager(self):
        return self.battleFieldManager

    def getAbilityEffectsExecutor(self):
        return self.abilityEffectsExecutor

    def getActionExecutorFacade(self):
        return self.actionExecutorFacade

