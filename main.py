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
    QListWidget,
    QPushButton,
    QInputDialog,
    QLabel,
)

from models import Character, DEFAULT_SKILLS, Skill, PsychicPower
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


# ------------------ New Tabs --------------------


class WoundsTab(QWidget):
    """Handles wounds, fatigue and movement speeds."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.spins: dict[str, QSpinBox] = {}
        form = QFormLayout(self)

        # Wounds / Fatigue
        for label in ["Current Wounds", "Max Wounds", "Fatigue"]:
            spin = QSpinBox()
            spin.setRange(0, 100)
            form.addRow(label + ":", spin)
            self.spins[label] = spin

        form.addRow(QLabel("<b>Movement</b>"))

        for mv_label in ["Half", "Full", "Charge", "Run"]:
            spin = QSpinBox()
            spin.setRange(0, 99)
            form.addRow(mv_label + ":", spin)
            self.spins[mv_label] = spin

    # Mapping keys
    _w_map = {
        "Current Wounds": "current",
        "Max Wounds": "max",
        "Fatigue": "fatigue",
    }

    _m_map = {
        "Half": "half",
        "Full": "full",
        "Charge": "charge",
        "Run": "run",
    }

    def load_character(self, char: Character):
        # Wounds
        for gui_label, attr in self._w_map.items():
            self.spins[gui_label].setValue(getattr(char.wounds, attr))

        for gui_label, attr in self._m_map.items():
            self.spins[gui_label].setValue(getattr(char.movement, attr))

    def update_character(self, char: Character):
        for gui_label, attr in self._w_map.items():
            setattr(char.wounds, attr, self.spins[gui_label].value())

        for gui_label, attr in self._m_map.items():
            setattr(char.movement, attr, self.spins[gui_label].value())


class ExperienceTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.total_sp = QSpinBox()
        self.spent_sp = QSpinBox()
        self.remaining_lbl = QLabel("0")

        for sp in (self.total_sp, self.spent_sp):
            sp.setRange(0, 100000)

        form = QFormLayout(self)
        form.addRow("Total XP:", self.total_sp)
        form.addRow("Spent XP:", self.spent_sp)
        form.addRow("Remaining XP:", self.remaining_lbl)

        # Update remaining when values change
        self.total_sp.valueChanged.connect(self._update_remaining)
        self.spent_sp.valueChanged.connect(self._update_remaining)

    def _update_remaining(self):
        remaining = max(0, self.total_sp.value() - self.spent_sp.value())
        self.remaining_lbl.setText(str(remaining))

    def load_character(self, char: Character):
        self.total_sp.setValue(char.experience.total)
        self.spent_sp.setValue(char.experience.spent)
        self._update_remaining()

    def update_character(self, char: Character):
        char.experience.total = self.total_sp.value()
        char.experience.spent = self.spent_sp.value()


class _ListEditTab(QWidget):
    """Utility base class for list-of-strings editing."""

    def __init__(self, title: str, items: list[str], parent: QWidget | None = None):
        super().__init__(parent)
        self._title = title
        self.list_widget = QListWidget()
        self.list_widget.addItems(items)

        add_btn = QPushButton("Add")
        remove_btn = QPushButton("Remove")

        add_btn.clicked.connect(self.add_item)
        remove_btn.clicked.connect(self.remove_selected)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)

    def add_item(self):
        text, ok = QInputDialog.getText(self, f"Add {self._title}", f"{self._title}:")
        if ok and text.strip():
            self.list_widget.addItem(text.strip())

    def remove_selected(self):
        for item in self.list_widget.selectedItems():
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)

    # subclasses implement load & update


class TalentsTab(_ListEditTab):
    def __init__(self, parent: QWidget | None = None):
        super().__init__("Talent", [], parent)

    def load_character(self, char: Character):
        self.list_widget.clear()
        self.list_widget.addItems(char.talents)

    def update_character(self, char: Character):
        char.talents = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]


class GearTab(_ListEditTab):
    def __init__(self, parent: QWidget | None = None):
        super().__init__("Gear", [], parent)

    def load_character(self, char: Character):
        self.list_widget.clear()
        self.list_widget.addItems(char.gear)

    def update_character(self, char: Character):
        char.gear = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]


# ---------------- Additional Tabs ----------------


class ArmourTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.spins: dict[str, QSpinBox] = {}
        form = QFormLayout(self)
        for part in ["Head", "Arms", "Body", "Legs"]:
            spin = QSpinBox()
            spin.setRange(0, 20)
            form.addRow(part + " AP:", spin)
            self.spins[part] = spin

    def load_character(self, char: Character):
        self.spins["Head"].setValue(char.armour.head)
        self.spins["Arms"].setValue(char.armour.arms)
        self.spins["Body"].setValue(char.armour.body)
        self.spins["Legs"].setValue(char.armour.legs)

    def update_character(self, char: Character):
        char.armour.head = self.spins["Head"].value()
        char.armour.arms = self.spins["Arms"].value()
        char.armour.body = self.spins["Body"].value()
        char.armour.legs = self.spins["Legs"].value()


class PsykerTab(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        rating_layout = QFormLayout()
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(0, 10)
        rating_layout.addRow("Psy Rating:", self.rating_spin)
        layout.addLayout(rating_layout)

        self.powers_tab = _ListEditTab("Power", [])
        layout.addWidget(self.powers_tab)

    def load_character(self, char: Character):
        self.rating_spin.setValue(char.psy_rating)
        self.powers_tab.list_widget.clear()
        self.powers_tab.list_widget.addItems([p.name for p in char.psychic_powers])

    def update_character(self, char: Character):
        char.psy_rating = self.rating_spin.value()
        char.psychic_powers = [PsychicPower(name=self.powers_tab.list_widget.item(i).text()) for i in range(self.powers_tab.list_widget.count())]


class StatusTab(QWidget):
    """Corruption, Insanity, Mutations, Disorders"""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.corr_spin = QSpinBox(); self.corr_spin.setRange(0, 100)
        self.ins_spin = QSpinBox(); self.ins_spin.setRange(0, 100)
        form.addRow("Corruption:", self.corr_spin)
        form.addRow("Insanity:", self.ins_spin)
        layout.addLayout(form)

        self.mutations_tab = _ListEditTab("Mutation", [])
        self.disorders_tab = _ListEditTab("Disorder", [])

        layout.addWidget(QLabel("Mutations:"))
        layout.addWidget(self.mutations_tab)
        layout.addWidget(QLabel("Disorders:"))
        layout.addWidget(self.disorders_tab)

    def load_character(self, char: Character):
        self.corr_spin.setValue(char.corruption)
        self.ins_spin.setValue(char.insanity)

        self.mutations_tab.list_widget.clear()
        self.mutations_tab.list_widget.addItems(char.mutations)

        self.disorders_tab.list_widget.clear()
        self.disorders_tab.list_widget.addItems(char.disorders)

    def update_character(self, char: Character):
        char.corruption = self.corr_spin.value()
        char.insanity = self.ins_spin.value()
        char.mutations = [self.mutations_tab.list_widget.item(i).text() for i in range(self.mutations_tab.list_widget.count())]
        char.disorders = [self.disorders_tab.list_widget.item(i).text() for i in range(self.disorders_tab.list_widget.count())]


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
        self.wounds_tab = WoundsTab()
        self.experience_tab = ExperienceTab()
        self.talents_tab = TalentsTab()
        self.gear_tab = GearTab()
        self.armour_tab = ArmourTab()
        self.psyker_tab = PsykerTab()
        self.status_tab = StatusTab()

        self.tabs.addTab(self.basic_tab, "Basic Info")
        self.tabs.addTab(self.attr_tab, "Attributes")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.wounds_tab, "Wounds & Movement")
        self.tabs.addTab(self.experience_tab, "Experience")
        self.tabs.addTab(self.talents_tab, "Talents")
        self.tabs.addTab(self.gear_tab, "Gear")
        self.tabs.addTab(self.armour_tab, "Armour")
        self.tabs.addTab(self.psyker_tab, "Psyker")
        self.tabs.addTab(self.status_tab, "Status")
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
        self.wounds_tab.load_character(self.character)
        self.experience_tab.load_character(self.character)
        self.talents_tab.load_character(self.character)
        self.gear_tab.load_character(self.character)
        self.armour_tab.load_character(self.character)
        self.psyker_tab.load_character(self.character)
        self.status_tab.load_character(self.character)

    def update_character_from_ui(self):
        self.basic_tab.update_character(self.character)
        self.attr_tab.update_character(self.character)
        self.skills_tab.update_character(self.character)
        self.wounds_tab.update_character(self.character)
        self.experience_tab.update_character(self.character)
        self.talents_tab.update_character(self.character)
        self.gear_tab.update_character(self.character)
        self.armour_tab.update_character(self.character)
        self.psyker_tab.update_character(self.character)
        self.status_tab.update_character(self.character)

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