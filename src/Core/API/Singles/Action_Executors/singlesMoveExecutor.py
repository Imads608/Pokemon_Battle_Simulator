from src.Core.API.Common.Data_Types.moveAction import MoveAction
from src.Core.API.Singles.Types.singlesMoveProperties import SinglesMoveProperties
from src.Core.API.Common.Data_Types.pokemonTemporaryMetadata import PokemonTemporaryMetadata
from src.Common.damageCategory import DamageCategory
from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
from src.Common.stats import Stats
from src.Core.API.Common.Data_Types.stages import Stages
from src.Core.API.Common.Data_Types.statusConditions import NonVolatileStatusConditions

import copy
from pubsub import pub
import random

class SinglesMoveExecutor(object):
    def __init__(self, pokemonDAL, battleProperties):
        self.pokemonDAL = pokemonDAL
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None
        #self.functionCodesManager = FunctionCodesManager(battleProperties, pokemonDataSource, typeBattle="singles")

        self.currentWeather = None
        self.hazards = [None, None, None]

        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())
        pub.subscribe(self.battleWidgetsSignalsBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())


    ############ Listeners ############
    def battleFieldWeatherListener(self, currentWeather):
        self.currentWeather = currentWeather

    def battleFieldHazardsListener(self, hazardsByP1, hazardsByP2, fieldHazards):
        self.hazards[0] = hazardsByP1
        self.hazards[1] = hazardsByP2
        self.hazards[2] = fieldHazards

    def battleWidgetsSignalsBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

    ##### Helpers ################
    def checkPP(self, pokemon, moveIndex):
        movesSetMap = pokemon.internalMovesMap
        pokemonMove = movesSetMap.get(moveIndex + 1)
        if (pokemonMove.ppLeft > 0):
            return "Available"

        ppAvailableFlag = False
        for moveIndex in movesSetMap:
            pokemonMove = movesSetMap.get(moveIndex + 1)
            if (pokemonMove.ppLeft > 0):
                ppAvailableFlag = True

        if (ppAvailableFlag == True):
            return "Other Moves Available"
        return "All Moves Over"

    def getMovePriority(self, moveInternalName):
        if (self.pokemonDAL.getMoveDefinitionForInternalName(moveInternalName) == None):
            return
        moveDefinition = self.pokemonDAL.getMoveDefinitionForInternalName(moveInternalName)
        return int(moveDefinition.priority)

    def initializeMoveProperties(self, move, pokemonBattler, opponentPokemonBattler):
        moveDefinition = self.pokemonDAL.getMoveDefinitionForInternalName(move.getMoveInternalName())

        move.getMoveProperties().setMovePower(int(moveDefinition.basePower))
        move.getMoveProperties().setMoveAccuracy(int(moveDefinition.accuracy))
        move.getMoveProperties().setTypeMove(moveDefinition.typeMove)
        move.getMoveProperties().setDamageCategory(moveDefinition.damageCategory)
        move.getMoveProperties().setFunctionCode(moveDefinition.functionCode)
        move.getMoveProperties().setAdditionalEffect(moveDefinition.additionalEffect)
        move.getMoveProperties().setTargetCode(moveDefinition.targetCode)
        move.getMoveProperties().setMoveFlags(moveDefinition.flag)
        if (moveDefinition.damageCategory == DamageCategory.PHYSICAL):
            move.getMoveProperties().setTargetAttackStat(pokemonBattler.getBattleStat(Stats.ATTACK))
            move.getMoveProperties().setTargetDefenseStat(opponentPokemonBattler.getBattleStat(Stats.DEFENSE))
        elif (moveDefinition.damageCategory == DamageCategory.SPECIAL):
            move.getMoveProperties().setTargetAttackStat(pokemonBattler.getBattleStat(Stats.SPATTACK))
            move.getMoveProperties().setTargetDefenseStat(opponentPokemonBattler.getBattleStat(Stats.SPDEFENSE))

    def calculateDamage(self, move, pokemonBattler):
        baseDamage = ((((2 * int(pokemonBattler.getLevel())) / 5 + 2) * move.getMoveProperties().getMovePower() * move.getMoveProperties().getTargetAttackStat()) / move.getMoveProperties().getTargetDefenseStat()) / 50 + 2
        return baseDamage

    def determineCriticalHitChance(self, move, pokemonBattlerTuple, opponentPokemonBattlerTuple, flag):
        pokemonBattler = pokemonBattlerTuple[0]
        pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]

        modifier = 1
        if (pokemonBattler.getPlayerNum() == 1):
            fieldHazardsOpponent = self.hazards[1]
        else:
            fieldHazardsOpponent = self.hazards[0]

        if (opponentPokemonBattlerTempProperties.getCurrentInternalAbility() in ["BATTLEARMOR" or "SHELLARMOR"] or (fieldHazardsOpponent != None and fieldHazardsOpponent.lucky_chant[0] == True)):
            move.getMoveProperties().setCriticalHit(False)
            modifier = 1
        elif (move.getMoveProperties().getCriticalHit() == True and pokemonBattlerTempProperties.getCurrentInternalAbility() == "SNIPER"):
            modifier = 3
        elif (move.getMoveProperties().getCriticalHit() == True):
            modifier = 2

        stageDenominator = self.battleProperties.getCriticalHitStageFromStageIndex(move.getMoveProperties().getCriticalHitStage())
        randomNum = random.randint(1, stageDenominator)
        if (randomNum == 1 and move.getMoveProperties().getCriticalHit() == False):
            move.getMoveProperties().setCriticalHit(True)
            modifier = 2
        return modifier

    def getModifiers(self, pokemonBattlerTuple, opponentPokemonBattlerTuple, move):
        pokemonBattler = pokemonBattlerTuple[0]
        pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]

        moveDefinition = self.pokemonDAL.getMoveDefinitionForInternalName(move.getMoveInternalName())

        # Check Weather
        if (self.currentWeather == WeatherTypes.RAINING and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(1.5)
        elif (self.currentWeather == WeatherTypes.RAINING and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(0.5)
        elif (self.currentWeather == WeatherTypes.SUNNY and move.getTypeMove() == "FIRE" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(1.5)
        elif (self.currentWeather == WeatherTypes.SUNNY and move.getTypeMove() == "WATER" and opponentPokemonBattlerTempProperties.getCurrentInternalAbility() not in ["AIRLOCK", "CLOUDNINE"]):
            move.getMoveProperties().multiplyModifier(0.5)

        # Determine Critical Hit Chance
        modifier = self.determineCriticalHitChance(move, pokemonBattlerTuple, opponentPokemonBattlerTuple, moveDefinition.flag)
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
            move.getMoveProperties().setMoveType("WATER")
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "SHOCKDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            move.getMoveProperties().setMoveType("ELECTRIC")
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "BURNDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            move.getMoveProperties().setMoveType("FIRE")
        elif (pokemonBattler.getName() == "GENESECT" and pokemonBattlerTempProperties.getCurrentInternalItem() == "CHILLDRIVE" and move.getMoveInternalName() == "TECHNOBLAST"):
            move.getMoveProperties().setMoveType("ICE")

        opponentPokemonPokedex = self.pokemonDAL.getPokedexEntryForNumber(opponentPokemonBattler.getPokedexEntry())
        if (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.weaknesses) == True):
            move.getMoveProperties().setMoveEffectiveness(self.battleProperties.getTypeEffectiveness(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.weaknesses))
        elif (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.immunities) == True):
            move.getMoveProperties().setMoveEffectiveness(0)
        elif (self.battleProperties.checkTypeEffectivenessExists(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.resistances) == True):
            move.getMoveProperties().setMoveEffectiveness(self.battleProperties.getTypeEffectiveness(move.getMoveProperties().getTypeMove(), opponentPokemonPokedex.resistances))
        move.getMoveProperties().multiplyModifier(move.getMoveProperties().getMoveEffectiveness())

        # Burn
        if (opponentPokemonBattlerTempProperties.getCurrentInternalAbility() != "GUTS" and move.getMoveProperties().getDamageCategory() == DamageCategory.PHYSICAL):
            move.getMoveProperties().multiplyModifier(0.5)
        return

    def determineMoveConnects(self, move, playerBattler, opponentBattler, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        #pokemonTempProperties = PokemonTemporaryMetadata(playerBattler.getCurrentPokemon())
        #opponentPokemonTempProperties = PokemonTemporaryMetadata(opponentBattler.getCurrentPokemon())

        # Check if move will miss or hit
        threshold = 1
        if (move.getMoveProperties().getMoveAccuracy() != 0):
            threshold *= move.getMoveProperties().getMoveAccuracy()
            if (pokemonBattlerTuple[1].getCurrentInternalAbility() == "KEENEYE"):
                threshold *= self.battleProperties.getAccuracyEvasionMultiplier(Stages.STAGE0 + pokemonBattlerTuple[0].getAccuracyStage() + pokemonBattlerTuple[1].getDeltaTupleChangesForAccuracyStat()[0])#getAccuracyEvasionMultipliers()[Stages.STAGE0 + pokemonBattlerTuple[0].getAccuracyStage() + pokemonTempProperties.getAccuracyStatTupleChanges()[0]]
            else:
                threshold *= self.battleProperties.getAccuracyEvasionMultipliers()[Stages.STAGE0 + (pokemonBattlerTuple[0].getAccuracyStage() - (pokemonBattlerTuple[1].getDeltaTupleChangesForAccuracyStat()[0] -
                                                                                opponentPokemonBattlerTuple[1].getDeltaTupleChangesForEvasionStat()[0]))]
            randomNum = random.randint(1, 100)
            if (randomNum > threshold and (
                    pokemonBattlerTuple[1].getCurrentInternalAbility() != "NOGUARD" and opponentPokemonBattlerTuple[1].getCurrentInternalAbility() != "NOGUARD")):
                move.getMoveProperties().setMoveMiss(True)

    def mergeTemporaryChangesInMoveCalculation(self, pokemonBattler, pokemonBattlerTempProperties):
        pokemonBattler.setInternalAbility(pokemonBattlerTempProperties.getCurrentInternalAbility())
        pokemonBattler.setTypes(pokemonBattlerTempProperties.getCurrentTypes())
        pokemonBattler.setInternalMovesMap(pokemonBattlerTempProperties.getCurrentInternalMovesMap())
        pokemonBattler.setHeight(pokemonBattlerTempProperties.getCurrentHeight())
        pokemonBattler.setWeight(pokemonBattlerTempProperties.getCurrentWeight())
        pokemonBattler.setInternalItem(pokemonBattlerTempProperties.getCurrentInternalItem())
        pokemonBattler.setTemporaryEffects(pokemonBattlerTempProperties.getCurrentTemporaryEffects())

        if (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions):
            statusConditions = pokemonBattlerTempProperties.getInflictedNonVolatileStatusConditions()
            if (len(statusConditions) > 0):
                pokemonBattler.setNonVolatileStatusConditionIndex(statusConditions[len(statusConditions)-1])
        pokemonBattler.addVolatileStatusConditions(pokemonBattlerTempProperties.getInflictedVolatileStatusConditions())

        #TODO: Forgot what the data structures for stat and accuracy evasion changes in pokemon temporary effects stood for



    def calculateMoveDetails(self, move, playerBattler, opponentBattler):
        # Intialization
        pokemonTempProperties = PokemonTemporaryMetadata(playerBattler.getCurrentPokemon())
        opponentPokemonTempProperties = PokemonTemporaryMetadata(opponentBattler.getCurrentPokemon())
        pokemonBattlerTuple = (playerBattler.getCurrentPokemon(), pokemonTempProperties)
        opponentPokemonBattlerTuple = (opponentBattler.getCurrentPokemon(), opponentPokemonTempProperties)
        self.initializeMoveProperties(move, pokemonBattlerTuple[0], opponentPokemonBattlerTuple[0])

        # TODO: Determine Item Effects

        # TODO: Check Weather Effects e.g Sandstorm raises special defense of rock pokemon

        # TODO: Field Effects e.g Gravity

        # TODO: Determine Pokemon Temporary Effects

        # Determine Modifiers
        self.getModifiers(pokemonBattlerTuple, opponentPokemonBattlerTuple, move)

        # Determine Ability Effects
        pub.sendMessage(self.battleProperties.getAbilityMoveEffectsByAttackerTopic(), playerBattler=playerBattler,
                        opponentPlayerBattler=opponentBattler, playerAction=move,
                        pokemonBattlerTuple=pokemonBattlerTuple,
                        opponentPokemonBattlerTuple=opponentPokemonBattlerTuple)

        # Calculate Damage
        damage = 0
        if (move.getMoveProperties().getDamageCategory() != DamageCategory.STATUS):
            damage = self.calculateDamage(move, playerBattler.getCurrentPokemon())
        move.getMoveProperties().setTotalDamage(int(damage * move.getMoveProperties().getModifier()))

        # Check if move will miss or hit
        self.determineMoveConnects(move, playerBattler, opponentBattler, pokemonBattlerTuple, opponentPokemonBattlerTuple)

        if (move.getMoveProperties().getMoveMiss()):
            return

        # Determine Function Code Effects
        pub.sendMessage(self.battleProperties.getFunctionCodeExecuteTopic(), playerBattler=playerBattler, functionCode=move.getMoveProperties().getFunctionCode(), playerAction=move, pokemonBattlerTuple=pokemonBattlerTuple, opponentPokemonBattlerTuple=opponentPokemonBattlerTuple)

        if (pokemonTempProperties.getCurrentInternalAbility() == "MAGICGUARD"):
            move.getMoveProperties().setRecoil(0)

        # Merge Temporary Properties with main pokemon metadata
        if (move.getIsValid() == False):
            return

        self.mergeTemporaryChangesInMoveCalculation(pokemonBattlerTuple[0], pokemonBattlerTuple[1])
        self.mergeTemporaryChangesInMoveCalculation(opponentPokemonBattlerTuple[0], opponentPokemonBattlerTuple[1])

        return

    def checkPokemonStatusConditions(self, pokemonBattler):
        retVal = True
        if (pokemonBattler.getNonVolatileStatusCondition() == NonVolatileStatusConditions.ASLEEP):
            randNum = random.randint(1, 3)
            if (randNum == 1 or pokemonBattler.getTurnsLastedForStatusCondition(pokemonBattler.getNonVolatileStatusCondition()) > 3):
                pokemonBattler.setNonVolatileStatusCondition(NonVolatileStatusConditions.HEALTHY)
                self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, pokemonBattler.getName() + " woke up")
                retVal = True
            else:
                self.battleWidgetsSignals.getBattleMessageSignal().emit(pokemonBattler.getName() + " is fast asleep")
                retVal = False
        return retVal

    ###### Main Functions #############
    def setupMove(self, playerBattler):
        pokemonBattler = playerBattler.getCurrentPokemon()
        moveProperties = SinglesMoveProperties()
        moveObject = MoveAction(playerBattler.getPlayerNumber(), moveProperties, pokemonBattler)
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

        if (internalMoveName == "SPLASH" and self.hazards[2].gravity[0] == True):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid Move", body="Move is Blocked")
            return False
        return True

    def executeMove(self, move, playerBattler, opponentBattler):
        pokemonNonVolatileStatusCondition = playerBattler.getCurrentPokemon().getNonVolatileStatusCondition()
        pokemonVolatileStatusConditionsCopy = copy.copy(playerBattler.getCurrentPokemon().getVolatileStatusConditions())
        opponentPokemonNonVolatileStatusCondition = opponentBattler.getCurrentPokemon().getNonVolatileStatusCondition()
        opponentPokemonVolatileStatusConditionsCopy = copy.copy(opponentBattler.getCurrentPokemon().getVolatileStatusConditions())

        shouldExecMove = self.checkPokemonStatusConditions(playerBattler.getCurrentPokemon())
        if (shouldExecMove == False):
            return

        self.battleWidgetsSignals.getBattleMessageSignal().emit(playerBattler.getCurrentPokemon().getName() + " used " + move.getMoveInternalName())
        self.calculateMoveDetails(move, playerBattler, opponentBattler)

        # Check if move missed
        if (move.getIsValid() == False):
            return
        elif (move.getMoveProperties().getMoveMiss() == True):
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

        # Check if pokemon got any status conditions
        currPokemonStatusConditionTuple = (playerBattler.getCurrentPokemon(), pokemonNonVolatileStatusCondition, pokemonVolatileStatusConditionsCopy)
        oppPokemonStatusConditionTuple = (opponentBattler.getCurrentPokemon(), opponentPokemonNonVolatileStatusCondition, opponentPokemonVolatileStatusConditionsCopy)
        statusConditionTuples = [currPokemonStatusConditionTuple, oppPokemonStatusConditionTuple]

        for pokemonStatusConditionTuple in statusConditionTuples:
            pokemonBattler, nonVolatileStatusCondition, volatileStatusConditions = pokemonStatusConditionTuple
            if (nonVolatileStatusCondition != pokemonBattler.getNonVolatileStatusCondition() and pokemonBattler.getNonVolatileStatusCondition() != NonVolatileStatusConditions.HEALTHY):
                message = pokemonBattler.getName() + " became " + self.battleProperties.getStatusConditionEnumToStringDict()[pokemonBattler.getNonVolatileStatusCondition()]
                self.battleWidgetsSignals.getShowPokemonStatusConditionSignal().emit(pokemonBattler.getPlayerNum(), pokemonBattler, message)
            for volStatus in pokemonBattler.getVolatileStatusConditions():
                if (volStatus not in volatileStatusConditions):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(pokemonBattler.getName() + " became " + str(self.battleProperties.getStatusConditionEnumToStringDict()[volStatus]))
