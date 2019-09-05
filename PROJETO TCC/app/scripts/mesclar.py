from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

from PIL import Image as pilImg
#from kivy.core.image import Image as CoreImage

import kivy.graphics.texture
import base64
import cv2
import numpy as np
import time

camera = cv2.VideoCapture(0)
hcamera = 200
wcamera = 125
camera.set(3, hcamera)  #resolução
camera.set(4, wcamera)

time.sleep(0.1)

kernel = np.ones((3,3), np.uint8)

class Gerenciador(ScreenManager):
    pass

class Mapa(Screen):   
    def on_enter(self):
        Clock.schedule_interval(self.leCamera,1/6)

    def leCamera(self,dt):
        ret, frame = camera.read()
        cv2.imwrite('img.jpg',frame)
        self.ids.imagem.source = 'img.jpg'
        self.ids.imagem.reload()

class MesclarApp(App):
    def build(self):
        return Gerenciador()

if __name__ == '__main__':
    MesclarApp().run()