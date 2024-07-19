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

## VARIABILI GLOBALI
valoreFocale = 0

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
		### VIDEO PRINCIPALE
		self.actionVideoPrincipale.triggered.connect(self.apriVideoPrincipale)
		### VIDEO TELLER
		self.actionVideoTeller.triggered.connect(self.apriVideoTeller)
		### VIDEO IRIDE
		self.actionVideoIride.triggered.connect(self.apriVideoIride)
		self.actionVideoMovimentoTesta.triggered.connect(self.apriVideoMovimentoTesta)
		## CHIUDI PROGRAMMA
		self.actionChiudiProgramma.triggered.connect(self.chiudi)

		## AVVIO THREAD
		self.videoPrincipale = Worker1()
		self.videoPrincipale.ImageUpdate.connect(self.ImageUpdateSlot)


		## RITORNO DELLA DISTANZA DAL VIDEO
		self.videoPrincipale.focale.connect(self.ritornoFocale)
		# RITORNO DELLA DISTANZA DAL NASO

		self.videoPrincipale.distanzaNasoDestra.connect(self.ritornoDistanzaDestra)
		self.videoPrincipale.distanzaNasoSinistra.connect(self.ritornoDistanzaSinistra)
		self.videoPrincipale.latoSguardo.connect(self.ritornoLatoSguardo)

		# AUMENTO - DIMINUISCO DISTANZA DAL VIDEO
		self.btnPiuDistanza.clicked.connect(self.piuDistanza)
		self.btnMenoDistanza.clicked.connect(self.menoDistanza)

		## METTO ASSI VIDEO
		self.btnAssiCentroVideo.clicked.connect(self.assiCentroVideo)

	## IMPOSTO ETICHETTA CON DISTANZA VIDEO
	def ritornoFocale(self, value):
		self.lblValoreFocale.setText(str(value) + " cm.")
	## AUMENTO FOCALE
	def aumentoFocale(self):
		pass
	## DIINUISCO FOCALE
	def diminuiscoFocale(self, value):
		pass

	# AUMENTO E DIMINUISCO DISTAMZA DAL VIDEO
	def piuDistanza(self, value):
		self.videoPrincipale.aumentoFocale()

	def menoDistanza(self):
		self.videoPrincipale.diminuiscoFocale()

	## IMPOSTO ETICHETTA CON DISTANZA NASO DESTRA E SINISTRA
	def ritornoDistanzaDestra(self, value):
		self.lblDistanzaDestra.setText(str(value) + " cm.")
	def ritornoDistanzaSinistra(self, value):
		self.lblDistanzaSinistra.setText(str(value) + " cm.")


	def ritornoLatoSguardo(self, value):
		self.lblSguardo.setText(value)

	## ASSI VIDEO
	def assiCentroVideo(self):
		self.videoPrincipale.mostroNacondoAssi()

		### TELLER

		### DATI
		### UTENTI





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