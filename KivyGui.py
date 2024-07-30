import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
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

# Load the .kv file
Builder.load_file("facerecognition.kv")

class FaceRecognitionLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(FaceRecognitionLayout, self).__init__(**kwargs)

        self.register_btn = Button(text="Register Face")
        self.register_btn.bind(on_press=lambda instance: self.register_face())  # No arguments passed
        self.add_widget(self.register_btn)

        self.recognize_btn = Button(text="Recognize Face")
        self.recognize_btn.bind(on_press=lambda instance: self.recognize_face())  # No arguments passed
        self.add_widget(self.recognize_btn)
    
    def register_face(self):
        # Implement your register_face logic here
        device_id = Vars.device_id
        database = Vars.database
        database_file = Vars.database_file
        cam.camera(device_id + ".jpg", database)
        checker = db.create_database(database, database_file, device_id)
        if (checker == True):
            self.show_message("Face has already been registered for this user.")
        else:
            self.show_message("Face registered.")

    def recognize_face(self):
        # Implement your recognize_face logic here
        device_id = Vars.device_id
        database = Vars.database
        cam.camera('Entry_face.jpg', database)
        image = face_recognition.load_image_file(os.path.join(database, device_id+".jpg"))
        unknown_image = face_recognition.load_image_file(os.path.join(database,"Entry_face.jpg"))

        registered_encoding = face_recognition.face_encodings(image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([registered_encoding], unknown_encoding)
        if results == [True]:
            self.show_message("Hello User!")
        else:  
            self.show_message("You are not the user")

        os.remove(os.path.join(database,"Entry_face.jpg"))
    
    def show_message(self, message):
        self.modal_view = ModalView(size_hint=(None, None), size=(400, 200))
        modal_layout = BoxLayout(orientation='vertical')
        message_label = Label(text=message)
        ok_button = Button(text='OK', size_hint=(None, None), size=(100, 50))
        ok_button.bind(on_press=self.modal_view.dismiss)

        modal_layout.add_widget(message_label)
        modal_layout.add_widget(ok_button)
        self.modal_view.add_widget(modal_layout)
        self.modal_view.open()

        
class FaceRecognitionApp(App):
    def build(self):
        return FaceRecognitionLayout()

if __name__ == "__main__":
    FaceRecognitionApp().run()
