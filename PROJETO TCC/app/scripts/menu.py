import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
#from kivy.core.window import Window
#Window.size = (1280,720)

caminho = '/home/daniel/PROJETO TCC/app/Salvos/'

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
                    self.ids.scrollbox.add_widget(ItemLista(text=pasta))
    
    def limpa_lista(self):
        while True:
            try:
                self.ids.scrollbox.remove_widget(self.ids.scrollbox.children[0])
            except:
                break

class CriaMapa(Screen):
    pass

class ItemLista(BoxLayout):
    def __init__(self,source='',text='',**kwargs):
        super().__init__(**kwargs)
        self.ids.imagembox.source = '../assets/previa_img.jpg'
        for arq in os.listdir(caminho+diretorio+'/'):
            if arq == 'previa_img.jpg':
                self.ids.imagembox.source = '../Salvos/'+diretorio+'/'+arq
                break
        self.ids.listabox.text = text

class MapeiaApp(App):
    def build(self):
        return Gerenciador()

if __name__ == '__main__':
    MapeiaApp().run()