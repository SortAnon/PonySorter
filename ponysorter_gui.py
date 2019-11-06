#!/usr/bin/env python3
import sys
import datetime
import threading
import queue
import os
import ffmpeg
from openal import *
import time
import gc
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QListWidgetItem,
    QDialogButtonBox,
    QDialogButtonBox,
    QMessageBox,
    QInputDialog,
)
from PySide2.QtCore import QFile, QTimer
from PySide2.QtGui import QColor, QTextCursor
from ui_main_window import Ui_MainWindow
from ui_load_episode import Ui_Dialog
import import_export
import hashes


class LoadDialog(QDialog):
    # Sets up the load episode window
    def __init__(self):
        super(LoadDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.detox_filenames()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.listWidget.itemSelectionChanged.connect(self.selected_episode)
        self.accepted.connect(self.pressed_ok)
        self.episode_data = None
        self.okay = False
        for k, v in hashes.friendly_names.items():
            item = QListWidgetItem()
            path1 = (
                os.path.dirname(os.path.realpath(__file__))
                + "/saved_changes/"
                + k
                + ".json"
            )
            path2 = (
                os.path.dirname(os.path.realpath(__file__)) + "/labels/" + k + ".txt"
            )
            if os.path.exists(path1):
                item.setData(32, path1)
                progress = import_export.check_progress(path1)
                item.setText(v + " (" + str(progress) + "% complete)")
                if progress == 100:
                    item.setBackgroundColor(QColor(20, 180, 20))
                else:
                    item.setBackgroundColor(QColor(180, 64, 20))
            elif os.path.exists(path2):
                item.setData(32, path2)
                item.setText(v)
            else:
                continue
            self.ui.listWidget.addItem(item)

    # Removes spaces from label filenames
    def detox_filenames(self):
        path = os.path.dirname(os.path.realpath(__file__)) + "/labels/"
        for r, _, f in os.walk(path):
            for file in f:
                os.rename(
                    os.path.join(r, file), os.path.join(r, file.replace(" ", "_"))
                )

    # Loads episode data
    def selected_episode(self):
        if self.ui.listWidget.currentIndex != -1:
            path = self.ui.listWidget.currentItem().data(32)
            if ".json" in path:
                self.episode_data = import_export.import_from_json(path)
            else:
                self.episode_data = import_export.import_from_labels(path)
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    # Called if OK is pressed
    def pressed_ok(self):
        self.okay = True


class MainWindow(QMainWindow):
    episode_data = {"labels": []}
    current_index = 0
    highest_index = 0
    listened = [False, False, False]
    moods = import_export.schema["properties"]["labels"]["items"]["properties"]["mood"][
        "items"
    ]["enum"]
    isUpdatingWidgets = False
    unsavedChanges = False

    # Sets up the main window
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.moodbox.addItems(self.moods)
        self.update_title(False)
        self.ui.all_buttons.setEnabled(False)
        # Dropdown events
        self.ui.actionLoad_episode.triggered.connect(self.load_episode)
        self.ui.actionSave_changes.triggered.connect(self.save_changes)
        self.ui.actionAdd_audio_path.triggered.connect(self.add_audio_path)
        self.ui.actionGenerate_Audacity_labels.triggered.connect(
            lambda: self.export_to_labels(None)
        )
        self.ui.actionSplit_by_pony.triggered.connect(
            lambda: self.split_by_pony("Twilight")
        )
        self.ui.actionGenerate_Audacity_labels_all_episodes.triggered.connect(
            lambda: self.export_all_labels(None)
        )
        # Previous/next events
        self.ui.button_next.clicked.connect(lambda: self.next_label(False))
        self.ui.button_previous.clicked.connect(lambda: self.next_label(True))
        # Listen/choose events
        self.ui.button_listenorig.clicked.connect(lambda: self.listen_to_source(0))
        self.ui.button_listenizo.clicked.connect(lambda: self.listen_to_source(1))
        self.ui.button_listenunmix.clicked.connect(lambda: self.listen_to_source(2))
        self.ui.button_chooseorig.clicked.connect(lambda: self.choose_source(0))
        self.ui.button_chooseizo.clicked.connect(lambda: self.choose_source(1))
        self.ui.button_chooseunmix.clicked.connect(lambda: self.choose_source(2))
        # Other events
        self.ui.startbox.valueChanged.connect(lambda: self.update_title(True))
        self.ui.endbox.valueChanged.connect(lambda: self.update_title(True))
        self.ui.characterbox.textChanged.connect(lambda: self.update_title(True))
        self.ui.moodbox.currentIndexChanged.connect(lambda: self.update_title(True))
        self.ui.transcriptbox.textChanged.connect(lambda: self.update_title(True))
        self.ui.radio_clean.clicked.connect(lambda: self.update_title(True))
        self.ui.radio_noisy.clicked.connect(lambda: self.update_title(True))
        self.ui.radio_verynoisy.clicked.connect(lambda: self.update_title(True))
        # End of events
        self.scan_for_files()

    # Updates the large text box at the bottom of the window
    def console(self, message):
        self.ui.consolebox.setText(self.ui.consolebox.toPlainText() + message + "\n")
        self.ui.consolebox.moveCursor(QTextCursor.End)

    # Updates the window title to show unsaved changes
    def update_title(self, isChanged=True):
        if isChanged:
            if not self.isUpdatingWidgets:
                self.setWindowTitle("Pony Sorter *")
                self.unsavedChanges = True
        else:
            self.setWindowTitle("Pony Sorter")
            self.unsavedChanges = False

    # Updates the widget contents with the info stored in episode_data
    def update_widgets(self, index):
        # Label data
        self.isUpdatingWidgets = True
        l = self.episode_data["labels"][index]
        self.ui.startbox.setValue(l["start"])
        self.ui.endbox.setValue(l["end"])
        self.ui.characterbox.setText(l["character"])
        self.ui.transcriptbox.setText(l["transcript"])
        self.ui.moodbox.setCurrentIndex(self.moods.index(l["mood"][0]))
        if len(l["mood"]) > 1:
            self.ui.secondarymoodlabel.setText(l["mood"][1] + " (secondary)")
        else:
            self.ui.secondarymoodlabel.setText("none (secondary)")
        if l["noise_level"] == "clean":
            self.ui.radio_clean.setChecked(True)
        elif l["noise_level"] == "noisy":
            self.ui.radio_noisy.setChecked(True)
        elif l["noise_level"] == "verynoisy":
            self.ui.radio_verynoisy.setChecked(True)
        self.isUpdatingWidgets = False

        # Navigation
        self.ui.all_buttons.setEnabled(True)
        self.listened = [l["reviewed"], l["reviewed"], l["reviewed"]]
        self.toggle_choices()
        if index >= len(self.episode_data["labels"]) - 1:
            self.ui.button_next.setEnabled(False)
        else:
            self.ui.button_next.setEnabled(l["reviewed"])
        if index <= 0:
            self.ui.button_previous.setEnabled(False)
        else:
            self.ui.button_previous.setEnabled(True)

    # Play audio from selected source
    def listen_to_source(self, index):
        self.update_dictionary()

        def play_audio(source, start, end):
            source.set(AL_SEC_OFFSET, start)
            source.play()
            time.sleep(end - start)
            source.stop()

        l = self.episode_data["labels"][self.current_index]
        if index == 0:
            play_audio(self.source1, l["start"], l["end"])
        elif index == 1:
            play_audio(self.source2, l["start"], l["end"])
        elif index == 2:
            play_audio(self.source3, l["start"], l["end"])
        self.listened[index] = True
        self.toggle_choices()

    def choose_source(self, index):
        l = self.episode_data["labels"][self.current_index]
        if index == 0:
            l["ideal_source"] = "original"
        elif index == 1:
            l["ideal_source"] = "izo"
        elif index == 2:
            l["ideal_source"] = "unmix"
        l["reviewed"] = True
        self.update_title(True)
        self.next_label(False)

    # Enables/disables the choice buttons
    def toggle_choices(self):
        if self.listened == [True, True, True]:
            self.ui.button_chooseorig.setEnabled(True)
            self.ui.button_chooseizo.setEnabled(True)
            self.ui.button_chooseunmix.setEnabled(True)
        else:
            self.ui.button_chooseorig.setEnabled(False)
            self.ui.button_chooseizo.setEnabled(False)
            self.ui.button_chooseunmix.setEnabled(False)

    # Writes the modified widget contents back to episode_data
    def update_dictionary(self):
        l = self.episode_data["labels"][self.current_index]
        l["start"] = self.ui.startbox.value()
        l["end"] = self.ui.endbox.value()
        l["character"] = self.ui.characterbox.text()
        l["transcript"] = self.ui.transcriptbox.text()
        if l["mood"][0] in self.moods:
            l["mood"][0] = self.moods[self.ui.moodbox.currentIndex()]
        if self.ui.radio_clean.isChecked():
            l["noise_level"] = "clean"
        elif self.ui.radio_noisy.isChecked():
            l["noise_level"] = "noisy"
        elif self.ui.radio_verynoisy.isChecked():
            l["noise_level"] = "verynoisy"

    # Goes to the next/previous label
    def next_label(self, isBackwards=False):
        if isBackwards:
            new_index = self.current_index - 1
        else:
            new_index = self.current_index + 1
        if new_index < 0:
            return False
        if new_index > len(self.episode_data["labels"]) - 1:
            message = "All done! Please save your changes and load a new episode."
            endOfFile = QMessageBox()
            endOfFile.setText(message)
            endOfFile.exec_()
            self.console(message)
            return False
        self.update_dictionary()
        self.current_index = new_index
        self.update_widgets(new_index)
        return True

    # Load a new episode
    def load_episode(self):
        if self.unsavedChanges:
            changesAsk = QMessageBox.question(
                self,
                "Save changes?",
                "Save changes before loading new episode?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            )
            if changesAsk == QMessageBox.Cancel:
                return
            if changesAsk == QMessageBox.Yes:
                self.save_changes()
        self.dialog = LoadDialog()
        self.dialog.exec_()
        if not self.dialog.okay:
            return
        self.episode_data = self.dialog.episode_data
        first_unreviewed = 0
        for i, l in enumerate(self.episode_data["labels"]):
            if l["reviewed"] == False:
                first_unreviewed = i
                break
        self.current_index = first_unreviewed
        self.highest_index = first_unreviewed
        self.update_widgets(first_unreviewed)
        self.load_audio()
        self.ui.actionSave_changes.setEnabled(True)

    # Load audio files. Converts to Ogg Vorbis first; OpenAL plays some FLAC files as loud static
    # Crashes occasionally with "double free or corruption (out)" or "corrupted size vs. prev_size"
    def load_audio(self):
        def convert_to_ogg(inpath, outname):
            outpath = (
                os.path.dirname(os.path.realpath(__file__)) + "/" + outname + ".ogg"
            )
            ffmpeg.input(inpath).output(outpath).overwrite_output().run()
            return outpath

        self.ui.all_buttons.setEnabled(False)
        original_path, izo_path, unmix_path = import_export.find_audio_path(
            self.episode_data["label_name"]
        )
        if original_path == "":
            self.console("Error: Original audio not found")
            self.source1 = None
        else:
            self.console("Loading original audio from " + original_path + "...")
            QApplication.processEvents()
            self.source1 = oalOpen(convert_to_ogg(original_path, ".temp1"))
        if izo_path == "":
            self.console("Error: iZo audio not found")
            self.source2 = None
        else:
            self.console("Loading iZo audio from " + izo_path + "...")
            QApplication.processEvents()
            self.source2 = oalOpen(convert_to_ogg(izo_path, ".temp2"))
        if unmix_path == "":
            self.console("Error: iZo+Unmix audio not found")
            self.source3 = None
        else:
            self.console("Loading iZo+Unmix audio from " + unmix_path + "...")
            QApplication.processEvents()
            self.source3 = oalOpen(convert_to_ogg(unmix_path, ".temp3"))
        self.console("\nLoading complete!")
        self.ui.all_buttons.setEnabled(True)

    # Save episode_data to JSON file
    def save_changes(self):
        self.update_dictionary()
        self.episode_data["last_modified"] = datetime.datetime.utcnow().isoformat()
        self.update_title(False)
        path = import_export.export_to_json(self.episode_data)
        self.console("Saved changes to " + path)

    # Save episode_data to Audacity labels
    def export_to_labels(self, character=None):
        self.update_dictionary()
        self.episode_data["last_modified"] = datetime.datetime.utcnow().isoformat()
        import_export.export_to_labels(self.episode_data, character, "original")
        import_export.export_to_labels(self.episode_data, character, "izo")
        import_export.export_to_labels(self.episode_data, character, "unmix")
        path = import_export.export_to_labels(self.episode_data, character, None)
        self.console("Exported labels to " + path)

    # Export all saved episodes to Audacity labels
    def export_all_labels(self, character=None):
        for k, _ in hashes.friendly_names.items():
            path1 = (
                os.path.dirname(os.path.realpath(__file__))
                + "/saved_changes/"
                + k
                + ".json"
            )
            path2 = (
                os.path.dirname(os.path.realpath(__file__)) + "/labels/" + k + ".txt"
            )
            if os.path.exists(path1):
                export_data = import_export.import_from_json(path1)
            elif os.path.exists(path2):
                export_data = import_export.import_from_labels(path2)
            else:
                continue
            import_export.export_to_labels(export_data, character, "original")
            import_export.export_to_labels(export_data, character, "izo")
            import_export.export_to_labels(export_data, character, "unmix")
            import_export.export_to_labels(export_data, character, None)
        self.console(
            "Exported all labels to "
            + os.path.dirname(os.path.realpath(__file__))
            + "/exported_labels/"
        )

    # Splits audio samples and generates LJ Speech metadata
    def split_by_pony(self, character=None):
        metadata = []
        for k, _ in hashes.friendly_names.items():
            path1 = (
                os.path.dirname(os.path.realpath(__file__))
                + "/saved_changes/"
                + k
                + ".json"
            )
            path2 = (
                os.path.dirname(os.path.realpath(__file__)) + "/labels/" + k + ".txt"
            )
            if os.path.exists(path1):
                export_data = import_export.import_from_json(path1)
            elif os.path.exists(path2):
                export_data = import_export.import_from_labels(path2)
            else:
                continue
            self.console("Exporting from " + export_data["label_name"] + "...")
            QApplication.processEvents()
            metadata.extend(import_export.split_by_pony(export_data, character, "izo"))
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + "/exported_splits/transcripts.csv",
            "w",
        ) as f:
            for m in metadata:
                f.write(m + "\n")
        self.console(
            "Done! Exported all "
            + character
            + " splits to "
            + os.path.dirname(os.path.realpath(__file__))
            + "/exported_splits/"
        )

    # Update the paths where the audio files are stored
    def add_audio_path(self):
        new_paths, okay = QInputDialog.getMultiLineText(
            self,
            "Add audio path(s)",
            "Enter the directories where the audio files are stored, separated by line breaks. Sub-directories will be scanned automatically.",
            "\n".join(import_export.config["audio_paths"]),
        )
        if okay:
            import_export.config["audio_paths"] = new_paths.splitlines()
            path = import_export.write_config()
            self.console("Saved settings to " + path)
            self.scan_for_files()

    # Find and hash audio files; takes about 5 minutes the first time
    def scan_for_files(self):
        self.ui.actionLoad_episode.setEnabled(False)
        self.ui.actionAdd_audio_path.setEnabled(False)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.hash_update)
        self.queue = queue.Queue()
        hash_thread = threading.Thread(
            target=import_export.hash_audio_files, args=(self.queue,)
        )
        hash_thread.daemon = True
        hash_thread.start()
        self.timer.start()

    # Check if hashes have finished computing
    def hash_update(self):
        while not self.queue.empty():
            data = self.queue.get()
            if data == "msgdone":
                self.timer.stop()
                self.ui.actionLoad_episode.setEnabled(True)
                self.ui.actionAdd_audio_path.setEnabled(True)
            else:
                self.console(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.move(
        (QApplication.desktop().availableGeometry().width() - window.width()) / 2,
        (QApplication.desktop().availableGeometry().height() - window.height()) / 2,
    )
    window.show()
    sys.exit(app.exec_())

