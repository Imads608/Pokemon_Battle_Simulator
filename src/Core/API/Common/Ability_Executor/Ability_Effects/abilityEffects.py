from src.Core.API.Common.Data_Types.pokemonTemporaryMetadata import PokemonTemporaryMetadata
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

from pubsub import pub

class AbilityEffects(object):
    def __init__(self, abilityName, typeBattle, battleProperties, pokemonDAL):
        self.name = abilityName
        self.typeBattle = typeBattle
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None
        self.currentWeather = None
        self.hazards = [None, None, None]
        self.pokemonDAL = pokemonDAL

        # Temporary Fields
        self.pokemonBattler = None
        self.playerBattler = None
        self.pokemonBattlerTempProperties = None
        self.playerAction = None

        self.opponentPokemonBattler = None
        self.opponentPlayerBattler = None
        self.opponentPokemonBattlerTempProperties = None
        self.opponentPlayerAction = None
        
        pub.subscribe(self.battleWidgetsSignalsBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())
        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())
    
    ######### Getters and Setters ########
    def getAbilityName(self):
        return self.name

    def setAbilityName(self, name):
        self.name = name

    def getTypeBattle(self):
        return self.typeBattle

    def setTypeBattle(self, typeBattle):
        self.typeBattle = typeBattle

    def getBattleProperties(self):
        return self.battleProperties

    def setBattleProperties(self, battleProperties):
        self.battleProperties = battleProperties

    def getBattleWidgetsSignals(self):
        return self.battleWidgetsSignals

    def setBattleWidgetsSignals(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    def getCurrentWeather(self):
        return self.currentWeather

    def setCurrentWeather(self, weather):
        self.currentWeather = weather

    def getAllHazards(self):
        return self.hazards

    def setAllHazards(self, allHazards):
        self.hazards = allHazards

    def getPokemonDAL(self):
        return self.pokemonDAL

    def setPokemonDAL(self, dataSource):
        self.pokemonDAL = dataSource

    def getPokemonBattler(self, typeBattler):
        if (typeBattler == "attacker"):
            return self.pokemonBattler
        return self.opponentPokemonBattler

    def setPokemonBattler(self, pokemonBattler, typeBattler):
        if (typeBattler == "attacker"):
            self.pokemonBattler = pokemonBattler
        else:
            self.opponentPokemonBattler = pokemonBattler

    def getPlayerBattler(self, typeBattler):
        if (typeBattler == "attacker"):
            return self.playerBattler
        return self.opponentPlayerBattler

    def setPlayerBattler(self, playerBattler, typeBattler):
        if (typeBattler == "attacker"):
            self.playerBattler = playerBattler
        else:
            self.opponentPlayerBattler = playerBattler

    def getPokemonTemporaryProperties(self, typeBattler):
        if (typeBattler == "attacker"):
            return self.pokemonBattlerTempProperties
        return self.opponentPokemonBattlerTempProperties

    def setPokemonTemporaryProperties(self, pokemonTemporaryProperties, typeBattler):
        if (typeBattler == "attacker"):
            self.pokemonBattlerTempProperties = pokemonTemporaryProperties
        else:
            self.opponentPokemonBattlerTempProperties = pokemonTemporaryProperties

    def getPlayerAction(self, typeBattler):
        if (typeBattler == "attacker"):
            return self.playerAction
        return self.opponentPlayerAction

    def setPlayerAction(self, playerAction, typeBattler):
        if (typeBattler == "attacker"):
            self.playerAction = playerAction
        else:
            self.opponentPlayerAction = playerAction

    ######### Setup and Destroyers ###########
    def setupFields(self, playerBattler, opponentPlayerBattler=None, playerAction=None, pokemonBattlerTuple=None, opponentPokemonBattlerTuple=None):
        if (self.typeBattle == BattleTypes.SINGLES):
            return self.setupSinglesFields(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple)

    def setupSinglesFields(self, playerBattler, opponentPlayerBattler=None, playerAction=None, pokemonBattlerTuple=None, opponentPokemonBattlerTuple=None):
        (indefiniteEffectsNode, tempEffectsNode) = playerBattler.getCurrentPokemon().getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return False
        if (indefiniteEffectsNode != None and indefiniteEffectsNode.getAbilitySuppressed() == True):
            return False

        self.playerBattler = playerBattler
        self.pokemonBattler = playerBattler.getCurrentPokemon()
        self.pokemonBattlerTempProperties = PokemonTemporaryMetadata(self.pokemonBattler)
        self.playerAction = playerAction

        self.opponentPlayerBattler = opponentPlayerBattler
        if (opponentPlayerBattler != None):
            self.opponentPokemonBattler = self.opponentPlayerBattler.getCurrentPokemon()
            self.opponentPokemonBattlerTempProperties = PokemonTemporaryMetadata(self.opponentPokemonBattler)

        if (pokemonBattlerTuple != None):
            self.pokemonBattler = pokemonBattlerTuple[0]
            self.pokemonBattlerTempProperties = pokemonBattlerTuple[1]

        if (opponentPokemonBattlerTuple != None):
            self.opponentPokemonBattler = opponentPokemonBattlerTuple[0]
            self.opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]
        return True

    def setupDoublesFields(self):
        pass

    def destroyTemporaryFields(self):
        self.pokemonBattler = None
        self.playerBattler = None
        self.pokemonBattlerTempProperties = None
        self.playerAction = None

        self.opponentPokemonBattler = None
        self.opponentPlayerBattler = None
        self.opponentPokemonBattlerTempProperties = None
        self.opponentPlayerAction = None


    ######### Listeners #########
    def battleWidgetsSignalsBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    def battleFieldWeatherListener(self, currentWeather):
        self.currentWeather = currentWeather

    def battleFieldHazardsListener(self, hazardsByP1, hazardsByP2, fieldHazards):
        self.hazards[0] = hazardsByP1
        self.hazards[1] = hazardsByP2
        self.hazards[2] = fieldHazards

    ######### Ability Effects #########
    def entryEffects(self, playerBattler, opponentPlayerBattler):
        if (self.setupFields(playerBattler, opponentPlayerBattler) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesEntryEffects()
        self.destroyTemporaryFields()

    def priorityEffects(self, playerBattler, opponentPlayerBattler, playerAction):
        if (self.setupFields(playerBattler, opponentPlayerBattler, playerAction) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesPriorityEffects()
        self.destroyTemporaryFields()

    def switchedInEffects(self):
        pass

    def switchedOutEffects(self, playerBattler):
        if (self.setupFields(playerBattler) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesSwitchedOutEffects()
        self.destroyTemporaryFields()

    def attackerMoveEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.setupFields(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesAttackerMoveEffects()
        self.destroyTemporaryFields()
    
    def opponentMoveEffects(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        if (self.setupFields(playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesOpponentMoveEffects()
        self.destroyTemporaryFields()

    def endofTurnEffects(self, playerBattler, opponentPlayerBattler):
        if (self.setupFields(playerBattler, opponentPlayerBattler) == False):
            return

        if (self.typeBattle == BattleTypes.SINGLES):
            self.singlesEndofTurnEffects()
        self.destroyTemporaryFields()

    ######## Singles Ability Effects #######
    def singlesEntryEffects(self):
        pass

    def singlesPriorityEffects(self):
        pass

    def singlesSwitchedInEffects(self):
        pass

    def singlesSwitchedOutEffects(self):
        pass

    def singlesAttackerMoveEffects(self):
        pass

    def singlesOpponentMoveEffects(self):
        pass

    def singlesEndofTurnEffects(self):
        pass

    ####### Doubles Ability Effects #######

    
