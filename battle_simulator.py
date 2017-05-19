# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'battle_simulator.ui'
#
# Created: Fri May 19 01:02:05 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 535)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabCreate = QtGui.QTabWidget(self.centralwidget)
        self.tabCreate.setGeometry(QtCore.QRect(0, 0, 1071, 531))
        self.tabCreate.setObjectName("tabCreate")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.viewPokemon1 = QtGui.QGraphicsView(self.tab)
        self.viewPokemon1.setGeometry(QtCore.QRect(10, 30, 256, 151))
        self.viewPokemon1.setObjectName("viewPokemon1")
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(-80, 0, 201, 31))
        self.label.setObjectName("label")
        self.listPokemon1_moves = QtGui.QListWidget(self.tab)
        self.listPokemon1_moves.setGeometry(QtCore.QRect(0, 240, 321, 81))
        self.listPokemon1_moves.setObjectName("listPokemon1_moves")
        QtGui.QListWidgetItem(self.listPokemon1_moves)
        QtGui.QListWidgetItem(self.listPokemon1_moves)
        QtGui.QListWidgetItem(self.listPokemon1_moves)
        QtGui.QListWidgetItem(self.listPokemon1_moves)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(390, 60, 201, 31))
        self.label_3.setObjectName("label_3")
        self.viewPokemon2 = QtGui.QGraphicsView(self.tab)
        self.viewPokemon2.setGeometry(QtCore.QRect(810, 30, 256, 151))
        self.viewPokemon2.setObjectName("viewPokemon2")
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(720, 0, 201, 31))
        self.label_2.setObjectName("label_2")
        self.listPokemon2_moves = QtGui.QListWidget(self.tab)
        self.listPokemon2_moves.setGeometry(QtCore.QRect(740, 240, 321, 81))
        self.listPokemon2_moves.setObjectName("listPokemon2_moves")
        QtGui.QListWidgetItem(self.listPokemon2_moves)
        QtGui.QListWidgetItem(self.listPokemon2_moves)
        QtGui.QListWidgetItem(self.listPokemon2_moves)
        QtGui.QListWidgetItem(self.listPokemon2_moves)
        self.pushStartBattle = QtGui.QPushButton(self.tab)
        self.pushStartBattle.setGeometry(QtCore.QRect(340, 50, 92, 27))
        self.pushStartBattle.setObjectName("pushStartBattle")
        self.pushRestart = QtGui.QPushButton(self.tab)
        self.pushRestart.setGeometry(QtCore.QRect(630, 50, 92, 27))
        self.pushRestart.setObjectName("pushRestart")
        self.pushDifferentTeam = QtGui.QPushButton(self.tab)
        self.pushDifferentTeam.setGeometry(QtCore.QRect(430, 10, 201, 27))
        self.pushDifferentTeam.setObjectName("pushDifferentTeam")
        self.label_190 = QtGui.QLabel(self.tab)
        self.label_190.setGeometry(QtCore.QRect(0, 340, 111, 31))
        self.label_190.setObjectName("label_190")
        self.listPlayer1_team = QtGui.QListWidget(self.tab)
        self.listPlayer1_team.setGeometry(QtCore.QRect(0, 370, 321, 81))
        self.listPlayer1_team.setObjectName("listPlayer1_team")
        self.label_191 = QtGui.QLabel(self.tab)
        self.label_191.setGeometry(QtCore.QRect(260, 0, 41, 31))
        self.label_191.setObjectName("label_191")
        self.label_192 = QtGui.QLabel(self.tab)
        self.label_192.setGeometry(QtCore.QRect(720, 0, 41, 31))
        self.label_192.setObjectName("label_192")
        self.txtPokemon1_Level = QtGui.QLineEdit(self.tab)
        self.txtPokemon1_Level.setGeometry(QtCore.QRect(300, 0, 41, 31))
        self.txtPokemon1_Level.setObjectName("txtPokemon1_Level")
        self.txtPokemon2_Level = QtGui.QLineEdit(self.tab)
        self.txtPokemon2_Level.setGeometry(QtCore.QRect(760, 0, 41, 31))
        self.txtPokemon2_Level.setObjectName("txtPokemon2_Level")
        self.label_230 = QtGui.QLabel(self.tab)
        self.label_230.setGeometry(QtCore.QRect(740, 340, 111, 31))
        self.label_230.setObjectName("label_230")
        self.listPlayer2_team = QtGui.QListWidget(self.tab)
        self.listPlayer2_team.setGeometry(QtCore.QRect(740, 370, 321, 81))
        self.listPlayer2_team.setObjectName("listPlayer2_team")
        self.label_231 = QtGui.QLabel(self.tab)
        self.label_231.setGeometry(QtCore.QRect(0, 200, 111, 31))
        self.label_231.setObjectName("label_231")
        self.txtPokemon1_HP = QtGui.QLineEdit(self.tab)
        self.txtPokemon1_HP.setGeometry(QtCore.QRect(30, 200, 113, 27))
        self.txtPokemon1_HP.setObjectName("txtPokemon1_HP")
        self.label_232 = QtGui.QLabel(self.tab)
        self.label_232.setGeometry(QtCore.QRect(750, 200, 41, 31))
        self.label_232.setObjectName("label_232")
        self.txtPokemon2_HP = QtGui.QLineEdit(self.tab)
        self.txtPokemon2_HP.setGeometry(QtCore.QRect(780, 200, 113, 27))
        self.txtPokemon2_HP.setObjectName("txtPokemon2_HP")
        self.txtPokemon1_Nature = QtGui.QLineEdit(self.tab)
        self.txtPokemon1_Nature.setGeometry(QtCore.QRect(230, 200, 61, 27))
        self.txtPokemon1_Nature.setObjectName("txtPokemon1_Nature")
        self.label_233 = QtGui.QLabel(self.tab)
        self.label_233.setGeometry(QtCore.QRect(180, 200, 51, 31))
        self.label_233.setObjectName("label_233")
        self.label_236 = QtGui.QLabel(self.tab)
        self.label_236.setGeometry(QtCore.QRect(920, 200, 51, 31))
        self.label_236.setObjectName("label_236")
        self.txtPokemon2_Nature = QtGui.QLineEdit(self.tab)
        self.txtPokemon2_Nature.setGeometry(QtCore.QRect(970, 200, 61, 27))
        self.txtPokemon2_Nature.setObjectName("txtPokemon2_Nature")
        self.label_237 = QtGui.QLabel(self.tab)
        self.label_237.setGeometry(QtCore.QRect(180, 330, 51, 31))
        self.label_237.setObjectName("label_237")
        self.txtPokemon1_Ability = QtGui.QLineEdit(self.tab)
        self.txtPokemon1_Ability.setGeometry(QtCore.QRect(230, 330, 61, 27))
        self.txtPokemon1_Ability.setObjectName("txtPokemon1_Ability")
        self.label_238 = QtGui.QLabel(self.tab)
        self.label_238.setGeometry(QtCore.QRect(920, 330, 51, 31))
        self.label_238.setObjectName("label_238")
        self.txtPokemon2_Ability = QtGui.QLineEdit(self.tab)
        self.txtPokemon2_Ability.setGeometry(QtCore.QRect(970, 330, 61, 27))
        self.txtPokemon2_Ability.setObjectName("txtPokemon2_Ability")
        self.pushSwitchPlayer1 = QtGui.QPushButton(self.tab)
        self.pushSwitchPlayer1.setGeometry(QtCore.QRect(330, 370, 92, 27))
        self.pushSwitchPlayer1.setObjectName("pushSwitchPlayer1")
        self.pushSwitchPlayer2 = QtGui.QPushButton(self.tab)
        self.pushSwitchPlayer2.setGeometry(QtCore.QRect(640, 370, 92, 27))
        self.pushSwitchPlayer2.setObjectName("pushSwitchPlayer2")
        self.txtBattleInfo = QtGui.QLineEdit(self.tab)
        self.txtBattleInfo.setGeometry(QtCore.QRect(340, 90, 381, 211))
        self.txtBattleInfo.setObjectName("txtBattleInfo")
        self.tabCreate.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(0, 10, 201, 17))
        self.label_4.setObjectName("label_4")
        self.comboBattleType = QtGui.QComboBox(self.tab_2)
        self.comboBattleType.setGeometry(QtCore.QRect(10, 30, 141, 27))
        self.comboBattleType.setObjectName("comboBattleType")
        self.comboBattleType.addItem("")
        self.comboBattleType.addItem("")
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(0, 130, 201, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(260, 10, 31, 17))
        self.label_6.setObjectName("label_6")
        self.txtPokedexEntry = QtGui.QLineEdit(self.tab_2)
        self.txtPokedexEntry.setGeometry(QtCore.QRect(60, 170, 151, 27))
        self.txtPokedexEntry.setObjectName("txtPokedexEntry")
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(0, 230, 201, 17))
        self.label_7.setObjectName("label_7")
        self.viewCurrentPokemon = QtGui.QGraphicsView(self.tab_2)
        self.viewCurrentPokemon.setGeometry(QtCore.QRect(0, 250, 241, 171))
        self.viewCurrentPokemon.setObjectName("viewCurrentPokemon")
        self.comboAvailableMoves = QtGui.QComboBox(self.tab_2)
        self.comboAvailableMoves.setGeometry(QtCore.QRect(260, 280, 141, 27))
        self.comboAvailableMoves.setObjectName("comboAvailableMoves")
        self.label_8 = QtGui.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(260, 260, 201, 17))
        self.label_8.setObjectName("label_8")
        self.listChosenMoves = QtGui.QListWidget(self.tab_2)
        self.listChosenMoves.setGeometry(QtCore.QRect(260, 340, 321, 81))
        self.listChosenMoves.setObjectName("listChosenMoves")
        QtGui.QListWidgetItem(self.listChosenMoves)
        QtGui.QListWidgetItem(self.listChosenMoves)
        QtGui.QListWidgetItem(self.listChosenMoves)
        QtGui.QListWidgetItem(self.listChosenMoves)
        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(260, 320, 201, 17))
        self.label_9.setObjectName("label_9")
        self.txtChosenLevel = QtGui.QLineEdit(self.tab_2)
        self.txtChosenLevel.setGeometry(QtCore.QRect(60, 200, 51, 27))
        self.txtChosenLevel.setObjectName("txtChosenLevel")
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(20, 200, 41, 17))
        self.label_11.setObjectName("label_11")
        self.label_10 = QtGui.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(260, 40, 31, 17))
        self.label_10.setObjectName("label_10")
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(260, 60, 41, 17))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtGui.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(260, 80, 61, 17))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtGui.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(260, 100, 101, 17))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtGui.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(260, 120, 111, 17))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtGui.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(260, 140, 41, 17))
        self.label_16.setObjectName("label_16")
        self.txtEV_HP = QtGui.QLineEdit(self.tab_2)
        self.txtEV_HP.setGeometry(QtCore.QRect(380, 40, 51, 16))
        self.txtEV_HP.setObjectName("txtEV_HP")
        self.txtEV_Attack = QtGui.QLineEdit(self.tab_2)
        self.txtEV_Attack.setGeometry(QtCore.QRect(380, 60, 51, 16))
        self.txtEV_Attack.setObjectName("txtEV_Attack")
        self.txtEV_Defense = QtGui.QLineEdit(self.tab_2)
        self.txtEV_Defense.setGeometry(QtCore.QRect(380, 80, 51, 16))
        self.txtEV_Defense.setObjectName("txtEV_Defense")
        self.txtEV_SpAttack = QtGui.QLineEdit(self.tab_2)
        self.txtEV_SpAttack.setGeometry(QtCore.QRect(380, 100, 51, 16))
        self.txtEV_SpAttack.setObjectName("txtEV_SpAttack")
        self.txtEV_SpDefense = QtGui.QLineEdit(self.tab_2)
        self.txtEV_SpDefense.setGeometry(QtCore.QRect(380, 120, 51, 16))
        self.txtEV_SpDefense.setObjectName("txtEV_SpDefense")
        self.txtEV_Speed = QtGui.QLineEdit(self.tab_2)
        self.txtEV_Speed.setGeometry(QtCore.QRect(380, 140, 51, 16))
        self.txtEV_Speed.setObjectName("txtEV_Speed")
        self.label_65 = QtGui.QLabel(self.tab_2)
        self.label_65.setGeometry(QtCore.QRect(510, 10, 31, 17))
        self.label_65.setObjectName("label_65")
        self.label_100 = QtGui.QLabel(self.tab_2)
        self.label_100.setGeometry(QtCore.QRect(510, 40, 31, 17))
        self.label_100.setObjectName("label_100")
        self.txtIV_HP = QtGui.QLineEdit(self.tab_2)
        self.txtIV_HP.setGeometry(QtCore.QRect(640, 40, 51, 16))
        self.txtIV_HP.setObjectName("txtIV_HP")
        self.label_101 = QtGui.QLabel(self.tab_2)
        self.label_101.setGeometry(QtCore.QRect(510, 60, 41, 17))
        self.label_101.setObjectName("label_101")
        self.txtIV_Attack = QtGui.QLineEdit(self.tab_2)
        self.txtIV_Attack.setGeometry(QtCore.QRect(640, 60, 51, 16))
        self.txtIV_Attack.setObjectName("txtIV_Attack")
        self.label_102 = QtGui.QLabel(self.tab_2)
        self.label_102.setGeometry(QtCore.QRect(510, 80, 61, 17))
        self.label_102.setObjectName("label_102")
        self.txtIV_Defense = QtGui.QLineEdit(self.tab_2)
        self.txtIV_Defense.setGeometry(QtCore.QRect(640, 80, 51, 16))
        self.txtIV_Defense.setObjectName("txtIV_Defense")
        self.label_103 = QtGui.QLabel(self.tab_2)
        self.label_103.setGeometry(QtCore.QRect(510, 100, 101, 17))
        self.label_103.setObjectName("label_103")
        self.txtIV_SpAttack = QtGui.QLineEdit(self.tab_2)
        self.txtIV_SpAttack.setGeometry(QtCore.QRect(640, 100, 51, 16))
        self.txtIV_SpAttack.setObjectName("txtIV_SpAttack")
        self.label_104 = QtGui.QLabel(self.tab_2)
        self.label_104.setGeometry(QtCore.QRect(510, 120, 111, 17))
        self.label_104.setObjectName("label_104")
        self.txtIV_SpDefense = QtGui.QLineEdit(self.tab_2)
        self.txtIV_SpDefense.setGeometry(QtCore.QRect(640, 120, 51, 16))
        self.txtIV_SpDefense.setObjectName("txtIV_SpDefense")
        self.label_127 = QtGui.QLabel(self.tab_2)
        self.label_127.setGeometry(QtCore.QRect(510, 140, 41, 17))
        self.label_127.setObjectName("label_127")
        self.txtIV_Speed = QtGui.QLineEdit(self.tab_2)
        self.txtIV_Speed.setGeometry(QtCore.QRect(640, 140, 51, 16))
        self.txtIV_Speed.setObjectName("txtIV_Speed")
        self.pushRandomizeEVs = QtGui.QPushButton(self.tab_2)
        self.pushRandomizeEVs.setGeometry(QtCore.QRect(260, 170, 92, 27))
        self.pushRandomizeEVs.setObjectName("pushRandomizeEVs")
        self.pushRandomizeIVs = QtGui.QPushButton(self.tab_2)
        self.pushRandomizeIVs.setGeometry(QtCore.QRect(510, 170, 92, 27))
        self.pushRandomizeIVs.setObjectName("pushRandomizeIVs")
        self.label_128 = QtGui.QLabel(self.tab_2)
        self.label_128.setGeometry(QtCore.QRect(20, 150, 201, 17))
        self.label_128.setObjectName("label_128")
        self.label_129 = QtGui.QLabel(self.tab_2)
        self.label_129.setGeometry(QtCore.QRect(840, 10, 131, 17))
        self.label_129.setObjectName("label_129")
        self.label_155 = QtGui.QLabel(self.tab_2)
        self.label_155.setGeometry(QtCore.QRect(840, 40, 31, 17))
        self.label_155.setObjectName("label_155")
        self.txtFinal_HP = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_HP.setGeometry(QtCore.QRect(950, 40, 51, 16))
        self.txtFinal_HP.setObjectName("txtFinal_HP")
        self.label_182 = QtGui.QLabel(self.tab_2)
        self.label_182.setGeometry(QtCore.QRect(840, 60, 41, 17))
        self.label_182.setObjectName("label_182")
        self.txtFinal_Attack = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_Attack.setGeometry(QtCore.QRect(950, 60, 51, 16))
        self.txtFinal_Attack.setObjectName("txtFinal_Attack")
        self.label_183 = QtGui.QLabel(self.tab_2)
        self.label_183.setGeometry(QtCore.QRect(840, 80, 61, 17))
        self.label_183.setObjectName("label_183")
        self.txtFinal_Defense = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_Defense.setGeometry(QtCore.QRect(950, 80, 51, 16))
        self.txtFinal_Defense.setObjectName("txtFinal_Defense")
        self.label_184 = QtGui.QLabel(self.tab_2)
        self.label_184.setGeometry(QtCore.QRect(840, 100, 101, 17))
        self.label_184.setObjectName("label_184")
        self.txtFinal_SpAttack = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_SpAttack.setGeometry(QtCore.QRect(950, 100, 51, 16))
        self.txtFinal_SpAttack.setObjectName("txtFinal_SpAttack")
        self.label_185 = QtGui.QLabel(self.tab_2)
        self.label_185.setGeometry(QtCore.QRect(840, 120, 111, 17))
        self.label_185.setObjectName("label_185")
        self.txtFinal_SpDefense = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_SpDefense.setGeometry(QtCore.QRect(950, 120, 51, 16))
        self.txtFinal_SpDefense.setObjectName("txtFinal_SpDefense")
        self.label_186 = QtGui.QLabel(self.tab_2)
        self.label_186.setGeometry(QtCore.QRect(840, 140, 41, 17))
        self.label_186.setObjectName("label_186")
        self.txtFinal_Speed = QtGui.QLineEdit(self.tab_2)
        self.txtFinal_Speed.setGeometry(QtCore.QRect(950, 140, 51, 16))
        self.txtFinal_Speed.setObjectName("txtFinal_Speed")
        self.label_187 = QtGui.QLabel(self.tab_2)
        self.label_187.setGeometry(QtCore.QRect(600, 210, 201, 17))
        self.label_187.setObjectName("label_187")
        self.label_188 = QtGui.QLabel(self.tab_2)
        self.label_188.setGeometry(QtCore.QRect(860, 210, 201, 17))
        self.label_188.setObjectName("label_188")
        self.pushClearP1 = QtGui.QPushButton(self.tab_2)
        self.pushClearP1.setGeometry(QtCore.QRect(600, 350, 92, 27))
        self.pushClearP1.setObjectName("pushClearP1")
        self.pushClearP2 = QtGui.QPushButton(self.tab_2)
        self.pushClearP2.setGeometry(QtCore.QRect(860, 350, 92, 27))
        self.pushClearP2.setObjectName("pushClearP2")
        self.pushDone = QtGui.QPushButton(self.tab_2)
        self.pushDone.setGeometry(QtCore.QRect(750, 390, 92, 27))
        self.pushDone.setObjectName("pushDone")
        self.label_189 = QtGui.QLabel(self.tab_2)
        self.label_189.setGeometry(QtCore.QRect(0, 70, 211, 17))
        self.label_189.setObjectName("label_189")
        self.comboPlayerNumber = QtGui.QComboBox(self.tab_2)
        self.comboPlayerNumber.setGeometry(QtCore.QRect(10, 90, 141, 27))
        self.comboPlayerNumber.setObjectName("comboPlayerNumber")
        self.comboPlayerNumber.addItem("")
        self.comboPlayerNumber.addItem("")
        self.comboPlayerNumber.addItem("")
        self.label_234 = QtGui.QLabel(self.tab_2)
        self.label_234.setGeometry(QtCore.QRect(430, 260, 121, 17))
        self.label_234.setObjectName("label_234")
        self.comboAvailableAbilities = QtGui.QComboBox(self.tab_2)
        self.comboAvailableAbilities.setGeometry(QtCore.QRect(430, 280, 141, 27))
        self.comboAvailableAbilities.setObjectName("comboAvailableAbilities")
        self.label_235 = QtGui.QLabel(self.tab_2)
        self.label_235.setGeometry(QtCore.QRect(260, 230, 51, 17))
        self.label_235.setObjectName("label_235")
        self.comboNatures = QtGui.QComboBox(self.tab_2)
        self.comboNatures.setGeometry(QtCore.QRect(310, 220, 81, 27))
        self.comboNatures.setObjectName("comboNatures")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.comboNatures.addItem("")
        self.labelLevelCheck = QtGui.QLabel(self.tab_2)
        self.labelLevelCheck.setGeometry(QtCore.QRect(110, 230, 131, 20))
        self.labelLevelCheck.setText("")
        self.labelLevelCheck.setObjectName("labelLevelCheck")
        self.labelEntryCheck = QtGui.QLabel(self.tab_2)
        self.labelEntryCheck.setGeometry(QtCore.QRect(130, 200, 131, 20))
        self.labelEntryCheck.setText("")
        self.labelEntryCheck.setObjectName("labelEntryCheck")
        self.labelEVCheck = QtGui.QLabel(self.tab_2)
        self.labelEVCheck.setGeometry(QtCore.QRect(300, 10, 131, 20))
        self.labelEVCheck.setText("")
        self.labelEVCheck.setObjectName("labelEVCheck")
        self.labelIVCheck = QtGui.QLabel(self.tab_2)
        self.labelIVCheck.setGeometry(QtCore.QRect(560, 10, 131, 20))
        self.labelIVCheck.setText("")
        self.labelIVCheck.setObjectName("labelIVCheck")
        self.pushFinished = QtGui.QPushButton(self.tab_2)
        self.pushFinished.setGeometry(QtCore.QRect(700, 170, 131, 27))
        self.pushFinished.setObjectName("pushFinished")
        self.labelCheckFinalized = QtGui.QLabel(self.tab_2)
        self.labelCheckFinalized.setGeometry(QtCore.QRect(700, 150, 131, 17))
        self.labelCheckFinalized.setText("")
        self.labelCheckFinalized.setObjectName("labelCheckFinalized")
        self.listCurr_p1Team = QtGui.QListWidget(self.tab_2)
        self.listCurr_p1Team.setGeometry(QtCore.QRect(600, 230, 161, 111))
        self.listCurr_p1Team.setObjectName("listCurr_p1Team")
        self.listCurr_p2Team = QtGui.QListWidget(self.tab_2)
        self.listCurr_p2Team.setGeometry(QtCore.QRect(840, 230, 161, 111))
        self.listCurr_p2Team.setObjectName("listCurr_p2Team")
        self.tabCreate.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabCreate.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.viewPokemon2, self.viewPokemon1)
        MainWindow.setTabOrder(self.viewPokemon1, self.listPokemon1_moves)
        MainWindow.setTabOrder(self.listPokemon1_moves, self.tabCreate)
        MainWindow.setTabOrder(self.tabCreate, self.listPokemon2_moves)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "                        Pokemon 1", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listPokemon1_moves.isSortingEnabled()
        self.listPokemon1_moves.setSortingEnabled(False)
        self.listPokemon1_moves.item(0).setText(QtGui.QApplication.translate("MainWindow", "Move 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon1_moves.item(1).setText(QtGui.QApplication.translate("MainWindow", "Move 2: ", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon1_moves.item(2).setText(QtGui.QApplication.translate("MainWindow", "Move 3:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon1_moves.item(3).setText(QtGui.QApplication.translate("MainWindow", "Move 4:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon1_moves.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "                        Battle Info:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "                        Pokemon 2", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listPokemon2_moves.isSortingEnabled()
        self.listPokemon2_moves.setSortingEnabled(False)
        self.listPokemon2_moves.item(0).setText(QtGui.QApplication.translate("MainWindow", "Move 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon2_moves.item(1).setText(QtGui.QApplication.translate("MainWindow", "Move 2: ", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon2_moves.item(2).setText(QtGui.QApplication.translate("MainWindow", "Move 3:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon2_moves.item(3).setText(QtGui.QApplication.translate("MainWindow", "Move 4:", None, QtGui.QApplication.UnicodeUTF8))
        self.listPokemon2_moves.setSortingEnabled(__sortingEnabled)
        self.pushStartBattle.setText(QtGui.QApplication.translate("MainWindow", "Start Battle", None, QtGui.QApplication.UnicodeUTF8))
        self.pushRestart.setText(QtGui.QApplication.translate("MainWindow", "Restart", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDifferentTeam.setText(QtGui.QApplication.translate("MainWindow", "Choose a different team", None, QtGui.QApplication.UnicodeUTF8))
        self.label_190.setText(QtGui.QApplication.translate("MainWindow", "Player 1\'s team", None, QtGui.QApplication.UnicodeUTF8))
        self.label_191.setText(QtGui.QApplication.translate("MainWindow", "Level", None, QtGui.QApplication.UnicodeUTF8))
        self.label_192.setText(QtGui.QApplication.translate("MainWindow", "Level", None, QtGui.QApplication.UnicodeUTF8))
        self.label_230.setText(QtGui.QApplication.translate("MainWindow", "Player 2\'s team", None, QtGui.QApplication.UnicodeUTF8))
        self.label_231.setText(QtGui.QApplication.translate("MainWindow", "HP: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_232.setText(QtGui.QApplication.translate("MainWindow", "HP: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_233.setText(QtGui.QApplication.translate("MainWindow", "Nature", None, QtGui.QApplication.UnicodeUTF8))
        self.label_236.setText(QtGui.QApplication.translate("MainWindow", "Nature", None, QtGui.QApplication.UnicodeUTF8))
        self.label_237.setText(QtGui.QApplication.translate("MainWindow", "Ability", None, QtGui.QApplication.UnicodeUTF8))
        self.label_238.setText(QtGui.QApplication.translate("MainWindow", "Ability", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSwitchPlayer1.setText(QtGui.QApplication.translate("MainWindow", "Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSwitchPlayer2.setText(QtGui.QApplication.translate("MainWindow", "Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.tabCreate.setTabText(self.tabCreate.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Step 1: Choose type of Battle", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBattleType.setItemText(0, QtGui.QApplication.translate("MainWindow", "1v1 Battle", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBattleType.setItemText(1, QtGui.QApplication.translate("MainWindow", "6v6 Battle", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Step 2: Choose Pokemon", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "EVs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Your Pokemon:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Available Moves", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listChosenMoves.isSortingEnabled()
        self.listChosenMoves.setSortingEnabled(False)
        self.listChosenMoves.item(0).setText(QtGui.QApplication.translate("MainWindow", "Move 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.listChosenMoves.item(1).setText(QtGui.QApplication.translate("MainWindow", "Move 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.listChosenMoves.item(2).setText(QtGui.QApplication.translate("MainWindow", "Move 3:", None, QtGui.QApplication.UnicodeUTF8))
        self.listChosenMoves.item(3).setText(QtGui.QApplication.translate("MainWindow", "Move 4:", None, QtGui.QApplication.UnicodeUTF8))
        self.listChosenMoves.setSortingEnabled(__sortingEnabled)
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Moves Chosen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Level", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "HP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "Special Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "Special Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_65.setText(QtGui.QApplication.translate("MainWindow", "IVs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_100.setText(QtGui.QApplication.translate("MainWindow", "HP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_101.setText(QtGui.QApplication.translate("MainWindow", "Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_102.setText(QtGui.QApplication.translate("MainWindow", "Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_103.setText(QtGui.QApplication.translate("MainWindow", "Special Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_104.setText(QtGui.QApplication.translate("MainWindow", "Special Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_127.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.pushRandomizeEVs.setText(QtGui.QApplication.translate("MainWindow", "Randomize", None, QtGui.QApplication.UnicodeUTF8))
        self.pushRandomizeIVs.setText(QtGui.QApplication.translate("MainWindow", "Randomize", None, QtGui.QApplication.UnicodeUTF8))
        self.label_128.setText(QtGui.QApplication.translate("MainWindow", "Enter Pokedex Entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label_129.setText(QtGui.QApplication.translate("MainWindow", "Final Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.label_155.setText(QtGui.QApplication.translate("MainWindow", "HP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_182.setText(QtGui.QApplication.translate("MainWindow", "Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_183.setText(QtGui.QApplication.translate("MainWindow", "Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_184.setText(QtGui.QApplication.translate("MainWindow", "Special Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_185.setText(QtGui.QApplication.translate("MainWindow", "Special Defense", None, QtGui.QApplication.UnicodeUTF8))
        self.label_186.setText(QtGui.QApplication.translate("MainWindow", "Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_187.setText(QtGui.QApplication.translate("MainWindow", "Player 1\'s team", None, QtGui.QApplication.UnicodeUTF8))
        self.label_188.setText(QtGui.QApplication.translate("MainWindow", "Player 2\'s team", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClearP1.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClearP2.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushDone.setText(QtGui.QApplication.translate("MainWindow", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.label_189.setText(QtGui.QApplication.translate("MainWindow", "Step 2: Choose team for player", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPlayerNumber.setItemText(0, QtGui.QApplication.translate("MainWindow", "Player 1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPlayerNumber.setItemText(1, QtGui.QApplication.translate("MainWindow", "Player 2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboPlayerNumber.setItemText(2, QtGui.QApplication.translate("MainWindow", "CPU", None, QtGui.QApplication.UnicodeUTF8))
        self.label_234.setText(QtGui.QApplication.translate("MainWindow", "Available Abilities", None, QtGui.QApplication.UnicodeUTF8))
        self.label_235.setText(QtGui.QApplication.translate("MainWindow", "Nature", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(0, QtGui.QApplication.translate("MainWindow", "Hardy", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(1, QtGui.QApplication.translate("MainWindow", "Bold", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(2, QtGui.QApplication.translate("MainWindow", "Modest", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(3, QtGui.QApplication.translate("MainWindow", "Calm", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(4, QtGui.QApplication.translate("MainWindow", "Timid", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(5, QtGui.QApplication.translate("MainWindow", "Lonely", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(6, QtGui.QApplication.translate("MainWindow", "Docile", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(7, QtGui.QApplication.translate("MainWindow", "Mild", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(8, QtGui.QApplication.translate("MainWindow", "Gentle", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(9, QtGui.QApplication.translate("MainWindow", "Hasty", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(10, QtGui.QApplication.translate("MainWindow", "Adamant", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(11, QtGui.QApplication.translate("MainWindow", "Impish ", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(12, QtGui.QApplication.translate("MainWindow", "Bashful", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(13, QtGui.QApplication.translate("MainWindow", "Careful", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(14, QtGui.QApplication.translate("MainWindow", "Rash", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(15, QtGui.QApplication.translate("MainWindow", "Jolly", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(16, QtGui.QApplication.translate("MainWindow", "Naughty", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(17, QtGui.QApplication.translate("MainWindow", "Lax", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(18, QtGui.QApplication.translate("MainWindow", "Quirky", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(19, QtGui.QApplication.translate("MainWindow", "Naive", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(20, QtGui.QApplication.translate("MainWindow", "Brave", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(21, QtGui.QApplication.translate("MainWindow", "Relaxed", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(22, QtGui.QApplication.translate("MainWindow", "Quiet", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(23, QtGui.QApplication.translate("MainWindow", "Sassy", None, QtGui.QApplication.UnicodeUTF8))
        self.comboNatures.setItemText(24, QtGui.QApplication.translate("MainWindow", "Serious", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFinished.setText(QtGui.QApplication.translate("MainWindow", "Finished Editing", None, QtGui.QApplication.UnicodeUTF8))
        self.tabCreate.setTabText(self.tabCreate.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))

