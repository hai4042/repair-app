[app]
title = RepairApp
package.name = repairapp
package.domain = com.example
source.dir = .
version = 1.0.0
orientation = portrait

# 核心依赖（已添加版本锁定）
requirements = 
    python3==3.8.5,
    kivy==2.2.1,
    requests==2.31.0,
    pyjnius,
    android,
    urllib3,
    chardet,
    idna,
    cython==0.29.32

# Android配置（国内镜像加速）
android.api = 33
android.minapi = 21
android.ndk = 23.1.7779620
android.sdk_path = /home/runner/.android
android.ndk_path = /home/runner/.android/ndk/23.1.7779620
android.build_tools = 34.0.0
android.accept_sdk_license = True
p4a.sdk = 33
android.arch = armeabi-v7a
android.permissions = INTERNET

# 构建优化配置
[buildozer]
log_level = 2
pypi_mirror = https://pypi.tuna.tsinghua.edu.cn/simple
warn_on_root = 0