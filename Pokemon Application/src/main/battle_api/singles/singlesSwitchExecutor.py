import sys
sys.path.append("../common/")

from switch import Switch

from pubsub import pub

class SinglesSwitchExecutor(object):
    def __init__(self, battleProperties):
        self.battleProperties = battleProperties

    ######## Visible Methods ###########
    def setupSwitch(self, playerBattler):
        currPokemonIndex = self.battleProperties.getPlayerPokemonIndex(playerBattler, playerBattler.getCurrentPokemon())
        switchObject = Switch(playerBattler.getPlayerNumber(), playerBattler, currPokemonIndex)
        pub.sendMessage(self.battleProperties.getPokemonSwitchTopic(), playerNum=playerBattler.getPlayerNumber(), switch=switchObject)
        return switchObject

    def validateSwitch(self, switchObject):
        if (switchObject.getCurrentPokemonIndex() == switchObject.getSwitchPokemonIndex()):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Cannot switch a pokemon that is already in battle")
            return False
        elif (switchObject.getSwitchPokemonIndex() > len(switchObject.getPlayerBattler().getPokemonTeam())-1):
            pub.sendMessage(self.battleProperties.getAlertPlayerTopic(), header="Invalid switch", body="Please select a valid pokemon to switch")
            return False
        return True