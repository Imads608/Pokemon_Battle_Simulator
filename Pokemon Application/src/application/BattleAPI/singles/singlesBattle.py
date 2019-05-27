from pubsub import pub

class SinglesBattle(BattleInterface):
    def __init__(self, battleWidgets, player1, player2, pokemonDB):
        BattleInterface.__init__(self, pokemonDB, player1, player2, pokemonDB)
        self.battleUI = battleWidgets

        # Topic to Publish Battle Messages
        self.battleMessageTopic = "pokemonBattle.battleInfo"

    def initializeTeamDetails(self):
        self.battleUI.setPlayerWidgetShortcuts(self.player1.getPokemonTeam(), self.player2.getPokemonTeam())
        i = 0
        for playerNum in range(1, 3):
            for pokemon in self.getPlayerTeam(playerNum):
                pokemonFullName = self.getPokemonDB().getPokedex().get(pokemon.getPokedexEntry()).pokemonName
                _, abilityName, _ = self.getPokemonDB().getAbilitiesDB().get(pokemon.getInternalAbility())
                itemName, _, _, _, _, _, _ = self.getPokemonDB().getItemsDB().get(pokemon.getInternalItem())
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

    def startBattle(self):
        self.initializeTeamDetails()

        self.battleUI.getSwitchPlayerPushButton(1).setEnabled(True)
        self.battleUI.getPokemonMovesListBox(1).setEnabled(True)

        self.battleUI.getStartBattlePushButton().setEnabled(False)
        self.battleUI.getPokemonMovesListBox(2).setEnabled(False)

        self.battleUI.getBattleInfoTextBox().setAlignment(QtCore.Qt.AlignHCenter)
        self.battleUI.getBattleInfoTextBox().setText("Battle Start!")

        self.battleUI.getPlayerTeamListBox(1).setCurrentRow(0)
        self.battleUI.getPlayerTeamListBox(2).setCurrentRow(0)

        self.player1.setCurrentPokemon(0)
        self.player2.setCurrentPokemon(0)

        pub.sendMessage(self.battleMessageTopic, message="===================================")
        pub.sendMessage(self.battleMessageTopic, message="Player 1 sent out " + self.getPlayerBattler(1).getPokemonTeam()[self.getPlayerBattler().getCurrentPokemon()].name)
        pub.sendMessage(self.battleMessageTopic, message="Player 2 sent out " + self.getPlayerBattler(2).getPokemonTeam()[self.getPlayerBattler().getCurrentPokemon()].name)

    def getPlayerBattler(self, playerNum):
        if (playerNum == 1):
            return self.player1
        return self.player2

    def executeAction(self, playerNum, actionName):
        if (actionName == "move"):
            actionExecutor = MoveExecutor(playerNum, self.getPlayerBattler(playerNum).getCurrentPokemon(), self.battleUI.getPokemonMovesListBox(playerNum))
        else:
            actionExecutor = SwitchExecutor(playerNum, self.getPlayerBattler(playerNum, self.getPlayerBattler().getCurrentPokemon(), self.battleUI.getPlayerTeamListBox(playerNum)))

    def executeMove(self, actionExecutor):
        isValid = actionExecutor.validate()

        pass

    def executeSwitch(self):
        pass