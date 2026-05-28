import json
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from utils import vorbeste

class EcranScriere(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Buton Înapoi
        anchor_top = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y=0.1)
        btn_back = Button(text="", size_hint=(None, None), size=(60, 60), 
                          background_normal='sageata_inapoi.png', border=(0,0,0,0))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'meniu'))
        anchor_top.add_widget(btn_back)
        self.layout.add_widget(anchor_top)

        # Zona text
        self.lbl_text = Label(text="Apasă butonul pentru un exercițiu!", font_size='30sp', 
                              color=(0.3, 0.1, 0.4, 1), halign='center')
        self.layout.add_widget(self.lbl_text)

        # Container butoane centrate
        self.box_butoane = BoxLayout(orientation='vertical', size_hint=(0.8, 0.4), 
                                     pos_hint={'center_x': 0.5}, spacing=10)
        
        self.btn_generare = Button(text="Exercițiu Nou", size_hint=(1, 1), 
                                   background_color=(0.8, 0.7, 0.9, 1))
        self.btn_generare.bind(on_release=self.genereaza_exercitiu)
        
        self.btn_asculta = Button(text="Ascultă cum se spune", size_hint=(1, 1), 
                                  background_color=(0.4, 0.6, 0.9, 1))
        self.btn_asculta.bind(on_release=self.asculta_textul)
        self.btn_asculta.disabled = True # Dezactivat până avem un text
        
        self.box_butoane.add_widget(self.btn_generare)
        self.box_butoane.add_widget(self.btn_asculta)
        self.layout.add_widget(self.box_butoane)

        self.add_widget(self.layout)
        self.text_curent = ""

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def genereaza_exercitiu(self, *args):
        with open("date_maya.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.text_curent = random.choice(data["scriere"])
        self.lbl_text.text = self.text_curent
        self.btn_asculta.disabled = False # Acum poate asculta

    def asculta_textul(self, *args):
        if self.text_curent:
            vorbeste(self.text_curent)