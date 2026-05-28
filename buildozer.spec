[app]
title = Maya Invata
package.name = mayainvata
package.domain = org.mayainvata
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0
requirements = python3,kivy,plyer,pyjnius,android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
fullscreen = 0
android.orientation = portrait
android.manifest.orientation = portrait

# Compatibilitate G7/J4+
android.archs = armeabi-v7a

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 23b
android.build_tools_version = 33.0.0

[buildozer]
log_level = 2
warn_on_root = 1
