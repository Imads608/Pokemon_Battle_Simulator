from pubsub import pub

class BattleFieldManager(object):
    def __init__(self, pokemonMetadata, battleProperties):
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None

        self.weather = None
        self.weatherInEffect = True
        self.player1Hazards = {}
        self.player2Hazards = {}
        self.fieldHazards = {}
        self.weatherRequestUpdateTopic = ""

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
        pub.sendMessage(self.battleProperties.getHazardsBroadcastTopic(), hazardsByP1=self.getPlayerHazards(1), hazardsByP2=self.getPlayerHazards(2), fieldHazards=self.getFieldHazards())
        
    ######## Subscribers/Listeners ###########
    def battleWidgetsSignaslBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    def requestWeatherUpdateListener(self, weatherRequested):
        self.setWeather(weatherRequested)
        
    def requestHazardUpdateListener(self, keyValueTuple, playerNum=None):
        if (playerNum == None):
            self.battleFieldManager.addFieldHazard(keyValueTuple)
        else:
            self.battleFieldManager.addPlayerHazard(playerNum, keyValueTuple)

    def requestWeatherInEffectToggleListener(self, toggleVal):
        self.weatherInEffect = toggleVal
        self.broadcastWeatherChanges()

    def determineEntryHazardEffectsListener(self, pokemonBattler):
        if (pokemonBattler.getPlayerNum() == 1):
            hazardsMap = self.player2Hazards
        else:
            hazardsMap = self.player1Hazards

        if (hazardsMap.get("spikes") != None and hazardsMap.get("spikes")[0] == True and "FLYING" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["LEVITATE","MAGICGUARD"]):
            tupleData = hazardsMap.get("spikes")
            damage = int(pokemonBattler.getFinalStats()[0] * self.battleProperties.getSpikesLayerDamage()[tupleData[1] - 1])
            message = pokemonBattler.getName() + " took some damage from Spikes"
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, message)
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (hazardsMap.get("toxic spikes") != None and hazardsMap.get("toxic spikes")[0] == True and "FLYING" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() != "LEVITATE" and pokemonBattler.getNonVolatileStatusConditionIndex() == 0):
            tupleData = hazardsMap.get("Toxic Spikes")
            pokemonBattler.setNonVolatileStatusConditionIndex(tupleData[2])
            if (tupleData[2] == 1):
                message = pokemonBattler.getName() + " became poisoned due to Toxic Spikes"
            else:
                message = pokemonBattler.getName() + " became badly poisoned due to Toxic Spikes"
            self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, message)
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (hazardsMap.get("stealth rock") != None and hazardsMap.get("stealth rock")[0] == True and pokemonBattler.getInternalAbility() != "MAGICGUARD"):
            pokemonPokedex = self.pokemonMetadata.getPokedex().get(pokemonBattler.getPokedexEntry())
            if (self.battleProperties.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.battleProperties.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    damage = int(pokemonBattler.getFinalStats()[0] * 3.125 / 100)
                else:
                    damage = int(pokemonBattler.getFinalStats()[0] * 6.25 / 100)
            elif (self.battleProperties.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.battleProperties.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    damage = int(pokemonBattler.getFinalStats()[0] * 25 / 100)
                else:
                    damage = int(pokemonBattler.getBattleStats()[0] / 2)
            else:
                damage = int(pokemonBattler.getFinalStats()[0] * 12.5 / 100)
            message = pokemonBattler.getName() + " took damage from Stealth Rock"
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, message)
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (hazardsMap.get("sticky web") != None and hazardsMap.get("sticky web")[0] == True):
            if (pokemonBattler.getInternalAbility() != "MAGICGUARD"):
                pokemonBattler.setBattleStat(5, int(pokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(-1)))
                pokemonBattler.setStatStage(5, pokemon.getStatsStages()[5] - 1)
                message = pokemonBattler.getName() + "\'s Speed fell due to Sticky Web"
                self.battleWidgetsSignals.getBattleMessageSignal().emit(message)
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()
            elif (pokemonBattler.getInternalAbility() == "CONTRARY"):
                pokemonBattler.setBattleStat(5, int(pokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1)))
                pokemonBattler.setStatStage(5, pokemonBattler.getStatsStages()[5] + 1)
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
        damage = int(pokemonBattler.getFinalStats()[0] / 16)
        if (self.getWeather() == "sandstorm" and doesAffect == True):
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, pokemonBattler.getName() + " is buffeted by the sandstorm")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        elif (self.getWeather() == "hail" and doesAffect == True):
            self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, damage, pokemonBattler.getName() + " is hurt by hail")
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()
        if (pokemonBattler.getIsFainted() == True):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(pokemonBattler.getPlayerNum())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()

    ####### Helpers ###########
    def weatherAffectPokemon(self, pokemonBattler):
        if (self.getWeather() == None or pokemonBattler.getInternalAbility() == "MAGICGUARD"):
            return False
        elif (self.getWeather() == "sandstorm"):
            if ("ROCK" not in pokemonBattler.getTypes() and "GROUND" not in pokemonBattler.getTypes() and "STEEL" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["SANDFORCE", "SANDVEIL", "SANDRUSH"] and pokemonBattler.getInternalItem() != "SANDGOGGLES"):
                return True
        elif (self.getWeather() == "hail"):
            if ("ICE" not in pokemonBattler.getTypes() and pokemonBattler.getInternalAbility() not in ["ICEBODY", "SNOWCLOAK", "MAGICGUARD", "OVERCOAT", "SLUSHRUSH"] and pokemonBattler.getInternalItem() != "SAFETYGOGGLES"):
                return True
        elif (self.getWeather() == "sunny" and pokemonBattler.getInternalAbility() == "DRYSKIN"):
            return True
        return False

    def updateWeatherTurnsRemaining(self):
        if (self.getWeather() == None):
            return
        self.weather = (self.weather[0], self.weather[1]-1)

    def updatePlayerHazardsRemaining(self, playerNum):
        pass

    ####### Getters and Setters ###########
    def getPokemonMetadata(self):
        return self.pokemonMetadata

    def getBattleProperties(self):
        return self.battleProperties

    def getWeather(self):
        if (self.weather == None or self.weatherInEffect == False):
            return None
        return self.weather[0]

    def setWeather(self, weather):
        self.weather = weather
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


