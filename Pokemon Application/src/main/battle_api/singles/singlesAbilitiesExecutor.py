import sys
sys.path.append("../common/")

from pokemonTemporaryProperties import PokemonTemporaryProperties

from pubsub import pub

class SinglesAbilitiesExecutor(object):
    def __init__(self, pokemonMetadata, battleProperties):
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties

        # Battle Field Subscribers/Listeners
        self.currWeather = None
        self.allHazards = {}
        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())

        # Temporary Fields/Attributes
        self.pokemonBattler = None
        self.pokemonBattlerTempProperties = None
        self.playerAction = Nonea

        self.opponentPokemonBattler = None
        self.opponentPokemonBattlerTempProperties = None
        self.opponentPlayerAction = None

    ############# Visible Methods #############
    def getPokemonEntryEffects(self, playerBattler, opponentBattler, pokemonAbility):
        self.pokemonBattler = playerBattler.getPokemonTeam()[playerBattler.getCurrentPokemon()]
        self.pokemonBattlerTempProperties = PokemonTemporaryProperties(self.pokemonBattler)
        self.opponentPokemonBattler = opponentBattler.getPokemonTeam()[opponentBattler.getCurrentPokemon()]
        self.opponentPokemonBattlerTempProperties = PokemonTemporaryProperties(self.opponentPokemonBattler)
        self.determineAbilityEffects("entry effects", self.pokemonBattler.getInternalAbility())
        self.destroyTemporaryFields()


    ########### Listeners ###############
    def battleFieldWeatherListener(self, currentWeather):
        self.currWeather = currentWeather

    def battleFieldHazardsListener(self, hazardsByP1, hazardsByP2, fieldHazards):
        if (hazardsByP1 == None):
            self.allHazards.pop("p1")
        elif (hazardsByP1 != None):
            self.allHazards.update({"p1": hazardsByP1})
        if (hazardsByP2 == None):
            self.allHazards.pop("p2")
        elif (hazardsByP2 != None):
            self.allHazards.update({"p2": hazardsByP2})
        if (fieldHazards == None):
            self.allHazards.pop("p1")
        elif (fieldHazards != None):
            self.allHazards.update({"field": fieldHazards})

    ############### Helpers ##############
    def destroyTemporaryFields(self):
        self.pokemonBattler = None
        self.pokemonBattlerTempProperties = None
        self.playerAction = None
        self.opponentPokemonBattler = None
        self.opponentPokemonBattlerTempProperties = None
        self.opponentPlayerAction = None

    def determineAbilityEffects(self, stateInBattle, pokemonAbility):
        if (pokemonAbility == "DOWNLOAD"):
            if (stateInBattle == "entry"):
                if (self.opponentPokemonBattler.getBattleStats()[2] < self.opponentPokemonBattler.getBattleStats()[4]):
                    self.pokemonBattler.setBattleStat(1, int(self.pokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(deviation=1)))
                    self.pokemonBattler.setStatStage(1, self.pokemonBattler.getStatsStages()[1]+1)
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "\'s Download raised its Attack")
                else:
                    self.pokemonBattler.setBattleStat(3, int(self.pokemonBattler.getBattleStats()[3] * self.battleProperties.getStatsStageMultiplier(deviation=1)))
                    self.pokemonBattler.setStatStage(3, self.pokemonBattler.getStatsStages()[3]+1)
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "\'s Download raised its Speciat Attack")
        elif (pokemonAbility == "INTIMIDATE"):
            if (stateInBattle == "entry"):
                currentNodeEffects = self.pokemonBattler.getTemporaryEffects().seek()
                if (currentNodeEffects.isSubstitueActive() == True):
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.opponentPokemonBattler.getName() + "'s Substitute prevented Intimidate from activating")
                if (self.opponentPokemonBattler.getInternalAbility() == "CONTRARY" and self.opponentPokemonBattler.getStatsStages()[1] != 6):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(1)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1]+1)
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "\'s Intimidate increased " + self.opponentPokemonBattler.getName() + "\'s Attack")
                elif (self.opponentPokemonBattler.getInternalAbility() == "SIMPLE" and self.opponentPokemonBattler.getStatsStages()[1] > -5):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-2)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 2)
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "\'s Intimidate sharply decreased " + self.opponentPokemonBattler.getName() + "\'s Attack")
                elif (self.opponentPokemonBattler.getInternalAbility() in ["CLEARBODY", "HYPERCUTTER", "WHITESMOKE"]):
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.opponentPokemonBattler.getName() + "\'s " + self.opponentPokemonBattler.getInternalAbility() + " prevented " + self.pokemonBattler.getName() + "\'s Intimiade from activating.")
                elif (self.opponentPokemonBattler.getStatsStages()[1] != -6):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-1)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 1)
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "\'s Intimidate decreased " + self.opponentPokemonBattler.getName() + "\'s Attack")
        elif (pokemonAbility == "DRIZZLE"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), requestedWeather=("rain", sys.maxsize))
                pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Drizzle made it Rain")
        elif (pokemonAbility == "DROUGHT"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), requestedWeather=("sunny", sys.maxsize))
                pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Drought made it Sunny")
        elif (pokemonAbility == "SANDSTREAM"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), requestedWeather=("sandstorm", sys.maxsize))
                pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Sandstream brewed a Sandstorm")
        elif (pokemonAbility == "SNOWWARNING"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), requestedWeather=("hail", sys.maxsize))
                pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Snow Warning made it Hail")
        elif (pokemonAbility == "FRISK"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Frisk showed " + self.opponentPokemonBattler.getName() + "'s held item")
                tupleData = self.pokemonMetadata.getItemsMetadata().get(self.opponentPokemonBattler.getInternalItem())
                if (tupleData == None):
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.opponentPokemonBattler.getName() + " is not holding an item")
                else:
                    fullName, _, _, _, _ = tupleData
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.opponentPokemonBattler.getName() + " is holding " + fullName)
        elif (pokemonAbility == "ANTICIPATION"):
            if (stateInBattle == "entry"):
                pokemonPokedex = self.pokemonMetadata.getPokedex().get(self.pokemonBattler.pokedexEntry)
                for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
                    if (self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + " shudders")
                    elif ((internalMoveName == "FISSURE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + " shudders")
        elif (pokemonAbility == "FOREWARN"):
            if (stateInBattle == "Entry"):
                maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Forewarn reveals " + self.opponentPokemonBattler.getName() + "'s strongest move to be " + moveName)
        elif (pokemonAbility == "TRACE"):  #TODO: Skill swap move functionality
            if (stateInBattle == "Entry"):
                if (self.opponentPokemonBattler.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
                    self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
                    _, fullName, _ = self.pokemonBattler.getAbilitiesMetadata().get(self.opponentPokemonBattler.getInternalName())
                    pub.sendMessage(self.battleProperties.getUpdateBattleInfoTopic(), message=self.pokemonBattler.getName() + "'s Trace caused its ability to change to " + fullName)
                    abilityChanged = True
                self.currPokemon.getTemporaryEffects().enQueue("ability changed", [True, True, {"Trace Activated": True}], -1)
        elif (pokemonAbility == "IMPOSTER"):
            if (stateInBattle == "Entry"):
                temporaryEffectsMap = self.opponentPokemonBattler.getTemporaryEffects().seek()
                ignoreFlag = True
                if (temporaryEffectsMap.get("illusion") != None):
                    metadata = temporaryEffectsMap.get("illusion")
                    if (metadata[1] == True):
                        ignoreFlag = False
                elif (temporaryEffectsMap.get("substitute") != None):
                    metadata = temporaryEffectsMap.get("substitute")
                    if (metadata[1] == True):
                        ignoreFlag = False
                if (ignoreFlag == True):
                    self.currPokemon.getTemporaryEffects().enQueue("disguise", [True, True, {"illusion": [True, copy.deepcopy(self.currPokemon)]}])
                    battleStats = copy.deepcopy(self.opponentPokemon.getBattleStats())
                    battleStats[0] = self.currPokemon.getBattleStats()[0]
                    types = copy.deepcopy(self.opponentPokemon.getTypes())
                    internalMovesMap = copy.deepcopy(self.opponentPokemon.getInternalMovesMap())
                    for moveIndex in internalMovesMap.keys():
                        tupleMetadata = internalMovesMap.get(moveIndex)
                        newTupleMetadata = (tupleMetadata[0], tupleMetadata[1], 5)
                        internalMovesMap.update({moveIndex: newTupleMetadata})
                    self.currPokemon.setBattleStats(self.opponentPokemon.getBattleStats())
                    self.currPokemon.setImage(self.opponentPokemon.getImage())
                    self.currPokemon.setInternalMovesMap(internalMovesMap)
                    self.currPokemon.setInternalAbility(self.opponentPokemon.getInternalAbility())
                    self.currPokemon.setWeight(self.opponentPokemon.getWeight())
                    self.currPokemon.setTypes(types)
                    self.battleTab.showPokemonBattleInfo(self.currPlayerWidgets, "view")
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + " transformed")
