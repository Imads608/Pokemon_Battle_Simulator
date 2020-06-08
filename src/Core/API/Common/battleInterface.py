from src.Core.API.Singles.Battle_Observer.singlesBattleObserver import  SinglesBattleObserver
from src.Core.API.Common.Data_Types.battleProperties import BattleProperties
from src.Core.API.Common.BattleField.battleFieldManager import BattleFieldManager
from src.Core.API.Common.Ability_Executor.abilityEffectsExecutor import AbilityEffectsExecutor
from src.Core.API.Common.Action_Executor.actionExecutorFacade import ActionExecutorFacade
from src.Core.API.Common.FunctionCode_Executor.functionCodesManager import FunctionCodesManager

class BattleInterface(object):
    def __init__(self, pokemonDAL, player1, player2, typeBattle, battleWidgets):
        self.player1Battler = player1
        self.player2Battler = player2        
        self.battleFinished = False

        # Pokemon Metadata
        self.pokemonDAL = pokemonDAL

        # Common Battle Properties
        self.battleProperties = BattleProperties()

        # Battle Observer
        self.battleObserver = SinglesBattleObserver(battleWidgets, pokemonDAL, self.battleProperties)

        # BattleField Manager
        self.battleFieldManager = BattleFieldManager(pokemonDAL, self.battleProperties)

        # Abilities Manager
        self.abilityEffectsExecutor = AbilityEffectsExecutor(typeBattle, pokemonDAL, self.battleProperties)

        # Action Executor
        self.actionExecutorFacade = ActionExecutorFacade(typeBattle, pokemonDAL, self.battleProperties)

        # Function Codes Manager
        self.functionCodesManager = FunctionCodesManager(self.battleProperties, pokemonDAL, typeBattle)

    ########### Getters and Setters #############
    def getPlayerBattler(self, playerNum):
        if (playerNum == 1):
            return self.player1Battler
        return self.player2Battler

    def getBattleFinished(self):
        return self.battleFinished

    def setBattleFinished(self, boolVal):
        self.battleFinished = boolVal

    def getPokemonDAL(self):
        return self.pokemonDAL

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

