import cv2
import time
from ASST.settings import BASE_DIR

face_cascade = cv2.CascadeClassifier("haarcacade_frontalface_default.xml")



def face_detect(face_path):
    face = cv2.imread(face_path)
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)
    return(len(faces))
