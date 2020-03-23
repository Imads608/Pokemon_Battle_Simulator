#import sys
#sys.path.append("../common/")

from battle_api.common.move import Move
from battle_api.singles.singlesMoveProperties import SinglesMoveProperties
from battle_api.common.pokemonTemporaryProperties import PokemonTemporaryProperties
from battle_api.common.functionCodesManager import FunctionCodesManager

from pubsub import pub
import random

class SinglesMoveExecutor(object):
    def __init__(self, pokemonDataSource, battleProperties):
        self.pokemonDataSource = pokemonDataSource
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None
        #self.functionCodesManager = FunctionCodesManager(battleProperties, pokemonDataSource, typeBattle="singles")

        self.currWeather = None
        self.allHazards = {}

        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())
        pub.subscribe(self.battleWidgetsSignalsBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())


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

    def battleWidgetsSignalsBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

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
        if (self.pokemonDataSource.getMovesMetadata().get(moveInternalName) == None):
            return
        _, _, _, _, _, _, _, _, _, _, _, priority, _ = self.pokemonDataSource.getMovesMetadata().get(moveInternalName)
        return int(priority)

    def initializeMoveProperties(self, move, pokemonBattler, opponentPokemonBattler):
        _, _, functionCode, basePower, typeMove, damageCategory, accuracy, _, _, addEffect, targetCode, _, flags = self.pokemonDataSource.getMovesMetadata().get(move.getMoveInternalName())

        move.getMoveProperties().setMovePower(int(basePower))
        move.getMoveProperties().setMoveAccuracy(int(accuracy))
        move.getMoveProperties().setTypeMove(typeMove)
        move.getMoveProperties().setDamageCategory(damageCategory)
        move.getMoveProperties().setFunctionCode(functionCode)
        move.getMoveProperties().setAdditionalEffect(addEffect)
        move.getMoveProperties().setTargetCode(targetCode)
        move.getMoveProperties().setMoveFlags(flags)
        if (damageCategory == "Physical"):
            move.getMoveProperties().setTargetAttackStat(pokemonBattler.getBattleStats()[1])
            move.getMoveProperties().setTargetDefenseStat(opponentPokemonBattler.getBattleStats()[2])
        elif (damageCategory == "Special"):
            move.getMoveProperties().setTargetAttackStat(pokemonBattler.getBattleStats()[3])
            move.getMoveProperties().setTargetDefenseStat(opponentPokemonBattler.getBattleStats()[4])

    def calculateDamage(self, move, pokemonBattler):
        baseDamage = ((((2 * int(pokemonBattler.getLevel())) / 5 + 2) * move.getMoveProperties().getMovePower() * move.getMoveProperties().getTargetAttackStat()) / move.getMoveProperties().getTargetDefenseStat()) / 50 + 2
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

        if (opponentPokemonBattlerTempProperties.getCurrentInternalAbility() in ["BATTLEARMOR" or "SHELLARMOR"] or (fieldHazardsOpponent != None and fieldHazardsOpponent.get("LUCKYCHANT") != None and fieldHazardsOpponent.get("LUCKYCHANT")[0] == True)):
            move.getMoveProperties().setCriticalHit(False)
            modifier = 1  # return 1
        elif (move.getMoveProperties().getCriticalHit() == True and pokemonBattlerTempProperties.getCurrentInternalAbility() == "SNIPER"):
            modifier = 3
        elif (move.getMoveProperties().getCriticalHit() == True):
            # action.setCriticalHit()
            modifier = 2  # return 2

        stageDenominator = self.battleProperties.getCriticalHitStages()[move.getMoveProperties().getCriticalHitStage()]
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and move.getMoveProperties().getCriticalHit() == False):
            move.getMoveProperties().setCriticalHit(True)
            modifier = 2  # return 2
        return modifier

    def getModifiers(self, pokemonBattlerTuple, opponentPokemonBattlerTuple, move):
        pokemonBattler = pokemonBattlerTuple[0]
        pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]

        _, _, _, _, _, _, _, _, _, _, _, _, flag = self.pokemonDataSource.getMovesMetadata().get(move.getMoveInternalName())

        # Check Weather
        if (self.currWeather == "Rain" and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(1.5)
        elif (self.currWeather == "Rain" and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(0.5)
        elif (self.currWeather == "Sunny" and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(1.5)
        elif (self.currWeather == "Sunny" and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(move, pokemonBattlerTuple, opponentPokemonBattlerTuple, flag)
        move.getMoveProperties().multiplyModifier(modifier)

        #  Random Num
        randomNum = random.randint(85, 100)
        move.getMoveProperties().multiplyModifier(randomNum / 100)

        # STAB
        if (move.getMoveProperties().getTypeMove() in pokemonBattlerTempProperties.getCurrentTypes()):
            if (pokemonBattlerTempProperties.getCurrentInternalAbility() == "ADAPTABILITY"):
                move.getMoveProperties().multiplyModifier(2)
            else:
                move.getMoveProperties().multiplyModifier(1.5)

        # Type effectiveness
        # Check edge case for GEnesect
        if (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "DOUSEDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            typeMove = "WATER"
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "SHOCKDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            typeMove = "ELECTRIC"
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "BURNDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            typeMove = "FIRE"
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "CHILLDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            typeMove = "ICE"

        opponentPokemonPokedex = self.pokemonDataSource.getPokedex().get(opponentPokemonBattler.getPokedexEntry())
        if (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.weaknesses) == True):
            move.getMoveProperties().setMoveEffectiveness(self.battleProperties.getTypeEffectiveness(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.weaknesses))
        elif (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.immunities) == True):
            move.getMoveProperties().setMoveEffectiveness(0)
            #if ("GHOST" in pokemonOpponent.currTypes and (action.typeMove == "FIGHTING" or action.typeMove == "NORMAL")):
            #    action.multModifier(1)
            #else:
            #    action.multModifier(0)
            #    action.multModifier(self.getTypeEffectiveness(action.typeMove, pokemonPokedex.resistances))
        elif (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.resistances) == True):
            move.getMoveProperties().setMoveEffectiveness(self.battleProperties.getTypeEffectiveness(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.resistances))
        move.getMoveProperties().multiplyModifier(move.getMoveProperties().getMoveEffectiveness())

        # Burn
        if (opponentPokemonBattlerTempProperties.getCurrentInternalAbility() != "GUTS" and move.getMoveProperties().getDamageCategory() == "Physical"):
            move.getMoveProperties().multiplyModifier(0.5)
        return

    def determineMoveConnects(self, move, playerBattler, opponentBattler, pokemonBattlerTuple):
        pokemonTempProperties = PokemonTemporaryProperties(playerBattler.getCurrentPokemon())
        opponentPokemonTempProperties = PokemonTemporaryProperties(opponentBattler.getCurrentPokemon())

        # Check if move will miss or hit
        threshold = 1
        if (move.getMoveProperties().getMoveAccuracy() != 0):
            threshold *= move.getMoveProperties().getMoveAccuracy()
            if (pokemonTempProperties.getCurrentInternalAbility() == "KEENEYE"):
                threshold *= self.battleProperties.getAccuracyEvasionMultipliers()[
                    self.battleProperties.getAccuracyEvasionStage0Index() + pokemonBattlerTuple[0].getAccuracyStage() +
                    pokemonTempProperties.getAccuracyStatTupleChanges()[0]]
            else:
                threshold *= self.battleProperties.getAccuracyEvasionMultipliers()[
                    self.battleProperties.getAccuracyEvasionStage0Index() + (
                                pokemonBattlerTuple[0].getAccuracyStage() - (
                                    pokemonTempProperties.getAccuracyStatTupleChanges()[0] -
                                    opponentPokemonTempProperties.getEvasionStatTupleChanges()[0]))]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    pokemonTempProperties.getCurrentInternalAbility() != "NOGUARD" and opponentPokemonTempProperties.getCurrentInternalAbility() != "NOGUARD")):
                move.getMoveProperties().setMoveMiss(True)
                # action.setBattleMessage("Its attack missed")

    def calculateMoveDetails(self, move, playerBattler, opponentBattler):
        # Intialization
        pokemonTempProperties = PokemonTemporaryProperties(playerBattler.getCurrentPokemon())
        opponentPokemonTempProperties = PokemonTemporaryProperties(opponentBattler.getCurrentPokemon())
        pokemonBattlerTuple = (playerBattler.getCurrentPokemon(), pokemonTempProperties)
        opponentPokemonBattlerTuple = (opponentBattler.getCurrentPokemon(), opponentPokemonTempProperties)

        self.initializeMoveProperties(move, pokemonBattlerTuple[0], opponentPokemonBattlerTuple[0])

        # TODO: Determine Item Effects

        # TODO: Check Weather Effects e.g Sandstorm raises special defense of rock pokemon

        # TODO: Field Effects e.g Gravity

        # TODO: Determine Pokemon Temporary Effects
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
        pub.sendMessage(self.battleProperties.getAbilityMoveEffectsByAttackerTopic(), playerBattler=playerBattler,
                        opponentPlayerBattler=opponentBattler, playerAction=move,
                        pokemonBattlerTuple=pokemonBattlerTuple,
                        opponentPokemonBattlerTuple=opponentPokemonBattlerTuple)
        # Calculate Damage
        if (move.getMoveProperties().getDamageCategory() != "Status"):
            damage = self.calculateDamage(move, playerBattler.getCurrentPokemon())
        move.getMoveProperties().setTotalDamage(int(damage * move.getMoveProperties().getModifier()))

        # Check if move will miss or hit
        self.determineMoveConnects(move, playerBattler, opponentBattler, pokemonBattlerTuple)

        # Determine Function Code Effects
        pub.sendMessage(self.battleProperties.getFunctionCodeExecuteTopic(), playerBattler=playerBattler, functionCode=move.getMoveProperties().getFunctionCode(), playerAction=move,
                        pokemonBattlerTuple=pokemonBattlerTuple, opponentPokemonBattlerTuple=opponentPokemonBattlerTuple)

        #if (self.isPokemonOutOfFieldMoveMiss(attackerPokemon, opponentPokemon, action)):
        #    move.getMoveProperties().setMoveMiss(True)
        if (pokemonTempProperties.getCurrentInternalAbility() == "MAGICGUARD"):
            move.getMoveProperties().setRecoil(0)
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
        currentEffectsNode = pokemon.getTemporaryEffects().seek()
        if (currentEffectsNode[1] != None):
            if (internalMoveName in currentEffectsNode[1].movesBlocked):
                pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is Blocked")
                return False

        if (internalMoveName == "SPLASH" and self.allHazards.get("field") != None and self.allHazards.get("field").get("GRAVITY") != None):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is Blocked")
            return False
        return True

    def executeMove(self, move, playerBattler, opponentBattler):
        self.battleWidgetsSignals.getBattleMessageSignal().emit(playerBattler.getCurrentPokemon().getName() + " used " + move.getMoveInternalName())
        self.calculateMoveDetails(move, playerBattler, opponentBattler)

        # Check if move missed
        if (move.getMoveProperties().getMoveMiss() == True):
            self.battleWidgetsSignals.getBattleMessageSignal().emit(playerBattler.getCurrentPokemon().getName() + "'s attack missed")
        else:
            # Check if damaging move
            if (move.getMoveProperties().getMoveEffectiveness() == 0):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(playerBattler.getCurrentPokemon().getName() + " is immune to the move")
            if (move.getMoveProperties().getTotalDamage() > 0):
                self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(opponentBattler.getPlayerNumber(), opponentBattler.getCurrentPokemon(), move.getMoveProperties().getTotalDamage(), None)
                self.battleProperties.tryandLock()
                self.battleProperties.tryandUnlock()
                if (move.getMoveProperties().getCriticalHit() == True):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit("It was a critical hit")
                if (move.getMoveProperties().getMoveEffectiveness() > 0 and move.getMoveProperties().getMoveEffectiveness() < 1):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit("It was not very effective")
                elif (move.getMoveProperties().getMoveEffectiveness() > 1):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit("It was super effective")

        # Check if pokemon fainted
        if (opponentBattler.getCurrentPokemon().getIsFainted()):
            self.battleWidgetsSignals.getPokemonFaintedSignal().emit(opponentBattler.getPlayerNumber())
            self.battleProperties.tryandLock()
            self.battleProperties.tryandUnlock()


