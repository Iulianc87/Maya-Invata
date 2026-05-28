[app]

# (str) Titlul aplicației tale
title = Maya Invata

# (str) Numele pachetului (trebuie să fie unic)
package.name = mayainvata

# (str) Domeniul pachetului
package.domain = org.mayainvata

# (str) Folderul sursă (punctul înseamnă folderul curent)
source.dir = .

# (list) Extensiile fișierelor incluse (am adăugat json)
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (str) Versiunea aplicației
version = 1.0

# (list) Dependențe necesare (am adăugat android și pyjnius)
requirements = python3,kivy,plyer,pyjnius,android

# (list) Permisiuni necesare pentru scriere fișiere și rețea
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Ecran complet (0 = nu, 1 = da)
fullscreen = 0

# (str) Orientare forțată (portrait)
android.orientation = portrait
android.manifest.orientation = portrait

# (list) Arhitecturi procesor pentru compatibilitate (G7 și telefoane noi)
android.archs = armeabi-v7a, arm64-v8a

# (int) Versiuni API (stabile pentru 2026)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0

# (list) Iconițe și splash screen (opțional - dacă le ai în folder)
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]
# (int) Log level (2 = debug, util pentru a vedea erorile)
log_level = 2
warn_on_root = 1
