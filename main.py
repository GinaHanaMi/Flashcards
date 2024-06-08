# -*- coding: utf-8 -*-

from googletrans import Translator
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QMenuBar, QMenu, QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, Qt, QTimer
import datetime
from gtts import gTTS
import os
import pygame
import speech_recognition as sr
import random

pl_work_dict = []
en_work_dict = []
work_file_directory = []

settings_data = {
    "Lenght of training in seconds": 60,
    "Max score": 120,
}

translator = Translator()
recognizer = sr.Recognizer()

class PopupWindowAdd(QDialog):
    def __init__(self):
        super().__init__()

        # Create a grid layout for the popup window
        layout = QGridLayout()

        # First column (column 1)
        image1 = QLabel()
        pixmap1 = QPixmap("imagepopupflagone.png")
        image1.setPixmap(pixmap1.scaled(50, 50))
        layout.addWidget(image1, 1, 1)

        self.text1 = QLineEdit("")
        layout.addWidget(self.text1, 1, 2)

        speak_button1 = QPushButton(QIcon("speakimage.png"), "")
        speak_button1.clicked.connect(self.speakimageone)
        layout.addWidget(speak_button1, 1, 3)
        
        record_button1 = QPushButton(QIcon("recordimage.png"), "")
        record_button1.clicked.connect(self.recordenglish)
        layout.addWidget(record_button1, 3, 4)

        # Second column (column 2)
        translate_button = QPushButton(QIcon("translateimage.png"), "")
        translate_button.clicked.connect(self.translatefunc)
        layout.addWidget(translate_button, 2, 2)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button, 2, 4)

        # Third column (column 3)
        image2 = QLabel()
        pixmap2 = QPixmap("imagepopupflagtwo.png")
        image2.setPixmap(pixmap2.scaled(50, 50))
        layout.addWidget(image2, 3, 1)

        self.text2 = QLineEdit("")
        layout.addWidget(self.text2, 3, 2)

        speak_button2 = QPushButton(QIcon("speakimage.png"), "")
        speak_button2.clicked.connect(self.speakimagetwo)
        layout.addWidget(speak_button2, 3, 3)
        

        self.setLayout(layout)
        self.setWindowTitle("Add flashcard, translate or listen")

    def speakimageone(self):
        text_pl = self.text1.text()
        if len(text_pl) > 0:
            tts_pl = gTTS(text_pl, lang='pl')
            tts_pl.save("output-pl.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("output-pl.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()

            os.remove("output-pl.mp3")
            
    def recordenglish(self):
        text_en = self.text2.text()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

        try:
            transcribed_text = recognizer.recognize_google(audio)

        except sr.UnknownValueError:
            transcribed_text = ""
        except sr.RequestError as e:
            transcribed_text = ""
        except Exception as e:
            transcribed_text = ""
        self.text2.setText(transcribed_text)


    def speakimagetwo(self):
        text_en = self.text2.text()
        if len(text_en) > 0:
            tts_en = gTTS(text_en, lang='en')
            tts_en.save("output-en.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("output-en.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()

            os.remove("output-en.mp3")
        

    def translatefunc(self):
        text_pl = self.text1.text()
        text_en = self.text2.text()
    
        if len(text_pl) > len(text_en):
            text_to_translate_pl = text_pl
            target_language_pl = "en"
            translated_text_pl = translator.translate(text_to_translate_pl, dest=target_language_pl)
            self.text2.setText(translated_text_pl.text)
        else:
            text_to_translate_en = text_en
            target_language_en = "pl"
            translated_text_en = translator.translate(text_to_translate_en, dest=target_language_en)
            self.text1.setText(translated_text_en.text)

    def save_data(self):
        text1 = self.text1.text()
        text2 = self.text2.text()

        pl_work_dict.append(text1)
        en_work_dict.append(text2)
        

class PopupWindowEdit(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()

        # Create a table widget for editing data
        self.edit_table = QTableWidget()
        self.edit_table.setColumnCount(3)  # Added one more column for the delete buttons
        self.edit_table.setHorizontalHeaderLabels(['PL', 'EN', 'Delete'])
        self.populate_edit_table(self.edit_table, pl_work_dict, en_work_dict)
        layout.addWidget(self.edit_table)

        # Add a save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setWindowTitle("Edit of delete")

        self.adjustSize()

    def populate_edit_table(self, table, data1, data2):
        table.setRowCount(len(data1))
        for i, (item1, item2) in enumerate(zip(data1, data2)):
            table.setItem(i, 0, QTableWidgetItem(item1))
            table.setItem(i, 1, QTableWidgetItem(item2))

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=i: self.delete_row(row))
            table.setCellWidget(i, 2, delete_button)

        # Automatically resize the table to fit its contents
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def delete_row(self, row):
        if row >= 0 and row < len(pl_work_dict) and row < len(en_work_dict):
            del pl_work_dict[row]
            del en_work_dict[row]

            # Re-populate the table with the updated data
            self.populate_edit_table(self.edit_table, pl_work_dict, en_work_dict)

    def save_data(self):
        # Save the edited data back to the lists
        for i in range(len(pl_work_dict)):
            pl_work_dict[i] = self.edit_table.item(i, 0).text()
            en_work_dict[i] = self.edit_table.item(i, 1).text()


class PopupWindowPlayFlashcards(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Play Flashcards")

        layout = QGridLayout()

        self.big_button = QPushButton()
        self.big_button.setFixedSize(1000, 400)

        font = QFont()
        font.setPointSize(30)

        self.big_button.setFont(font)

        self.big_button.clicked.connect(self.toggle_text)

        # Store the indices for the items to be displayed
        self.index1 = 0
        self.index2 = 0

        self.list1 = pl_work_dict
        self.list2 = en_work_dict

        if len(self.list1) > 0 and len(self.list2) > 0:
            self.current_list = self.list1
            self.current_index = self.index1
            self.big_button.setText(self.current_list[self.current_index])
        else:
            self.current_list = []
            self.current_index = -1
            self.big_button.setText("No data available")

        self.small_button1 = QPushButton(QIcon("speakimage.png"), "")
        self.small_button1.clicked.connect(self.window_play_one)

        self.small_button2 = QPushButton(QIcon("iconnext.png"), "")
        self.small_button2.clicked.connect(self.window_play_two)

        self.small_button3 = QPushButton(QIcon("correct.png"), "")
        self.small_button3.clicked.connect(self.window_play_three)

        self.small_button4 = QPushButton(QIcon("incorrect.png"), "")
        self.small_button4.clicked.connect(self.window_play_four)

        self.text_label1 = QLabel("")

        self.lenght_of_session = settings_data.get("Lenght of training in seconds", 60)
        self.number_of_repeated_flashcards = 0
        self.text_label2 = QLabel(f"{self.number_of_repeated_flashcards} / {self.lenght_of_session}")


        self.max_points_in_session = settings_data.get("Max score", 120)
        self.score_good = 0
        self.text_label3 = QLabel(f"{self.score_good} / {self.max_points_in_session}")

        self.score_bad = 0
        self.text_label4 = QLabel(f"{self.score_bad} / {self.max_points_in_session}")

        self.text_label1.setAlignment(Qt.AlignCenter)
        self.text_label2.setAlignment(Qt.AlignCenter)
        self.text_label3.setAlignment(Qt.AlignCenter)
        self.text_label4.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.big_button, 1, 1, 1, 4)
        layout.addWidget(self.small_button1, 2, 1)
        layout.addWidget(self.small_button2, 2, 2)
        layout.addWidget(self.small_button3, 2, 3)
        layout.addWidget(self.small_button4, 2, 4)
        layout.addWidget(self.text_label1, 3, 1)
        layout.addWidget(self.text_label2, 3, 2)
        layout.addWidget(self.text_label3, 3, 3)
        layout.addWidget(self.text_label4, 3, 4)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.remaining_time = self.lenght_of_session
        self.done = None
        self.submitted_good_bad = False

    def toggle_text(self):
        if self.current_list == self.list1:
            self.current_list = self.list2
            self.current_index = self.index2
        else:
            self.current_list = self.list1
            self.current_index = self.index1

        self.big_button.setText(self.current_list[self.current_index])


    def window_play_one(self):
        text_to_speak = self.big_button.text()

        if self.current_list is self.list2:
            tts_lang = 'en'
        else:
            tts_lang = 'pl'

        if len(text_to_speak) > 0:
            tts = gTTS(text_to_speak, lang=tts_lang)
            tts.save("output.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.quit()

            os.remove("output.mp3")


    def window_play_two(self):
        self.submitted_good_bad = False
        if len(self.list1) > 0:
            random_index = random.randint(0, len(self.list1) - 1)
            self.index1 = random_index
            self.index2 = random_index

            if self.current_list is self.list1:
                self.current_list = self.list2
            else:
                self.current_list = self.list1

            self.current_index = self.index1
            self.big_button.setText(self.current_list[self.current_index])

            self.number_of_repeated_flashcards += 1
            self.text_label2.setText(f"{self.number_of_repeated_flashcards} / {self.lenght_of_session}")
        else:
            self.current_index = -1
            self.big_button.setText("No data available")

    def window_play_three(self):
        if self.submitted_good_bad is False:
            self.score_good += 1
            self.text_label3.setText(f"{self.score_good} / {self.lenght_of_session}")
            self.submitted_good_bad = True

    def window_play_four(self):
        if self.submitted_good_bad is False:
            self.score_bad += 1
            self.text_label4.setText(f"{self.score_bad} / {self.lenght_of_session}")
            self.submitted_good_bad = True

    def update_timer(self):
        try:
            self.remaining_time = int(self.remaining_time)
            self.remaining_time -= 1
        except ValueError:
            self.remaining_time = 0

        if self.remaining_time < 0:
            self.accept()

        self.text_label1.setText(f"{self.remaining_time} seconds left")


class NoResizeMainWindow(QMainWindow):
    def __init__(self):
        super(NoResizeMainWindow, self).__init__()
        self.setFixedSize(85, 720)


class IconWidget(QWidget):
    def __init__(self, icon_path, click_function, icon_width, icon_height, parent=None):
        super(IconWidget, self).__init__(parent)

        self.icon_button = QPushButton()
        self.icon_button.setIcon(QIcon(icon_path))
        self.icon_button.setFixedSize(icon_width, icon_height)
        self.icon_button.clicked.connect(click_function)

        layout = QVBoxLayout()
        layout.addWidget(self.icon_button)
        self.setLayout(layout)

class PopupWindowSettings(QDialog):
    settings_data = {}
    selected_game_type = "Flashcards"

    def __init__(self, settings_data):
        super().__init__()

        PopupWindowSettings.settings_data = settings_data
        layout = QVBoxLayout()

        self.setting_labels = []
        self.setting_edits = []

        for setting_name, default_value in PopupWindowSettings.settings_data.items():
            setting_layout = QHBoxLayout()
            label = QLabel(setting_name)
            edit = QLineEdit()
            edit.setText(str(default_value))

            self.setting_labels.append(label)
            self.setting_edits.append(edit)

            setting_layout.addWidget(label)
            setting_layout.addWidget(edit)
            layout.addLayout(setting_layout)

        game_type_layout = QVBoxLayout()
        game_type_label = QLabel("Select Game Type:")
        game_type_layout.addWidget(game_type_label)

        game_types = ["Flashcards"]

        if PopupWindowSettings.selected_game_type is None:
            PopupWindowSettings.selected_game_type = game_types[0]

        self.radio_buttons = []

        for game_type in game_types:
            radio_button = QRadioButton(game_type)
            radio_button.toggled.connect(self.game_type_selected)
            self.radio_buttons.append(radio_button)
            game_type_layout.addWidget(radio_button)
            if game_type == PopupWindowSettings.selected_game_type:
                radio_button.setChecked(True)

        layout.addLayout(game_type_layout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setWindowTitle("Settings")

    def game_type_selected(self):
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                PopupWindowSettings.selected_game_type = radio_button.text()

    def save_settings(self):
        # Update the class attribute with the edited settings
        for label, edit in zip(self.setting_labels, self.setting_edits):
            setting_name = label.text()
            setting_value = edit.text()
            PopupWindowSettings.settings_data[setting_name] = setting_value


def icon1_click_function():
    popup_window_add = PopupWindowAdd()
    popup_window_add.exec_()

def icon2_click_function():
    popup_window_edit = PopupWindowEdit()
    popup_window_edit.exec_()

def icon3_click_function():
    popup_window_settings = PopupWindowSettings(settings_data)
    popup_window_settings.exec_()
    
def icon4_click_function():
    if len(pl_work_dict) > 0 and len(en_work_dict) > 0 and PopupWindowSettings.selected_game_type == "Flashcards":
        popup_window_play_flashcards = PopupWindowPlayFlashcards()
        popup_window_play_flashcards.exec_()

def custom_datetime_string():
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%d-%m-%Y-%H-%M")
    return formatted_date_time

def read_data_from_file(file_name, en_work_dict, pl_work_dict):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) == 2:
                    pl_word, en_word  = parts
                    en_work_dict.append(en_word)
                    pl_work_dict.append(pl_word)
    except FileNotFoundError:
        print(f"File not found: {file_name}")


# Function definitions for menu actions
def new_action_function():
    new_file_directory = QFileDialog.getExistingDirectory(None, "Select folder", "")
    new_formatted_time = custom_datetime_string()
    work_file_directory.clear()
    pl_work_dict.clear()
    en_work_dict.clear()
    work_file_directory.append(f"{new_file_directory}/new-flascards-{new_formatted_time}.txt")
    with open(work_file_directory[0], "w", encoding="utf-8"):
        pass
    

def open_action_function():
    work_file_directory.clear()
    pl_work_dict.clear()
    en_work_dict.clear()
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, "Select file", "", "Text file (*.txt)", options=options)
    read_data_from_file(file_name, en_work_dict, pl_work_dict)
    work_file_directory.append(file_name)


def save_action_function():
    with open(work_file_directory[0], "w", encoding="utf-8") as file:
        for pl_word, en_word in zip(pl_work_dict, en_work_dict):
            file.write(f"{en_word}, {pl_word}\n")


def debug_action_function():
    print(f"English words in memory: {en_work_dict}")
    print(f"Polish words in memory: {pl_work_dict}")
    print(settings_data)
    chosen_game_type = PopupWindowSettings.selected_game_type
    print(f"Selected Game Type: {PopupWindowSettings.selected_game_type}")


# Create the application instance
app = QApplication(sys.argv)

# Create a main window
window = NoResizeMainWindow()
window.setWindowTitle("GUI")
window.move(0, 0)

central_widget = QWidget()
window.setCentralWidget(central_widget)

menu_bar = window.menuBar()
file_menu = menu_bar.addMenu("File")

left_column_layout = QVBoxLayout()

icon1 = IconWidget("icon1.png", icon1_click_function, 50, 50)
left_column_layout.addWidget(icon1)

icon2 = IconWidget("icon2.png", icon2_click_function, 50, 50)
left_column_layout.addWidget(icon2)

icon3 = IconWidget("icon3.png", icon3_click_function, 50, 50)
left_column_layout.addWidget(icon3)

icon4 = IconWidget("icon4.png", icon4_click_function, 50, 50)
left_column_layout.addWidget(icon4)

left_column_layout.setAlignment(Qt.AlignTop)
central_widget.setLayout(left_column_layout)


nowe_action = QAction("New", window)
nowe_action.triggered.connect(new_action_function)
file_menu.addAction(nowe_action)

otworz_action = QAction("Open", window)
otworz_action.triggered.connect(open_action_function)
file_menu.addAction(otworz_action)

zapisz_action = QAction("Save", window)
zapisz_action.triggered.connect(save_action_function)
file_menu.addAction(zapisz_action)

export_action = QAction("Export", window)
file_menu.addAction(export_action)

debug_action = QAction("Debug", window)
debug_action.triggered.connect(debug_action_function)
file_menu.addAction(debug_action)

window.show()

sys.exit(app.exec_())