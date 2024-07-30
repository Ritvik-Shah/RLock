import face_recognition
from PIL import Image
import numpy as np
import cv2
import os
import time

def camera(name, output_folder):
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           
            # Display the resulting frame
            img_item = os.path.join(output_folder, name)
            cv2.imwrite(img_item, frame) 
            cv2.imshow('frame',frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
