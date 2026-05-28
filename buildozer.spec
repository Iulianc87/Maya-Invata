[app]
title = Maya Invata
package.name = maya_invata
package.domain = org.maya
source.include_exts = py,png,jpg,kv,json
version = 0.1

# Adaugă pyjnius aici, este necesar pentru ca Python să comunice cu Android
requirements = python3,kivy,gtts,pygame,pyjnius

android.permissions = INTERNET
android.api = 28
android.minapi = 21
android.ndk = 21b
android.archs = armeabi-v7a

# Asigură-te că ecranul este setat pe landscape dacă așa vrei să ruleze
orientation = portrait