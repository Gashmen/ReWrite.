import os
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from src.interface_backend import gland_ui

from config import csv_config

from src.csv import gland_csv
from src.Widgets_Custom import ExtendedCombobox


class DxfQtConnect(QtWidgets.QMainWindow, gland_ui.GlandInterface):

    def __init__(self):

        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()




