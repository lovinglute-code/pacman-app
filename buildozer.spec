[app]

# (str) Title of your application
title = Pacman Game

# (str) Package name
package.name = pacmanapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.pacman

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ttf

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,pygame

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

#
# Android Specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for android toolchain)
android.presplash_color = #000000

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
# GitHub Actions 오류 방지를 위해 자동 설정(주석 처리)
#android.api = 31

# (int) Minimum API your APK will support.
#android.minapi = 21

# (int) Android SDK version to use
# GitHub Actions 오류 방지를 위해 자동 설정(주석 처리)
#android.sdk = 33

# (str) Android NDK version to use
# GitHub Actions 오류 방지를 위해 자동 설정(주석 처리)
#android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to exclude from the compilation
#android.skip_update_options = path/to/exclude/*

# (bool) Force the build system to use the NDK from the environment
#android.force_build_tools = False

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# 호환성을 위해 v7a와 v8a 둘 다 포함하는 것이 좋습니다.
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) Skip byte compile for .py files
# android.no-byte-compile-python = False

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters = intent_filters.xml

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (str) screenOrientation to set for the main activity.
#android.manifest.orientation = landscape

# (bool) Indicate whether the screen should stay on
# Don't sleep while playing the game
android.wakelock = True

# (str) The format used to package the app for release mode (aab or apk or aar).
# android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
# android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) Bootstrap to use for android builds
# Pygame 사용 시 sdl2 필수
p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 

# (int) Webview content port number to specify an explicit --webview-port= p4a argument
#p4a.webview_port = 

#
# iOS Specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# (str) Name of the certificate to use for signing the debug version
#ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
#ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

# -----------------------------------------------------------------------------
# List as sections
#
# You can define all the "list" as [section:key].
# Each line will be considered as a option to the list.
# Let's take [app] / source.exclude_patterns.
# Instead of doing:
#
#     [app]
#     source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
# This can be translated to:
#
#     [app:source.exclude_patterns]
#     license
#     data/audio/*.wav
#     data/images/original/*
#
