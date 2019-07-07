import sys
sys.path.append("../common/")

from move import Move
from singlesMoveProperties import SinglesMoveProperties

from pubsub import pub

class SinglesMoveExecutor(object):
    def __init__(self, pokemonMetadata, battleProperties):
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties

        self.currWeather = None
        self.allHazards = {}
        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())


    ############ Listeners ############
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

    ##### Helpers ################
    def checkPP(self, pokemon, moveIndex):
        movesSetMap = pokemon.internalMovesMap
        internalName, _, currPP = movesSetMap.get(moveIndex + 1)
        if (currPP > 0):
            return "Available"

        ppAvailableFlag = False
        for moveIndex in movesSetMap:
            _, _, currPP = movesSetMap.get(moveIndex + 1)
            if (currPP > 0):
                ppAvailableFlag = True

        if (ppAvailableFlag == True):
            return "Other Moves Available"
        return "All Moves Over"

    def getMovePriority(self, moveInternalName):
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
        return int(priority)

    ###### Visible Main Functions #############
    def setupMove(self, playerBattler):
        pokemonBattler = playerBattler.getCurrentPokemon()
        moveProperties = SinglesMoveProperties()
        moveObject = Move(playerBattler.getPlayerNumber(), moveProperties, pokemonBattler)
        pub.sendMessage(self.battleProperties.getPokemonMoveSelectedTopic(), pokemonBattler=pokemonBattler, move=moveObject)
        moveObject.setPriority(self.getMovePriority(moveObject.getMoveInternalName()))
        return moveObject

    def validateMove(self, move):
        if (move.getMoveIndex() == None or move.getMoveInternalName() == None):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Please select a valid move")
            return False

        ## Check PP left of move selected
        pokemon = move.getPokemonExecutor()
        moveIndex = move.getMoveIndex()
        internalMoveName = move.getMoveInternalName()
        result = self.checkPP(pokemon, moveIndex)
        if (result == "Other Moves Available"):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is out PP")
            return False
        elif (result == "All Moves Over"):
            move.setInternalMoveName("STRUGGLE")
            move.setMoveIndex(-1)
            return True

        # Check if move is blocked
        currentEffectsNode = pokemonObject.getTemporaryEffects().seek()
        if (currentEffectsNode != None):
            if (internalMoveName in currentEffectsNode.movesBlocked):
                pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is Blocked")
                return False

        if (internalMoveName == "SPLASH" and self.allHazards.get("field") != None and self.allHazards.get("field").get("GRAVITY") != None):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is Blocked")
            return False

        return True

