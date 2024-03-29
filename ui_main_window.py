# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui',
# licensing of 'main_window.ui' applies.
#
# Created: Fri Nov  5 10:16:35 2021
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setWhatsThis("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.consolebox = QtWidgets.QTextEdit(self.centralwidget)
        self.consolebox.setGeometry(QtCore.QRect(10, 300, 781, 261))
        self.consolebox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.consolebox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.consolebox.setReadOnly(True)
        self.consolebox.setObjectName("consolebox")
        self.all_buttons = QtWidgets.QWidget(self.centralwidget)
        self.all_buttons.setGeometry(QtCore.QRect(0, 0, 801, 291))
        self.all_buttons.setObjectName("all_buttons")
        self.label_5 = QtWidgets.QLabel(self.all_buttons)
        self.label_5.setGeometry(QtCore.QRect(650, 180, 71, 18))
        self.label_5.setObjectName("label_5")
        self.radio_verynoisy = QtWidgets.QRadioButton(self.all_buttons)
        self.radio_verynoisy.setEnabled(True)
        self.radio_verynoisy.setGeometry(QtCore.QRect(670, 150, 104, 22))
        self.radio_verynoisy.setObjectName("radio_verynoisy")
        self.button_chooseunmix = QtWidgets.QPushButton(self.all_buttons)
        self.button_chooseunmix.setEnabled(False)
        self.button_chooseunmix.setGeometry(QtCore.QRect(510, 70, 201, 61))
        self.button_chooseunmix.setObjectName("button_chooseunmix")
        self.button_next = QtWidgets.QPushButton(self.all_buttons)
        self.button_next.setEnabled(True)
        self.button_next.setGeometry(QtCore.QRect(740, 10, 41, 121))
        self.button_next.setObjectName("button_next")
        self.button_previous = QtWidgets.QPushButton(self.all_buttons)
        self.button_previous.setEnabled(True)
        self.button_previous.setGeometry(QtCore.QRect(20, 10, 41, 121))
        self.button_previous.setObjectName("button_previous")
        self.moodbox = QtWidgets.QComboBox(self.all_buttons)
        self.moodbox.setEnabled(True)
        self.moodbox.setGeometry(QtCore.QRect(280, 200, 221, 32))
        self.moodbox.setObjectName("moodbox")
        self.button_listenorig = QtWidgets.QPushButton(self.all_buttons)
        self.button_listenorig.setEnabled(True)
        self.button_listenorig.setGeometry(QtCore.QRect(90, 10, 201, 51))
        self.button_listenorig.setObjectName("button_listenorig")
        self.button_listenizo = QtWidgets.QPushButton(self.all_buttons)
        self.button_listenizo.setEnabled(True)
        self.button_listenizo.setGeometry(QtCore.QRect(300, 10, 201, 51))
        self.button_listenizo.setObjectName("button_listenizo")
        self.transcriptbox = QtWidgets.QLineEdit(self.all_buttons)
        self.transcriptbox.setEnabled(True)
        self.transcriptbox.setGeometry(QtCore.QRect(10, 260, 781, 32))
        self.transcriptbox.setObjectName("transcriptbox")
        self.radio_clean = QtWidgets.QRadioButton(self.all_buttons)
        self.radio_clean.setEnabled(True)
        self.radio_clean.setGeometry(QtCore.QRect(490, 150, 81, 22))
        self.radio_clean.setObjectName("radio_clean")
        self.button_listenunmix = QtWidgets.QPushButton(self.all_buttons)
        self.button_listenunmix.setEnabled(False)
        self.button_listenunmix.setGeometry(QtCore.QRect(510, 10, 201, 51))
        self.button_listenunmix.setObjectName("button_listenunmix")
        self.label_3 = QtWidgets.QLabel(self.all_buttons)
        self.label_3.setGeometry(QtCore.QRect(290, 180, 101, 18))
        self.label_3.setObjectName("label_3")
        self.button_chooseorig = QtWidgets.QPushButton(self.all_buttons)
        self.button_chooseorig.setEnabled(True)
        self.button_chooseorig.setGeometry(QtCore.QRect(90, 70, 201, 61))
        self.button_chooseorig.setObjectName("button_chooseorig")
        self.startbox = QtWidgets.QDoubleSpinBox(self.all_buttons)
        self.startbox.setEnabled(True)
        self.startbox.setGeometry(QtCore.QRect(510, 200, 121, 32))
        self.startbox.setDecimals(6)
        self.startbox.setMaximum(9999.99)
        self.startbox.setSingleStep(0.01)
        self.startbox.setObjectName("startbox")
        self.characterbox = QtWidgets.QLineEdit(self.all_buttons)
        self.characterbox.setEnabled(True)
        self.characterbox.setGeometry(QtCore.QRect(10, 200, 261, 32))
        self.characterbox.setObjectName("characterbox")
        self.label_2 = QtWidgets.QLabel(self.all_buttons)
        self.label_2.setGeometry(QtCore.QRect(20, 180, 71, 18))
        self.label_2.setObjectName("label_2")
        self.endbox = QtWidgets.QDoubleSpinBox(self.all_buttons)
        self.endbox.setEnabled(True)
        self.endbox.setGeometry(QtCore.QRect(640, 200, 121, 32))
        self.endbox.setDecimals(6)
        self.endbox.setMaximum(9999.99)
        self.endbox.setSingleStep(0.01)
        self.endbox.setObjectName("endbox")
        self.radio_noisy = QtWidgets.QRadioButton(self.all_buttons)
        self.radio_noisy.setEnabled(True)
        self.radio_noisy.setGeometry(QtCore.QRect(580, 150, 81, 22))
        self.radio_noisy.setObjectName("radio_noisy")
        self.label_4 = QtWidgets.QLabel(self.all_buttons)
        self.label_4.setGeometry(QtCore.QRect(520, 180, 71, 20))
        self.label_4.setObjectName("label_4")
        self.button_chooseizo = QtWidgets.QPushButton(self.all_buttons)
        self.button_chooseizo.setEnabled(True)
        self.button_chooseizo.setGeometry(QtCore.QRect(300, 70, 201, 61))
        self.button_chooseizo.setObjectName("button_chooseizo")
        self.label = QtWidgets.QLabel(self.all_buttons)
        self.label.setGeometry(QtCore.QRect(20, 240, 61, 18))
        self.label.setObjectName("label")
        self.secondarymoodlabel = QtWidgets.QLabel(self.all_buttons)
        self.secondarymoodlabel.setGeometry(QtCore.QRect(280, 230, 151, 18))
        self.secondarymoodlabel.setObjectName("secondarymoodlabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        self.menuLabels = QtWidgets.QMenu(self.menubar)
        self.menuLabels.setObjectName("menuLabels")
        self.menuSplit = QtWidgets.QMenu(self.menubar)
        self.menuSplit.setObjectName("menuSplit")
        MainWindow.setMenuBar(self.menubar)
        self.actionExport_dataset = QtWidgets.QAction(MainWindow)
        self.actionExport_dataset.setObjectName("actionExport_dataset")
        self.actionLoad_episode = QtWidgets.QAction(MainWindow)
        self.actionLoad_episode.setObjectName("actionLoad_episode")
        self.actionSave_changes = QtWidgets.QAction(MainWindow)
        self.actionSave_changes.setEnabled(False)
        self.actionSave_changes.setObjectName("actionSave_changes")
        self.actionGenerate_Audacity_labels = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Audacity_labels.setObjectName("actionGenerate_Audacity_labels")
        self.actionAdd_audio_path = QtWidgets.QAction(MainWindow)
        self.actionAdd_audio_path.setObjectName("actionAdd_audio_path")
        self.actionGenerate_Audacity_labels_all_episodes = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Audacity_labels_all_episodes.setObjectName("actionGenerate_Audacity_labels_all_episodes")
        self.menuLabels.addAction(self.actionLoad_episode)
        self.menuLabels.addAction(self.actionSave_changes)
        self.menuLabels.addAction(self.actionAdd_audio_path)
        self.menuSplit.addAction(self.actionExport_dataset)
        self.menuSplit.addAction(self.actionGenerate_Audacity_labels)
        self.menuSplit.addAction(self.actionGenerate_Audacity_labels_all_episodes)
        self.menubar.addAction(self.menuLabels.menuAction())
        self.menubar.addAction(self.menuSplit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.button_previous, self.button_listenorig)
        MainWindow.setTabOrder(self.button_listenorig, self.button_listenizo)
        MainWindow.setTabOrder(self.button_listenizo, self.button_listenunmix)
        MainWindow.setTabOrder(self.button_listenunmix, self.button_chooseorig)
        MainWindow.setTabOrder(self.button_chooseorig, self.button_chooseizo)
        MainWindow.setTabOrder(self.button_chooseizo, self.button_chooseunmix)
        MainWindow.setTabOrder(self.button_chooseunmix, self.button_next)
        MainWindow.setTabOrder(self.button_next, self.radio_clean)
        MainWindow.setTabOrder(self.radio_clean, self.radio_noisy)
        MainWindow.setTabOrder(self.radio_noisy, self.radio_verynoisy)
        MainWindow.setTabOrder(self.radio_verynoisy, self.characterbox)
        MainWindow.setTabOrder(self.characterbox, self.moodbox)
        MainWindow.setTabOrder(self.moodbox, self.startbox)
        MainWindow.setTabOrder(self.startbox, self.endbox)
        MainWindow.setTabOrder(self.endbox, self.transcriptbox)
        MainWindow.setTabOrder(self.transcriptbox, self.consolebox)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Pony Sorter", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "End time", None, -1))
        self.radio_verynoisy.setText(QtWidgets.QApplication.translate("MainWindow", "Very noisy (6)", None, -1))
        self.radio_verynoisy.setShortcut(QtWidgets.QApplication.translate("MainWindow", "6", None, -1))
        self.button_chooseunmix.setText(QtWidgets.QApplication.translate("MainWindow", "Select iZotope+Unmix (9)", None, -1))
        self.button_chooseunmix.setShortcut(QtWidgets.QApplication.translate("MainWindow", "9", None, -1))
        self.button_next.setText(QtWidgets.QApplication.translate("MainWindow", ">", None, -1))
        self.button_previous.setText(QtWidgets.QApplication.translate("MainWindow", "<", None, -1))
        self.button_listenorig.setText(QtWidgets.QApplication.translate("MainWindow", "Listen to original (1)", None, -1))
        self.button_listenorig.setShortcut(QtWidgets.QApplication.translate("MainWindow", "1", None, -1))
        self.button_listenizo.setText(QtWidgets.QApplication.translate("MainWindow", "Listen to iZotope (2)", None, -1))
        self.button_listenizo.setShortcut(QtWidgets.QApplication.translate("MainWindow", "2", None, -1))
        self.radio_clean.setText(QtWidgets.QApplication.translate("MainWindow", "Clean (4)", None, -1))
        self.radio_clean.setShortcut(QtWidgets.QApplication.translate("MainWindow", "4", None, -1))
        self.button_listenunmix.setText(QtWidgets.QApplication.translate("MainWindow", "Listen to iZotope+Unmix (3)", None, -1))
        self.button_listenunmix.setShortcut(QtWidgets.QApplication.translate("MainWindow", "3", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Primary mood", None, -1))
        self.button_chooseorig.setText(QtWidgets.QApplication.translate("MainWindow", "Select original (7)", None, -1))
        self.button_chooseorig.setShortcut(QtWidgets.QApplication.translate("MainWindow", "7", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Character", None, -1))
        self.radio_noisy.setText(QtWidgets.QApplication.translate("MainWindow", "Noisy (5)", None, -1))
        self.radio_noisy.setShortcut(QtWidgets.QApplication.translate("MainWindow", "5", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Start time", None, -1))
        self.button_chooseizo.setText(QtWidgets.QApplication.translate("MainWindow", "Select iZotope (8)", None, -1))
        self.button_chooseizo.setShortcut(QtWidgets.QApplication.translate("MainWindow", "8", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Transcript", None, -1))
        self.secondarymoodlabel.setText(QtWidgets.QApplication.translate("MainWindow", "none (secondary)", None, -1))
        self.menuLabels.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.menuSplit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Export", None, -1))
        self.actionExport_dataset.setText(QtWidgets.QApplication.translate("MainWindow", "Export clips (UNFINISHED)", None, -1))
        self.actionLoad_episode.setText(QtWidgets.QApplication.translate("MainWindow", "Load episode", None, -1))
        self.actionSave_changes.setText(QtWidgets.QApplication.translate("MainWindow", "Save changes", None, -1))
        self.actionSave_changes.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+S", None, -1))
        self.actionGenerate_Audacity_labels.setText(QtWidgets.QApplication.translate("MainWindow", "Generate Audacity labels (current episode)", None, -1))
        self.actionAdd_audio_path.setText(QtWidgets.QApplication.translate("MainWindow", "Add audio path(s)", None, -1))
        self.actionGenerate_Audacity_labels_all_episodes.setText(QtWidgets.QApplication.translate("MainWindow", "Generate Audacity labels (all episodes)", None, -1))

