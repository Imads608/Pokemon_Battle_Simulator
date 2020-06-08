import sys
#sys.path.append("../../resources")
from PyQt5 import QtCore, QtWidgets
from pubsub import pub


from src.UI.battle_simulator import Ui_MainWindow
from src.DAL.pokemonDAL import PokemonDAL
from src.Team_Builder.teamBuilder import TeamBuilder
from src.Core.API.battleFacade import BattleFacade
from src.Team_Builder.teamBuilderWidgets import TeamBuilderWidgets
from src.Core.API.Singles.Widgets.singlesBattleWidgets import SinglesBattleWidgets
from src.Core.API.Common.Data_Types.battleTypes import BattleTypes

class GameController(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GameController, self).__init__(parent)
        self.setupUi(self)

        # Publisher/Subscriber to events in Team Builder
        self.teamBuilderTopic = "teamBuilder.playersReady"
        pub.subscribe(self.teamBuilderDoneListener, self.teamBuilderTopic)

        # Pokemon Data Access Layer
        self.pokemonDAL = PokemonDAL()

        # Team Builder
        self.teamBuilder = TeamBuilder(self.teamBuilderSetup(), self.pokemonDAL, self.teamBuilderTopic)

        # Battle Client
        self.battleFacade = None

        # Team Builder Signals/Events
        self.teamBuilderSignalEvents()

        # Initialize Game
        self.initializeGame()


    ########## Initialization #############
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

        itemKeys = list(self.pokemonDAL.getItemsDictionary().keys())
        itemKeys.sort()
        count = 0
        self.pushFinished.setEnabled(False)
        self.pushDone.setEnabled(False)

        for key in itemKeys:
            itemDefinition = self.pokemonDAL.getItemDefinitionForInternalName(key)
            self.comboItems.addItem(itemDefinition.name)
            self.comboItems.setItemData(count, itemDefinition.description, QtCore.Qt.ToolTipRole)
            self.teamBuilder.listInternalItems.append(key)
            count += 1

        for count in range(25):
            increased, decreased = self.teamBuilder.natureEffects[count]
            string = "Increased: " + increased + "\tDecreased: " + decreased
            self.comboNatures.setItemData(count, string, QtCore.Qt.ToolTipRole)
            count += 1

        finalStats = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack,
                      self.txtFinal_SpDefense, self.txtFinal_Speed]
        for i in range(6):
            finalStats[i].setEnabled(False)

        return

    ################### Widget Events and Signals ###################
    def battleSignalEvents(self):
        self.battleFacade.getBattleWidgets().getPlayerTeamListBox(1).doubleClicked.connect(lambda: self.battleFacade.viewPokemon(1))
        self.battleFacade.getBattleWidgets().getPlayerTeamListBox(2).doubleClicked.connect(lambda: self.battleFacade.viewPokemon(2))
        self.battleFacade.getBattleWidgets().getStartBattlePushButton().clicked.connect(self.battleFacade.startBattle)
        self.battleFacade.getBattleWidgets().getSwitchPlayerPokemonPushButton(1).clicked.connect(lambda: self.battleFacade.switchPokemon(1))
        self.battleFacade.getBattleWidgets().getSwitchPlayerPokemonPushButton(2).clicked.connect(lambda: self.battleFacade.switchPokemon(2))
        self.battleFacade.getBattleWidgets().getPokemonMovesListBox(1).doubleClicked.connect(lambda: self.battleFacade.selectMove(1))
        self.battleFacade.getBattleWidgets().getPokemonMovesListBox(2).doubleClicked.connect(lambda: self.battleFacade.selectMove(2))

    def teamBuilderSignalEvents(self):
        self.teamBuilder.getTeamBuilderWidgets().getPokedexEntryTextBox().textChanged.connect(self.teamBuilder.updatePokemonEntry)
        self.teamBuilder.getTeamBuilderWidgets().getChosenLevelTextBox().textChanged.connect(self.teamBuilder.checkPokemonLevel)
        self.teamBuilder.getTeamBuilderWidgets().getAddMovePushButton().clicked.connect(self.teamBuilder.updateMoveSet)
        self.teamBuilder.getTeamBuilderWidgets().getRandomizeEVsPushButton().clicked.connect(self.teamBuilder.randomizeEVStats)
        self.teamBuilder.getTeamBuilderWidgets().getRandomizeIVsPushButton().clicked.connect(self.teamBuilder.randomizeIVStats)
        self.teamBuilder.getTeamBuilderWidgets().getNaturesCombinationBox().currentIndexChanged.connect(self.teamBuilder.updateStats)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[0].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[1].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[2].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[3].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[4].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getEvsList()[5].textChanged.connect(self.teamBuilder.updateEVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[0].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[1].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[2].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[3].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[4].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getIvsList()[5].textChanged.connect(self.teamBuilder.updateIVs)
        self.teamBuilder.getTeamBuilderWidgets().getHappinessValueTextBox().textChanged.connect(self.teamBuilder.finalizePokemon)
        self.teamBuilder.getTeamBuilderWidgets().getPokemonSetupFinishedPushButton().clicked.connect(self.teamBuilder.savePokemon)
        self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(1).doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(1), self.teamBuilder.getPlayerTeamList(1)))
        self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(2).doubleClicked.connect(lambda: self.teamBuilder.restorePokemonDetails(self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(2), self.teamBuilder.getPlayerTeamList(2)))
        self.teamBuilder.getTeamBuilderWidgets().getClearPlayerTeamPushButton(1).clicked.connect(lambda: self.teamBuilder.clearPokemon(self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(1), self.teamBuilder.getPlayerTeamList(1)))
        self.teamBuilder.getTeamBuilderWidgets().getClearPlayerTeamPushButton(2).clicked.connect(lambda: self.teamBuilder.clearPokemon(self.teamBuilder.getTeamBuilderWidgets().getCurrentPlayerTeam(2), self.teamBuilder.getPlayerTeamList(2)))
        self.teamBuilder.getTeamBuilderWidgets().getBattleTypeCombinationBox().currentIndexChanged.connect(self.teamBuilder.checkPlayerTeams)
        self.teamBuilder.getTeamBuilderWidgets().getTeamBuilderDonePushButton().clicked.connect(self.teamBuilder.creationDone)


