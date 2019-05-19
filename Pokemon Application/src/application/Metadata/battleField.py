class BattleField(object):
    def __init__(self):
        self.weatherEffect = None
        self.weatherInEffect = True
        self.fieldHazardsP1 = {}    # Field Hazards Set by Player 1
        self.fieldHazardsP2 = {}    # Field Hazards Set by Player 2
        self.fieldHazardsAll = []   # Field Hazards that affect both Players

    def getWeatherEffect(self):
        return self.weatherEffect

    def getWeather(self):
        if (self.weatherEffect == None or self.weatherInEffect == False):
            return None
        return self.weatherEffect[0]

    def setWeatherEffect(self, weather, turns):
        self.weatherEffect = (weather, turns)

    def getWeatherInEffect(self):
        return self.weatherInEffect

    def setWeatherInEffect(self, value):
        self.weatherInEffect = value

    def getFieldHazards(self):
        return self.fieldHazardsAll

    def addFieldHazard(self, hazard):
        self.fieldHazardsAll.append(hazard)

    def getPlayerFieldHazards(self, playerNum):
        if (playerNum == 1):
            return self.fieldHazardsP1
        return self.fieldHazardsP2

    def addPlayer1FieldHazard(self, hazard, numTurns):
        if (self.fieldHazardsP1.get(hazard) == None):
            if (hazard in ["Spikes", "Toxic Spikes"]):
                self.fieldHazardsP1.update({hazard: (numTurns, 1)})
            else:
                self.fieldHazardsP1.update({hazard:numTurns})
        else:
            tupleData = self.fieldHazardsP1.get(hazard)
            if (hazard == "Stealth Rock" or hazard == "Sticky Web" or hazard == "Reflect" or hazard == "Light Screen"):
                return
            elif (hazard == "Spikes" and tupleData[1] == 3):
                return
            elif (hazard == "Toxic Spikes" and tupleData[1] == 2):
                return
            tupleData[1] += 1
            self.fieldHazardsP1.update({hazard: tupleData})
        return

    def addPlayer2FieldHazard(self, hazard, numTurns):
        if (self.fieldHazardsP2.get(hazard) == None):
            if (hazard in ["Spikes", "Toxic Spikes"]):
                self.fieldHazardsP2.update({hazard: (numTurns, 1)})
            else:
                self.fieldHazardsP2.update({hazard:numTurns})
        else:
            tupleData = self.fieldHazardsP2.get(hazard)
            if (hazard == "Stealth Rock" or hazard == "Sticky Web" or hazard == "Reflect" or hazard == "Light Screen"):
                return
            elif (hazard == "Spikes" and tupleData[1] == 3):
                return
            elif (hazard == "Toxic Spikes" and tupleData[1] == 2):
                return
            tupleData[1] += 1
            self.fieldHazardsP2.update({hazard: tupleData})
        return

    def weatherAffectPokemon(self, pokemon):
        weather = self.getWeather()
        if (weather == None or pokemon.internalAbility == "MAGICGUARD" or self.weatherInEffect == False):
            return False
        elif (weather == "Sandstorm"):
            if ("ROCK" not in pokemon.types and "GROUND" not in pokemon.types and "STEEL" not in pokemon.types and pokemon.internalAbility not in ["SANDFORCE", "SANDVEIL", "SANDRUSH"] and pokemon.internalItem != "SANDGOGGLES"):
                return True
        elif (weather == "Hail"):
            if ("ICE" not in pokemon.types and pokemon.internalAbility not in ["ICEBODY", "SNOWCLOAK", "MAGICGUARD", "OVERCOAT", "SLUSHRUSH"] and pokemon.internalItem != "SAFETYGOGGLES"):
                return True
        elif (weatherObj[0] == "Sunny" and pokemon.internalAbility == "DRYSKIN"):
            return True
        return False

    def updateEoT(self):
        self.updatePlayerFieldHazardsEoT(1)
        self.updatePlayerFieldHazardsEoT(2)
        self.updateWeatherEoT()

    def updatePlayerFieldHazardsEoT(self, playerNum):
        if (playerNum == 1):
            playerFieldHazards = self.fieldHazardsP1
        else:
            playerFieldHazards = self.fieldHazardsP2

        for hazard in playerFieldHazards:
            value = playerFieldHazards.get(hazard)
            if (hazard in ["Spikes", "Toxic Spikes"]):
                if (value[0] - 1 == 0):
                    playerFieldHazards.pop(hazard)
                else:
                    value[0] -= 1
                    playerFieldHazards.update({hazard: value})
            else:
                value -= 1
                if (value == 0):
                    playerFieldHazards.pop(hazard)
                else:
                    playerFieldHazards.update({hazard: value})
        return

    def updateWeatherEoT(self):
        if (self.weatherEffect == None):
            return
        weather = self.weatherEffect[0]
        numTurns = self.weatherEffect[1]
        numTurns -= 1
        if (numTurns == 0):
            self.weatherEffect = None
        else:
            self.weatherEffect = (weather, numTurns)
        return
