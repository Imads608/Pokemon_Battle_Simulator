from src.Core.API.Common.Data_Types.weatherTypes import WeatherTypes
import sys

class Weather(object):
    def __init__(self):
        self.weatherType = WeatherTypes.NORMAL
        self.inEffect = True
        self.turnsRemaining = sys.maxsize