from PyQt5 import QtCore, QtGui, QtWidgets

from as64_common import resource_utils
from as64_core import config
from as64_ui.widgets import HLine
from as64_ui.constants import (
    ICON_PATH
)


class SettingsDialog(QtWidgets.QDialog):
    applied = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowCloseButtonHint)

        self.window_title = "Settings"
        self.setWindowIcon(QtGui.QIcon(resource_utils.resource_path(ICON_PATH)))

        # Layouts
        self.main_layout = QtWidgets.QHBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.apply_cancel_layout = QtWidgets.QHBoxLayout()

        # Widgets
        self.right_widget = QtWidgets.QWidget()
        self.apply_cancel_widget = QtWidgets.QWidget()
        self.menu_list = QtWidgets.QListWidget()
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.stacked_widget = QtWidgets.QStackedWidget()

        self.general_menu = GeneralMenu()
        self.connection_menu = ConnectionMenu()
        self.thresholds_menu = ThresholdsMenu()
        self.error_menu = ErrorCorrectionMenu()
        self.adv_menu = AdvancedMenu()

        self.initialize()

    def initialize(self):
        self.setWindowTitle(self.window_title)
        self.resize(650, 400)

        # Set Layouts
        self.setLayout(self.main_layout)
        self.right_widget.setLayout(self.right_layout)
        self.apply_cancel_widget.setLayout(self.apply_cancel_layout)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

        # Configure Widgets
        self.menu_list.setMinimumWidth(80)
        self.menu_list.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.menu_list.addItems(["General", "Connection", "Thresholds", "Error Correction", "Advanced"])
        self.menu_list.setSpacing(8)

        self.stacked_widget.addWidget(self.general_menu)
        self.stacked_widget.addWidget(self.connection_menu)
        self.stacked_widget.addWidget(self.thresholds_menu)
        self.stacked_widget.addWidget(self.error_menu)
        self.stacked_widget.addWidget(self.adv_menu)

        self.stacked_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add Widgets
        self.apply_cancel_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.apply_cancel_layout.addWidget(self.apply_btn)
        self.apply_cancel_layout.addWidget(self.cancel_btn)

        self.right_layout.addWidget(self.stacked_widget)
        self.right_layout.addWidget(HLine())
        self.right_layout.addWidget(self.apply_cancel_widget)

        self.main_layout.addWidget(self.menu_list, 33)
        self.main_layout.addWidget(self.right_widget, 66)

        # Connections
        self.menu_list.currentRowChanged.connect(self.display_at)
        self.apply_btn.clicked.connect(self.apply_clicked)
        self.cancel_btn.clicked.connect(self.cancel_clicked)

    def show(self):
        super().show()

    def apply_clicked(self):
        # Update and save preferences
        self.general_menu.update_preferences()
        self.connection_menu.update_preferences()
        self.thresholds_menu.update_preferences()
        self.error_menu.update_preferences()
        self.adv_menu.update_preferences()
        config.save_config()
        self.hide()

        self.applied.emit()

    def cancel_clicked(self):
        self.hide()

    def display_at(self, index):
        self.stacked_widget.setCurrentIndex(index)


