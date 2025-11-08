# KivyGui.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import FaceRecognition as fr
import cv2
import io
from kivy.core.image import Image as CoreImage

# Manually load your kv file
Builder.load_file("facerecognition.kv")

class FaceRecognitionLayout(BoxLayout):
    def on_register(self):
        self.ids.status.text = "Registering user..."
        ok = fr.register_user()
        self.ids.status.text = "Registration successful!" if ok else "Registration failed."

    def on_recognize(self):
        self.ids.status.text = "Recognizing..."
        result = fr.recognize_user()
        self.ids.status.text = f"Unlocked ({result})" if result else "Face not recognized."

    def show_preview(self, frame):
        _, buf = cv2.imencode('.png', frame)
        data = io.BytesIO(buf.tobytes())
        self.ids.preview.texture = CoreImage(data, ext="png").texture

class RLockApp(App):
    def build(self):
        return FaceRecognitionLayout()

if __name__ == "__main__":
    RLockApp().run()