########### Game Components Setup ################
    def teamBuilderSetup(self):
        evsList = [self.txtEV_HP, self.txtEV_Attack, self.txtEV_Defense, self.txtEV_SpAttack, self.txtEV_SpDefense, self.txtEV_Speed]
        ivsList = [self.txtIV_HP, self.txtIV_Attack, self.txtIV_Defense, self.txtIV_SpAttack, self.txtIV_SpDefense, self.txtIV_Speed]
        finalStats = [self.txtFinal_HP, self.txtFinal_Attack, self.txtFinal_Defense, self.txtFinal_SpAttack, self.txtFinal_SpDefense, self.txtFinal_Speed]
        return TeamBuilderWidgets(self.comboBattleType, self.comboPlayerNumber, self.txtPokedexEntry, self.txtChosenLevel, self.comboGenders, self.txtHappinessVal, self.viewCurrentPokemon, evsList, ivsList, finalStats,
                                          self.pushRandomizeEVs, self.pushRandomizeIVs, self.comboNatures, self.comboAvailableMoves, self.pushAddMove, self.comboItems, self.comboAvailableAbilities, self.listChosenMoves,
                                          self.pushFinished, self.listCurr_p1Team, self.listCurr_p2Team, self.pushClearP1, self.pushClearP2, self.pushDone, self.pushStartBattle, self.pushRestart, self.pushDifferentTeam)

    def singlesBattleWidgetsSetup(self):
        battleWidgets = SinglesBattleWidgets(self.lbl_hpPokemon1, self.lbl_hpPokemon2, self.txtPokemon1_Level,
                                         self.txtPokemon2_Level, self.lbl_statusCond1, self.lbl_statusCond2,
                                         self.hpBar_Pokemon1, self.hpBar_Pokemon2, self.viewPokemon1, self.viewPokemon2,
                                         self.listPokemon1_moves, self.listPokemon2_moves, self.listPlayer1_team,
                                         self.listPlayer2_team, self.pushSwitchPlayer1, self.pushSwitchPlayer2,
                                         self.pushStartBattle, self.txtBattleInfo)
        return battleWidgets

############# Subscription Listeners ##################
    def teamBuilderDoneListener(self, battleTypeChosen):
        battleWidgets = None
        if (battleTypeChosen == "singles"):
            battleWidgets = self.singlesBattleWidgetsSetup()
        self.battleFacade = BattleFacade(battleWidgets, self.pokemonDAL, BattleTypes.SINGLES, self.teamBuilder.player1Team, self.teamBuilder.player2Team)
        self.battleFacade.getBattleWidgets().getStartBattlePushButton().setEnabled(True)
        #self.battleFacade.getBattleWidgets().getRestartBattlePushButton().setEnabled(True)
        #self.battleFacade.getBattleWidgets().getDifferentTeamsPushButton().setEnabled(True)
        self.battleSignalEvents()



def startGame():
    currentApp = QtWidgets.QApplication(sys.argv)
    currentForm = GameController()
    currentForm.show()
    currentApp.exec_()

    #currentApp.exec_()

    return


if __name__ == "__main__":
    startGame()