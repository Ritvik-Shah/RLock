import tkinter as tk
from tkinter import filedialog, messagebox
import face_recognition
from PIL import Image
import numpy as np
import cv2
import os
import time
import hashlib
import Device_Identifier as dev_id
import Database as db
import Camera as cam
import Vars

class FaceRecognitionApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        self.register_btn = tk.Button(root, text="Register Face", command=self.register_face)
        self.register_btn.pack(pady=10)

        self.recognize_btn = tk.Button(root, text="Recognize Face", command=self.recognize_face)
        self.recognize_btn.pack(pady=10)

    def register_face(self):
        # Implement your code to take a picture and save it here
        # This function should save the picture with the person's name
        device_id = Vars.device_id
        database = Vars.database
        database_file = Vars.database_file
        cam.camera(device_id + ".jpg", database)
        checker = db.create_database(database, database_file, device_id)
        if (checker == True):
            messagebox.showinfo("Success", "Face has already been registered for this user.")
        else:
            messagebox.showinfo("Success", "Face registered.")

    def recognize_face(self):
        # Implement your code to recognize a face here
        # This function should detect the face in an image and perform recognition
        device_id = Vars.device_id
        database = Vars.database
        cam.camera('Entry_face.jpg', database)
        image = face_recognition.load_image_file(os.path.join(database, device_id+".jpg"))
        unknown_image = face_recognition.load_image_file(os.path.join(database,"Entry_face.jpg"))

        registered_encoding = face_recognition.face_encodings(image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([registered_encoding], unknown_encoding)
        if results == [True]:
            messagebox.showinfo("Recognition Result", "Hello User!")
        else:  
            messagebox.showinfo("Recognition Result", "You are not the user") 

        os.remove(os.path.join(database,"Entry_face.jpg"))           
        
    


    
def main():
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
