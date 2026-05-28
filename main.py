import os
import json
from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock # Adăugat
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

# --- IMPORTURILE MODULELOR ---
from catalog import EcranCatalog
from mate import EcranMate
from scriere import EcranScriere
from dictare import EcranDictare

# Gestionare cale fișiere pentru Android
if platform == 'android':
    from android.storage import app_storage_path
    APP_STORAGE = app_storage_path()
else:
    APP_STORAGE = os.path.dirname(__file__)

class SecretLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apasari = 0

class EcranGreseli(Screen):
    def on_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10)
        main_layout.add_widget(Label(text="Jurnalul greșelilor", font_size='30sp', size_hint_y=0.1))
        
        scroll = ScrollView()
        lista_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        lista_layout.bind(minimum_height=lista_layout.setter('height'))
        
        cale = os.path.join(APP_STORAGE, "greseli.json")
        
        if os.path.exists(cale):
            with open(cale, "r", encoding="utf-8") as f:
                try:
                    greseli = json.load(f)
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

        btn_back = Button(text="Înapoi", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5})
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'meniu'))
        main_layout.add_widget(btn_back)
        self.add_widget(main_layout)

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
        # ... logica ta de UI ...
        
    def verific_apasari_secrete(self, instance):
        self.click_counter += 1
        if self.click_counter >= 3:
            self.click_counter = 0
            self.manager.current = 'ecran_greseli'

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MayaInvataApp(App):
    def build(self):
        # AICI AM MODIFICAT: Orientarea e setată înainte de orice
        if platform == 'android':
            from jnius import autoclass
            ActivityInfo = autoclass('android.content.pm.ActivityInfo')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT)

        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(EcranMeniu(name='meniu'))
        sm.add_widget(EcranCatalog(name='catalog'))
        sm.add_widget(EcranMate(name='mate'))
        sm.add_widget(EcranScriere(name='scriere'))
        sm.add_widget(EcranDictare(name='dictare'))
        sm.add_widget(EcranGreseli(name='ecran_greseli'))
        return sm

    def on_start(self):
        # AICI AM MODIFICAT: Delay pentru Fullscreen ca să nu crape pe G7
        Clock.schedule_once(self._set_fullscreen, 0.5)

    def _set_fullscreen(self, dt):
        if platform == 'android':
            try:
                from jnius import autoclass
                activity = autoclass('org.kivy.android.PythonActivity').mActivity
                LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
                activity.getWindow().setFlags(LayoutParams.FLAG_FULLSCREEN, LayoutParams.FLAG_FULLSCREEN)
            except:
                pass

if __name__ == '__main__':
    MayaInvataApp().run()
