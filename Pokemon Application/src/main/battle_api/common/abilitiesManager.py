import sys
sys.path.append("ability_effects/")

from abilityEffects import AbilityEffects
from download import Download
from intimidate import Intimidate
from drizzle import Drizzle
from drought import Drought
from sandstream import Sandstream
from snowwarning import SnowWarning
from frisk import Frisk

class AbilitiesManager(object):
    def __init__(self, typeBattle, battleProperties, pokemonDataSource):
        self.abilitiesMapping = {"DOWNLOAD": Download("DOWNLOAD", typeBattle, battleProperties, pokemonDataSource), "INTIMIDATE": Intimidate("INTIMIDATE", typeBattle, battleProperties, pokemonDataSource), 
                                 "DRIZZLE": Drizzle("DRIZZLE", typeBattle, battleProperties, pokemonDataSource), "DROUGHT": Drought("DROUGHT", typeBattle, battleProperties, pokemonDataSource), 
                                 "SANDSTREAM": Sandstream("SANDSTREAM",typeBattle, battleProperties, pokemonDataSource), "SNOWWARNING": SnowWarning("SNOWWARNING", typeBattle, battleProperties, pokemonDataSource), 
                                 "FRISK": Frisk("FRISK", typeBattle, battleProperties, pokemonDataSource)}

    def getAbilityEffect(self, internalName):
        return self.abilitiesMapping.get(internalName)
