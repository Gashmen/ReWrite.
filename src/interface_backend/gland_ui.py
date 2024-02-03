import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from src.interface_backend import shell_ui

from config import csv_config
from src.Widgets_Custom.Error import Ui_WidgetError
from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox

class GlandInterface(shell_ui.ShellInterface):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.install_gland_csv()
        self.gland_information.set_main_dict(main_path=self.gland_information.gland_csv_path)

        '''Установка разрежения видимости'''
        self.set_gland_enabled()
        '''ОБНОВЛЕНИЕ ВИДЖЕТОВ'''
        self.improve_choose_widget()

        '''RADIO BUTTONS'''
        self.gland_from_allRadioButton.toggled.connect(self.install_choose_gland_widget_enabled)
        self.gland_from_propertiesRadioButton.toggled.connect(self.install_gland_designation_widget_enabled)

        '''КНОПКИ'''
        self.inputsButton_leftMenu.clicked.connect(self.set_gland_page)

        '''COMBOBOX'''
        self.gland_designationcomboBox.currentTextChanged.connect(self.set_gland_designation)
        self.gland_designationcomboBox.currentTextChanged.connect(self.install_gland_material_enabled)

        self.gland_materialcomboBox.currentTextChanged.connect(self.set_gland_material)
        self.gland_materialcomboBox.currentTextChanged.connect(self.install_gland_cabletype_enabled)

        self.gland_cabletypecomboBox.currentTextChanged.connect(self.set_gland_cabletype)
        self.gland_cabletypecomboBox.currentTextChanged.connect(self.install_gland_threadtype_enabled)

        self.gland_threadtypecomboBox.currentTextChanged.connect(self.set_gland_thread)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.install_gland_ckeckdiam_enabled)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.install_gland_g_npt_enabled)
        self.gland_threadtypecomboBox.currentTextChanged.connect(self.set_dict_for_calculate_gland_diam)

        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.set_gland_additional_marking)
        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.install_gland_type_mr_marking_enabled)
        self.gland_additionalmarkingcomboBox.currentTextChanged.connect(self.give_gland_tube_mr_modification)

        self.gland_tube_mr_markingcomboBox.currentTextChanged.connect(self.set_gland_tube_mr_modification)
        self.gland_tube_mr_markingcomboBox.currentTextChanged.connect(self.set_key_gland)

        '''LINE EDIT'''
        self.gland_checkdiam_minlineedit.editingFinished.connect(self.set_min_diam_qt)
        self.gland_checkdiam_minlineedit.editingFinished.connect(self.set_max_diam_qt)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.set_max_diam_qt)

        self.gland_checkdiam_minlineedit.editingFinished.connect(self.calculate_diam_modification_for_M_thread)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.calculate_diam_modification_for_M_thread)

        self.gland_checkdiam_minlineedit.editingFinished.connect(self.install_gland_additional_marking_enabled)
        self.gland_checkdiam_maxlineedit.editingFinished.connect(self.install_gland_additional_marking_enabled)


    def set_gland_page(self):
        '''Устанавливает 1 индекс у SHELL PAGE, если он не установлен'''
        if self.stackedWidget.count() != 5:
            self.stackedWidget.setCurrentIndex(5)

    def install_gland_csv(self):
        self.smb_specmash.get_gland_csv_path()
        self.gland_information = gland_csv.GlandMainDictQt(gland_csv_path=self.smb_specmash.gland_csv_path)


    def improve_choose_widget(self):
        '''ИЗМЕНЕНИЕ КЛАССА COMBOBOX WIDGET'''
        self.vzorglandcomboBox = ExtendedCombobox.ExtendedComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vzorglandcomboBox.sizePolicy().hasHeightForWidth())
        self.vzorglandcomboBox.setSizePolicy(sizePolicy)
        self.vzorglandcomboBox.setObjectName("vzorglandcomboBox")
        self.verticalLayout_14.addWidget(self.vzorglandcomboBox)

    def set_gland_enabled(self):
        '''Поставить disabled изначально'''
        self.b_vzorglandWidget.setEnabled(False)
        self.c_gland_designationWidget.setEnabled(False)
        self.d_gland_materialWidget.setEnabled(False)
        self.e_gland_cabletypeWidget.setEnabled(False)
        self.f_gland_threadtypeWidget.setEnabled(False)
        self.g_gland_checkdiamWidget.setEnabled(False)
        self.h_gland_mr_or_tubeWidget.setEnabled(False)
        self.i_gland_additionalmarkingWidget.setEnabled(False)
        self.j_gland_tube_mr_markingWidget.setEnabled(False)
        self.k_gland_optionsWidget.setEnabled(False)

    def install_choose_gland_widget_enabled(self):
        if self.gland_from_allRadioButton.isChecked():
            self.b_vzorglandWidget.setEnabled(True)
        else:
            self.b_vzorglandWidget.setEnabled(False)

    def install_gland_designation_widget_enabled(self):
        if self.gland_from_propertiesRadioButton.isChecked():
            self.c_gland_designationWidget.setEnabled(True)
            self.give_gland_designation()
        else:
            self.c_gland_designationWidget.setEnabled(False)
            self.gland_designationcomboBox.clear()


    def give_gland_designation(self):
        if self.c_gland_designationWidget.isEnabled():
            self.gland_designationcomboBox.clear()
            self.gland_information.get_unique_designation()
            self.gland_designationcomboBox.addItems(['',*self.gland_information.gland_unique_designation])

    def set_gland_designation(self):
        self.gland_designation = self.gland_designationcomboBox.currentText()
        self.gland_information.set_gland_designation(gland_designation=self.gland_designation)

    def install_gland_material_enabled(self):
        if hasattr(self, 'gland_designation'):
            if self.gland_designation == 'Кабельный ввод':
                self.d_gland_materialWidget.setEnabled(True)
                self.give_gland_material()
            else:
                self.d_gland_materialWidget.setEnabled(False)
        else:
            self.d_gland_materialWidget.setEnabled(False)

    def give_gland_material(self):
        if self.d_gland_materialWidget.isEnabled():
            self.gland_materialcomboBox.clear()
            self.gland_information.get_unique_material()
            self.gland_materialcomboBox.addItems(['',*self.gland_information.gland_unique_material])

    def set_gland_material(self):
        self.gland_material = self.gland_materialcomboBox.currentText()
        self.gland_information.set_gland_material(gland_material=self.gland_material)

    def install_gland_cabletype_enabled(self):
        if hasattr(self,'gland_material'):
            if self.gland_material != '':
                self.e_gland_cabletypeWidget.setEnabled(True)
                self.give_gland_calbetype()
            else:
                self.e_gland_cabletypeWidget.setEnabled(False)
        else:
            self.e_gland_cabletypeWidget.setEnabled(False)

    def give_gland_calbetype(self):
        if self.e_gland_cabletypeWidget.isEnabled():
            self.gland_cabletypecomboBox.clear()
            self.gland_information.get_unique_cable_type()
            self.gland_cabletypecomboBox.addItems(['',*self.gland_information.gland_unique_cable_type])

    def set_gland_cabletype(self):
        self.gland_cabletype = self.gland_cabletypecomboBox.currentText()
        self.gland_information.set_cable_type(gland_cable_type=self.gland_cabletype)

    def install_gland_threadtype_enabled(self):
        if hasattr(self,'gland_cabletype'):
            if self.gland_cabletype != '':
                self.f_gland_threadtypeWidget.setEnabled(True)
                self.give_gland_threadtype()
            else:
                self.f_gland_threadtypeWidget.setEnabled(False)
        else:
            self.f_gland_threadtypeWidget.setEnabled(False)

    def give_gland_threadtype(self):
        if self.f_gland_threadtypeWidget.isEnabled():
            self.gland_threadtypecomboBox.clear()
            self.gland_information.get_unique_thread()
            self.gland_threadtypecomboBox.addItems(['',*self.gland_information.gland_unique_thread])

    def set_gland_thread(self):
        self.gland_threadtype = self.gland_threadtypecomboBox.currentText()
        self.gland_information.set_gland_thread(gland_thread=self.gland_threadtype)

    def install_gland_ckeckdiam_enabled(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'М':
                self.g_gland_checkdiamWidget.setEnabled(True)
            else:
                self.g_gland_checkdiamWidget.setEnabled(False)
        else:
            self.g_gland_checkdiamWidget.setEnabled(False)

    def set_min_diam_qt(self):
        if self.g_gland_checkdiamWidget.isEnabled():
            if self.gland_checkdiam_minlineedit.text() != '':
                min_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_minlineedit.text())
                if min_diam_qt <0:
                    self.gland_checkdiam_minlineedit.setText('0')
                    min_diam_qt = 0
                self.min_diam_qt =min_diam_qt

    def set_max_diam_qt(self):
        if self.g_gland_checkdiamWidget.isEnabled():
            if self.gland_checkdiam_maxlineedit.text() != '':
                max_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_maxlineedit.text())
                if max_diam_qt <0:
                    self.gland_checkdiam_maxlineedit.setText(self.gland_checkdiam_minlineedit.text())
                    max_diam_qt = 0
                if self.gland_checkdiam_minlineedit.text() != '':
                    min_diam_qt = gland_csv.set_correct_number(number=self.gland_checkdiam_minlineedit.text())
                    if max_diam_qt < min_diam_qt:
                        max_diam_qt = min_diam_qt
                        self.gland_checkdiam_maxlineedit.setText(self.gland_checkdiam_minlineedit.text())
                self.max_diam_qt = max_diam_qt


    def install_gland_g_npt_enabled(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'NPT' or self.gland_threadtype == 'G':
                self.h_gland_mr_or_tubeWidget.setEnabled(True)
            else:
                self.h_gland_mr_or_tubeWidget.setEnabled(False)
        else:
            self.h_gland_mr_or_tubeWidget.setEnabled(False)

    def set_dict_for_calculate_gland_diam(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype != '':
                self.gland_information.set_dict_for_calculate_gland_diam()

    def install_gland_additional_marking_enabled(self):
        if hasattr(self.gland_information, 'dict_for_choose_modification_cable'):
            if self.gland_information.dict_for_choose_modification_cable != {}:
                self.i_gland_additionalmarkingWidget.setEnabled(True)
            else:
                self.i_gland_additionalmarkingWidget.setEnabled(False)
        else:
            self.i_gland_additionalmarkingWidget.setEnabled(False)

    def calculate_diam_modification_for_M_thread(self):
        if hasattr(self,'gland_threadtype'):
            if self.gland_threadtype == 'М':
                if self.gland_checkdiam_minlineedit.text() !='' and self.gland_checkdiam_maxlineedit.text() !='':
                    if hasattr(self,'min_diam_qt') and hasattr(self,'max_diam_qt'):
                        self.gland_information.give_possible_glands_for_calculate(min_diam_from_qt=self.min_diam_qt,
                                                                                  max_diam_from_qt=self.max_diam_qt)
                        #На выходе self.dict_for_choose_modification_cable со значениями тех ключей и данных по вводам
                        #Которые по диаметру проходят
                        self.give_gland_additional_marking()


    def give_gland_additional_marking(self):
        self.gland_additionalmarkingcomboBox.clear()
        if hasattr(self.gland_information, 'dict_for_choose_modification_cable'):
            if self.gland_information.dict_for_choose_modification_cable != {}:
                self.gland_information.give_modification_for_calculated_diam()
                if self.gland_information.list_with_modifications_name != []:
                    self.gland_additionalmarkingcomboBox.addItems(
                        ['',*self.gland_information.list_with_modifications_name])

    def set_gland_additional_marking(self):
        if self.i_gland_additionalmarkingWidget.isEnabled():
            if self.gland_additionalmarkingcomboBox.count() != 0:
                if self.gland_additionalmarkingcomboBox.currentText() != '':
                    self.gland_additionalmarking = self.gland_additionalmarkingcomboBox.currentText()
                    self.gland_information.set_gland_additional_marking(
                        gland_additional_marking=self.gland_additionalmarking
                    )

    def install_gland_type_mr_marking_enabled(self):
        if self.gland_additionalmarkingcomboBox.isEnabled():
            if self.gland_additionalmarkingcomboBox.currentText() != '':
                self.j_gland_tube_mr_markingWidget.setEnabled(True)
            else:
                self.j_gland_tube_mr_markingWidget.setEnabled(False)
        else:
            self.j_gland_tube_mr_markingWidget.setEnabled(False)

    def give_gland_tube_mr_modification(self):
        self.gland_tube_mr_markingcomboBox.clear()
        if self.gland_additionalmarkingcomboBox.isEnabled():
            if self.gland_additionalmarkingcomboBox.currentText() != '':
                self.gland_information.get_uniqie_tube_mr_modification()
                self.gland_tube_mr_markingcomboBox.addItems(['',*self.gland_information.unique_tube_mr_modification])
                if self.gland_information.gland_additional_marking == 'МР':
                    self.gland_tube_mr_markinglabel.setText('Металлорукав')
                elif self.gland_information.gland_additional_marking == 'Т':
                    self.gland_tube_mr_markinglabel.setText('Трубная')

    def set_gland_tube_mr_modification(self):
        if self.gland_tube_mr_markingcomboBox.isEnabled():
            if self.gland_tube_mr_markingcomboBox.currentText() != '':
                self.gland_tube_mr_modification = self.gland_tube_mr_markingcomboBox.currentText()
                self.gland_information.set_gland_tube_mr_modification(
                    gland_tube_mr_modification= self.gland_tube_mr_modification)

    def set_key_gland(self):
        if hasattr(self,'gland_tube_mr_modification'):
            if self.gland_tube_mr_markingcomboBox.currentText() != '':
                self.gland_information.set_gland()






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_window = GlandInterface()
    welcome_window.show()
    sys.exit(app.exec_())


