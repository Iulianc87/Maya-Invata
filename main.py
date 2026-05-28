import os
import json
from kivy.config import Config
# Forțăm aplicația să ignore rotația automată
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '1280')
from kivy.utils import platform

class MayaInvataApp(App):
    def build(self):
        if platform == 'android':
            from jnius import autoclass
            # Forțăm portretul la nivel de sistem Android
            ActivityInfo = autoclass('android.content.pm.ActivityInfo')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)
        
        return ScreenManager()
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView # Adaugă asta sus la importuri
from kivy.graphics import Color, Rectangle

# --- IMPORTURILE MODULELOR TALE ---
from catalog import EcranCatalog
from mate import EcranMate
from scriere import EcranScriere 
from dictare import EcranDictare

# --- CLASA PENTRU BUTONUL SECRET ---
class SecretLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apasari = 0

# --- ECRANUL DE JURNAL GREȘELI ---
class EcranGreseli(Screen):
    def on_enter(self):
        self.clear_widgets()
        
        # 1. Container principal
        main_layout = BoxLayout(orientation='vertical', padding=10)
        main_layout.add_widget(Label(text="Jurnalul greșelilor", font_size='30sp', size_hint_y=0.1))
        
        # 2. ScrollView pentru a vedea lista lungă de greșeli
        scroll = ScrollView()
        lista_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        lista_layout.bind(minimum_height=lista_layout.setter('height'))
        
        cale = os.path.join(os.path.dirname(__file__), "greseli.json")
        if os.path.exists(cale):
            with open(cale, "r", encoding="utf-8") as f:
                try:
                    greseli = json.load(f)
                    # Eliminăm [-10:] pentru a vedea TOT istoricul
                    for g in greseli: 
                        text_g = f"Exercițiu: {g['ex']} | A pus: {g['gresit']} | Corect: {g['corect']}"
                        lbl = Label(text=text_g, size_hint_y=None, height=40, font_size='16sp')
                        lista_layout.add_widget(lbl)
                except:
                    lista_layout.add_widget(Label(text="Eroare la citirea jurnalului."))
        else:
            lista_layout.add_widget(Label(text="Nu există greșeli salvate.", font_size='20sp'))
        
        scroll.add_widget(lista_layout)
        main_layout.add_widget(scroll)

        # 3. Butonul Înapoi
        btn_back = Button(text="Înapoi", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'meniu'))
        main_layout.add_widget(btn_back)
        
        self.add_widget(main_layout)

# --- CLASA MENIU ---
class ResponsiveIconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True

class EcranMeniu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.click_counter = 0
        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.afiseaza_continut()

    def afiseaza_continut(self):
        self.layout.clear_widgets()
        
        # 1. Cartea (Catalog)
        anchor_carte = AnchorLayout(anchor_x='right', anchor_y='top', size_hint=(0.15, 0.15), pos_hint={'top': 1, 'right': 1})
        btn_cat = ResponsiveIconButton(source='carte.png', size_hint=(0.8, 0.8))
        btn_cat.bind(on_release=lambda x: self.schimba_ecran('catalog'))
        anchor_carte.add_widget(btn_cat)
        self.layout.add_widget(anchor_carte)
        
        # 2. Header cu butonul secret
        header_box = BoxLayout(orientation='vertical', size_hint=(0.8, 0.2), pos_hint={'center_x': 0.5, 'top': 0.95})
        lbl_nume = SecretLabel(text="Bun venit, [b]Maya![/b]", markup=True, font_size='28sp', color=(0.3, 0.1, 0.4, 1))
        lbl_nume.bind(on_release=self.verific_apasari_secrete)
        header_box.add_widget(lbl_nume)
        header_box.add_widget(Label(text="Ce vrei să facem azi?", font_size='22sp', color=(0.4, 0.2, 0.5, 1)))
        self.layout.add_widget(header_box)

        # 3. Butoanele Modulelor
        icons_box = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.7, 0.55), pos_hint={'center_x': 0.5, 'center_y': 0.40})
        for nume in ['mate', 'scriere', 'dictare']:
            btn = ResponsiveIconButton(source=f'{nume}.png', size_hint=(1, 1))
            btn.bind(on_release=lambda x, n=nume: self.schimba_ecran(n))
            anchor = AnchorLayout(anchor_x='center', anchor_y='center')
            anchor.add_widget(btn)
            icons_box.add_widget(anchor)
        self.layout.add_widget(icons_box)

    def verific_apasari_secrete(self, instance):
        self.click_counter += 1
        if self.click_counter >= 3:
            self.click_counter = 0
            self.manager.current = 'ecran_greseli'

    def schimba_ecran(self, nume):
        self.manager.current = nume

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(EcranMeniu(name='meniu'))
        sm.add_widget(EcranCatalog(name='catalog'))
        sm.add_widget(EcranMate(name='mate'))
        sm.add_widget(EcranScriere(name='scriere'))
        sm.add_widget(EcranDictare(name='dictare'))
        sm.add_widget(EcranGreseli(name='ecran_greseli'))
        return sm

if __name__ == '__main__':
    TestApp().run()
