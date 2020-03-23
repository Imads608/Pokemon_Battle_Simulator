from pubsub import pub

class FunctionCode(object):
    def __init__(self, battleProperties, pokemonDataSource, typeBattle):
        self.playerBattler = None
        self.playerAction = None
        self.pokemonBattlerTuple = None
        self.opponentPokemonBattlerTuple = None
        self.battleProperties = battleProperties
        self.typeBattle = typeBattle
        self.pokemonDataSource = pokemonDataSource

        self.battleWidgetsSignals = None
        self.currentWeather = None
        self.allHazards = {}

        pub.subscribe(self.battleWidgetsSignalsBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())
        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())

    ######### Listeners #########
    def battleWidgetsSignalsBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    def battleFieldWeatherListener(self, currentWeather):
        self.currentWeather = currentWeather

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

    ###### Setup ########
    def initializePlayerMetadata(self, playerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        self.playerBattler = playerBattler
        self.playerAction = playerAction
        self.pokemonBattlerTuple = pokemonBattlerTuple
        self.opponentPokemonBattlerTuple = opponentPokemonBattlerTuple

    def isMetadataInitialized(self):
        return (self.playerAction != None and self.pokemonBattlerTuple != None and self.opponentPokemonBattlerTuple != None and self.typeBattle != None)

    ###### Singles Effect ##########
    def singlesEffect(self):
        return


    ###### Doubles Effect #########
    def doublesEffect(self):
        return
