import time
import cv2 as cv
import mss
import numpy as np
import win32gui

with mss.mss() as sct: 
  while "Screen capturing":
    last_time = time.time()
    monitor = {"top": 0, "left": 0, "width": 1600, "height": 900}
    img = np.array(sct.grab(monitor))

    print("FPS: {: .2f}".format(1 / (time.time() - last_time)))

    faceCascade = cv.CascadeClassifier('Resources/haarcascades/haarcascade_frontalface_default.xml')
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
      cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)
  
    cv.namedWindow('Screen', cv.WINDOW_NORMAL)
    cv.imshow("Screen", img)

    # Press "q" to quit
    if cv.waitKey(25) & 0xFF == ord("q"):
      cv.destroyAllWindows()
      break