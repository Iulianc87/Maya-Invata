[app]
title = Maya Invata
package.name = maya_invata
package.domain = org.maya

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf

version = 0.1

requirements = python3,kivy==2.2.1

orientation = portrait

fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

presplash.color = #f2e6f5

[buildozer]
log_level = 2
