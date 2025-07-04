from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QScrollArea,
    QCheckBox,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QAction,
    QHBoxLayout,
)

from models import Character, DEFAULT_SKILLS, Skill
from storage import load_character, save_character


class BasicInfoTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.fields: dict[str, QLineEdit] = {}
        layout = QFormLayout(self)
        for label in [
            "Name",
            "Homeworld",
            "Background",
            "Role",
            "Divination",
            "Gender",
            "Height",
            "Weight",
            "Age",
            "Build",
            "Hair",
            "Eyes",
            "Aura",
        ]:
            line = QLineEdit()
            layout.addRow(label + ":", line)
            self.fields[label] = line

    def load_character(self, char: Character):
        self.fields["Name"].setText(char.name)
        self.fields["Homeworld"].setText(char.homeworld)
        self.fields["Background"].setText(char.background)
        self.fields["Role"].setText(char.role)
        self.fields["Divination"].setText(char.divination)
        self.fields["Gender"].setText(char.gender)
        self.fields["Height"].setText(char.height)
        self.fields["Weight"].setText(char.weight)
        self.fields["Age"].setText(char.age)
        self.fields["Build"].setText(char.build)
        self.fields["Hair"].setText(char.hair)
        self.fields["Eyes"].setText(char.eyes)
        self.fields["Aura"].setText(char.aura)

    def update_character(self, char: Character):
        char.name = self.fields["Name"].text()
        char.homeworld = self.fields["Homeworld"].text()
        char.background = self.fields["Background"].text()
        char.role = self.fields["Role"].text()
        char.divination = self.fields["Divination"].text()
        char.gender = self.fields["Gender"].text()
        char.height = self.fields["Height"].text()
        char.weight = self.fields["Weight"].text()
        char.age = self.fields["Age"].text()
        char.build = self.fields["Build"].text()
        char.hair = self.fields["Hair"].text()
        char.eyes = self.fields["Eyes"].text()
        char.aura = self.fields["Aura"].text()


class AttributesTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.spinboxes: dict[str, QSpinBox] = {}
        form = QFormLayout(self)
        for attr_label in ["WS", "BS", "S", "T", "Ag", "Int", "Per", "WP", "Fel"]:
            spin = QSpinBox()
            spin.setRange(0, 100)
            form.addRow(f"{attr_label}:", spin)
            self.spinboxes[attr_label] = spin

    def load_character(self, char: Character):
        self.spinboxes["WS"].setValue(char.attributes.ws)
        self.spinboxes["BS"].setValue(char.attributes.bs)
        self.spinboxes["S"].setValue(char.attributes.s)
        self.spinboxes["T"].setValue(char.attributes.t)
        self.spinboxes["Ag"].setValue(char.attributes.ag)
        self.spinboxes["Int"].setValue(char.attributes.int_)
        self.spinboxes["Per"].setValue(char.attributes.per)
        self.spinboxes["WP"].setValue(char.attributes.wp)
        self.spinboxes["Fel"].setValue(char.attributes.fel)

    def update_character(self, char: Character):
        char.attributes.ws = self.spinboxes["WS"].value()
        char.attributes.bs = self.spinboxes["BS"].value()
        char.attributes.s = self.spinboxes["S"].value()
        char.attributes.t = self.spinboxes["T"].value()
        char.attributes.ag = self.spinboxes["Ag"].value()
        char.attributes.int_ = self.spinboxes["Int"].value()
        char.attributes.per = self.spinboxes["Per"].value()
        char.attributes.wp = self.spinboxes["WP"].value()
        char.attributes.fel = self.spinboxes["Fel"].value()


class SkillsTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.widgets: dict[str, tuple[QCheckBox, QSpinBox]] = {}

        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        form = QFormLayout(inner)

        for skill in DEFAULT_SKILLS:
            cb = QCheckBox("Trained")
            spin = QSpinBox()
            spin.setRange(0, 5)  # ranks/advancements
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.addWidget(cb)
            row_layout.addWidget(spin)
            form.addRow(skill + ":", row_widget)
            self.widgets[skill] = (cb, spin)

        scroll.setWidget(inner)
        layout.addWidget(scroll)

    def load_character(self, char: Character):
        for skill, (cb, spin) in self.widgets.items():
            skl = char.skills.get(skill)
            if skl:
                cb.setChecked(skl.trained)
                spin.setValue(skl.rank)
            else:
                cb.setChecked(False)
                spin.setValue(0)

    def update_character(self, char: Character):
        for skill, (cb, spin) in self.widgets.items():
            char.skills[skill] = char.skills.get(skill) or Skill()
            char.skills[skill].trained = cb.isChecked()
            char.skills[skill].rank = spin.value()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark Heresy Character Sheet Manager")
        self.resize(800, 600)

        self.character = Character()
        self.current_file: Path | None = None

        # Tabs
        self.tabs = QTabWidget()
        self.basic_tab = BasicInfoTab()
        self.attr_tab = AttributesTab()
        self.skills_tab = SkillsTab()
        self.tabs.addTab(self.basic_tab, "Basic Info")
        self.tabs.addTab(self.attr_tab, "Attributes")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.setCentralWidget(self.tabs)

        # Menu
        self._create_menu()
        self.update_ui_from_character()

    # ------------------ Menu ----------------------
    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_act = QAction("New", self)
        new_act.triggered.connect(self.action_new)
        file_menu.addAction(new_act)

        open_act = QAction("Open...", self)
        open_act.triggered.connect(self.action_open)
        file_menu.addAction(open_act)

        save_act = QAction("Save", self)
        save_act.triggered.connect(self.action_save)
        file_menu.addAction(save_act)

        save_as_act = QAction("Save As...", self)
        save_as_act.triggered.connect(self.action_save_as)
        file_menu.addAction(save_as_act)

        file_menu.addSeparator()
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

    # ----------------- Actions --------------------
    def action_new(self):
        if self.maybe_save_changes():
            self.character = Character()
            self.current_file = None
            self.update_ui_from_character()

    def action_open(self):
        if not self.maybe_save_changes():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Character", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.character = load_character(path)
            self.current_file = Path(path)
            self.update_ui_from_character()

    def action_save(self):
        if self.current_file is None:
            self.action_save_as()
        else:
            self.update_character_from_ui()
            save_character(self.character, self.current_file)
            QMessageBox.information(self, "Saved", f"Character saved to {self.current_file}")

    def action_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character As", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.current_file = Path(path)
            self.update_character_from_ui()
            save_character(self.character, self.current_file)
            QMessageBox.information(self, "Saved", f"Character saved to {self.current_file}")

    # --------------- Helper methods ----------------
    def update_ui_from_character(self):
        self.basic_tab.load_character(self.character)
        self.attr_tab.load_character(self.character)
        self.skills_tab.load_character(self.character)

    def update_character_from_ui(self):
        self.basic_tab.update_character(self.character)
        self.attr_tab.update_character(self.character)
        self.skills_tab.update_character(self.character)

    def maybe_save_changes(self) -> bool:
        if self.current_file is None:
            return True  # nothing saved yet
        # For simplicity, always prompt to save. Could implement change tracking.
        ret = QMessageBox.question(
            self,
            "Save Changes?",
            "Save changes before continuing?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
        )
        if ret == QMessageBox.StandardButton.Yes:
            self.action_save()
            return True
        elif ret == QMessageBox.StandardButton.No:
            return True
        else:
            return False


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()