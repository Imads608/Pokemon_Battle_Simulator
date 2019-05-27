from pubsub import pub


class GameController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GameController, self).__init__(parent)
        self.setupUi(self)

        # Publisher/Subscriber to events in Team Builder
        self.teamBuilderTopic = "teamBuilder.playersReady"
        pub.subscribe(self.teamBuilderDoneListener, self.teamBuilderTopic)

        # Pokemon Database
        self.pokemonDB = PokemonDatabase()

        # Team Builder
        self.teamBuilder = TeamBuilder(self.teamBuilderSetup(), self.pokemonDB, self.teamBuilderTopic)

        # Battle Client
        self.battleFacade = None

        # Battle Client Signals/Events
        self.battleFacade.getBattleUI().getPlayerTeamListBox(1).doubleClicked.connect(lambda: self.battleFacade.viewPokemon(1))
        self.battleFacade.getBattleUI().getPlayerTeamListBox(2).doubleClicked.connect(lambda: self.battleFacade.viewPokemon(2))

        self.battleFacade.getBattleUI().getStartBattlePushButton().clicked.connect(self.battleFacade.startBattle())

        self.battleFacade.getBattleUI().getSwitchPlayerPokemonPushButton(1).doubleClicked.connect(lambda: self.battleFacade.switchPokemon(1))
        self.battleFacade.getBattleUI().getSwitchPlayerPokemonPushButton(2).doubleClicked.connect(lambda: self.battleFacade.switchPokemon(2))

        self.battleFacade.getBattleUI().getPokemonMovesListBox(1).doubleClicked.connect(lambda: self.battleFacade.executeMove(1))
        self.battleFacade.getBattleUI().getPokemonMovesListBox(2).doubleClicked.connect(lambda: self.battleFacade.executeMove(2))

        # Team Builder Signals/Events
        self.txtPokedexEntry.textChanged.connect(self.teamBuilder.updatePokemonEntry)
        self.txtChosenLevel.textChanged.connect(self.teamBuilder.checkPokemonLevel)
        self.pushAddMove.clicked.connect(self.teamBuilder.updateMoveSet)
        self.pushRandomizeEVs.clicked.connect(self.teamBuilder.randomizeEVStats)
        self.pushRandomizeIVs.clicked.connect(self.teamBuilder.randomizeIVStats)
        self.comboNatures.currentIndexChanged.connect(self.teamBuilder.updateStats)
        self.txtEV_HP.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Attack.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Defense.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_SpAttack.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_SpDefense.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtEV_Speed.textChanged.connect(self.teamBuilder.updateEVs)
        self.txtIV_HP.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Attack.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Defense.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_SpAttack.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_SpDefense.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtIV_Speed.textChanged.connect(self.teamBuilder.updateIVs)
        self.txtHappinessVal.textChanged.connect(self.teamBuilder.finalizePokemon)
        self.pushFinished.clicked.connect(self.teamBuilder.savePokemon)
        self.listCurr_p1Team.doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.listCurr_p1Team, self.teamBuilder.player1Team))
        self.listCurr_p2Team.doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.listCurr_p2Team, self.teamBuilder.player2Team))
        self.pushClearP1.clicked.connect(lambda: self.teamBuilder.clearPokemon(self.listCurr_p1Team, self.teamBuilder.player1Team))
        self.pushClearP2.clicked.connect(lambda: self.teamBuilder.clearPokemon(self.listCurr_p2Team, self.teamBuilder.player2Team))
        self.comboBattleType.currentIndexChanged.connect(self.teamBuilder.checkPlayerTeams)
        self.pushDone.clicked.connect(self.teamBuilder.creationDone)

        # Initialize Game
        self.initializeGame()


    def initializeGame(self):
        # Battle Tab
        self.txtBattleInfo.setReadOnly(True)

        self.txtPokemon1_Level.setEnabled(False)

        self.txtPokemon2_Level.setEnabled(False)

        self.pushStartBattle.setEnabled(False)
        self.pushRestart.setEnabled(False)
        self.pushDifferentTeam.setEnabled(False)
        self.pushSwitchPlayer1.setEnabled(False)
        self.pushSwitchPlayer2.setEnabled(False)

        # Team Buider Tab
        self.teamBuilder.disableDetails()

        itemKeys = list(self.pokemonDB.itemsDatabase.keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            displayName, _, description, _, _, _, _ = self.pokemonDB.itemsDatabase.get(key)
            self.comboItems.addItem(displayName)
            self.comboItems.setItemData(count, description, QtCore.Qt.ToolTipRole)
            self.teamBuilder.listInternalItems.append(key)
            count += 1

        count = 0
        for count in range(25):
            increased, decreased = self.teamBuilder.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1

        for i in range(6):
            self.finalStats[i].setEnabled(False)
        return

    def teamBuilderSetup(self):
        return TeamBuilderWidgets(self.comboBattleType, self.comboPlayerNumber, self.txtPokedexEntry, self.txtChosenLevel, self.comboGenders, self.txtHappinessVal, self.viewCurrentPokemon, self.evsList, self.ivsList, self.finalStats,
                                          self.pushRandomizeEVs, self.pushRandomizeIVs, self.comboNatures, self.comboAvailableMoves, self.pushAddMove, self.comboItems, self.comboAvailableAbilities, self.listChosenMoves,
                                          self.pushFinished, self.listCurr_p1Team, self.listCurr_p2Team, self.pushClearP1, self.pushClearP2, self.pushDone, self.pushStartBattle, self.pushRestart, self.pushDifferentTeam)

    def teamBuilderDoneListener(self):
        battleWidgets = BattleWidgets1v1(self.lbl_hpPokemon1, self.lbl_hpPokemon2, self.txtPokemon1_Level,
                                        self.txtPokemon2_Level, self.lbl_statusCond1, self.lbl_statusCond2,
                                        self.hpBar_Pokemon1, self.hpBar_Pokemon2, self.viewPokemon1, self.viewPokemon2,
                                        self.listPokemon1_moves, self.listPokemon2_moves, self.listPlayer1_team,
                                        self.listPlayer2_team, self.pushSwitchPlayer1, self.pushSwitchPlayer2,
                                        self.pushStartBattle, self.txtBattleInfo)
        self.battleFacade = BattleFacade(battleWidgets, self.pokemonDB, "Singles")
        self.battleFacade.getStartBattlePushButton().setEnabled(True)
        self.battleFacade.getRestartBattlePushButton().setEnabled(True)
        self.battleFacade.getDifferentTeamsPushButton().setEnabled(True)