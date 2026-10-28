
[app]
title = Gareth X
package.name = garethx
package.domain = com.garethx.broker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js
version = 1.0
requirements = python3,kivy,requests
orientation = portrait

[buildozer]
log_level = 2

[app:android]
fullscreen = 0
android.api = 33
android.minapi = 21
android.permissions = INTERNET
android.accept_sdk_license_agreement = True
