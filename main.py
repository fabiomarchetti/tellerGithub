import sqlite3
import sys
from sqlite3 import Error
import time
import datetime
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow

from videoUtente import Worker1


class PrimoVideo(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('ui/educatore.ui', self)

		# STATUS BAR #################################################################
		self.lblStatusBar = QLabel("sviluppo: " + "Fabio Marchetti" + "* *" + "versione: 1.0")
		self.statusBar().addPermanentWidget(self.lblStatusBar)
		## CREA MENU ###################
		menu = self.menuBar()
		menu.setNativeMenuBar(False)
		# VOCI MENU
		### VIDEO
		self.actionVideoPrincipale.triggered.connect(self.apriVideoPrincipale)
		self.actionVideoTeller.triggered.connect(self.apriVideoTeller)
		self.actionVideoIride.triggered.connect(self.apriVideoIride)
		self.actionVideoMovimentoTesta.triggered.connect(self.apriVideoMovimentoTesta)
		### TELLER

		### DATI
		### UTENTI

		## CHIUDI PROGRAMMA
		self.actionChiudiProgramma.triggered.connect(self.chiudi)

		## AVVIO THREAD
		self.videoPrincipale = Worker1()
		self.videoPrincipale.ImageUpdate.connect(self.ImageUpdateSlot)

	def ImageUpdateSlot(self, Image):
		self.lblVideoPrincipale.setPixmap(QPixmap.fromImage(Image))

# FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI FUNZIONI

	def apriVideoPrincipale(self):
		self.videoPrincipale.start()
	def apriVideoTeller(self):
		pass
	def apriVideoMovimentoTesta(self):
		pass
	def apriVideoIride(self):
		pass



	def chiudi(self):
		self.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = PrimoVideo()
	window.show()
	app.exec_()