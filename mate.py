import random
import json
import os
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class IconButton(ButtonBehavior, Image):
    pass

class EcranMate(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.incercari_gresite = 0
        self.text_color = (0.2, 0.1, 0.3, 1)

        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def on_enter(self):
        self.scor = 0
        self.intrebare_curenta = 0
        self.total_intrebari = 10

        # Coada echilibrată
        pachet = ['oriz'] * 5 + ['vert'] * 3 + ['problema'] * 1 + ['grila'] * 1
        random.shuffle(pachet)
        self.coada_exercitii = pachet

        cale_json = os.path.join(
            os.path.dirname(__file__),
            "intrebari_grila.json"
        )

        try:
            with open(cale_json, "r", encoding="utf-8") as f:
                self.banca_intrebari = json.load(f)
                random.shuffle(self.banca_intrebari)

        except:
            self.banca_intrebari = [{
                "text": "Eroare!",
                "optiuni": ["1", "2", "3"],
                "corect": "1"
            }]

        self.index_grila = 0

        self.clear_widgets()

        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10
        )

        header = BoxLayout(
            size_hint=(1, 0.12),
            padding=5
        )

        btn_inapoi = IconButton(
            source='sageata_inapoi.png',
            size_hint=(0.18, 1)
        )

        btn_inapoi.bind(
            on_release=lambda x:
            setattr(self.manager, 'current', 'meniu')
        )

        self.lbl_progres = Label(
            text="",
            color=self.text_color,
            font_size='20sp'
        )

        header.add_widget(btn_inapoi)
        header.add_widget(self.lbl_progres)

        self.main_layout.add_widget(header)

        self.container = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=15
        )

        self.main_layout.add_widget(self.container)

        self.add_widget(self.main_layout)

        self.genereaza_exercitiu()

    def genereaza_exercitiu(self):
        self.incercari_gresite = 0

        self.container.clear_widgets()

        if self.intrebare_curenta < self.total_intrebari:

            tip = self.coada_exercitii[self.intrebare_curenta]
            self.intrebare_curenta += 1

            self.lbl_progres.text = (
                f"Exercițiul "
                f"{self.intrebare_curenta}/{self.total_intrebari}"
            )

            if tip == 'grila':
                self.mod_grila()

            elif tip == 'problema':
                self.mod_problema()

            else:
                self.mod_calcul(tip)

        else:
            self.final_test()

    def mod_calcul(self, tip):

        op = random.choice(['+', '-'])

        a = random.randint(10, 50)
        b = random.randint(1, 20)

        if op == '-':
            if a < b:
                a, b = b, a

        self.raspuns_corect = (
            a + b if op == '+' else a - b
        )

        self.text_exercitiu_curent = f"{a} {op} {b}"

        zona_ex = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint=(1, 0.28)
        )

        if tip == 'vert':

            grid = GridLayout(
                cols=1,
                size_hint=(None, None),
                width=180,
                height=180
            )

            grid.add_widget(
                Label(
                    text=str(a),
                    font_size='42sp',
                    color=self.text_color,
                    halign='right'
                )
            )

            grid.add_widget(
                Label(
                    text=f"{op} {b}",
                    font_size='42sp',
                    color=self.text_color,
                    halign='right'
                )
            )

            grid.add_widget(
                Label(
                    text="-----",
                    font_size='42sp',
                    color=self.text_color,
                    halign='right'
                )
            )

            zona_ex.add_widget(grid)

        else:

            lbl_ex = Label(
                text=f"{a} {op} {b} = ?",
                font_size='42sp',
                color=self.text_color,
                halign='center',
                valign='middle',
                text_size=(Window.width * 0.9, None)
            )

            zona_ex.add_widget(lbl_ex)

        self.container.add_widget(zona_ex)

        self.creare_input()

    def mod_grila(self):

        q = self.banca_intrebari[
            self.index_grila % len(self.banca_intrebari)
        ]

        self.text_exercitiu_curent = q["text"]

        self.index_grila += 1

        lbl_q = Label(
            text=q["text"],
            font_size='28sp',
            color=self.text_color,
            size_hint_y=0.3,
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, None)
        )

        self.container.add_widget(lbl_q)

        grid = GridLayout(
            cols=3,
            spacing=10,
            size_hint_y=0.3
        )

        for v in q["optiuni"]:

            btn = Button(
                text=v,
                font_size='24sp',
                background_color=(0.5, 0.3, 0.7, 1)
            )

            btn.bind(
                on_release=lambda x, val=v:
                self.verific_grila(val, q["corect"])
            )

            grid.add_widget(btn)

        self.container.add_widget(grid)

    def mod_problema(self):

        n1 = random.randint(5, 10)
        n2 = random.randint(1, 4)

        self.raspuns_corect = n1 - n2

        self.text_exercitiu_curent = (
            f"Ai {n1} bomboane și mănânci {n2}. "
            f"Câte ți-au rămas?"
        )

        lbl_prob = Label(
            text=(
                f"Ai {n1} bomboane și mănânci {n2}.\n"
                f"Câte ți-au rămas?"
            ),
            font_size='28sp',
            color=self.text_color,
            size_hint_y=0.3,
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, None)
        )

        self.container.add_widget(lbl_prob)

        self.creare_input()

    def creare_input(self):

        self.txt_input = TextInput(
            multiline=False,

            input_filter='int',
            input_type='number',
            keyboard_suggestions=False,

            font_size='36sp',

            halign='center',

            size_hint=(0.55, None),
            height='80dp',

            pos_hint={'center_x': 0.5}
        )

        self.container.add_widget(self.txt_input)

        btn = Button(
            text="Verifică",

            font_size='24sp',

            size_hint=(0.5, None),
            height='65dp',

            pos_hint={'center_x': 0.5},

            background_color=(0.5, 0.3, 0.7, 1)
        )

        btn.bind(
            on_release=lambda x:
            self.verific_calcul(
                self.txt_input.text,
                self.raspuns_corect
            )
        )

        self.container.add_widget(btn)

    def verific_calcul(self, raspuns, corect):

        if str(raspuns) == str(corect):

            self.scor += 1
            self.genereaza_exercitiu()

        else:

            self.incercari_gresite += 1

            if self.incercari_gresite >= 3:

                self.logheaza_greseala(
                    self.text_exercitiu_curent,
                    raspuns,
                    corect
                )

                self.genereaza_exercitiu()

            else:

                self.lbl_progres.text = (
                    f"Mai încearcă! "
                    f"({self.incercari_gresite}/3)"
                )

                self.txt_input.text = ""

    def verific_grila(self, val, corect):

        if str(val) == str(corect):

            self.scor += 1
            self.incercari_gresite = 0

            self.genereaza_exercitiu()

        else:

            self.incercari_gresite += 1

            self.logheaza_greseala(
                self.text_exercitiu_curent,
                val,
                corect
            )

            if self.incercari_gresite >= 3:

                self.incercari_gresite = 0
                self.genereaza_exercitiu()

            else:

                self.lbl_progres.text = (
                    f"Mai încearcă! "
                    f"({self.incercari_gresite}/3)"
                )

    def logheaza_greseala(
        self,
        text_ex,
        raspuns_dat,
        raspuns_corect
    ):

        cale = os.path.join(
            os.path.dirname(__file__),
            "greseli.json"
        )

        data = []

        if os.path.exists(cale):

            try:
                with open(cale, "r", encoding="utf-8") as f:
                    data = json.load(f)

            except:
                data = []

        data.append({
            "ex": text_ex,
            "gresit": raspuns_dat,
            "corect": raspuns_corect
        })

        with open(cale, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def salveaza_scor(self):

        if self.scor < 5:
            animal = "broscuta"

        elif self.scor < 7:
            animal = "veverita"

        elif self.scor < 9:
            animal = "iepuras"

        else:
            animal = "unicorn"

        cale = os.path.join(
            os.path.dirname(__file__),
            "scoruri.json"
        )

        date = {
            "istoric_teste": [],
            "inventar": {}
        }

        if os.path.exists(cale):

            try:
                with open(cale, "r", encoding="utf-8") as f:
                    date = json.load(f)

            except:
                pass

        date["istoric_teste"].append({
            "scor": self.scor,
            "total": self.total_intrebari,
            "animal": animal
        })

        date["inventar"][animal] = (
            date["inventar"].get(animal, 0) + 1
        )

        with open(cale, "w", encoding="utf-8") as f:
            json.dump(date, f, indent=4)

    def final_test(self):

        self.salveaza_scor()

        recompense = {
            "broscuta": "o",
            "veverita": "o",
            "iepuras": "un",
            "unicorn": "un"
        }

        if self.scor < 5:
            animal = "broscuta"

        elif self.scor < 7:
            animal = "veverita"

        elif self.scor < 9:
            animal = "iepuras"

        else:
            animal = "unicorn"

        articol = recompense[animal]

        self.container.clear_widgets()

        lbl_final = Label(
            text=(
                f"Bravo! Scor: {self.scor}\n"
                f"Ai câștigat {articol} {animal}!"
            ),
            color=self.text_color,
            font_size='28sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, None)
        )

        self.container.add_widget(lbl_final)

        btn = Button(
            text="Meniu",

            font_size='22sp',

            size_hint=(0.4, None),
            height='60dp',

            pos_hint={'center_x': 0.5},

            on_release=lambda x:
            setattr(self.manager, 'current', 'meniu')
        )

        self.container.add_widget(btn)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
