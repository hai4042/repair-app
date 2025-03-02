[app]
title = RepairApp
package.name = repairapp
package.domain = com.example

# 强制要求的配置
source.dir = .
version = 1.0.0
orientation = portrait

# 核心依赖
requirements = python3,kivy==2.2.1,requests==2.31.0,pyjnius,android,cryptography

# Android配置
android.api = 33
android.minapi = 21
android.sdk_path = /home/runner/work/repair-app/repair-app/android-sdk
android.ndk = 25.2.9519653
android.ndk_path = /home/runner/work/repair-app/repair-app/android-sdk/ndk/25.2.9519653
android.build_tools = 34.0.0
android.accept_sdk_license = True

# 构建配置
log_level = 2
p4a.branch = 2023.09.16