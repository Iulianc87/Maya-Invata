import json
import random

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle


class EcranDictare(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        # ---------------- BUTON ÎNAPOI ----------------

        anchor_top = AnchorLayout(
            anchor_x='left',
            anchor_y='top',
            size_hint_y=0.1
        )

        btn_back = Button(
            text="",

            size_hint=(None, None),
            size=(55, 55),

            background_normal='sageata_inapoi.png',

            border=(0, 0, 0, 0)
        )

        btn_back.bind(
            on_release=lambda x:
            setattr(self.manager, 'current', 'meniu')
        )

        anchor_top.add_widget(btn_back)

        self.layout.add_widget(anchor_top)

        # ---------------- TEXT PRINCIPAL ----------------

        self.lbl_status = Label(
            text="Apasă pentru a începe!",

            font_size='28sp',

            color=(0.3, 0.1, 0.4, 1),

            halign='center',
            valign='middle',

            text_size=(Window.width * 0.9, None),

            size_hint=(1, 0.45)
        )

        self.layout.add_widget(self.lbl_status)

        # ---------------- BUTON START ----------------

        self.btn_actiune = Button(
            text="Începe dictarea",

            font_size='22sp',

            size_hint=(0.7, None),
            height='65dp',

            pos_hint={'center_x': 0.5},

            background_color=(0.8, 0.7, 0.9, 1)
        )

        self.btn_actiune.bind(
            on_release=self.porneste_dictare
        )

        self.layout.add_widget(self.btn_actiune)

        self.add_widget(self.layout)

        self.cuvant_curent = ""
        self.box_butoane = None

    def _update_rect(self, *args):

        self.rect.size = self.size
        self.rect.pos = self.pos

    def incarca_text_nou(self):

        with open(
            "date_maya.json",
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        self.cuvant_curent = random.choice(
            data["dictare"]
        )

    def porneste_dictare(self, *args):

        self.incarca_text_nou()

        # momentan adultul citește
        self.lbl_status.text = (
            "Adultul citește propoziția.\n"
            "Copilul scrie pe caiet."
        )

        if self.btn_actiune.parent:
            self.layout.remove_widget(self.btn_actiune)

        self.box_butoane = BoxLayout(
            orientation='vertical',

            size_hint=(0.85, 0.3),

            pos_hint={'center_x': 0.5},

            spacing=12
        )

        btn_aratadinou = Button(
            text="Arată din nou",

            font_size='22sp',

            size_hint=(1, None),
            height='65dp',

            background_color=(0.4, 0.6, 0.9, 1)
        )

        btn_aratadinou.bind(
            on_release=lambda x:
            setattr(
                self.lbl_status,
                'text',
                self.cuvant_curent
            )
        )

        btn_verifica = Button(
            text="Am scris! Vreau să verific.",

            font_size='20sp',

            size_hint=(1, None),
            height='65dp',

            background_color=(0.3, 0.8, 0.3, 1)
        )

        btn_verifica.bind(
            on_release=self.afiseaza_textul
        )

        self.box_butoane.add_widget(btn_aratadinou)
        self.box_butoane.add_widget(btn_verifica)

        self.layout.add_widget(self.box_butoane)

    def afiseaza_textul(self, *args):

        self.lbl_status.text = (
            f"Textul era:\n\n{self.cuvant_curent}"
        )

        if self.box_butoane:

            self.layout.remove_widget(
                self.box_butoane
            )

            self.box_butoane = None

        self.btn_actiune.text = "Altă propoziție"

        self.layout.add_widget(self.btn_actiune)
