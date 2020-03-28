import battle_api.common.ability_effects as ability

class AbilitiesManager(object):
    def __init__(self, typeBattle, battleProperties, pokemonDataSource):
        self.abilitiesMapping = {"DOWNLOAD": ability.Download("DOWNLOAD", typeBattle, battleProperties, pokemonDataSource),
                                 "INTIMIDATE": ability.Intimidate("INTIMIDATE", typeBattle, battleProperties, pokemonDataSource),
                                 "DRIZZLE": ability.Drizzle("DRIZZLE", typeBattle, battleProperties, pokemonDataSource), "DROUGHT": ability.Drought("DROUGHT", typeBattle, battleProperties, pokemonDataSource),
                                 "SANDSTREAM": ability.Sandstream("SANDSTREAM",typeBattle, battleProperties, pokemonDataSource), "SNOWWARNING": ability.SnowWarning("SNOWWARNING", typeBattle, battleProperties, pokemonDataSource),
                                 "FRISK": ability.Frisk("FRISK", typeBattle, battleProperties, pokemonDataSource), "ANTICIPATION":ability.Anticipation("ANTICIPATION", typeBattle, battleProperties, pokemonDataSource),
                                 "FOREWARN": ability.Forewarn("FOREWARN", typeBattle, battleProperties, pokemonDataSource), "TRACE": ability.Trace("TRACE", typeBattle, battleProperties, pokemonDataSource),
                                 "IMPOSTER": ability.Imposter("IMPOSTER", typeBattle, battleProperties, pokemonDataSource)}

    def getAbilityEffect(self, internalName):
        return self.abilitiesMapping.get(internalName)


