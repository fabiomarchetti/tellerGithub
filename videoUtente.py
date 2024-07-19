#https://www.youtube.com/watch?v=jsoe1M2AjFk&t=104s
import mediapipe as mp

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from screeninfo import get_monitors
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from math import hypot

def midPoint(p1, p2):
    return int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)
    print('punto medio: ', midPoint)
for m in get_monitors():
    print(str(m))
    print(str(m.width))
    print(str(m.height))
    larghezzaScreen = m.width
    altezzaScreen = m.height

##########################################################################################
## MODULO SPECIFICO PER IL CORPO
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
########################################


class Worker1(QThread):
	ImageUpdate = pyqtSignal(QImage)
	dist = 0
	distanzaDalVideo = 0
	face = []
	f = 950
	## ASSI VERTICALE ED ORIZZONTALE
	## SPOSTAMENTO ASSI LINEA VERTICALE ## 768, 1024
	spostamentoAltoX = 640
	spostamentoAltoY = 0
	####
	spostamentoBassoX = 640
	spostamentoBassoY = 720

	## SPOSTAMENTO ASSI LINEA ORIZZONTALE
	spostamentoSinistroX = 0
	spostamentoSinistroY = 360
	####
	spostamentoDestroX = 1280
	spostamentoDestroY = 360



	# VARIABILE FOCALE PER TRASFERIMENTO
	focale = pyqtSignal(int)
	# VARIABILE AUMENTO FOCALE
	piuFocale = pyqtSignal(int)
	# VARIABILE DIMINUISCO FOCALE
	menoFocale = pyqtSignal(int)

	#################################
	## DISTANZA NASO - DESTRA
	distanzaNasoDestra = pyqtSignal(int)
	##DISTAZA NASO - SINISTRA
	distanzaNasoSinistra = pyqtSignal(int)
	## LATO SGUARDO
	latoSguardo = pyqtSignal(str)



	def run(self):
		self.TheadActivate = True
		cap = cv2.VideoCapture(0)
		detector = FaceMeshDetector(maxFaces=1)

		#self.focale.emit(self.aumentoFocale)

		while self.TheadActivate:
			success, img = cap.read()
			# mostra tutti i punti della faccia se True
			img, self.faces = detector.findFaceMesh(img, draw=False)

			if self.faces:
				## PUNTI PER RILEVARE LA FOCALE
				face = self.faces[0]
				pointLeft = face[145]
				pointRight = face[374]
				#cv2.line(img, pointLeft, pointRight, (255, 0, 0), 3)
				#cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
				#cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)

				## ALTRI PUNTI
				naso = face[4]
				puntoSinistro = (1160, (naso[1]))
				puntoDestro = (120, naso[1])

				##############################################################################################################
				## CECHIO NASO
				cv2.circle(img, naso, 5, (255, 0, 255), cv2.FILLED)

				## CERCHIO A SN DEL NASO
				cv2.circle(img, puntoSinistro, 10, (0, 0, 255), cv2.FILLED)
				## CERCHIO A DX DEL NASO
				cv2.circle(img, puntoDestro, 10, (0, 0, 255), cv2.FILLED)
				##  LINEA DESTRA
				cv2.line(img,naso, puntoDestro, (255, 0, 0), 3)
				## MISURA LINEA DESTRA
				lunghezzaNasoPuntoDestro = int(hypot(naso[0] - puntoDestro[0], naso[1] - puntoDestro[1]))
				## MISURA LINEA SINISTRA
				lunghezzaNasoPuntoSinistro = int(hypot(naso[0] - puntoSinistro[0], naso[1] - puntoSinistro[1]))

				## PUNTO CENTRALE DELLO SCHERMO
				puntoCentraleX = img.shape[1] // 2
				puntoCentraleY = img.shape[0] // 2
				cv2.circle(img, (puntoCentraleX, puntoCentraleY), 10, (0, 255, 0), cv2.FILLED)

				## ASSI CENTRALI DELLO SCHERMO
				cv2.line(img, (self.spostamentoAltoX, self.spostamentoAltoY), (self.spostamentoBassoX, self.spostamentoBassoY), (0, 255, 0), 2)
				cv2.line(img, (self.spostamentoSinistroX, self.spostamentoSinistroY), (self.spostamentoDestroX, self.spostamentoDestroY), (0, 255, 0), 2)

				print(img.shape[0], img.shape[1])





				# distanza tra gli occhi
				w, _ = detector.findDistance(pointLeft, pointRight)
				# cerco il punto focale
				W = 6.3
				# d = 50
				# f = (w*d)/W
				# print(f) #ESTRAGGO VALORE DI F CHE RISULTA ESSERE DI 588

				# DISTANZA DALLA TELECAMERA MISURATA == 588
				#f = 588
				#f = 950

				self.dist = (W * self.f) / w
				self.distanzaDalVIdeo = int(self.dist)
				print(f'distanza dal video: {int(self.dist)}')
				## INVIO DISTANZA AL MAIN
				self.focale.emit(self.distanzaDalVIdeo)
				## INVIO DISTANZA NASO AL MAIN

				self.distanzaNasoDestra.emit(lunghezzaNasoPuntoDestro)
				self.distanzaNasoSinistra.emit(lunghezzaNasoPuntoSinistro)

				differenzaDistanzaDxSn = lunghezzaNasoPuntoDestro - lunghezzaNasoPuntoSinistro

				if lunghezzaNasoPuntoSinistro > 500 and lunghezzaNasoPuntoDestro > 500:
					self.latoSguardo.emit("centro")
				elif(differenzaDistanzaDxSn < 0):
					self.latoSguardo.emit("destra")
				else:
					self.latoSguardo.emit("sinistra")








			img = cv2.flip(img, 1)
			'''
			cvzone.putTextRect(img, str(lunghezzaNasoPuntoDestro - lunghezzaNasoPuntoSinistro), (100, 100),
				   scale=2, thickness=2, colorT=(255, 255, 255),
				   colorR=(255, 0, 0), font=cv2.FONT_HERSHEY_PLAIN,
				   offset=10, border=None, colorB=(0, 255, 0))
			'''
			ConvertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
			Pic = ConvertToQtFormat.scaled(1024, 768, Qt.KeepAspectRatio)
			self.ImageUpdate.emit(Pic)



	def aumentoFocale(self):
		self.f += 10

	def diminuiscoFocale(self):
		self.f -= 10


	def mostroNacondoAssi(self):
		if(self.spostamentoAltoX == 0):
			self.spostamentoAltoX = 640
			self.spostamentoAltoY = 0
			####
			self.spostamentoBassoX = 640
			self.spostamentoBassoY = 720

			## SPOSTAMENTO ASSI LINEA ORIZZONTALE
			self.spostamentoSinistroX = 0
			self.spostamentoSinistroY = 360
			####
			self.spostamentoDestroX = 1280
			self.spostamentoDestroY = 360
		else:
			self.spostamentoAltoX = 0
			self.spostamentoAltoY = 0
			####
			self.spostamentoBassoX = 0
			self.spostamentoBassoY = 0

			## SPOSTAMENTO ASSI LINEA ORIZZONTALE
			self.spostamentoSinistroX = 0
			self.spostamentoSinistroY = 0
			####
			self.spostamentoDestroX = 0
			self.spostamentoDestroY = 0



	def stop(self):
		self.ThreadActive = False
		self.wait()
		self.terminate()

