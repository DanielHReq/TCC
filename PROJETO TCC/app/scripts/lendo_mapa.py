from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock, mainthread
from kivy.graphics import *

from PIL import Image as pilImg
#from kivy.core.image import Image as CoreImage

import numpy as np
import time

Window.clearcolor = (.4,.4,.7,1)
teste = ['Dan',100,100,(0,1,0,1)] #nome,x,y,rgba
teste2 = ['iel',300,300,(0,0,1,1)]
num_pin = []
num_pin.append(teste)
num_pin.append(teste2)

click_anterior = None

class Gerenciador(ScreenManager):
    pass

class Mapa(Screen):
    clicavel = ObjectProperty()

    @mainthread
    def on_enter(self):
        self.posiciona_pins()

    def posiciona_pins(self):
        for p in num_pin:
            nome_pin = p[0]
            x_num = p[1]
            y_num = p[2]
            cor = p[3]
            self.ids.pin_layout.add_widget(Pin(pos=(x_num,y_num),pin_name=nome_pin,cor=cor,editable=False))

    def novo_pin(self):
        global click_anterior
        if click_anterior != None:
            self.ids.pin_layout.children[0].remove_widget(self.ids.pin_layout.children[0].children[0])
            self.ids.pin_layout.add_widget(Pin(pos=(coord_touch[0]-7.5,coord_touch[1]),cor=(1,0,0,1),editable=True))
            click_anterior = None

    def unselect(self):
        global coord_touch, click_anterior
        if click_anterior != None:
            self.ids.pin_layout.children[0].remove_widget(self.ids.pin_layout.children[0].children[0])
            click_anterior = None
        coord_touch = None

    def on_touch_down(self,touch):
        if touch.is_double_tap:
            if self.ids.pin_layout.children[0].collide_point(touch.x,touch.y):
                global coord_touch, click_anterior
                coord_touch = self.ids.pin_layout.children[0].to_widget(touch.x,touch.y)
                if click_anterior != None:
                    self.ids.pin_layout.children[0].remove_widget(self.ids.pin_layout.children[0].children[0])
                else:
                    click_anterior = 1
                self.click = Click(pos=(coord_touch[0]-8/2,coord_touch[1]-8/2))
                self.ids.pin_layout.add_widget(self.click)
        return super(Mapa,self).on_touch_down(touch)

class Pin(BoxLayout):
    def __init__(self,pos='',pin_name='',cor='',editable='',**kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.pin_name = pin_name
        self.editable = editable
        self.cor = cor
        with self.canvas.before:
            Color(rgba=self.cor)

# DEIXAR PARA DEPOIS    
    def on_touch_down(self,touch):
        if touch.is_double_tap:
#            self.parent.add_widget(PinInfo(pos=self.pos,text=self.pin_name))
            pass
        return super(Pin,self).on_touch_down(touch)

#class PinInfo(BoxLayout):
#    def __init__(self,pos='',text='',**kwargs):
#        super().__init__(**kwargs)
#        self.pos = (pos[0],pos[1]+60)
#        self.ids.label_name.text = text

class Click(BoxLayout):
    pass

class LendoApp(App):
    def build(self):
        return Gerenciador()

if __name__ == '__main__':
    LendoApp().run()