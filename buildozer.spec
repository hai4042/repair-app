[app]
title = RepairApp
package.name = repairapp
package.domain = com.example

# 强制要求的配置
source.dir = .
version = 1.0.0
orientation = portrait

# 核心依赖
requirements = python3,kivy==2.2.1,requests==2.31.0,pyjnius,android

# Android配置
android.api = 33
android.minapi = 21
android.ndk = 23.1.7779620
android.sdk_path = $HOME/.android
android.ndk_path = $HOME/.android/ndk/23.1.7779620
android.build_tools = 34.0.0
android.accept_sdk_license = True
p4a.sdk = 33
# 构建配置
log_level = 2
android.accept_sdk_license = True