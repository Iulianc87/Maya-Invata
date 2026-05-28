[app]
title = Maya Invata
package.name = mayainvata
package.domain = org.mayainvata
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0
requirements = python3,kivy,plyer

# Permisiuni
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Setări grafice
fullscreen = 0
android.orientation = portrait
android.manifest.orientation = portrait

# Compatibilitate pentru ambele procesoare (G7 și S26 Ultra)
android.archs = armeabi-v7a, arm64-v8a

# Setări API stabile
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.build_tools_version = 33.0.0

[buildozer]
log_level = 2
warn_on_root = 1
