from pubsub import pub

class BattleFieldManager(object):
    def __init__(self, pokemonDB, battleProperties):
        self.pokemonDB = pokemonDB
        self.battleProperties = battleProperties
        self.weather = None
        self.weatherInEffect = True
        self.player1Hazards = {}
        self.player2Hazards = {}
        self.fieldHazards = {}

    def getPokemonDB(self):
        return self.pokemonDB

    def getBattleProperties(self):
        return self.battleProperties

    def getWeather(self):
        if (self.weather == None or self.weatherInEffect == False):
            return None
        return self.weather[0]

    def setWeather(self, weather):
        self.weather = weather

    def getPlayerHazards(self, playerNum):
        if (playerNum == 1):
            return self.player1Hazards
        return self.player2Hazards

    def setPlayerHazards(self, playerNum, hazards):
        if (playerNum == 1):
            self.player1Hazards = hazards
        else:
            self.player2Hazards = hazards

    def getFieldHazards(self):
        return self.fieldHazards

    def setFieldHazards(self, hazards):
        self.fieldHazards = hazards

    def determineEntryHazardEffects(self, playerWidgets, pokemon):
        if (pokemon.getPlayerNum() == 1):
            hazardsMap = self.player2Hazards
        else:
            hazardsMap = self.player1Hazards

        if (hazardsMap.get("Spikes") != None and "FLYING" not in pokemon.getTypes() and pokemon.getInternalAbility() != "LEVITATE" and pokemon.getInternalAbility() != "MAGICGUARD"):
            tupleData = hazardsMap.get("Spikes")
            damage = int(pokemon.getFinalStats()[0] * self.battleProperties.getSpikesLayerDamage()[tupleData[1] - 1])
            message = pokemon.getName() + " took some damage from Spikes"
            pub.sendMessage(self.battleProperties.getPokemonDamageTopic(), pokemon, playerWidgets, damage, message)
        if (hazardsMap.get("Toxic Spikes") != None and "FLYING" not in pokemon.getTypes() and pokemon.getInternalAbility() != "LEVITATE" and pokemon.getNonVolatileStatusConditionIndex() == None):
            tupleData = hazardsMap.get("Toxic Spikes")
            pokemon.setNonVolatileStatusConditionIndex(tupleData[1])
            if (tupleData[1] == 1):
                message = pokemon.getName() + " became poisoned due to Toxic Spikes"
            else:
                message = pokemon.getName() + " became badly poisoned due to Toxic Spikes"
            pub.sendMessage(self.battleProperties.getStatusConditionBattleTopic(), pokemon, playerWidgets, message)
        if (hazardsMap.get("Stealth Rock") != None and pokemon.getInternalAbility() != "MAGICGUARD"):
            pokemonPokedex = self.getPokemonDB().getPokedex().get(pokemon.getPokedexEntry())
            if (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    damage = int(pokemon.getFinalStats()[0] * 3.125 / 100)
                else:
                    damage = int(pokemon.getFinalStats()[0] * 6.25 / 100)
            elif (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    damage = int(pokemon.getFinalStats()[0] * 25 / 100)
                else:
                    damage = int(pokemon.getBattleStats()[0] / 2)
            else:
                damage = int(pokemon.getFinalStats()[0] * 12.5 / 100)
            message = pokemon.getName() + " took damage from Stealth Rock"
            pub.sendMessage(self.battleProperties.getPokemonDamageTopic(), pokemon, playerWidgets, damage, message)
        if (hazardsMap.get("Sticky Web") != None):
            if (pokemon.getInternalAbility() != "MAGICGUARD"):
                pokemon.setBattleStat(5, int(pokemon.getBattleStats()[5] * self.battleProperties.getStatsStageMultipliers()[self.battleProperties.getStatsStage0Index() - 1]))
                pokemon.setStatStage(5, pokemon.getStatsStages()[5] - 1)
                message = pokemon.getName() + "\'s Speed fell due to Sticky Web"
                pub.sendMessage(self.battleProperties.battleInfoTopic(), message)
            elif (currPokemon.getInternalAbility() == "CONTRARY"):
                pokemon.setBattleStat(5, int(pokemon.getBattleStats()[5] * self.battleProperties.getStatsStageMultipliers()[self.battleProperties.getStatsStage0Index() + 1]))
                pokemon.setStatStage(5, pokemon.getStatsStages()[5] + 1)
                message = pokemon.getName() + "\'s Speed rose due to Contrary"
                pub.sendMessage(self.battleProperties.battleInfoTopic(), message)

        return



