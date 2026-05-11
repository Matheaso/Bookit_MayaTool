
import maya.cmds as cmds
import random
from PySide6 import QtCore, QtWidgets
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui

from bookit import (
    core,
    __version__,
    __title__,
    settings
)


def main_window_ui():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window), QtWidgets.QWidget)


class BookitToolUI(QtWidgets.QDialog):
    WINDOW_TITLE = f"{__title__} v{__version__}"
    dlg_instance = None
    is_seed_random = True

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = cls()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()


    def __init__(self, parent=main_window_ui()):
        super(BookitToolUI, self).__init__(parent)

        self.core = core.BookitTool()
        self.settings = settings.load_settings()
        self.was_button_clicked = False

        self.set_style()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(400, 900)
        self.create_widget()
        self.create_layout()

        self.create_connection()

        self.apply_settings_to_ui()
        self.apply_settings_to_core()


    def create_widget(self):

        # seed counter
        self.seed_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.seed_slider.setRange(1, 1000)
        self.seed_slider.setSingleStep(1)
        self.seed_box = QtWidgets.QSpinBox(self)
        self.seed_box.setRange(1, 1000)

        # additional rotation counter
        self.rotation_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.setSingleStep(1)
        self.rotation_slider.setValue(0)

        self.rotation_box = QtWidgets.QSpinBox(self)
        self.rotation_box.setRange(-180, 180)

        # delete percent counter
        self.delete_percent_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.delete_percent_slider.setRange(0, 100)
        self.delete_percent_slider.setSingleStep(1)
        self.delete_percent_slider.setValue(0)

        self.delete_percent_box = QtWidgets.QSpinBox(self)
        self.delete_percent_box.setRange(0, 100)

        # rotation counters synchronization
        self.rotation_slider.valueChanged.connect(self.rotation_box.setValue)
        self.rotation_box.valueChanged.connect(self.rotation_slider.setValue)

        # seed counters synchronization
        self.seed_slider.valueChanged.connect(self.seed_box.setValue)
        self.seed_box.valueChanged.connect(self.seed_slider.setValue)

        # delete counters synchronizaiton
        self.delete_percent_slider.valueChanged.connect(self.delete_percent_box.setValue)
        self.delete_percent_box.valueChanged.connect(self.delete_percent_slider.setValue)



        # labels
        self.seed_label = QtWidgets.QLabel("Seed:  ")
        self.rotation_label = QtWidgets.QLabel("Add Rotation:  ")
        self.label = QtWidgets.QLabel("Books:  ")
        self.delete_percent_label = QtWidgets.QLabel("Delete %:  ")

        #groups
        self.setup_group = QtWidgets.QGroupBox("1) Books Setup:")
        self.books_button = QtWidgets.QPushButton("Books")
        self.draw_spline_group = QtWidgets.QGroupBox("2) Draw Spline:")
        self.additional_group = QtWidgets.QGroupBox("Additional Settings")
        self.generate_group = QtWidgets.QGroupBox("3) Generate:")
        self.bake_group = QtWidgets.QGroupBox("4) Bake:")

        # buttons
        self.books_button = QtWidgets.QPushButton("Set Books")
        self.bookit_button = QtWidgets.QPushButton("Book It!")
        self.select_active_books_button = QtWidgets.QPushButton("Active Books")
        self.select_active_curve_button = QtWidgets.QPushButton("Active Curve")
        self.draw_spline_button = QtWidgets.QPushButton("Draw Spline")
        self.select_created_books_button = QtWidgets.QPushButton("Created Books")
        self.bake_button = QtWidgets.QPushButton("Bake")
        self.delete_settings_data_button = QtWidgets.QPushButton("Delete Settings Data")

        # variables
        self.seed_slider.valueChanged.connect(self.on_box_slider_value_changed)
        self.seed_box.valueChanged.connect(self.on_box_slider_value_changed)

        # checkboxes
        self.random_seed_checkbox = QtWidgets.QCheckBox("Random Seed")
        self.random_seed_checkbox.setChecked(True)
        self.random_seed_checkbox.toggled.connect(self.on_seed_changed)
        self.auto_save_on_exit_checkbox = QtWidgets.QCheckBox("Auto Save On Exit")
        self.auto_save_on_exit_checkbox.setChecked(False)

        self.rotate_checkbox = QtWidgets.QCheckBox("Rotate")
        self.rotate_checkbox.setChecked(True)
        self.rotate_checkbox.toggled.connect(self.on_rotate_box_change)

        self.select_created_checkbox = QtWidgets.QCheckBox("Auto Select")
        self.select_created_checkbox.setChecked(False)
        self.select_created_checkbox.toggled.connect(self.on_select_created_box_change)

    def create_layout(self):

        ## Layouts
        main_layout = QtWidgets.QVBoxLayout(self)

        seed_layout = QtWidgets.QHBoxLayout()
        setup_layout = QtWidgets.QVBoxLayout()
        additional_main_layout = QtWidgets.QVBoxLayout()
        h_qol_buttons_layout = QtWidgets.QHBoxLayout()
        draw_spline_layout = QtWidgets.QHBoxLayout()
        bookit_layout = QtWidgets.QHBoxLayout()
        rotation_layout = QtWidgets.QHBoxLayout()
        bake_layout = QtWidgets.QHBoxLayout()
        delete_percent_layout = QtWidgets.QHBoxLayout()

        ## groups setup
        self.setup_group.setLayout(setup_layout)
        self.additional_group.setLayout(additional_main_layout)
        self.draw_spline_group.setLayout(draw_spline_layout)
        self.generate_group.setLayout(bookit_layout)
        self.bake_group.setLayout(bake_layout)

        ## init layout
        main_layout.addWidget(self.setup_group)
        main_layout.addWidget(self.draw_spline_group)
        setup_layout.addWidget(self.books_button)

        ## init draw spline
        draw_spline_layout.addWidget(self.draw_spline_button)

        ## Bookit (generate)
        main_layout.addWidget(self.generate_group)
        bookit_layout.addWidget(self.bookit_button)

        ## Bake
        main_layout.addWidget(self.bake_group)
        bake_layout.addWidget(self.bake_button)


        ## Qol buttons
        main_layout.addLayout(h_qol_buttons_layout)
        h_qol_buttons_layout.addWidget(self.select_active_books_button)
        h_qol_buttons_layout.addWidget(self.select_active_curve_button)
        h_qol_buttons_layout.addWidget(self.select_created_books_button)

        ## additional settings layout
        main_layout.addWidget(self.additional_group)
        additional_main_layout.addLayout(seed_layout)
        seed_layout.addWidget(self.seed_label)
        seed_layout.addWidget(self.seed_slider)
        seed_layout.addWidget(self.seed_box)
        additional_main_layout.addLayout(delete_percent_layout)
        delete_percent_layout.addWidget(self.delete_percent_label)
        delete_percent_layout.addWidget(self.delete_percent_slider)
        delete_percent_layout.addWidget(self.delete_percent_box)
        additional_main_layout.addLayout(rotation_layout)
        additional_main_layout.addWidget(self.random_seed_checkbox)
        additional_main_layout.addWidget(self.rotate_checkbox)
        additional_main_layout.addWidget(self.select_created_checkbox)
        additional_main_layout.addWidget(self.auto_save_on_exit_checkbox)
        rotation_layout.addWidget(self.rotation_label)
        rotation_layout.addWidget(self.rotation_slider)
        rotation_layout.addWidget(self.rotation_box)
        additional_main_layout.addWidget(self.delete_settings_data_button)


        main_layout.addWidget(self.label)
        main_layout.addStretch()


    def create_connection(self):
        self.books_button.clicked.connect(self.on_set_meshes)
        self.bookit_button.clicked.connect(self.on_bookit_clicked)
        self.select_active_books_button.clicked.connect(self.on_select_active_books)
        self.select_active_curve_button.clicked.connect(self.on_select_active_curve)
        self.draw_spline_button.clicked.connect(self.on_draw_spline_clicked)
        self.select_created_books_button.clicked.connect(self.on_select_created_books)
        self.rotation_slider.valueChanged.connect(self.on_rotation_changed)
        self.rotation_box.valueChanged.connect(self.on_rotation_changed)
        self.delete_percent_slider.valueChanged.connect(self.on_delete_percent_changed)
        self.bake_button.clicked.connect(self.on_bake_button_clicked)
        self.delete_settings_data_button.clicked.connect(self.on_delete_settings_data)


    def on_delete_settings_data(self):
        settings.delete_settings()

        self.settings = settings.BookitSettings()

        self.apply_settings_to_ui()
        self.apply_settings_to_core()


    def apply_settings_to_ui(self):
        self.seed_slider.setValue(self.settings.seed)
        self.seed_box.setValue(self.settings.seed)

        self.random_seed_checkbox.setChecked(self.settings.random_seed)
        self.rotate_checkbox.setChecked(self.settings.rotate)
        self.select_created_checkbox.setChecked(self.settings.auto_select)
        self.auto_save_on_exit_checkbox.setChecked(self.settings.auto_save_on_exit_button)

        self.delete_percent_slider.setValue(self.settings.delete_percent)
        self.delete_percent_box.setValue(self.settings.delete_percent)

        self.rotation_slider.setValue(self.settings.rotation_value)
        self.rotation_box.setValue(self.settings.rotation_value)

        self.is_seed_random = self.settings.random_seed


    def apply_settings_to_core(self):
        self.core.rotate = self.settings.rotate
        self.core.auto_select = self.settings.auto_select
        self.core.delete_percent = self.settings.delete_percent
        self.core.rotation_value = self.settings.rotation_value


    def get_settings_from_ui(self) -> settings.BookitSettings:
        return settings.BookitSettings(
            seed=self.seed_slider.value(),
            random_seed=self.random_seed_checkbox.isChecked(),
            rotate=self.rotate_checkbox.isChecked(),
            auto_select=self.select_created_checkbox.isChecked(),
            delete_percent=self.delete_percent_slider.value(),
            rotation_value=self.rotation_slider.value(),
            auto_save_on_exit_button=self.auto_save_on_exit_checkbox.isChecked(),
        )


    def on_bake_button_clicked(self):
        self.core.bake()


    def on_delete_percent_changed(self, value):
        self.core.delete_percent = value
        self.generate_without_seed()


    def on_rotation_changed(self, value):
        self.core.rotation_value = value
        self.generate_without_seed()


    def on_select_created_box_change(self, checked):
        self.core.auto_select = checked


    def on_seed_changed(self, checked):
        self.is_seed_random = checked


    def on_rotate_box_change(self, checked):
        self.core.rotate = checked
        self.on_bookit_clicked()


    def on_select_active_books(self):
        active_books = self.core.meshes
        if not active_books:
            cmds.warning("No Active Meshes")
            return

        cmds.select(active_books)


    def on_select_active_curve(self):
        active_curve = self.core.curve
        if not active_curve:
            cmds.warning("No Active Curve")
            return

        cmds.select(active_curve)


    def on_select_created_books(self):
        created_books = self.core.preview_books
        if not created_books:
            cmds.warning("No Created Books")
            return
        cmds.select(created_books)


    def block_box_slider_signals(self, is_blocked=True):
        self.seed_box.blockSignals(is_blocked)
        self.seed_slider.blockSignals(is_blocked)


    def on_box_slider_value_changed(self, value):
        self.generate_without_seed()


    def on_bookit_clicked(self):
        if self.is_seed_random:
            seed = random.randint(1, 1000)
            self.block_box_slider_signals()

            self.seed_slider.setValue(seed)
            self.seed_box.setValue(seed)

            self.block_box_slider_signals(False)
        else:
            seed = self.seed_slider.value()

        self.core.generate(seed)


    @staticmethod
    def on_draw_spline_clicked():
        if not cmds.contextInfo("curveEPCtx", exists=True):
            cmds.curveEPCtx("curveEPCtx")

        cmds.setToolTo("curveEPCtx")


    def on_set_meshes(self):
        meshes = self.core.set_books_from_selection()

        text = ""
        for mesh in meshes:
            text = text + str(mesh) + "\n"
        self.label.setText(f"Books:\n{text}")


    def generate_without_seed(self):
        if self.is_seed_random:
            self.is_seed_random = False
            self.on_bookit_clicked()
            self.is_seed_random = True
        else:
            self.on_bookit_clicked()


    def set_style(self):
        self.setStyleSheet("""
                QGroupBox {
                    border: 1px solid #FFD54F;
                    border-radius: 6px;
                    margin-top: 10px;
                    padding: 10px;
                }
                QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                 color: #1111;
                }
                """)


    def closeEvent(self, event):
        if self.auto_save_on_exit_checkbox.isChecked():
            settings.save_settings(self.get_settings_from_ui())

        self.core.cleanup()
        BookitToolUI.dlg_instance = None
        super().closeEvent(event)


def show():
    BookitToolUI.show_dialog()