from pubsub import pub
from src.Core.API.Common.Data_Types.weather import Weather
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Core.API.Common.Data_Types.playerHazards import PlayerHazards
from src.Core.API.Common.Data_Types.fieldHazards import BattleFieldHazards
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stageChanges import StageChanges

class BattleFieldManager(object):
    def __init__(self, pokemonDAL, battleProperties):
        self.pokemonDAL = pokemonDAL
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None

        self.weather = Weather()
        self.player1Hazards = PlayerHazards()
        self.player2Hazards = PlayerHazards()
        self.fieldHazards = BattleFieldHazards()

        pub.subscribe(self.battleWidgetsSignaslBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())
        pub.subscribe(self.requestWeatherUpdateListener, self.battleProperties.getWeatherRequestTopic())
        pub.subscribe(self.requestWeatherInEffectToggleListener, self.battleProperties.getWeatherInEffectToggleRequestTopic())
        pub.subscribe(self.requestHazardUpdateListener, self.battleProperties.getHazardsRequestTopic())
        pub.subscribe(self.determineEntryHazardEffectsListener, self.battleProperties.getBattleFieldEntryHazardEffectsTopic())
        pub.subscribe(self.updateEoTEffectsListener, self.battleProperties.getBattleFieldUpdateEoTEffectsTopic())
        pub.subscribe(self.updateWeatherDamageonPokemonListener, self.battleProperties.getUpdateWeatherDamageTopic())
        
    ######### Broadcast Publishers #########
    def broadcastWeatherChanges(self):
        pub.sendMessage(self.battleProperties.getWeatherBroadcastTopic(), currentWeather=self.getWeather())

    def broadcastHazardChanges(self):
        pub.sendMessage(self.battleProperties.getHazardsBroadcastTopic(), hazardsByP1=self.player1Hazards, hazardsByP2=self.player2Hazards, fieldHazards=self.fieldHazards)
        
    ######## Subscribers/Listeners ###########
    def battleWidgetsSignaslBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    def requestWeatherUpdateListener(self, weatherRequested, numTurns):
        self.setWeather(weatherRequested, numTurns)
        
    def requestHazardUpdateListener(self, updatedHazards, playerNum=None):
        if (playerNum == None):
            self.addFieldHazard(updatedHazards)
        else:
            self.addPlayerHazard(playerNum, updatedHazards)

    def requestWeatherInEffectToggleListener(self, toggleVal):
        self.weather.inEffect = toggleVal
        self.broadcastWeatherChanges()


    ################# Main Functions ##########################
    def determineEntryHazardEffectsListener(self, pokemonBattler):
        if (pokemonBattler.getPlayerNum() == 1):
            playerHazards = self.player2Hazards
        else:
            playerHazards = self.player1Hazards

        if (playerHazards.spikes[0] == True and "FLYING" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["LEVITATE", "MAGICGUARD"]):
            damage = int(pokemonBattler.getGivenStat(Stats.HP) * self.battleProperties.getSpikesLayerDamage()[playerHazards.spikes[1]])
            message = pokemonBattler.getName() + " took some damage from Spikes"
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, message)
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (playerHazards.toxic_spikes[0] == True and "FLYING" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() != "LEVITATE" and pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.HEALTHY):
            pokemonBattler.setNonVolatileStatusCondition(playerHazards.toxic_spikes[1])
            if (playerHazards.toxic_spikes[1] == NonVolatileStatusConditions.POISONED):
                message = pokemonBattler.getName() + " became poisoned due to Toxic Spikes"
            else:
                message = pokemonBattler.getName() + " became badly poisoned due to Toxic Spikes"
            self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, message)
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (playerHazards.steath_rock == True and pokemonBattler.getInternalAbility() != "MAGICGUARD"):
            pokemonPokedex = self.pokemonDAL.getPokedexEntryForNumber(pokemonBattler.getPokedexEntry())
            effectiveness = self.battleProperties.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
            damageOutput = self.battleProperties.getStealthRockDamageFromEffectiveness(str(effectiveness))
            damageTaken = int(pokemonBattler.getGivenStat(Stats.HP) * damageOutput / 100)
            if (damageTaken > 0):
                message = pokemonBattler.getName() + " took damage from Stealth Rock"
                self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damageTaken, message)
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()
        if (playerHazards.sticky_web == True):
            if (pokemonBattler.getInternalAbility() != "MAGICGUARD"):
                pokemonBattler.setBattleStat(Stats.SPEED, int(pokemonBattler.getBattleStat(Stats.SPEED) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGENEG1)))
                pokemonBattler.setStatStage(Stats.SPEED, pokemonBattler.getStatsStage(Stats.SPEED) + StageChanges.STAGENEG1)
                message = pokemonBattler.getName() + "\'s Speed fell due to Sticky Web"
                self.battleWidgetsSignals.getBattleMessageSignal().emit(message)
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()
            elif (pokemonBattler.getInternalAbility() == "CONTRARY"):
                pokemonBattler.setBattleStat(Stats.SPEED, int(pokemonBattler.getBattleStat(Stats.SPEED) * self.battleProperties.getStatsStageMultiplier(StageChanges.STAGE1)))
                pokemonBattler.setStatStage(Stats.SPEED, pokemonBattler.getStatsStage(Stats.SPEED) + StageChanges.STAGE1)
                message = pokemonBattler.getName() + "\'s Speed rose due to Contrary"
                self.battleWidgetsSignals.getBattleMessageSignal().emit(message)
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()
        return

    def updateEoTEffectsListener(self):
        self.updateWeatherTurnsRemaining()
        self.updatePlayerHazardsRemaining(1)
        self.updatePlayerHazardsRemaining(2)
        self.broadcastWeatherChanges()
        self.broadcastHazardChanges()

    def updateWeatherDamageonPokemonListener(self, pokemonBattler):
        doesAffect = self.weatherAffectPokemon(pokemonBattler)
        damage = int(pokemonBattler.getGivenStats()[Stats.HP] / 16)
        if (self.getWeather() == WeatherTypes.SANDSTORM and doesAffect == True):
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, pokemonBattler.getName() + " is buffeted by the sandstorm")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        elif (self.getWeather() == WeatherTypes.HAIL and doesAffect == True):
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by hail")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (pokemonBattler.getIsFainted() == True):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(pokemonBattler.getPlayerNum())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    ####### Helpers ###########
    def weatherAffectPokemon(self, pokemonBattler):
        if (self.getWeather() == WeatherTypes.NORMAL or pokemonBattler.getInternalAbility() == "MAGICGUARD"):
            return False
        elif (self.getWeather() == WeatherTypes.SANDSTORM):
            if ("ROCK" not in pokemonBattler.getTypes() and "GROUND" not in pokemonBattler.getTypes() and "STEEL" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["SANDFORCE", "SANDVEIL", "SANDRUSH"] and pokemonBattler.getInternalItem() != "SANDGOGGLES"):
                return True
        elif (self.getWeather() == WeatherTypes.HAIL):
            if ("ICE" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["ICEBODY", "SNOWCLOAK", "MAGICGUARD", "OVERCOAT", "SLUSHRUSH"] and pokemonBattler.getInternalItem() != "SAFETYGOGGLES"):
                return True
        elif (self.getWeather() == WeatherTypes.SUNNY and pokemonBattler.getInternalAbility() == "DRYSKIN"):
            return True
        return False

    def updateWeatherTurnsRemaining(self):
        if (self.getWeather() == WeatherTypes.NORMAL):
            return
        self.weather.turnsRemaining -= 1
        if (self.weather.turnsRemaining == 0):
            self.weather.weatherType = WeatherTypes.NORMAL
            self.battleWidgetsSignals.getBattleMessageSignal().emit("The weaether turned back to normal")

    def updatePlayerHazardsRemaining(self, playerNum):
        pass

    ####### Getters and Setters ###########
    def getPokemonDAL(self):
        return self.pokemonDAL

    def getBattleProperties(self):
        return self.battleProperties

    def getWeather(self):
        if (self.weather.inEffect == False):
            return WeatherTypes.NORMAL
        return self.weather.weatherType

    def setWeather(self, weather, numTurns):
        self.weather.weatherType = weather
        self.weather.inEffect = True
        self.weather.turnsRemaining = numTurns
        self.broadcastWeatherChanges()

    def getPlayerHazards(self, playerNum):
        if (playerNum == 1):
            return self.player1Hazards
        return self.player2Hazards

    def setPlayerHazards(self, playerNum, hazards):
        if (playerNum == 1):
            self.player1Hazards = hazards
        else:
            self.player2Hazards = hazards

    def addPlayerHazard(self, playerNum, keyValueTuple):
        pass

    def getFieldHazards(self):
        return self.fieldHazards

    def setFieldHazards(self, hazards):
        self.fieldHazards = hazards

    def addFieldHazard(self, keyValueTuple):
        pass


