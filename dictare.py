import json
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from utils import vorbeste

class EcranDictare(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Fundal unitar
        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Buton Înapoi
        anchor_top = AnchorLayout(anchor_x='left', anchor_y='top', size_hint_y=0.1)
        btn_back = Button(text="", size_hint=(None, None), size=(60, 60), 
                          background_normal='sageata_inapoi.png', border=(0,0,0,0))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'meniu'))
        anchor_top.add_widget(btn_back)
        self.layout.add_widget(anchor_top)

        # Zona de afișare text
        self.lbl_status = Label(text="Apasă pentru a începe!", font_size='30sp', 
                                color=(0.3, 0.1, 0.4, 1), halign='center')
        self.layout.add_widget(self.lbl_status)

        # Buton Start
        self.btn_actiune = Button(text="Ascultă dictarea", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5},
                                  background_color=(0.8, 0.7, 0.9, 1))
        self.btn_actiune.bind(on_release=self.porneste_dictare)
        self.layout.add_widget(self.btn_actiune)

        self.add_widget(self.layout)
        self.cuvant_curent = ""
        self.box_butoane = None # Container pentru butoanele de control

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def incarca_text_nou(self):
        with open("date_maya.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.cuvant_curent = random.choice(data["dictare"])

    def porneste_dictare(self, *args):
        self.incarca_text_nou()
        self.lbl_status.text = "Scrie pe caiet..."
        vorbeste(self.cuvant_curent)
        
        # Eliminăm butonul de start
        self.layout.remove_widget(self.btn_actiune)
        
        # Container pentru butoanele de control (centrate)
        self.box_butoane = BoxLayout(orientation='vertical', size_hint=(0.8, 0.3), 
                                     pos_hint={'center_x': 0.5}, spacing=10)
        
        btn_asculta_iar = Button(text="Ascultă din nou", size_hint=(1, 1), 
                                 background_color=(0.4, 0.6, 0.9, 1))
        btn_asculta_iar.bind(on_release=lambda x: vorbeste(self.cuvant_curent))
        
        btn_verifica = Button(text="Am scris! Vreau să verific.", size_hint=(1, 1), 
                              background_color=(0.3, 0.8, 0.3, 1)) # Verde
        btn_verifica.bind(on_release=self.afiseaza_textul)
        
        self.box_butoane.add_widget(btn_asculta_iar)
        self.box_butoane.add_widget(btn_verifica)
        self.layout.add_widget(self.box_butoane)

    def afiseaza_textul(self, *args):
        # Afișăm textul imediat
        self.lbl_status.text = f"Textul era:\n{self.cuvant_curent}"
        # Apoi pornim vocea
        vorbeste(self.cuvant_curent)
        
        # Curățăm zona de butoane dacă există
        if self.box_butoane:
            self.layout.remove_widget(self.box_butoane)
            self.box_butoane = None
        
        # Adăugăm butonul de reluare
        self.btn_actiune.text = "Altă propoziție"
        self.layout.add_widget(self.btn_actiune)