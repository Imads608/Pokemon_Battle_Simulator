import sys
sys.path.append("../common/")

from pokemonTemporaryProperties import PokemonTemporaryProperties
from pokemonTemporaryEffectsQueue import PokemonTemporaryEffectsNode

from pubsub import pub
import copy

class SinglesAbilitiesExecutor(object):
    def __init__(self, pokemonMetadata, battleProperties):
        self.pokemonMetadata = pokemonMetadata
        self.battleProperties = battleProperties
        self.battleWidgetsSignals = None

        # Battle Field Subscribers/Listeners fields
        self.currWeather = None
        self.allHazards = {}

        # Temporary Fields/Attributes
        self.pokemonBattler = None
        self.pokemonBattlerTempProperties = None
        self.playerAction = None
        self.playerBattler = None

        self.opponentPokemonBattler = None
        self.opponentPokemonBattlerTempProperties = None
        self.opponentPlayerAction = None
        self.opponentPlayerBattler = None

        pub.subscribe(self.battleWidgetsSignaslBroadcastListener, self.battleProperties.getBattleWidgetsBroadcastSignalsTopic())
        pub.subscribe(self.battleFieldWeatherListener, self.battleProperties.getWeatherBroadcastTopic())
        pub.subscribe(self.battleFieldHazardsListener, self.battleProperties.getHazardsBroadcastTopic())


    ############# Visible Methods #############
    def getPokemonEntryEffects(self, playerBattler, opponentBattler):
        tempEffectsNode = playerBattler.getCurrentPokemon().getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        self.playerBattler = playerBattler
        self.pokemonBattler = playerBattler.getCurrentPokemon()
        self.pokemonBattlerTempProperties = PokemonTemporaryProperties(self.pokemonBattler)

        self.opponentPokemonBattler = opponentBattler.getCurrentPokemon()
        self.opponentPokemonBattlerTempProperties = PokemonTemporaryProperties(self.opponentPokemonBattler)
        self.opponentPlayerBattler = opponentBattler

        self.determineAbilityEffects("entry", self.pokemonBattler.getInternalAbility())
        self.destroyTemporaryFields()

    def getPriorityEffects(self, playerBattler, opponentPlayerBattler, playerAction):
        tempEffectsNode = playerBattler.getCurrentPokemon().getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        elif (playerAction.getActionType() == "switch"):
            return

        self.playerBattler = playerBattler
        self.pokemonBattler = playerBattler.getCurrentPokemon()
        self.pokemonBattlerTempProperties = PokemonTemporaryProperties(self.pokemonBattler)
        self.playerAction = playerAction

        self.opponentPlayerBattler = opponentPlayerBattler
        self.opponentPokemonBattler = opponentPlayerBattler.getCurrentPokemon()

        self.determineAbilityEffects("priority", self.pokemonBattler.getInternalAbility())
        self.destroyTemporaryFields()

    def getSwitchedOutEffects(self, playerBattler):
        tempEffectsNode = playerBattler.getCurrentPokemon().getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        self.playerBattler = playerBattler
        self.pokemonBattler = playerBattler.getCurrentPokemon()

        self.determineAbilityEffects("switched out", self.pokemonBattler.getInternalAbility())
        self.destroyTemporaryFields()

    def getMoveEffectsByAttacker(self, playerBattler, opponentPlayerBattler, playerAction, pokemonBattlerTuple, opponentPokemonBattlerTuple):
        tempEffectsNode = pokemonBattlerTuple[0].getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        self.pokemonBattler = pokemonBattlerTuple[0]
        self.pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        self.opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        self.opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]
        self.playerAction = playerAction
        self.determineAbilityEffects("move effects by attacker", self.pokemonBattlerTempProperties.getCurrentInternalAbility())
        self.destroyTemporaryFields()

    def getMoveEffectsByOpponent(self, playerBattler, opponentPlayerBattler, playerAction, pokmeonBattlerTuple, opponentPokemonBattlerTuple):
        tempEffectsNode = pokemonBattlerTuple[0].getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        self.pokemonBattler = pokemonBattlerTuple[0]
        self.pokemonBattlerTempProperties = pokemonBattlerTuple[1]
        self.opponentPokemonBattler = opponentPokemonBattlerTuple[0]
        self.opponentPokemonBattlerTempProperties = opponentPokemonBattlerTuple[1]
        self.playerAction = playerAction
        self.determineAbilityEffects("move effects by opponent", self.pokemonBattlerTempProperties.getCurrentInternalAbility())
        self.destroyTemporaryFields()

    def getEndofTurnEffects(self, playerBattler, opponentPlayerBattler):
        tempEffectsNode = playerBattler.getCurrentPokemon().getTemporaryEffects().seek()
        if (tempEffectsNode != None and tempEffectsNode.getAbilitySuppressed() == True):
            return
        self.pokemonBattler = playerBattler.getCurrentPokemon()
        self.playerBattler = playerBattler
        self.opponentPokemonBattler = opponentPlayerBattler.getCurrentPokemon()
        self.opponentPlayerBattler = opponentPlayerBattler
        self.determineAbilityEffects("end of turn", self.pokemonBattler.getInternalAbility())
        self.destroyTemporaryFields()



    ########### Listeners ###############
    def battleWidgetsSignaslBroadcastListener(self, battleWidgetsSignals):
        self.battleWidgetsSignals = battleWidgetsSignals

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
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Attack")
                else:
                    self.pokemonBattler.setBattleStat(3, int(self.pokemonBattler.getBattleStats()[3] * self.battleProperties.getStatsStageMultiplier(deviation=1)))
                    self.pokemonBattler.setStatStage(3, self.pokemonBattler.getStatsStages()[3]+1)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Download raised its Special Attack")
        elif (pokemonAbility == "INTIMIDATE"):
            if (stateInBattle == "entry"):
                currentNodeEffects = self.pokemonBattler.getTemporaryEffects().seek()
                if (currentNodeEffects != None and currentNodeEffects.isSubstitueActive() == True):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Substitute prevented Intimidate from activating")
                if (self.opponentPokemonBattler.getInternalAbility() == "CONTRARY" and self.opponentPokemonBattler.getStatsStages()[1] != 6):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(1)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1]+1)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate increased " + self.opponentPokemonBattler.getName() + "'s Attack")
                elif (self.opponentPokemonBattler.getInternalAbility() == "SIMPLE" and self.opponentPokemonBattler.getStatsStages()[1] > -5):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-2)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 2)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate sharply decreased " + self.opponentPokemonBattler.getName() + "'s Attack")
                elif (self.opponentPokemonBattler.getInternalAbility() in ["CLEARBODY", "HYPERCUTTER", "WHITESMOKE"]):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s " + self.opponentPokemonBattler.getInternalAbility() + " prevented " + self.pokemonBattler.getName() + "'s Intimiade from activating.")
                elif (self.opponentPokemonBattler.getStatsStages()[1] != -6):
                    self.opponentPokemonBattler.setBattleStat(1, int(self.opponentPokemonBattler.getBattleStats()[1] * self.battleProperties.getStatsStageMultiplier(-1)))
                    self.opponentPokemonBattler.setStatStage(1, self.opponentPokemonBattler.getStatsStages()[1] - 1)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Intimidate decreased " + self.opponentPokemonBattler.getName() + "'s Attack")
        elif (pokemonAbility == "DRIZZLE"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("rain", sys.maxsize))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drizzle made it Rain")
        elif (pokemonAbility == "DROUGHT"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("sunny", sys.maxsize))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Drought made it Sunny")
        elif (pokemonAbility == "SANDSTREAM"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("sandstorm", sys.maxsize))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Sandstream brewed a Sandstorm")
        elif (pokemonAbility == "SNOWWARNING"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherRequestTopic(), weatherRequested=("hail", sys.maxsize))
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Snow Warning made it Hail")
        elif (pokemonAbility == "FRISK"):
            if (stateInBattle == "entry"):
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Frisk showed " + self.opponentPokemonBattler.getName() + "'s held item")
                tupleData = self.pokemonMetadata.getItemsMetadata().get(self.opponentPokemonBattler.getInternalItem())
                if (tupleData == None):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + " is not holding an item")
                else:
                    fullName, _, _, _, _ = tupleData
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + " is holding " + fullName)
        elif (pokemonAbility == "ANTICIPATION"):
            if (stateInBattle == "entry"):
                pokemonPokedex = self.pokemonMetadata.getPokedex().get(self.pokemonBattler.pokedexEntry)
                for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
                    _, _, _, _, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
                    if (self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.weaknesses) == True and damageCategory != "Status"):
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders")
                    elif ((internalMoveName == "FISSURE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "SHEERCOLD" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "GUILLOTINE" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities) == False) or (internalMoveName == "HORNDRILL" and self.battleProperties.checkTypeEffectivenessExists(typeMove, pokemonPokedex.immunities))):
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " shudders")
        elif (pokemonAbility == "FOREWARN"):
            if (stateInBattle == "entry"):
                maxPower = -1
                moveName = ""
                for moveIndex in self.opponentPokemonBattler.getInternalMovesMap():
                    internalMoveName, _, _ = self.opponentPokemonBattler.getInternalMovesMap().get(moveIndex)
                    _, fullName, _, basePower, typeMove, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.getMovesMetadata().get(internalMoveName)
                    if (basePower > maxPower):
                        maxPower = basePower
                        moveName = fullName
                if (moveName != ""):
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Forewarn reveals " + self.opponentPokemonBattler.getName() + "'s strongest move to be " + moveName)
        elif (pokemonAbility == "TRACE"):  #TODO: Skill swap move functionality
            if (stateInBattle == "entry"):
                if (self.opponentPokemonBattler.getInternalAbility() not in  ["FORECAST", "FLOWERGIFT", "MULTITYPE", "ILLUSION", "ZENMODE"]):
                    self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
                    _, fullName, _ = self.pokemonMetadata.getAbilitiesMetadata().get(self.opponentPokemonBattler.getInternalName())
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Traced the opposing " + fullName + "'s " + self.opponentPokemonBattler.getInternalAbility())
                    if (self.opponentPokemonBattler.getInternalAbility() != "TRACE"):
                        self.determineAbilityEffects("entry", self.pokemonBattler.getInternalAbility())
                effectsNode = PokemonTemporaryEffectsNode()
                effectsNode.setTraceActivated(True)
                self.pokemonBattler.getTemporaryEffects().enQueue(effectsNode, -1)
        elif (pokemonAbility == "IMPOSTER"):
            if (stateInBattle == "entry"):
                temporaryEffectsNode = self.opponentPokemonBattler.getTemporaryEffects().seek()
                ignoreFlag = True
                if (temporaryEffectsNode == None or (temporaryEffectsNode.getIllusionEffect() != True and temporaryEffectsNode.getSubsituteEffect() == None)):
                    battleStats = copy.deepcopy(self.opponentPokemon.getBattleStats())
                    battleStats[0] = self.currPokemon.getBattleStats()[0]
                    types = copy.deepcopy(self.opponentPokemon.getTypes())
                    internalMovesMap = copy.deepcopy(self.opponentPokemon.getInternalMovesMap())
                    for moveIndex in internalMovesMap.keys():
                        tupleMetadata = internalMovesMap.get(moveIndex)
                        newTupleMetadata = (tupleMetadata[0], tupleMetadata[1], 5)
                        internalMovesMap.update({moveIndex: newTupleMetadata})
                    self.pokemonBattler.setBattleStats(battleStats)
                    self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
                    self.pokemonBattler.setInternalMovesMap(internalMovesMap)
                    self.pokemonBattler.setInternalAbility(self.opponentPokemonBattler.getInternalAbility())
                    self.pokemonBattler.setWeight(self.opponentPokemonBattler.getWeight())
                    self.pokemonBattler.setTypes(types)
                    self.battleWidgetsSignals.getDisplayPokemonInfoSignal().emit(self.pokemonBattler)
                    self.battleProperties.tryandLock()
                    self.battleProperties.tryandUnlock()
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " transformed")
        elif (pokemonAbility == "ILLUSION"):
            if (stateInBattle == "entry"):
                # TODO: Implement switching function call for this to work
                currPlayerTeam = self.currPlayerWidgets[6]
                teamSize = len(self.playerBattler.getPokemonTeam())
                if (self.playerBattler.getPokemonTeam()[teamSize - 1].getName() != self.pokemonBattler.getName() and self.playerBattler[teamSize - 1].getIsFainted() == False):
                    tempEffectsNode = PokemonTemporaryEffectsNode()
                    tempEffectsNode.setIllusionEffect(True)
                    self.pokemonBattler.getTemporaryEffects().enQueue(tempEffectsNode)
                    self.pokemonBattler.setImage(self.opponentPokemonBattler.getImage())
                    self.pokemonBattler.setGender(self.opponentPokemonBattler.getGender())
                    self.pokemonBattler.setTypes(copy.copy(self.opponentPokemonBattler.getTypes()))
                    self.pokemonBattler.setName(self.opponentPokemonBattler.getName())
        elif (pokemonAbility == "IMMUNITY"):
            if (stateInBattle == "entry"):
               if (self.pokemonBattler.getNonVolatileStatusConditionIndex() in [1, 2]):
                   self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                   self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Immunity cured its poison!")
               #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
               #    if (self.currPokemon.getNonVolatileStatusConditionIndex() in [1, 2]):
               #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
               #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Immunity cured its poison")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() in [1,2]):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Immunity prevented it from being poisoned")
            if (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() in [1,2]):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
        elif (pokemonAbility == "MAGMAARMOR"):
            if (stateInBattle == "entry"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 5):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Magma Armor unthawed the ice!")
               #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
               #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 5):
               #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
               #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Magma Armor unthawed itself")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 5):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Magma Armor prevented it from being frozen")
                elif (stateInBattle == "end of turn"):
                    if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 5):
                        self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Magma Armor unthawed the ice!")
        elif (pokemonAbility == "LIMBER"):
            if (stateInBattle == "entry"):
               if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 3):
                   self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                   self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber cured its paralysis!")
               #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
               #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
               #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 3):
               #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
               #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Limber cured its paralysis")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 3):
                    self.currPlayerAction.setNonVolatileStatusConditionsbyAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(False)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Limber prevented it from being paralyzed")
            elif (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 3):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Limber cured its paralysis")
        elif (pokemonAbility == "INSOMNIA"):
            if (stateInBattle == "entry"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia cured its sleep")
                #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Insomnia cured its sleep")
            elif (stateInBattle == "move effects attacker"):
                if (self.playerAction.getInternalMove() == "REST"):
                    self.playerAction.setInvalid(True)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia prevented it from sleeping")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 4 or self.currPlayerAction.getVolatileStatusConditionByAttacker() == 7):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Insomnia prevented it from sleeping")
            elif (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia cured its sleep")
        elif (pokemonAbility == "VITALSPIRIT"):
            if (stateInBattle == "entry"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Vital Spirit cured its sleep")
                #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 4):
                #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Vital Spirit cured its sleep")
            elif (stateInBattle == "Move Effect Attacker"):
                if (self.playerAction.getInternalMove() == "REST"):
                    self.playerAction.setInvalid(True)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Insomnia prevented it from sleeping")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 4 or self.currPlayerAction.getVolatileStatusConditionByAttacker() == 7):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Vital Spirit prevented it from sleeping")
                elif (stateInBattle == "end of turn"):
                    if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 4):
                        self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Vital Spirit cured its sleep")
        elif (pokemonAbility == "WATERVEIL"):
            if (stateInBattle == "entry"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Water Veil cured its burn")
                #prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
                #if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
                #    if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
                #        self.currPokemon.setNonVolatileStatusConditionIndex(None)
                #        self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 6):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Water Veil prevented it from burned")
            elif (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(None)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Water Veil cured its burn")
        elif (pokemonAbility == "OWNTEMPO"):
            if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
                self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Own Tempo cured its burn")
            #if (stateInBattle == "entry"):
            #    prevAction = self.battleTab.getPlayerAction(self.currPokemonTemp.getPlayerNum())
            #    if (prevAction == None or (prevAction.getAction() == "switch" and prevAction.getSwitchPokemonIndex() == self.battleTab.getPlayerCurrentPokemonIndex(self.currPokemonTemp.getPlayerNum()))):
            #        if (self.currPokemon.getNonVolatileStatusConditionIndex() == 6):
            #            self.currPokemon.setNonVolatileStatusConditionIndex(None)
            #            self.battleTab.updateBattleInfo(self.currPokemon.getName() + "'s Water Veil cured its burn")
            elif (stateInBattle == "Move Retaliate"):
                if (self.currPlayerAction.getVolatileStatusConditionByOpponent() == 8):
                    self.currPlayerAction.setVolatileConditionByOpponent(None)
                    self.currPlayerAction.getInflicted
            elif (stateInBattle == "Move Execution Opponent"):
                if (self.currPlayerAction.getNonVolatileStatusConditionsByAttacker() == 6):
                    self.currPlayerAction.setVolatileStatusConditionsByAttacker(None)
                    self.currPlayerAction.setInflictStatusConditionsByAttacker(None)
                    self.currPlayerAction.setBattleMessage(self.currPokemonTemp.getName() + "'s Water Veil prevented it from burned")
            elif (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Water Veil cured its burn")
        elif (pokemonAbility == "AIRLOCK"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=False)
            elif (stateInBattle == "switched out"):
                pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=True)
            elif (stateInBattle == "end of turn"):
                # Handled already elsewhere
                pass
        elif (pokemonAbility == "CLOUDNINE"):
            if (stateInBattle == "entry"):
                pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=False)
            elif (stateInBattle == "switched out"):
                pub.sendMessage(self.battleProperties.getWeatherInEffectToggleRequestTopic(), toggleVal=True)
            elif (stateInBattle == "end of turn"):
                # Handled already elsewhere
                pass
        elif (pokemonAbility == "REGENERATOR"):
            if (stateInBattle == "switched out"):
                healthGained = int(self.pokemonBattler.getBattleStats()[0] *1/3)
                if (self.pokemonBattler.getBattleStats()[0] + healthGained > self.pokemonBattler.getFinalStats()[0]):
                    healthGained = self.pokemonBattler.getFinalStats()[0] - self.pokemonBattler.getBattleStats()[0]
                self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healthGained)
        elif (pokemonAbility == "NATURALCURE"):
            if (stateInBattle == "switched Out"):
                #TODO: Verify that Trace can also activate this when switched out:
                self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
        elif (pokemonAbility == "QUICKFEET"):
            if (stateInBattle == "priority"):
                if (self.pokemonBattler.getStatsStages()[5] != 6):
                    self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "UNBURDEN"):
            if (stateInBattle == "priority"):
                if (self.pokemonBattler.getInternalItem() == None and self.pokemonBattler.getWasHoldingItem() == True and self.pokemonBattler.getStatsStages()[5] < 6):
                    if (self.pokemonBattler.getStatsStages()[5] < 5):
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "SLOWSTART"):
            if (stateInBattle == "priority"):
                if (self.pokemonBattler.getTurnsPlayed() < 5 and self.pokemonBattler.getStatsStages()[5] != -6):
                    self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(-1)))
            elif (stateInBattle == "move effects by attacker"):
                self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
        elif (pokemonAbility == "CHLOROPHYLL"):
            if (stateInBattle == "priority"):
                if (self.currWeather == "sunny" and self.opponentPokemonBattler.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.pokemonBattler.getStatsStages()[5] < 6):
                    if (self.pokemonBattler.getStatsStages()[5] < 5):
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "SWIFTSWIM"):
            if (stateInBattle == "priority"):
                if (self.currWeather == "rain" and self.opponentPokemonBattler.getInternalAbility() not in ["AIRLOCK", "CLOUDNINE"] and self.pokemonBattler.getStatsStages()[5] < 6):
                    if (self.pokemonBattler.getStatsStages()[5] < 5):
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "SANDRUSH"):
            if (stateInBattle == "priority"):
                if (self.currWeather == "sandstorm" and self.pokemonBattler.getStatsStages()[5] < 6):
                    if (self.pokemonBattler.getStatsStages()[5] < 5):
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setCurrentPokemonSpeed(int(self.playerAction.getCurrentPokemonSpeed() * self.battleProperties.getStatsStageMultiplier(1)))
            if (stateInBattle == "end of turn"):
                # Just needs checking if it gets hurt in sandstorm which is already checked in another area of code
                pass
        elif (pokemonAbility == "PRANKSTER"):
            if (stateInBattle == "priority"):
                _, _, _, _, _, damageCategory, _, _, _, _, _, _, _ = self.pokemonMetadata.movesMetadata.get(self.playerAction.getMoveInternalName())
                if (damageCategory == "Status"):
                    self.playerAction.setPriority(self.playerAction.getPriority()+1)
        elif (pokemonAbility == "STALL"):
            if (stateInBattle == "priority"):
                self.playerAction.setQueuePosition(2)
        elif (pokemonAbility == "FLAREBOOST"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getDamageCategory() == "Special" and self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "GUTS"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() == 6 and self.pokemonBattler.getStatsStages()[1] != 6 and self.playerAction.getDamageCategory() == "Physical"):
                    self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "TOXICBOOST"):
            if (stateInBattle == "move effects by attacker"):
                if ((self.pokemonBattler.getNonVolatileStatusConditionIndex() in [1, 2]) and self.pokemonBattler.getStatsStages()[1] != 6):
                    self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "HUSTLE"):
            if (stateInBattle == "Move effects by attacker"):
                if (self.playerAction.getDamageCategory() == "Physical"):
                    if (self.pokemonBattler.getStatsStages()[1] != 6):
                        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
                    self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 0.8))
        elif (pokemonAbility == "PUREPOWER"):
            if (stateInBattle == "Move Effect Attacker"):
                if (self.playerAction.getDamageCategory() == "Physical" and self.pokemonBattler.getStatsStages()[1] != 6):
                    if (self.pokemonBattler.getStatsStages()[1] < 5):
                        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "HUGEPOWER"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getDamageCategory() == "Physical" and self.pokemonBattler.getStatsStages()[1] != 6):
                    if (self.pokemonBattler.getStatsStages()[1] < 5):
                        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(2)))
                    else:
                        self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * self.battleProperties.getStatsStageMultiplier(1)))
        elif (pokemonAbility == "COMPOUNDEYES"):
            if (stateInBattle == "move effects by attacker"):
                self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 1.3))
        elif (pokemonAbility == "DEFEATIST"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 2)):
                    self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 0.5))
        elif (pokemonAbility == "VICTORYSTAR"):
            if (stateInBattle == "move effects by attacker"):
                self.playerAction.setMoveAccuracy(int(self.playerAction.getMoveAccuracy() * 1.1))
        elif (pokemonAbility == "SOLARPOWER"):
            if (stateInBattle == "move effects by attacker"):
                if (self.currWeather == "sunny" and self.playerAction.getDamageCategory() == "Special"):
                    self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
            elif (stateInBattle == "end of turn"):
                if (self.currWeather == "sunny"):
                    damage = int(self.pokemonBattler.getFinalStats()[0] * 1/8)
                    self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.pokemonBattler.getName() + "'s Solar Power caused it to be hurt by Sunlight")
                    self.battleProperties.tryandLock()
                    self.battleProperties.tryandUnlock()
        elif (pokemonAbility == "FLOWERGIFT"):
            if (stateInBattle == "move effects by attacker"):
                if (self.currWeather == "sunny" and self.playerAction.getDamageCategory() == "Physical"):
                    self.playerAction.setTargetAttackStat(int(self.playerAction.getTargetAttackStat() * 1.5))
            elif (stateInBattle == "Move Effect Opponent"):
                if (self.currPlayerAction.getDamageCategory() == "Special" and self.opponentPokemonTemp.getCurrentStatsStages()[4] != 6 and self.battleTab.getBattleField().getWeather() == "Sunny"):
                    self.currPlayerAction.setTargetDefenseStat(int(self.currPlayerAction.getTargetDefenseStat() * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 1]))
        elif (pokemonAbility == "BLAZE"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 3) and self.playerAction.getDamageCategory() != "Status" and self.playerAction.getTypeMove() == "FIRE"):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "OVERGROW"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 3) and self.playerAction.getDamageCategory() != "Status" and self.playerAction.getTypeMove() == "GRASS"):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "TORRENT"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 3) and self.playerAction.getDamageCategory() != "Status" and self.playerAction.getTypeMove() == "WATER"):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "SWARM"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getBattleStats()[0] <= int(self.pokemonBattler.getFinalStats()[0] / 3) and self.playerAction.getDamageCategory() != "Status" and self.playerAction.getTypeMove() == "BUG"):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "SANDFORCE"):
            if (stateInBattle == "move effects by attavcker"):
                if ((self.playerAction.getTypeMove() in ["ROCK", "GROUND", "STEEL"]) and self.playerAction.getDamageCategory() != "Status" and self.currWeather == "sandstorm"):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.3))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already handled
                pass
        elif (pokemonAbility == "IRONFIST"):
            if (stateInBattle == "move effects by attacker"):
                _, _, _, _, _, _, _, _, _, _, _, _, flag = self.pokemonMetadata.getMovesMetadata().get(self.playerAction.getInternalMove())
                if ("j" in flag):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
        elif (pokemonAbility == "RECKLESS"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getFunctionCode() in ["OFA","0FB", "0FC", "0FD", "0FE"] or self.playerAction.getInternalMove() in ["JUMPKICK", "HIGHJUMPKICK"]):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.2))
        elif (pokemonAbility == "RIVALRY"):
            if (stateInBattle == "move effects by attacker"):
                if (self.pokemonBattler.getGender() != "Genderless" and self.opponentPokemonBattler.getGender() != "Genderless"):
                    if (self.pokemonBattler.getGender() == self.opponentPokemonBattler.getGender()):
                        self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.25))
                    else:
                        self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 0.75))
        elif (pokemonAbility == "SHEERFORCE"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getAddEffect() != 0):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.3))
                    self.playerAction.setAddEffect(0)
        elif (pokemonAbility == "TECHNICIAN"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getMovePower() <= 60):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.5))
        elif (pokemonAbility == "TINTEDLENS"):
            if (stateInBattle == "move effects by attacker"):
                pokemonPokedex = self.pokemonMetadata.getPokedex().get(self.opponentPokemonBattler.getPokedexEntry())
                if (self.battleProperties.checkTypeEffectivenessExists(self.playerAction.getTypeMove(), pokemonPokedex.resistances) == True):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 2))
        elif (pokemonAbility == "SNIPER"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getCriticalHit() == True):
                    pass  # Handled in Critical Hit Determine Function
        elif (pokemonAbility == "ANALYTIC"):
            if (stateInBattle == "move effects by attacker"):
                if (self.playerAction.getIsFirst() == False):
                    self.playerAction.setMovePower(int(self.playerAction.getMovePower() * 1.3))
        elif (pokemonAbility == "SANDVEIL"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.getBattleField().getWeather() == "Sandstorm"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 4/5))
            elif (stateInBattle == "End of Turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (pokemonAbility == "SNOWCLOAK"):
            if (stateInBattle == "Move Effect Opponent"):
                if (self.battleTab.getBattleField().getWeather() == "Hail"):
                    self.currPlayerAction.setMoveAccuracy(int(self.currPlayerAction.getCurrentMoveAccuracy() * 4/5))
            elif (stateInBattle == "end of turn"):
                # Just needs checking if hurt in sandstorm which is already covered in another area of code
                pass
        elif (pokemonAbility == "INNERFOCUS"):
            if (stateInBattle == "move effects by opponent"):
                if (self.playerAction.getFlinch() == True):
                    self.playerAction.setFlinch(False)
        elif (pokemonAbility == "LEAFGUARD"):
            # TODO: Items trigger this ability
            if (stateInBattle == "move effects by opponent"):
                if (self.currWeather == "sunny"):
                    if (self.opponentPokemonBattlerTempProperties.getInflictedNonVolatileStatusCondition() in [1,2,3,4,5,6]):
                        self.opponentPokemonBattlerTempProperties.setInflictedNonVolatileStatusCondition(None)
                    if (self.opponentPokemonBattlerTempProperties.getInflictedVolatileStatusCondition() == 7):
                        self.opponentPokemonBattlerTempProperties.setInflictedVolatileStatusCondition(None)
        elif (ability == "FLASHFIRE"):
            # Fire types move powered up handled in determineMoveDetails Function
            if (stateInBattle == "Move Effect Opponent"):
                if (self.playerAction.getTypeMove() == "FIRE"):
                    self.playerAction.setEffectiveness(0)
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.opponentPokemonBattler.getName() + "'s Flash Fire made it immune to Fire Type Moves")
                    temporaryEffectsNode = PokemonTemporaryEffectsNode()
                    temporaryEffectsNode.setTypeMovesPowered({"Fire":1.5})
                    self.opponentPokemonBattlerTempProperties.getCurrentTemporaryEffects.push(temporaryEffectsNode, -1)
        elif (ability == "STORMDRAIN"):
            if (stateInBattle == "Move Effect Opponent"):
                #TODO: Check for opponent in semi-invulnerable state or is protected
                if (self.currPlayerAction.typeMove == "WATER"):
                    self.currPlayerAction.setEffectiveness(0)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain made it immune to Water type moves")
                    if (self.opponentPokemonTemp.currStatsStages[3] != 6):
                        self.opponentPokemonTemp.statsStagesChanges[3] += 1
                        self.currPlayerAction.setBattleMessage(self.opponentPokemon.name + "'s Storm Drain also increased its Special Attack")
        elif (pokemonAbility == "SPEEDBOOST"):
            #TODO: Also triggers if this pokemon was switched in after prev pokmeon fainted. must implement
            if (stateInBattle == "end of turn"):
                if (self.pokemonBattler.getTurnsPlayed() > 0 and self.pokemonBattler.getStatsStages()[5] != 6):
                    self.pokemonBattler.setStatStage(5, self.pokemonBattler.getStatsStages()[5] + 1)
                    self.pokemonBattler.setBattleStat(5, int(self.pokemonBattler.getBattleStats()[5] * self.battleProperties.getStatsStageMultiplier(1)))
                    self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " 's Speed Boost increased its speed")
        elif (pokemonAbility == "MOODY"):
            if (stateInBattle == "end of turn"):
                arrStats = ["Health", self.pokemonBattler.getStatsStages()[1], self.pokemonBattler.getStatsStages()[2], self.pokemonBattler.getStatsStages()[3], self.pokemonBattler.getStatsStages()[4], self.pokemonBattler.getStatsStages()[5], self.pokemonBattler.getAccuracyStage(), self.pokemonBattler.getEvasionStage()]
                statsNames = ["Health", "Attack", "Special Attack", "Defense", "Special Defense", "Speed", "Accuracy", "Evasion"]
                repeatFlag = True
                while (repeatFlag == True):
                    randomInc = random.randint(1, 7)
                    randomDec = random.randint(1, 7)
                    if (randomInc == randomDec):
                        continue
                    elif (arrStats == ["Health",6,6,6,6,6,6,6]):
                        repeatFlag = False
                        if (randomDec == 6):
                            self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage()-1)
                            self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                        elif (randomDec == 7):
                            self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage()-1)
                            self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                        else:
                            self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] - 1)
                            self.pokemonBattler.setBattleStat(randomDec, int(self.pokemonBattler.getBattleStats()[randomDec] * self.pokemonBattler.getStatsStageMultipliers()[self.battleTab.getStage0Index() - 1]))
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody decreased its " + statsNames[randomDec])
                    elif (arrStats == ["Health", -6,-6,-6,-6,-6,-6,-6]):
                        repeatFlag = False
                        if (randomInc == 6):
                            self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage()+2)
                            self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultipliers(2)))
                        elif (randomInc == 7):
                            self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage()+2)
                            self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultipliers(2)))
                        else:
                            self.pokemonBattler.setStatStage(randomInc, self.currPokemon.getStatsStages()[randomInc] + 2)
                            self.pokemonBattler.setBattleStat(randomInc, int(self.currPokemon.getBattleStats()[randomInc] * self.battleTab.getStatsStageMultipliers()[self.battleTab.getStage0Index() + 2]))
                        self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s Moody sharply raised its " + statsNames[randomInc])
                    elif (arrStats[randomInc] != 6 and arrStats[randomDec] == -6):
                        repeatFlag = False
                        if (arrStats[randomInc] == 5):
                            incNum = 1
                            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + "'s raised its " + statsName[randomInc] + " but lowered its " + statsNames[randomDec])
                        else:
                            incNum = 2
                            self.battleWidgetsSignals.getBattleMessageSignal().emit(self.pokemonBattler.getName() + " 's Moody sharply raised its " + statsNames[randomInc] + " but lowered its " + statsNames[randomDec])
                        if (randomInc == 6):
                            self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage()+incNum)
                            self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(incNum)))
                        elif (randomInc == 7):
                            self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage() + incNum)
                            self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(incNum)))
                        else:
                            self.pokemonBattler.setStatStage(randomInc, self.pokemonBattler.getStatsStages()[randomInc] + incNum)
                            self.pokemonBattler.setBattleStat(randomInc, int(self.pokemonBattler.getBattleStats()[randomInc] * self.battleProperties.getStatsStageMultiplier(incNum)))
                        if (randomDec == 6):
                            self.pokemonBattler.setAccuracyStage(self.pokemonBattler.getAccuracyStage()-1)
                            self.pokemonBattler.setAccuracy(int(self.pokemonBattler.getAccuracy() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                        elif (randomDec == 7):
                            self.pokemonBattler.setEvasionStage(self.pokemonBattler.getEvasionStage()-1)
                            self.pokemonBattler.setEvasion(int(self.pokemonBattler.getEvasion() * self.battleProperties.getAccuracyEvasionMultiplier(-1)))
                        else:
                            self.pokemonBattler.setStatStage(randomDec, self.pokemonBattler.getStatsStages()[randomDec] - 1)
                            self.pokemonBattler.setBattleStat(randomDec, int(self.currPokemon.getBattleStats()[randomDec] * self.battleTab.getStatsStageMultiplier(-1)))
        elif (pokemonAbility == "SHEDSKIN"):
            if (stateInBattle == "end of turn"): #TODO: Make sure this happens before burn or poison damage takes effect
                randNum = random.randint(1,100)
                if (self.pokemonBattler.getNonVolatileStatusConditionIndex() != 0 and randNum <= 30):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getShowStatusConditionSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, self.pokemonBattler.getName() + "'s Shed Skin cured its status condition")
                    self.battleProperties.tryandLock()
                    self.battleProperties.tryandUnlock()
                    #pub.sendMessage(self.battleProperties.getShowStatusConditionTopic(), playerNum=self.pokemonBattler.getPlayerNum(), pokemonBattler=self.pokemonBattler, message=self.pokemonBattler.getName() + "'s Shed Skin cured its status condition")
        elif (pokemonAbility == "HEALER"):
            # Useful in double and triple battles
            pass
        elif (pokemonAbility == "BADDREAMS"):
            if (stateInBattle == "end of turn"): #TODO: Make sure Shed Skin has chance to activate before checking for this
                if (self.opponentPokemonBattler.getInternalAbility() != "HYDRATION"):
                    damage = int(self.opponentPokemonBattler.getFinalStats()[0] * 1/8)
                    self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.opponentPokemonBattler.getPlayerNum(), self.opponentPokemonBattler, damage, self.pokemonBattler.getName() + "'s Bad Dreams hurt " + self.opponentPokemonBattler.getName())
                    pub.sendMessage(self.battleProperties.getShowDamageTopic(), playerNum=self.opponentPokemonBattler.getPlayerNum(), pokemonBattler=self.opponentPokemonBattler, amount=damage, message=self.pokemonBattler.getName() + "'s Bad Dreams hurt " + self.opponentPokemonBattler.getName())
                    self.battleProperties.tryandLock()
                    self.battleProperties.tryandUnlock()
        elif (pokemonAbility == "HYDRATION"):
            if (stateInBattle == "end of turn"): #TODO: Check how Yawn works this case
                if (self.currWeather == "raining"):
                    self.pokemonBattler.setNonVolatileStatusConditionIndex(0)
                    self.battleWidgetsSignals.getShowStatusConditionSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, self.pokemonBattler.getName() + " Hydration cured its status condition")
                    self.battleProperties.tryandLock()
                    self.battleProperties.tryandUnlock()
                    #pub.sendMessage(self.battleProperties.getShowStatusConditionTopic(), playerNum=self.pokemonBattler.getPlayerNum(), pokemonBattler=self.pokemonBattler, message=self.pokemonBattler.getName() + "'s Hydration cured its status condition")
        elif (pokemonAbility == "DRYSKIN"): #TODO: Won't work if pokemon is protected
            if (stateInBattle == "Move Exection Opponent"):
                if (self.currPlayerAction.getTypeMove() == "FIRE" and self.currPlayerAction.getDamageCategory() != "Status"):
                    self.currPlayerAction.setMovePower(int(self.currPlayerAction.getMovePower() * 1.25))
                    #self.battleTab.calculateDamage(self.currPlayerAction, self.currPokemon)
                elif (self.currPlayerAction.getTypeMove() == "WATER"):
                    self.currPlayerAction.setEffectiveness(0)
                    healAmt = int(0.25 * self.opponentPokemon.getFinalStats()[0])
                    if (healAmt + self.opponentPokemon.getBattleStats()[0] > self.opponentPokemon.getFinalStats()[0]):
                        self.currPlayerAction.setHealAmount(self.opponentPokemon.getFinalStats()[0] - self.opponentPokemon.getBattleStats()[0])
                    else:
                        self.currPlayerAction.setHealAmount(healAmt)
                    self.currPlayerAction.setBattleMessage(self.opponentPokemon.getName() + "\'s Dry Skin absorbed the move and restored some HP")
                    #self.battleTab.showHealHealthAnimation(self.opponentPokemon, healAmt, self.opponentPlayerWidgets[2])
                    #self.message = self.opponentPokemon.getName() + "\'s Dry Skin absorbed the move and restored some HP"
                    #self.executeFlag = False
            elif (stateInBattle == "end of turn"):
                if (self.currWeather == "sunny"):
                    damage = int(self.pokemonBattler.getFinalStats()[0] * 1/8)
                    self.battleWidgetsSignals.getPokemonHPDecreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, damage, self.pokemonBattler.getName() + "'s Dry Skin hurt it because of the Weather")

                elif (self.battleTab.getBattleField().getWeather() == "Raining"):
                    healAmt = int(self.pokemonBattler.getFinalStats()[0] * 1/8)
                    self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin gained some HP due to the Weather")
        elif (pokemonAbility == "RAINDISH"):
            if (stateInBattle == "end of turn"):
                if (self.currWeather == "raining"):
                    healAmt = int(self.pokemonBattler.getFinalStats()[0] * 1/16)
                    self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin gained some HP due to the Weather")
        elif (pokemonAbility == "ICEBODY"):
            if (stateInBattle == "end of turn"):
                if (self.currWeather == "Hail"):
                    healAmt = int(self.pokemonBattler.getFinalStats()[0] *1/16)
                    self.battleWidgetsSignals.getPokemonHPIncreaseSignal().emit(self.pokemonBattler.getPlayerNum(), self.pokemonBattler, healAmt, self.pokemonBattler.getName() + "'s Dry Skin gained some HP due to the Weather")
        elif (pokemonAbility == "PICKUP"): #TODO: Revise this
            #if (stateInBattle == "End of Turn"):
            #    if (self.currPokemon.getInternalItem() == None and self.opponentPokemon.getInternalItem() == None and self.opponentPokemon.getWasHoldingItem() == True):
             #       if (self.opponentPokemon.getName() == self.currPlayerAction.getCurrentOpponent().getName() and self.opponentPokemon.getName() == self.opponentPlayerAction.getCurrentAttacker().getName()):
              #          pass
            if (stateInBattle == "End of Turn"):
                #TODO: Revise and assign player actions for stateInBattle of End of Turn
                tempEffects = self.currPokemon.getTemporaryEffects().seek()
                values = tempEffects.get("ability effect")
                randomNum = rand.randint(0,1)
                if (self.currPokemon.getInternalItem() == None or values[1] == True and self.opponentPokemon.getInternalItem() == None and self.opponentPokemon.wasHoldingItem == True):
                    if (self.opponentPokemon.getInternalAbility() == ability and (self.currPokemon.getBattleStats()[5] < self.opponentPokemon.getBattleStats()[5] or (self.currPokemon.getBattleStats()[5] == self.opponentPokemon.getBattleStats()[5] and randomNum == 0))):
                        return
                    if (isinstance(self.currPlayerAction, Move) and self.currPlayerAction.getInternalMove() in ["Incinerate", "Bug Bite", "Pluck", "Knock Off"]):
                        return
                    if (self.opponentPokemon.getImmutableCopy().getInternalItem() == "Air Balloon"):
                        return
                    self.battleTab.getBattleUI().updateBattleInfo(self.currPokemon.getName() + "'s Pickup picked up" + self.opponentPokemon.getImmutableCopy().getInternalItem())
                    self.currPokemon.setInternalItem(self.opponentPokemon.getImmutableCopy().getInternalItem())
        elif (pokemonAbility == "HARVEST"):
            if (stateInBattle == "End of Turn"):
                #TODO: Implement Later
                pass



