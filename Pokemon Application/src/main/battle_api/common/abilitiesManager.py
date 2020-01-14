from battle_api.common.ability_effects.abilityEffects import AbilityEffects
from battle_api.common.ability_effects.download import Download
from battle_api.common.ability_effects.intimidate import Intimidate
from battle_api.common.ability_effects.drizzle import Drizzle
from battle_api.common.ability_effects.drought import Drought
from battle_api.common.ability_effects.sandstream import Sandstream
from battle_api.common.ability_effects.snowwarning import SnowWarning
from battle_api.common.ability_effects.frisk import Frisk
from battle_api.common.ability_effects.anticipation import Anticipation
from battle_api.common.ability_effects.forewarn import Forewarn
from battle_api.common.ability_effects.trace import Trace
from battle_api.common.ability_effects.imposter import Imposter

class AbilitiesManager(object):
    def __init__(self, typeBattle, battleProperties, pokemonDataSource):
        self.abilitiesMapping = {"DOWNLOAD": Download("DOWNLOAD", typeBattle, battleProperties, pokemonDataSource),
                                 "INTIMIDATE": Intimidate("INTIMIDATE", typeBattle, battleProperties, pokemonDataSource),
                                 "DRIZZLE": Drizzle("DRIZZLE", typeBattle, battleProperties, pokemonDataSource), "DROUGHT": Drought("DROUGHT", typeBattle, battleProperties, pokemonDataSource), 
                                 "SANDSTREAM": Sandstream("SANDSTREAM",typeBattle, battleProperties, pokemonDataSource), "SNOWWARNING": SnowWarning("SNOWWARNING", typeBattle, battleProperties, pokemonDataSource), 
                                 "FRISK": Frisk("FRISK", typeBattle, battleProperties, pokemonDataSource), "ANTICIPATION":Anticipation("ANTICIPATION", typeBattle, battleProperties, pokemonDataSource),
                                 "FOREWARN": Forewarn("FOREWARN", typeBattle, battleProperties, pokemonDataSource), "TRACE": Trace("TRACE", typeBattle, battleProperties, pokemonDataSource),
                                 "IMPOSTER": Imposter("IMPOSTER", typeBattle, battleProperties, pokemonDataSource)}

    def getAbilityEffect(self, internalName):
        return self.abilitiesMapping.get(internalName)


