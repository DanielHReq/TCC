from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scatterlayout import ScatterLayout
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

class Gerenciador(ScreenManager):
    pass

class Mapa(Screen):
    def on_pre_enter(self):
        image_pin = Image()

        texture_pin = Texture.create(size=(30,30), colorfmt='bgr')
        texture_pin.blit_buffer(image_pin, colorfmt='bgr', bufferfmt='ubyte')

class MapeandoApp(App):
    def build(self):
        return Gerenciador()

if __name__ == '__main__':
    MapeandoApp().run()