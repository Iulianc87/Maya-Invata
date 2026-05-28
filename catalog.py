import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle

class ResponsiveIconButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True

class EcranCatalog(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_enter = self.incarca_date  # Reîncărcăm datele la fiecare intrare
        with self.canvas.before:
            Color(0.95, 0.90, 0.96, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def incarca_date(self):
        self.clear_widgets()
        main_layout = FloatLayout()
        
        # 1. Citim fișierul corect
        try:
            with open("scoruri.json", "r", encoding="utf-8") as f:
                date_salvate = json.load(f)
            # Extragem doar dicționarul de inventar
            inventar = date_salvate.get("inventar", {})
        except:
            inventar = {"unicorn": 0, "iepuras": 0, "veverita": 0, "broscuta": 0}

        content = BoxLayout(orientation='vertical', padding=[20, 80, 20, 20], spacing=10)
        content.add_widget(Label(text="[b]Catalogul meu cu prieteni[/b]", markup=True, font_name='scoalamaya', 
                                   font_size='32sp', color=(0.3, 0.1, 0.4, 1), size_hint_y=0.2))

        grid = GridLayout(cols=2, spacing=20)
        animale = [
            {'nume': 'unicorn', 'titlu': 'Unicorni'},
            {'nume': 'iepuras', 'titlu': 'Iepurași'},
            {'nume': 'veverita', 'titlu': 'Veverițe'},
            {'nume': 'broscuta', 'titlu': 'Broscuțe'}
        ]

        for a in animale:
            box = BoxLayout(orientation='vertical', spacing=5)
            # Asigură-te că imaginile există în folder (unicorn.png etc.)
            box.add_widget(Image(source=f"{a['nume']}.png"))
            
            # 2. Folosim dicționarul 'inventar' extras mai sus
            nr = inventar.get(a['nume'], 0) 
            
            box.add_widget(Label(text=f"[b]{nr} {a['titlu']}[/b]", markup=True, font_name='scoalamaya', 
                                   font_size='24sp', color=(0.3, 0.1, 0.4, 1), size_hint_y=0.2))
            grid.add_widget(box)
            
        content.add_widget(grid)
        main_layout.add_widget(content)
        
        anchor_exit = AnchorLayout(anchor_x='left', anchor_y='top', size_hint=(0.15, 0.15), pos_hint={'top': 1, 'left': 1})
        btn_exit = ResponsiveIconButton(source='sageata_inapoi.png', size_hint=(0.6, 0.6))
        btn_exit.bind(on_release=lambda x: setattr(self.manager, 'current', 'meniu'))
        anchor_exit.add_widget(btn_exit)
        main_layout.add_widget(anchor_exit)
        self.add_widget(main_layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos