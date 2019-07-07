class BattleProperties(object):
    def __init__(self):
        self.criticalHitStages = [16, 8, 4, 3, 2]
        self.statsStageMultipliers = [2 / 8, 2 / 7, 2 / 6, 2 / 5, 2 / 4, 2 / 3, 2 / 2, 3 / 2, 4 / 2, 5 / 2, 6 / 2, 7 / 2, 8 / 2]
        self.stage0Index = 6
        self.accuracy_evasionMultipliers = [3 / 9, 3 / 8, 3 / 7, 3 / 6, 3 / 5, 3 / 4, 3 / 3, 4 / 3, 5 / 3, 6 / 3, 7 / 3, 8 / 3, 9 / 3]
        self.accuracy_evasionStage0Index = 6
        self.spikesLayersDamage = [1 / 4, 1 / 6, 1 / 8]
        self.statusConditions = ["Healthy", "Poisoned", "Badly Poisoned", "Paralyzed", "Asleep", "Frozen", "Burn", "Drowsy", "Confused", "Infatuated"]

        # Battle Widget Changes Topics
        self.battleRootTopic = "pokemonBattle"
        self.updateBattleInfoTopic = "pokemonBattle.widgets.updateBattleInfo"
        self.showDamageTopic = "pokemonBattle.widgets.showDamage"
        self.showHealingTopic = "pokemonBattle.widgets.showHealing"
        self.showStatusConditionTopic = "pokemonBattle.widgets.showStatusCondition"
        self.alertPlayerTopic = "pokemonBattle.widgets.alertPlayer"
        self.displayPokemonInfoTopic = "pokemonBattle.widgets.displayPokemonInfo"
        self.addPokemontoTeamTopic = "pokemonBattle.widgets.addPokemontoTeam"
        self.toggleSwitchPokemonTopic = "pokemonBattle.widgets.togglePokemonSwitch"
        self.toggleStartBattleTopic = "pokemonBattle.widgets.toggleStartBattle"
        self.togglePokemonMovesSelectionTopic = "pokemonBattle.widgets.toggleMovesSelection"
        self.togglePokemonSelectionTopic = "pokemonBattle.widgets.togglePokemonSelection"
        self.setCurrentPokemonTopic = "pokemonBattle.widgets.setCurrentPokemon"
        self.pokemonSwitchTopic = "pokemonBattle.widgets.pokemonSwitchSelected"
        self.pokemonMoveTopic = "pokemonBattle.widgets.pokemonMoveSelected"

        # Battke Mechanics Topics
        self.handleFaintedPokemonTopic = "pokemonBattle.battleMechanics.handlePokemonFainted"

        # Ability Effects Topics
        self.abilityEntryEffectsTopic = "pokemonBattle.abilityEffects.entryEffects"
        self.abilityPriorityEffectsTopic = "pokemonBattle.abilityEffects.priorityEffects"

        # BattleField Update Topics
        self.weatherBroadcastTopic = "pokemonBattle.battleField.broadcastWeather"
        self.hazardsBroadcastTopic = "pokemonBattle.battleField.broadcastHazard"
        self.weatherRequestTopic = "pokemonBattle.battleField.requestWeather"
        self.hazardRequestTopic = "pokemonBattle.battleField.requestHazard"
        self.fieldEntryHazardsTopic = "pokemonBattle.battleField.entryHazardsEffects"
        self.battleFieldEoTTopic = "pokemonBattle.battleField.updateEndOfTurnEffects"


        # Pokemon Status Conditions
        ''' Non Volatile '''
        # Healthy -> 0
        # Poisoned -> 1
        # Badly Poisoned -> 2
        # Paralyzed -> 3
        # Asleep -> 4
        # Frozen -> 5
        # Burn -> 6
        ''' Volatile '''
        # Drowsy -> 7
        # Confused -> 8
        # Infatuated -> 9


    ################# Getters ####################

    def getStatsStageMultiplier(self, deviation):
        return self.statsStageMultipliers[self.stage0Index+deviation]

    def getAccuracyEvasionMultiplier(self, deviation):
        return self.accuracy_evasionMultipliers[self.accuracy_evasionStage0Index+deviation]

    def getCriticalHitStages(self):
        return self.criticalHitStages

    def getStatsStageMultipliers(self):
        return self.statsStageMultipliers

    def getStatsStage0Index(self):
        return self.stage0Index

    def getAccuracyEvasionMultipliers(self):
        return self.accuracy_evasionMultipliers

    def getAccuracyEvasionStage0Index(self):
        return self.accuracy_evasionStage0Index

    def getSpikesLayersDamage(self):
        return self.spikesLayersDamage

    def getStatusConditions(self):
        return self.statusConditions

    def getBattleRootTopic(self):
        return self.battleRootTopic

    def getUpdateBattleInfoTopic(self):
        return self.updateBattleInfoTopic

    def getShowDamageTopic(self):
        return self.showDamageTopic

    def getShowHealingTopic(self):
        return self.showHealingTopic

    def getShowStatusConditionTopic(self):
        return self.showStatusConditionTopic

    def getAlertPlayerTopic(self):
        return self.alertPlayerTopic

    def getDisplayPokemonInfoTopic(self):
        return self.displayPokemonInfoTopic

    def getAddPokemonToTeamTopic(self):
        return self.addPokemontoTeamTopic

    def getToggleSwitchPokemonTopic(self):
        return self.toggleSwitchPokemonTopic

    def getToggleStartBattleTopic(self):
        return self.toggleStartBattleTopic

    def getTogglePokemonMovesSelectionTopic(self):
        return self.togglePokemonMovesSelectionTopic

    def getTogglePokemonSelectionTopic(self):
        return self.togglePokemonSelectionTopic

    def getSetCurrentPokemonTopic(self):
        return self.setCurrentPokemonTopic

    def getPokemonSwitchTopic(self):
        return self.pokemonSwitchTopic

    def getPokemonMoveSelectedTopic(self):
        return self.pokemonMoveTopic

    def getPokemonFaintedHandlerTopic(self):
        return self.handleFaintedPokemonTopic

    def getAbilityEntryEffectsTopic(self):
        return self.abilityEntryEffectsTopic

    def getAbilityPriorityEffectsTopic(self):
        return self.abilityPriorityEffectsTopic

    def getWeatherBroadcastTopic(self):
        return self.weatherBroadcastTopic

    def getHazardsBroadcastTopic(self):
        return self.hazardsBroadcastTopic

    def getWeatherRequestTopic(self):
        return self.weatherRequestTopic

    def getHazardsRequestTopic(self):
        return self.hazardRequestTopic

    def getBattleFieldEntryHazardEffectsTopic(self):
        return self.fieldEntryHazardsTopic

    def getBattleFieldUpdateEoTEffectsTopic(self):
        return self.battleFieldEoTTopic

    ############## Common Helper Functions ################9oooooo9
    def checkTypeEffectivenessExists(self, typeMove, effectivenessList):
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                return True
        return False

    def getTypeEffectiveness(self, typeMove, effectivenessList):
        numEffectiveness = 1
        for internalType, effectiveness in effectivenessList:
            if (internalType == typeMove):
                numEffectiveness = float(effectiveness[1:])
                break
        return numEffectiveness

    def getPlayerPokemonIndex(self, playerBattler, pokemonBattler):
        index = 0
        for pokemon in playerBattler.getPokemonTeam():
            if (pokemonBattler.getName() == pokemon.getName()):
                break
            index += 1
        return index

    def checkPlayerTeamFainted(self, playerTeam):
        retValue = True
        for pokemon in playerTeam:
            if (pokemon.getIsFainted() == False):
                retValue = False
        return retValue
