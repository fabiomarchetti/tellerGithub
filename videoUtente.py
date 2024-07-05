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



	def run(self):
		self.TheadActivate = True
		cap = cv2.VideoCapture(0)
		while self.TheadActivate:
			success, img = cap.read()
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			if success:
				img = cv2.flip(img, 1)

				results = pose.process(img)
				#img = cv2.resize(img, (854, 660), interpolation=cv2.INTER_AREA)
				print('dimensiioni: ' +str(img.shape))

				print(results.pose_landmarks)

				ConvertToQtFormat = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
				Pic = ConvertToQtFormat.scaled(1024, 768, Qt.KeepAspectRatio)
				self.ImageUpdate.emit(Pic)

	def stop(self):
		self.ThreadActive = False
		self.wait()
		self.terminate()