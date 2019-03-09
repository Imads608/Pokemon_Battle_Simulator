class BattleField(object):
    def __init__(self):
        self.weatherEffect = None
        self.weatherInEffect = False
        self.fieldHazardsP1 = {}    # Field Hazards Set by Player 1
        self.fieldHazardsP2 = {}    # Field Hazards Set by Player 2
        self.fieldHazardsAll = []   # Field Hazards that affect both Players

    def addWeatherEffect(self, weather, turns):
        self.weatherEffect = (weather, turns)

    def setWeatherInEffect(self, value):
        self.weatherInEffect = value

    def addFieldHazard(self, hazard):
        self.fieldHazards.append(hazard)

    def addFieldHazardP1(self, hazard):
        self.fieldHazardsP1.append(hazard)

    def addFieldHazardP2(self, hazard, numTurns):
        if (self.fieldHazardsP1.get(hazard) == None):
            self.fieldHazardsP1.update({hazard: (numTurns, 1)})
        else:
            tupleData = self.fieldHazardsP1.get(hazard)
            if (hazard == "Stealth Rock" or hazard == "Sticky Web" or hazard == "Reflect" or hazard == "Light Screen"):
                return False
            elif (hazard == "Spikes" and tupleData[1] == 3):
                return False
            elif (hazard == "Toxic Spikes" and tupleData[1] == 2):
                return False
            tupleData[1] += 1
            self.fieldHazardsP1.update({hazard: tupleData})
        return True

    def weatherAffectPokemon(self, pokemon):
        if (pokemon.internalAbility == "MAGICGUARD" or self.weatherInEffect == False):
            return False
        if (self.weatherEffect[0] == "Sandstorm"):
            if ("ROCK" not in pokemon.types or "GROUND" not in pokemon.types or "STEEL" not in pokemon.types or pokemon.internalAbility not in ["SANDFORCE", "SANDVEIL", "SANDRUSH"] or pokemon.internalItem != "SANDGOGGLES"):
                return True
        if (self.weatherEffect[0] == "Hail"):
            if ("ICE" not in pokemon.types or pokemon.internalAbility not in ["ICEBODY", "SNOWCLOAK", "MAGICGUARD", "OVERCOAT", "SLUSHRUSH"] or pokemon.internalItem != "SAFETYGOGGLES"):
                return True
        return False
