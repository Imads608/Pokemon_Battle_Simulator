from pubsub import pub

class SinglesMoveExecutor(object):
    def __init__(self, battleProperties):
        self.moveProperties = None
        self.battleProperties = battleProperties

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

    ###### Visible Main Functions #############

    def validateMove(self, move):
        ## Check PP left of move selected
        pokemon = move.getPokemonBattler()
        moveIndex = move.getMoveIndex()
        internalMoveName = move.getMoveInternalName()
        result = self.checkPP(pokemon, moveIndex)
        if (result == "Other Moves Available"):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), message="Move is out of PP")
            return None
        elif (result == "All Moves Over"):
            move.setInternalMoveName("STRUGGLE")
            move.setMoveIndex(-1)
            return move

        # Check if move is blocked
        effectsMap = pokemonObject.getTemporaryEffects().seek()
        if (effectsMap == None):
            return (True, None)
        values = effectsMap.get("move block")

        if (values[1].get(internalMoveName) != None):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), "Move is Blocked")
            return None
        if (internalMoveName == "SPLASH" and self.checkFieldHazardExists(self.getBattleField().getFieldHazards(), "GRAVITY") == True):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), "Move is Blocked")
            return None

        return move

