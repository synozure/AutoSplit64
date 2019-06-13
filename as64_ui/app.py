import os
from functools import partial
import re

from PyQt5 import QtCore, QtGui, QtWidgets

from as64_core import route_loader, config
from as64_common.resource_utils import base_path, resource_path, absolute_path, rel_to_abs
from . import constants
from .widgets import PictureButton, StateButton, StarCountDisplay, SplitListWidget
from .dialogs import AboutDialog, CaptureEditor, SettingsDialog, RouteEditor, ResetGeneratorDialog


class App(QtWidgets.QMainWindow):
    start = QtCore.pyqtSignal()
    stop = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Window Properties
        self.title = constants.TITLE
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.width = 365
        self.height = 259
        self.setWindowIcon(QtGui.QIcon(base_path(constants.ICON_PATH)))

        # Dragging
        self._drag = False
        self._drag_position = None

        # Pixmaps
        self.start_pixmap = QtGui.QPixmap(base_path(constants.START_PATH))
        self.stop_pixmap = QtGui.QPixmap(base_path(constants.STOP_PATH))
        self.init_pixmap = QtGui.QPixmap(base_path(constants.INIT_PATH))

        # Widgets
        self.central_widget = QtWidgets.QWidget(self)
        self.star_count = StarCountDisplay(parent=self.central_widget)
        self.start_btn = StateButton(self.start_pixmap, self.start_pixmap, parent=self.central_widget)
        self.close_btn = PictureButton(QtGui.QPixmap(base_path(constants.CLOSE_PATH)), parent=self.central_widget)
        self.minimize_btn = PictureButton(QtGui.QPixmap(base_path(constants.MINIMIZE_PATH)), parent=self.central_widget)
        self.split_list = SplitListWidget(self.central_widget)

        # Font
        self.button_font = QtGui.QFont("Tw Cen MT", 14)
        self.start_count_font = QtGui.QFont("Tw Cen MT", 20)

        # Route
        self.route = None

        # Dialogs
        self.dialogs = {
            "about_dialog": AboutDialog(self),
            "capture_editor": CaptureEditor(self),
            "settings_dialog": SettingsDialog(self),
            "route_editor": RouteEditor(self),
            "reset_dialog": ResetGeneratorDialog(self)
        }

        self._routes = {}
        self._load_route_dir()

        self.initialize()
        self.show()

    def initialize(self):
        # Configure window
        self.setWindowTitle(self.title)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(self.width, self.height)

        # Configure Central Widget
        self.central_widget.setObjectName("central_widget")

        self.central_widget.setStyleSheet(r"QWidget#central_widget{background-image: url(" +
                                          resource_path(constants.BACKGROUND_PATH) +
                                          "); background-attachment: fixed;}")
        self.setCentralWidget(self.central_widget)

        # Configure Other Widgets
        self.close_btn.move(340, 8)
        self.minimize_btn.move(320, 8)

        self.star_count.setFixedWidth(150)
        self.star_count.move(197, 115)
        self.star_count.setFont(self.start_count_font)
        self.star_count.star_count = "-"
        self.star_count.split_star = "-"

        self.start_btn.move(206, 200)
        self.start_btn.setFont(self.button_font)
        self.start_btn.setTextColour(QtGui.QColor(225, 227, 230))
        self.start_btn.add_state("start", self.start_pixmap, "Start")
        self.start_btn.add_state("stop", self.stop_pixmap, "Stop")
        self.start_btn.add_state("init", self.init_pixmap, "Initializing..")
        self.start_btn.set_state("start")

        self.split_list.setFont(self.button_font)
        self.split_list.setFixedSize(183, self.height)
        self.split_list.move(0, 0)

        self.open_route()

        # Connections
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.start_btn.clicked.connect(self.start_clicked)
        self.dialogs["route_editor"].route_updated.connect(self._on_route_update)

    def update_display(self, split_index, current_star, split_star):
        if split_index > len(self.split_list.splits) - 1:
            index = len(self.split_list.splits) - 1
        else:
            index = split_index

        self.split_list.set_selected_index(index)
        self.star_count.star_count = current_star
        self.star_count.split_star = split_star

    def start_clicked(self):
        if self.start_btn.get_state() == "stop":
            self.start_btn.set_state("start")
            self.split_list.set_selected_index(0)
            self.star_count.star_count = self.route.initial_star
            self.star_count.split_star = self.route.splits[0].star_count
            self.stop.emit()
        elif self.start_btn.get_state() == "start":
            self.start_btn.set_state("init")
            self.start.emit()

    def set_started(self, started):
        if started:
            self.start_btn.set_state("stop")
        else:
            self.start_btn.set_state("start")

        self.start_btn.repaint()

    def open_route(self):
        self.stop.emit()

        if config.get("route", "path") == "":
            return

        try:
            route = route_loader.load(config.get("route", "path"))
        except KeyError:
            self.display_error_message("Key Error", "Route Error")
            return False

        if not route:
            self.display_error_message("Could not load route", "Route Error")
            self._load_route_dir()
            config.set_key("route", "path", "")
            config.save_config()
            return False

        error = route_loader.validate_route(route)

        if error:
            self.display_error_message(error, "Route Error")
            return False

        self.route = route

        self.split_list.clear()
        self.star_count.star_count = route.initial_star
        self.star_count.split_star = route.splits[0].star_count

        for split in route.splits:
            split_icon_path = split.icon_path

            if split_icon_path:
                split_icon_path = rel_to_abs(split_icon_path)
                icon = QtGui.QPixmap(split_icon_path)
            else:
                icon = None

            self.split_list.add_split(split.title, icon)

        self.split_list.repaint()

        return True

    def open_route_browser(self):
        """ Show native file dialog to select a .route file for use. """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Route", absolute_path("routes"),
                                                             "AS64 Route Files (*.as64)")

        if file_path:
            self._save_open_route(file_path)

    def contextMenuEvent(self, event):
        context_menu = QtWidgets.QMenu(self)
        route_menu = QtWidgets.QMenu("Open Route")
        route_actions = {}
        category_menus = {}

        for category in sorted(self._routes, key=lambda text:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]):
            if len(self._routes[category]) == 1 or category == "":
                for route in self._routes[category]:
                    route_menu.addAction(route[0])
                    route_actions[route[0]] = partial(self._save_open_route, route[1])
            else:
                category_menus[category] = QtWidgets.QMenu(str(category))
                route_menu.addMenu(category_menus[category])

                for route in self._routes[category]:
                    category_menus[category].addAction(route[0])
                    route_actions[route[0]] = partial(self._save_open_route, route[1])

        route_menu.addSeparator()
        file_action = route_menu.addAction("From File")

        # Actions
        edit_route = context_menu.addAction("Edit Route")
        context_menu.addMenu(route_menu)
        context_menu.addSeparator()
        cords_action = context_menu.addAction("Edit Coordinates")
        context_menu.addSeparator()
        advanced_action = context_menu.addAction("Settings")
        context_menu.addSeparator()
        reset_gen_action = context_menu.addAction("Generate Reset Templates")
        context_menu.addSeparator()
        about_action = context_menu.addAction("About")
        exit_action = context_menu.addAction("Exit")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        # Connections
        if action == edit_route:
            self.dialogs["route_editor"].show()
        elif action == file_action:
            self.open_route_browser()
        elif action == cords_action:
            self.dialogs["capture_editor"].show()
        elif action == advanced_action:
            self.dialogs["settings_dialog"].show()
        elif action == reset_gen_action:
            self.dialogs["reset_dialog"].show()
        elif action == about_action:
            self.dialogs["about_dialog"].show()
        elif action == exit_action:
            self.close()
        else:
            try:
                route_actions[action.text()]()
            except (KeyError, AttributeError):
                pass

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self._drag = True
            self._drag_position = event.globalPos()-self.pos()
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag = False
        event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(event.globalPos() - self._drag_position)
                event.accept()
        except AttributeError:
            pass

    def display_error_message(self, message, title="Core Error"):
        """
        Display a warning dialog with given title and message
        :param title: Window title
        :param message: Warning/error message
        :return:
        """
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.show()

    def _load_route_dir(self):
        self._routes = {}

        for file in os.listdir("routes"):
            if file.endswith(".as64"):
                route = route_loader.load("routes/" + file)

                if route:
                    category = route.category

                    try:
                        self._routes[category].append([route.title, "routes/" + file])
                    except KeyError:
                        self._routes[category] = []
                        self._routes[category].append([route.title, "routes/" + file])

    def _on_route_update(self):
        self._load_route_dir()
        self.open_route()

    def _save_open_route(self, file_path):
        prev_route = config.get("route", "path")
        config.set_key("route", "path", file_path)
        config.save_config()
        success = self.open_route()

        if success:
            return
        else:
            config.set_key("route", "path", prev_route)
            config.save_config()
            self.open_route()
