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
from math import *

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
	face = []
	# VARIABILE FOCALE
	focale = pyqtSignal(int)

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
				face = self.faces[0]
				pointLeft = face[145]
				pointRight = face[374]
				cv2.line(img, pointLeft, pointRight, (255, 0, 0), 3)
				cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
				cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
				# distanza tra gli occhi
				w, _ = detector.findDistance(pointLeft, pointRight)
				# cerco il punto focale
				W = 6.3
				# d = 50
				# f = (w*d)/W
				# print(f) #ESTRAGGO VALORE DI F CHE RISULTA ESSERE DI 588

				# DISTANZA DALLA TELECAMERA MISURATA == 588
				#f = 588
				f = 950
				self.dist = (W * f) / w
				print(self.dist)


			img = cv2.flip(img, 1)

			cvzone.putTextRect(img, f'distanza dal video: {int(self.dist)}', (100, 100),
				   scale=2, thickness=2, colorT=(255, 255, 255),
				   colorR=(255, 0, 0), font=cv2.FONT_HERSHEY_PLAIN,
				   offset=10, border=None, colorB=(0, 255, 0))

			ConvertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
			Pic = ConvertToQtFormat.scaled(1024, 768, Qt.KeepAspectRatio)
			self.ImageUpdate.emit(Pic)

	def stop(self):
		self.ThreadActive = False
		self.wait()
		self.terminate()

	def aumentaFocale(self):
		pass