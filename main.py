import sqlite3
from sqlite3 import Error
import time
import datetime
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow


class primoVideo(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('ui/eductore.ui', self)