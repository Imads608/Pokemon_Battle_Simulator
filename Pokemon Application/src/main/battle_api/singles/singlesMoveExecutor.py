import sys
sys.path.append("../common/")

from move import Move
from singlesMoveProperties import SinglesMoveProperties
from pokemonTemporaryProperties import PokemonTemporaryProperties

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

    def initializeMoveProperties(self, move, pokemonBattler, opponentPokemonBattler):
        _, _, functionCode, basePower, typeMove, damageCategory, accuracy, _, _, addEffect, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(move.getMoveInternalName())

        move.setMovePower(int(basePower))
        move.setMoveAccuracy(int(accuracy))
        move.setTypeMove(typeMove)
        move.setDamageCategory(damageCategory)
        move.setFunctionCode(functionCode)
        move.setAdditionalEffect(addEffect)
        if (damageCategory == "Physical"):
            move.setTargetAttackStat(pokemonBattler.getCurrentStats()[1])
            move.setTargetDefenseStat(opponentPokemonBattler.getCurrentStats()[2])
        elif (damageCategory == "Special"):
            move.setTargetAttackStat(pokemonBattler.getCurrentStats()[3])
            move.setTargetDefenseStat(opponentPokemonBattler.getCurrentStats()[4])

    def calculateDamage(self, move, pokemonBattler):
        baseDamage = ((((2 * int(pokemonBattler.getLevel())) / 5 + 2) * move.getMovePower() * move.getTargetAttackStat()) / move.getTargetDefenseStat()) / 50 + 2
        return baseDamage

    def determineCriticalHitChance(self, move, pokemonBattlerTuple, opponentPokemonBattlerTuple, flag):
        pokemonBattler = pokemonBattlerTuple[0]
        pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]

        modifier = 1
        if (pokemonBattler.getPlayerNum() == 1):
            fieldHazardsOpponent = self.allHazards.get("p2")#self.getBattleField().getP2FieldHazards()
        else:
            fieldHazardsOpponent = self.allHazards.get("p1")

        if (opponentPokemonBattlerTempProperties.getCurrentInternalAbility() in ["BATTLEARMOR" or "SHELLARMOR"] or (fieldHazardsOpponent.get("LUCKYCHANT") != None and fieldHazardsOpponent.get("LUCKYCHANT")[0] == True)):
            move.setCriticalHit(False)
            modifier = 1  # return 1
        elif (move.getCriticalHit() == True and pokemonBattlerTempProperties.getCurrentInternalAbility() == "SNIPER"):
            modifier = 3
        elif (move.getCriticalHit() == True):
            # action.setCriticalHit()
            modifier = 2  # return 2

        stageDenominator = self.battleProperties.getCritcalHitStages()[move.getCriticalHitStage()]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and move.getCriticalHit() == False):
            action.setCriticalHit(True)
            modifier = 2  # return 2
        return modifier

    def getModifiers(self, pokemonBattlerTuple, opponentPokemonBattlerTuple, move):
        pokemonBattler = pokemonBattlerTuple[0]
        pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]

        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.pokemonMetadata.getMovesMetadata().get(move.getInternalMove())

        # Check Weather
        if (self.currWeather == "Rain" and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.multiplyModifier(1.5)
        elif (self.currWeather == "Rain" and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.multiplyModifier(0.5)
        elif (self.currWeather == "Sunny" and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.multiplyModifier(1.5)
        elif (self.currWeather == "Sunny" and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.multiplyModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(action, pokemonAttacker, pokemonOpponent, flag)
        action.multModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        action.multModifier(randomNum / 100)

        # STAB
        if (action.getTypeMove() in pokemonAttacker.getCurrentTypes()):
            if (pokemonAttacker.getCurrentInternalAbility() == "ADAPTABILITY"):
                action.multModifier(2)
            else:
                action.multModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "DOUSEDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "SHOCKDRIVE" and action.getIntenralMove() == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "BURNDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (pokemonAttacker.getName() == "GENESECT" and pokemonAttacker.getCurrentInternalItem() == "CHILLDRIVE" and action.getInternalMove() == "TECHNOBLAST"):
            typeMove = "ICE"

        pokemonPokedex = self.getPokemonDB().getPokedex().get(pokemonOpponentRead.getPokedexEntry())
        if (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.weaknesses) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.getTypeMove(), pokemonPokedex.weaknesses))
        elif (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.immunities) == True):
            action.setEffectiveness(0)
            #if ("GHOST" in pokemonOpponent.currTypes and (action.typeMove == "FIGHTING" or action.typeMove == "NORMAL")):
            #    action.multModifier(1)
            #else:
            #    action.multModifier(0)
            #    action.multModifier(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.resistances))
        elif (self.checkTypeEffectivenessExists(action.getTypeMove(), pokemonPokedex.resistances) == True):
            action.setEffectiveness(self.getTypeEffectiveness(action.getTypeMove(), pokemonPokedex.resistances))
        action.multModifier(action.getEffectiveness())

        # Burn
        if (pokemonOpponent.getCurrentInternalAbility() != "GUTS" and action.getDamageCategory() == "Physical"):
            action.multModifier(0.5)
        return

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

    def executeMove(self, move, playerBattler, opponentBattler):
        # Intialization
        pokemonTempProperties = PokemonTemporaryProperties(playerBattler.getCurrentPokemon())
        opponentPokemonTempProperties = PokemonTemporaryProperties(opponentBattler.getCurrentPokemon())
        pokemonBattlerTuple = (playerBattler.getCurrentPokemon(), pokemonTempProperties)
        opponentPokemonBattlerTuple = (opponentBattler.getCurrentPokemon(), opponentPokemonTempProperties)

        self.initializeMoveProperties(move, pokemonBattlerTuple[0], opponentPokemonBattlerTuple[0])

        #TODO: Determine Function Code Effects

        #TODO: Determine Item Effects

        #TODO: Check Weather Effects e.g Sandstorm raises special defense of rock pokemon

        #TODO: Field Effects e.g Gravity

        #TODO: Determine Pokemon Temporary Effects
        '''
        mapEffects = pokemonBattler.getCurrentTemporaryEffects().seek()
        if (mapEffects != None):
            arrMovesPowered = mapEffects.get("move powered")
            arrTypeMovesPowered = mapEffects.get("type move powered")
            if (arrMovesPowered != None):
                if (arrMovesPowered.get(action.getInternalMove()) != None):
                    metadata = arrMovesPowered.get(action.getInternalMove())
                    if (metadata[0] == True):
                        action.setTargetAttackStat(int(action.getTargetAttackStat() * metadata[1]))
            if (arrTypeMovesPowered != None):
                if (arrTypeMovesPowered.get(action.getTypeMove()) != None):
                    metadata = arrTypeMovesPowered.get(action.getTypeMove())
                    if (metadata[0] == True):
                        action.setTargetAttackStat(int(action.getTargetAttackStat() * metadata[1]))
        '''

        # Determine Modifiers
        self.getModifiers(pokemonBattlerTuple, opponentPokemonBattlerTuple, move)

        # Determine Ability Effects
        pub.sendMessage(self.battleProperties.getAbilityMoveEffectsByAttackerTopic(), playerBattler=playerBattler, opponentPlayerBattler=opponentBattler, playerAction=move, pokemonBattlerTuple=pokemonBattlerTuple, opponentPokemonBattlerTuple=opponentPokemonBattlerTuple)
        self.getAbilityEffects().determineAbilityEffects(attackerPokemon.getPlayerNum(), "Move Effect Opponent",
                                                         opponentPokemon.getCurrentInternalAbility())

        # Calculate Damage
        if (move.getDamageCategory() != "Status"):
            damage = self.calculateDamage(move, playerBattler.getCurrentPokemon())
        move.setDamage(int(damage * move.getModifier()))

        # Check if move will miss or hit
        threshold = 1
        if (move.getMoveAccuracy() != 0):
            threshold *= move.getMoveAccuracy()
            if (attackerPokemon.getCurrentInternalAbility() == "KEENEYE"):
                threshold *= self.getAccuracyEvasionMultipliers()[
                    self.getAccuracyEvasionStage0Index() + attackerPokemon.getCurrentAccuracyStage() +
                    attackerPokemon.getAccuracyEvasionStagesChangesTuples()[0][0]]
            else:
                threshold *= self.getAccuracyEvasionMultipliers()[self.getAccuracyEvasionStage0Index() + (
                            attackerPokemon.getCurrentAccuracyStage() - (
                                attackerPokemon.getAccuracyEvasionStagesChangesTuples()[0][0] -
                                opponentPokemon.getAccuracyEvasionStagesChangesTuples()[1][0]))]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    attackerPokemon.getCurrentInternalAbility() != "NOGUARD" and opponentPokemon.getCurrentInternalAbility() != "NOGUARD")):
                action.setMoveMiss(True)
                # action.setBattleMessage("Its attack missed")

        if (self.isPokemonOutOfFieldMoveMiss(attackerPokemon, opponentPokemon, action)):
            action.setMoveMiss(True)
        if (attackerPokemon.getCurrentInternalAbility() == "MAGICGUARD"):
            action.setRecoil(0)
        return