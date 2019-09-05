import os
import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.graphics import *

from PIL import Image as pilImg
#Window.size = (1280,720)

caminho = '/home/daniel/PROJETO TCC/app/Salvos/'
#Window.clearcolor = (.2,.1,.35,1)
#Window.clearcolor = (.7,.7,.75,1)
Window.clearcolor = (.5,.5,.6,1)

class Gerenciador(ScreenManager):
	pass

class Menu(Screen):
	pass

class Lista(Screen):
    def on_pre_enter(self):
        self.pesquisa_lista()

    def on_leave(self):
        self.limpa_lista()
        self.ids.pesquisa.text = ''
        self.ids.cb_coletaneas.active = True
        self.ids.cb_mapas.active = True

    def pesquisa_lista(self):
        global diretorio
        self.limpa_lista()
        texto_pesquisa = self.ids.pesquisa.text
        for pasta in os.listdir(caminho):
            if pasta.lower().count(texto_pesquisa.lower()) > 0 :
                diretorio = pasta
                num_subpasta = 0
                if pasta[0] == '#':
                    if self.ids.cb_coletaneas.active == True:
                        for subpasta in os.listdir(caminho+pasta+'/'):
                            num_subpasta+=1
                        self.ids.scrollbox.add_widget(ItemLista(text='Coletânea '+pasta+'\n'+str(num_subpasta)+' Arquivos'))
                elif self.ids.cb_mapas.active == True:
                    self.ids.scrollbox.add_widget(ItemLista(text=pasta,nome_mapa=pasta))

    def limpa_lista(self):
        while True:
            try:
                self.ids.scrollbox.remove_widget(self.ids.scrollbox.children[0])
            except:
                break

class CriaMapa(Screen):
    def mostra_box(self, num):
        self.ids.box_criacao.clear_widgets()
        self.ids.box_criacao.add_widget(BoxCriacao(opcao=num))

class BoxCriacao(BoxLayout):
    def __init__(self,opcao='',**kwargs):
        super().__init__(**kwargs)
        self.opcao = opcao
        self.att_box(self.opcao)

    def att_box(self,opcao):
        if opcao == 3 :
            self.clear_widgets()
            self.add_widget(BoxNovaCol())
            self.add_widget(BoxNome())
            self.add_widget(BoxSVideo())
        elif opcao == 2 :
            self.clear_widgets()
            self.add_widget(BoxSpinner())
            self.add_widget(BoxNome())
            self.add_widget(BoxSVideo())
        elif opcao == 1 :
            self.clear_widgets()
            self.add_widget(BoxNome())
            self.add_widget(BoxSVideo())

class BoxNome(BoxLayout):
    pass

class BoxSVideo(BoxLayout):
    pass

class BoxSpinner(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        spinner_values = []
        for pasta in os.listdir(caminho):
            if pasta[0] == '#':
                spinner_values.append(pasta)
        self.ids.spinner_coletanea.values = spinner_values

class BoxNovaCol(BoxLayout):
    pass

class ItemLista(BoxLayout):
    def __init__(self,text='',nome_mapa='',**kwargs):
        super().__init__(**kwargs)
        self.ids.imagembox.source = '../assets/previa_img.jpg'
        for arq in os.listdir(caminho+diretorio+'/'):
            if arq == 'previa_img.jpg':
                self.ids.imagembox.source = '../Salvos/'+diretorio+'/'+arq
                break
        self.ids.listabox.text = text

        self.nome_mapa = nome_mapa
        self.arq_json = caminho+self.nome_mapa+'/info.json'
    
    def on_touch_down(self,touch):
        if touch.is_double_tap:
            if self.collide_point(*touch.pos):
                global mapa_editado, inf
                mapa_editado = self.nome_mapa
                ger.current = 'telaMapa'
                with open(self.arq_json,'r') as j:
                    inf = json.load(j)
                return True
        return super(ItemLista,self).on_touch_down(touch)








#teste = ['Dan',100,100,(0,1,0,1)] #nome,x,y,rgba
#teste2 = ['iel',300,300,(0,0,1,1)]
#num_pin.append(teste)
#num_pin.append(teste2)


click_anterior = None

class Mapa(Screen):
    clicavel = ObjectProperty()

    @mainthread
    def on_pre_enter(self):
        self.ids.image_mapa.source = '../Salvos/'+mapa_editado+'/img_mapa.jpg'

    def on_enter(self):
        self.posiciona_pins()
    
    def on_leave(self):
        self.retira_pins()

    def retira_pins(self):
        global click_anterior
        click_anterior = None
        print(self.ids.pin_layout.children[0].children)
        for w in self.ids.pin_layout.children[0].children:
            self.remove_widget(w)

    def posiciona_pins(self):
        for p in inf["pontos"]:
            num_pin = []
            num_pin.append(inf["pontos"][p]["x"]) #x y nome r g b
            num_pin.append(inf["pontos"][p]["y"])
            num_pin.append(inf["pontos"][p]["nome_pin"])
            num_pin.append(inf["pontos"][p]["r"])
            num_pin.append(inf["pontos"][p]["g"])
            num_pin.append(inf["pontos"][p]["b"])
            self.ids.pin_layout.add_widget(Pin(pos=(num_pin[0],num_pin[1]),pin_name=num_pin[2],cor=(num_pin[3],num_pin[4],num_pin[5]),editable=False))

    def novo_pin(self):
        global click_anterior
        if click_anterior != None:
            self.ids.pin_layout.children[0].remove_widget(self.ids.pin_layout.children[0].children[0])
            self.ids.pin_layout.add_widget(Pin(pos=(coord_touch[0]-7.5,coord_touch[1]),cor=(1,0,0),editable=True))
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
            Color(rgb=self.cor)

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

class MapeiaApp(App):
    def build(self):
        global ger
        ger = Gerenciador()
        return ger
    def corFundo(self):
        Window.clearcolor = (.2,.1,.35,1)

if __name__ == '__main__':
    MapeiaApp().run()