class BaseMenu(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.title = title

        # Layouts
        self.primary_layout = QtWidgets.QVBoxLayout()

        # Widgets
        self.title_label = QtWidgets.QLabel(self.title)
        self.menu_frame = QtWidgets.QFrame()
        self.title_line = QtWidgets.QFrame()

        # Font
        self.title_font = QtGui.QFont()
        self.title_font.setPointSize(12)

        self.initialize()

    def initialize(self):
        # Set Layout
        self.setLayout(self.primary_layout)

        # Configure Widgets
        self.title_label.setFont(self.title_font)
        self.title_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.title_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.title_line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.menu_frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add Widgets
        self.primary_layout.addWidget(self.title_label)
        self.primary_layout.addWidget(self.title_line)
        self.primary_layout.addWidget(self.menu_frame)

    def set_menu_layout(self, layout):
        self.menu_frame.setLayout(layout)


class GeneralMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(title="General", parent=parent)

        # Layouts
        self.menu_layout = QtWidgets.QGridLayout()

        # Widgets
        self.override_ver_lb = QtWidgets.QLabel("Override Game Version:")
        self.override_ver_cb = QtWidgets.QCheckBox()
        self.override_ver_combo = QtWidgets.QComboBox()

        self.init()

    def init(self):
        # Set Layout
        self.set_menu_layout(self.menu_layout)

        # Configure Widgets
        self.override_ver_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.override_ver_lb.setMaximumWidth(120)
        self.override_ver_cb.setMaximumWidth(20)
        self.override_ver_combo.setMaximumWidth(120)

        self.override_ver_combo.addItems(["JP", "US"])

        # Add Widgets
        self.menu_layout.addWidget(self.override_ver_lb, 0, 0)
        self.menu_layout.addWidget(self.override_ver_cb, 0, 1)
        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 0, 2)
        self.menu_layout.addWidget(self.override_ver_combo, 1, 1)

        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 2, 0)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 10, 0)

        # Connections
        self.override_ver_cb.clicked.connect(self.override_clicked)

        self.load_preferences()

    def override_clicked(self, checked):
        self.override_ver_combo.setDisabled(not checked)

    def load_preferences(self):
        self.override_ver_cb.setChecked(config.get("game", "override_version"))

        if config.get("game", "version") == "US":
            self.override_ver_combo.setCurrentIndex(1)
        else:
            self.override_ver_combo.setCurrentIndex(0)

        self.override_ver_combo.setDisabled(not self.override_ver_cb.isChecked())

    def update_preferences(self):
        config.set_key("game", "override_version", self.override_ver_cb.isChecked())
        config.set_key("game", "version", self.override_ver_combo.itemText(self.override_ver_combo.currentIndex()))


class ThresholdsMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(title="Thresholds", parent=parent)

        # Layouts
        self.menu_layout = QtWidgets.QGridLayout()

        # Widgets
        self.prob_lb = QtWidgets.QLabel("Probability Threshold:")
        self.prob_le = QtWidgets.QLineEdit("")
        self.reset_lb = QtWidgets.QLabel("Reset Threshold:")
        self.reset_le = QtWidgets.QLineEdit("")
        self.confirmation_lb = QtWidgets.QLabel("Confirmation Threshold:")
        self.confirmation_le = QtWidgets.QLineEdit("")

        self.black_lb = QtWidgets.QLabel("Black Threshold:")
        self.black_le = QtWidgets.QLineEdit("")
        self.white_lb = QtWidgets.QLabel("White Threshold:")
        self.white_le = QtWidgets.QLineEdit("")

        self.double_validator = QtGui.QDoubleValidator(0, 1, 3)
        self.double_validator.setRange(0, 1, 3)

        self.init()

    def init(self):
        # Set Layout
        self.set_menu_layout(self.menu_layout)

        # Configure Widgets
        self.prob_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.reset_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.confirmation_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.black_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.prob_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.reset_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.confirmation_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.white_lb.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.black_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.white_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        # Add Widgets
        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 4, 0)

        self.menu_layout.addWidget(self.prob_lb, 5, 0)
        self.menu_layout.addWidget(self.prob_le, 5, 1)
        self.menu_layout.addWidget(self.reset_lb, 5, 2)
        self.menu_layout.addWidget(self.reset_le, 5, 3)
        self.menu_layout.addWidget(self.confirmation_lb, 6, 0)
        self.menu_layout.addWidget(self.confirmation_le, 6, 1)

        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 7, 0)

        self.menu_layout.addWidget(HLine(), 8, 0, 1, 4)

        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 9, 0)

        self.menu_layout.addWidget(self.black_lb, 10, 0)
        self.menu_layout.addWidget(self.black_le, 10, 1)
        self.menu_layout.addWidget(self.white_lb, 10, 2)
        self.menu_layout.addWidget(self.white_le, 10, 3)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 15, 0)

        self.prob_le.setValidator(self.double_validator)
        self.reset_le.setValidator(self.double_validator)
        self.confirmation_le.setValidator(self.double_validator)
        self.black_le.setValidator(self.double_validator)
        self.white_le.setValidator(self.double_validator)

        self.load_preferences()

    def load_preferences(self):
        self.prob_le.setText(str(config.get('thresholds', 'probability_threshold')))
        self.reset_le.setText(str(config.get('thresholds', 'reset_threshold')))
        self.confirmation_le.setText(str(config.get('thresholds', 'confirmation_threshold')))

        self.black_le.setText(str(config.get('thresholds', 'black_threshold')))
        self.white_le.setText(str(config.get('thresholds', 'white_threshold')))

    def update_preferences(self):
        config.set_key('thresholds', 'probability_threshold', float(self.prob_le.text()))
        config.set_key('thresholds', 'reset_threshold', float(self.reset_le.text()))
        config.set_key('thresholds', 'confirmation_threshold', float(self.confirmation_le.text()))

        config.set_key('thresholds', 'black_threshold', float(self.black_le.text()))
        config.set_key('thresholds', 'white_threshold', float(self.white_le.text()))


class ConnectionMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(title="Connection", parent=parent)

        # Layouts
        self.menu_layout = QtWidgets.QGridLayout()

        # Widgets
        self.host_lb = QtWidgets.QLabel("LiveSplit Host:")
        self.host_le = QtWidgets.QLineEdit("")
        self.port_lb = QtWidgets.QLabel("LiveSplit Port:")
        self.port_le = QtWidgets.QLineEdit("")

        self.int_validator = QtGui.QIntValidator()

        self.init()

    def init(self):
        # Set Layout
        self.set_menu_layout(self.menu_layout)

        # Configure Widgets
        self.host_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.port_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.host_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.port_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.host_le.setMaximumWidth(150)
        self.port_le.setMaximumWidth(150)

        # Add Widgets
        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 4, 0)

        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 5, 2)
        self.menu_layout.addWidget(self.host_lb, 5, 0)
        self.menu_layout.addWidget(self.host_le, 5, 1)
        self.menu_layout.addWidget(self.port_lb, 6, 0)
        self.menu_layout.addWidget(self.port_le, 6, 1)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 15, 0)

        self.port_le.setValidator(self.int_validator)

        self.load_preferences()

    def load_preferences(self):
        self.host_le.setText(str(config.get('connection', 'ls_host')))
        self.port_le.setText(str(config.get('connection', 'ls_port')))

    def update_preferences(self):
        config.set_key('connection', 'ls_host', self.host_le.text())
        config.set_key('connection', 'ls_port', int(self.port_le.text()))


class ErrorCorrectionMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(title="Error Correction", parent=parent)

        # Layouts
        self.menu_layout = QtWidgets.QGridLayout()

        # Widgets
        self.processing_lb = QtWidgets.QLabel("Processing Length:")
        self.processing_le = QtWidgets.QLineEdit("")
        self.undo_count_lb = QtWidgets.QLabel("Undo Minimum Length:")
        self.undo_count_le = QtWidgets.QLineEdit("")

        self.undo_threshold_lb = QtWidgets.QLabel("Undo Average Threshold:")
        self.undo_threshold_le = QtWidgets.QLineEdit("")

        self.double_validator = QtGui.QDoubleValidator(0, 1, 3)
        self.double_validator.setRange(0, 1, 3)
        self.int_validator = QtGui.QIntValidator()

        self.init()

    def init(self):
        # Set Layout
        self.set_menu_layout(self.menu_layout)

        # Configure Widgets
        self.processing_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.undo_count_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.undo_threshold_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.processing_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.undo_count_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.undo_threshold_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.processing_le.setMaximumWidth(50)
        self.undo_count_le.setMaximumWidth(50)
        self.undo_threshold_le.setMaximumWidth(50)

        # Add Widgets
        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 4, 0)

        self.menu_layout.addItem(
            QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 5, 2)
        self.menu_layout.addWidget(self.processing_lb, 5, 0)
        self.menu_layout.addWidget(self.processing_le, 5, 1)
        self.menu_layout.addWidget(self.undo_count_lb, 6, 0)
        self.menu_layout.addWidget(self.undo_count_le, 6, 1)
        self.menu_layout.addWidget(self.undo_threshold_lb, 7, 0)
        self.menu_layout.addWidget(self.undo_threshold_le, 7, 1)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 15, 0)

        self.processing_le.setValidator(self.int_validator)
        self.undo_count_le.setValidator(self.int_validator)
        self.undo_threshold_le.setValidator(self.double_validator)

        self.load_preferences()

    def load_preferences(self):
        self.processing_le.setText(str(config.get('error', 'processing_length')))
        self.undo_count_le.setText(str(config.get('error', 'minimum_undo_count')))
        self.undo_threshold_le.setText(str(config.get('error', 'undo_threshold')))

    def update_preferences(self):
        config.set_key('error', 'processing_length', int(self.processing_le.text()))
        config.set_key('error', 'minimum_undo_count', int(self.undo_count_le.text()))
        config.set_key('error', 'undo_threshold', float(self.undo_threshold_le.text()))


class AdvancedMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(title="Advanced", parent=parent)

        # Layouts
        self.menu_layout = QtWidgets.QGridLayout()

        # Widgets
        self.reset_one_lb = QtWidgets.QLabel("Reset Frame One:")
        self.reset_one_le = QtWidgets.QLineEdit("")
        self.reset_one_btn = QtWidgets.QPushButton("Browse")

        self.reset_two_lb = QtWidgets.QLabel("Reset Frame Two:")
        self.reset_two_le = QtWidgets.QLineEdit("")
        self.reset_two_btn = QtWidgets.QPushButton("Browse")

        self.restart_delay_lb = QtWidgets.QLabel("Restart Split Delay:")
        self.restart_delay_le = QtWidgets.QLineEdit("")

        self.star_delay_lb = QtWidgets.QLabel("Star Frame Rate:")
        self.star_delay_le = QtWidgets.QLineEdit("")

        self.fadeout_delay_lb = QtWidgets.QLabel("Fadeout Frame Rate:")
        self.fadeout_delay_le = QtWidgets.QLineEdit("")

        self.model_lb = QtWidgets.QLabel("Detection Model:")
        self.model_le = QtWidgets.QLineEdit("")
        self.model_btn = QtWidgets.QPushButton("Browse")

        self.model_width_lb = QtWidgets.QLabel("Model Width:")
        self.model_width_le = QtWidgets.QLineEdit()
        self.model_height_lb = QtWidgets.QLabel("Model Height:")
        self.model_height_le = QtWidgets.QLineEdit()

        self.int_validator = QtGui.QIntValidator()

        self.int_validator = QtGui.QIntValidator()
        self.double_validator = QtGui.QDoubleValidator()

        self.init()

    def init(self):
        # Set Layout
        self.set_menu_layout(self.menu_layout)

        # Configure Widgets
        self.restart_delay_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.reset_one_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.reset_two_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.star_delay_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.fadeout_delay_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.restart_delay_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.reset_one_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.reset_two_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.star_delay_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.fadeout_delay_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.restart_delay_le.setMaximumWidth(50)
        self.star_delay_le.setMaximumWidth(50)
        self.fadeout_delay_le.setMaximumWidth(50)

        self.restart_delay_le.setValidator(self.double_validator)
        self.star_delay_le.setValidator(self.double_validator)
        self.fadeout_delay_le.setValidator(self.double_validator)

        # configure model section
        self.model_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.model_width_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.model_height_lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.model_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.model_width_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.model_height_le.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.model_width_le.setValidator(self.int_validator)
        self.model_height_le.setValidator(self.int_validator)

        # Add Widgets
        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 4, 0)

        self.menu_layout.addWidget(self.restart_delay_lb, 5, 0)
        self.menu_layout.addWidget(self.restart_delay_le, 5, 1, 1, 2)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 7, 0)
        self.menu_layout.addWidget(HLine(), 8, 0, 1, 4)
        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 9, 0)

        self.menu_layout.addWidget(self.reset_one_lb, 18, 0)
        self.menu_layout.addWidget(self.reset_one_le, 18, 1, 1, 3)
        self.menu_layout.addWidget(self.reset_one_btn, 18, 4)

        self.menu_layout.addWidget(self.reset_two_lb, 19, 0)
        self.menu_layout.addWidget(self.reset_two_le, 19, 1, 1, 3)
        self.menu_layout.addWidget(self.reset_two_btn, 19, 4)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 20, 0)
        self.menu_layout.addWidget(HLine(), 21, 0, 1, 4)
        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 22, 0)

        self.menu_layout.addWidget(self.star_delay_lb, 23, 0)
        self.menu_layout.addWidget(self.star_delay_le, 23, 1)

        self.menu_layout.addWidget(self.fadeout_delay_lb, 24, 0)
        self.menu_layout.addWidget(self.fadeout_delay_le, 24, 1)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 25, 0)
        self.menu_layout.addWidget(HLine(), 26, 0, 1, 4)
        self.menu_layout.addItem(QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum), 27, 0)

        self.menu_layout.addWidget(self.model_lb, 28, 0)
        self.menu_layout.addWidget(self.model_le, 28, 1, 1, 3)
        self.menu_layout.addWidget(self.model_btn, 28, 4)

        self.menu_layout.addWidget(self.model_width_lb, 29, 0)
        self.menu_layout.addWidget(self.model_width_le, 29, 1)
        self.menu_layout.addWidget(self.model_height_lb, 29, 2)
        self.menu_layout.addWidget(self.model_height_le, 29, 3)

        self.menu_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 30, 0)

        # Connections
        self.reset_one_btn.clicked.connect(self.open_reset_one)
        self.reset_two_btn.clicked.connect(self.open_reset_two)
        self.model_btn.clicked.connect(self.open_model_dialog)

        self.load_preferences()

    def load_preferences(self):
        self.restart_delay_le.setText(str(config.get('advanced', 'restart_split_delay')))
        self.reset_one_le.setText(str(config.get('advanced', 'reset_frame_one')))
        self.reset_two_le.setText(str(config.get('advanced', 'reset_frame_two')))
        self.star_delay_le.setText(str(config.get('advanced', 'star_process_frame_rate')))
        self.fadeout_delay_le.setText(str(config.get('advanced', 'fadeout_process_frame_rate')))
        self.model_le.setText(config.get('model', 'path'))
        self.model_width_le.setText(str(config.get('model', 'width')))
        self.model_height_le.setText(str(config.get('model', 'height')))

    def update_preferences(self):
        config.set_key('advanced', 'restart_split_delay', float(self.restart_delay_le.text()))
        config.set_key('advanced', 'reset_frame_one', resource_utils.abs_to_rel(self.reset_one_le.text()))
        config.set_key('advanced', 'reset_frame_two', resource_utils.abs_to_rel(self.reset_two_le.text()))
        config.set_key('advanced', 'star_process_frame_rate', float(self.star_delay_le.text()))
        config.set_key('advanced', 'fadeout_process_frame_rate', float(self.fadeout_delay_le.text()))
        config.set_key('model', 'path', self.model_le.text())
        config.set_key('model', 'width', int(self.model_width_le.text()))
        config.set_key('model', 'height', int(self.model_height_le.text()))

    def open_reset_one(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Reset Frame One", "")

        if file_name:
            self.reset_one_le.setText(file_name)

    def open_reset_two(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Reset Frame Two", "")

        if file_name:
            self.reset_two_le.setText(file_name)

    def open_model_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Detection Model", "", "Model (*.hdf5)")

        if file_name:
            self.model_le.setText(file_name)
