class BattleProperties(object):
    def __init__(self):
        self.criticalHitStages = [16, 8, 4, 3, 2]
        self.statsStageMultipliers = [2 / 8, 2 / 7, 2 / 6, 2 / 5, 2 / 4, 2 / 3, 2 / 2, 3 / 2, 4 / 2, 5 / 2, 6 / 2, 7 / 2, 8 / 2]
        self.stage0Index = 6
        self.accuracy_evasionMultipliers = [3 / 9, 3 / 8, 3 / 7, 3 / 6, 3 / 5, 3 / 4, 3 / 3, 4 / 3, 5 / 3, 6 / 3, 7 / 3, 8 / 3, 9 / 3]
        self.accuracy_evasionStage0Index = 6
        self.spikesLayersDamage = [1 / 4, 1 / 6, 1 / 8]
        self.statusConditions = ["Healthy", "Poisoned", "Badly Poisoned", "Paralyzed", "Asleep", "Frozen", "Burn", "Drowsy", "Confused", "Infatuated"]

        # Publisher/Subscriber Topics
        self.battleRootTopic = "pokemonBattle"
        self.updateBattleInfoTopic = "pokemonBattle.updateBattleInfo"
        self.showDamageTopic = "pokemonBattle.showDamage"
        self.showHealingTopic = "pokemonBattle.showHealing"

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