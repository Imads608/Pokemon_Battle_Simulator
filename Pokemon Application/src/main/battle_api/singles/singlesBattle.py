import sys
sys.path.append("../common/")

from battleInterface import BattleInterface

from PyQt5 import QtCore, QtGui, QtWidgets
from pubsub import pub

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonMetadata):
        BattleInterface.__init__(self, pokemonMetadata, player1, player2, "singles", battleWidgets)
        self.battleUI = battleWidgets

    ####### Getters ########
    def getBattleWidgets(self):
        return self.battleUI

    ######## Battle Initialization ###########

    def initializeTeamDetails(self):
        for playerNum in range(1, 3):
            i = 0
            for pokemon in self.getPlayerBattler(playerNum).getPokemonTeam():
                pokemonFullName = self.getPokemonMetadata().getPokedex().get(pokemon.getPokedexEntry()).pokemonName
                _, abilityName, _ = self.getPokemonMetadata().getAbilitiesMetadata().get(pokemon.getInternalAbility())
                itemName, _, _, _, _, _, _ = self.getPokemonMetadata().getItemsMetadata().get(pokemon.getInternalItem())
                self.battleUI.getPlayerTeamListBox(playerNum).addItem(pokemonFullName)
                # self.listPlayer1_team.item(i).setForeground(QtCore.Qt.blue)
                self.battleUI.getPlayerTeamListBox(playerNum).item(i).setToolTip("Ability:\t\t" + abilityName + "\n" +
                                                              "Nature:\t\t" + pokemon.getNature() + "\n" +
                                                              "Item:\t\t" + itemName + "\n\n" +
                                                              "HP:\t\t" + str(pokemon.getFinalStats()[0]) + "\n" +
                                                              "Attack:\t\t" + str(pokemon.getFinalStats()[1]) + "\n" +
                                                              "Defense:\t" + str(pokemon.getFinalStats()[2]) + "\n" +
                                                              "SpAttack:\t" + str(pokemon.getFinalStats()[3]) + "\n" +
                                                              "SpDefense:\t" + str(pokemon.getFinalStats()[4]) + "\n" +
                                                              "Speed:\t\t" + str(pokemon.getFinalStats()[5]))
                i += 1
        return


    ############## Main Signals/Events  ##############
    def startBattle(self):
        self.initializeTeamDetails()

        self.battleUI.getSwitchPlayerPokemonPushButton(1).setEnabled(True)
        self.battleUI.getPokemonMovesListBox(1).setEnabled(True)

        self.battleUI.getStartBattlePushButton().setEnabled(False)
        self.battleUI.getPokemonMovesListBox(2).setEnabled(False)

        self.battleUI.getBattleInfoTextBox().setAlignment(QtCore.Qt.AlignHCenter)
        self.battleUI.getBattleInfoTextBox().setText("Battle Start!")

        self.battleUI.getPlayerTeamListBox(1).setCurrentRow(0)
        self.battleUI.getPlayerTeamListBox(2).setCurrentRow(0)

        self.getPlayerBattler(1).setCurrentPokemon(0)
        self.getPlayerBattler(2).setCurrentPokemon(0)

        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="===================================")
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 1 sent out " + self.getPlayerBattler(1).getPokemonTeam()[self.getPlayerBattler(1).getCurrentPokemon()].name)
        pub.sendMessage(self.getBattleProperties().getUpdateBattleInfoTopic(), message="Player 2 sent out " + self.getPlayerBattler(2).getPokemonTeam()[self.getPlayerBattler(2).getCurrentPokemon()].name)
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(1))
        pub.sendMessage(self.getBattleProperties().getDisplayPokemonInfoTopic(), playerBattler=self.getPlayerBattler(2))

    def executeAction(self, playerNum, actionType):
        if (playerNum == 1):
            opponentPlayerNum = 2
        else:
            opponentPlayerNum = 1

        if (self.actionExecutorFacade.setupAndValidate(self.getPlayerBattler(playerNum), self.getPlayerBattler(opponentPlayerNum), actionType) == True):
            self.actionExecutorFacade.executeAction(actionType)
            #actionExecutor = MoveExecutor(playerNum, self.getPlayerBattler(playerNum).getCurrentPokemon(), self.battleUI.getPokemonMovesListBox(playerNum))
            #actionExecutor = SwitchExecutor(playerNum, self.getPlayerBattler(playerNum, self.getPlayerBattler().getCurrentPokemon(), self.battleUI.getPlayerTeamListBox(playerNum)))

    def executeMove(self, actionExecutor):
        isValid = actionExecutor.validate()

        pass

    def executeSwitch(self):
        pass