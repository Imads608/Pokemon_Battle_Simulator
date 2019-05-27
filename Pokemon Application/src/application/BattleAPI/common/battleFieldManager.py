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
        damage = 0
        message = ""

        if (hazardsMap.get("Spikes") != None and "FLYING" not in pokemon.getTypes() and pokemon.getInternalAbility() != "LEVITATE" and pokemon.getInternalAbility() != "MAGICGUARD"):
            tupleData = hazardsMap.get("Spikes")
            damage = int(pokemon.getFinalStats()[0] * self.battleProperties.getSpikesLayerDamage()[tupleData[1] - 1])
            message = pokemon.getName() + " took some damage from Spikes"
            pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), pokemon, playerWidgets, damage, message)
        if (hazardsMap.get("Toxic Spikes") != None and "FLYING" not in pokemon.getTypes() and pokemon.getInternalAbility() != "LEVITATE" and pokemon.getNonVolatileStatusConditionIndex() == None):
            tupleData = hazardsMap.get("Toxic Spikes")
            pokemon.setNonVolatileStatusConditionIndex(tupleData[1])
            if (tupleData[1] == 1):
                message += "\n" + currPokemon.name + " became poisoned"
            else:
                message += "\n" + currPokemon.name + " became badly poisoned"
        if (hazardsMap.get("Stealth Rock") != None and currPokemon.getInternalAbility() != "MAGICGUARD"):
            pokemonPokedex = self.getPokemonDB().getPokedex().get(currPokemon.getPokedexEntry())
            if (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.resistances) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.resistances)
                if (effectiveness == 0.25):
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 3.125 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 6.25 / 100)))
            elif (self.checkTypeEffectivenessExists("ROCK", pokemonPokedex.weaknesses) == True):
                effectiveness = self.getTypeEffectiveness("ROCK", pokemonPokedex.weaknesses)
                if (effectiveness == 2):
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 25 / 100)))
                else:
                    currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] / 2))
            else:
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] - (currPokemon.getFinalStats()[0] * 12.5 / 100)))
            message = currPokemon.getName() + " took damage from Stealth Rock"
        if (hazardsMap.get("Sticky Web") != None):
            if (currPokemon.getInternalAbility() != "MAGICGUARD"):
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] * self.getStatsStageMultipliers()[self.stage0Index - 1]))
                currPokemon.setStatStage(0, currPokemon.getStatsStages()[0] - 1)
                message = currPokemon.getName() + "\'s Speed fell due to Sticky Web"
            elif (currPokemon.getInternalAbility() == "CONTRARY"):
                currPokemon.setBattleStat(0, int(currPokemon.getBattleStats()[0] * self.getStatsStageMultipliers()[self.stage0Index + 1]))
                currPokemon.setStatStage(0, currPokemon.getStatsStages()[0] + 1)

        if (currPokemon.getBattleStats()[0] <= 0):
            currPokemon.setBattleStat(0, 0)
            currPokemon.setIsFainted(True)

        return message



