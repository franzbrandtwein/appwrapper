"""
Helper script for generating pysidedeploy.spec and running pyside6-android-deploy.
Called from GitHub Actions with required environment variables set.
"""
import configparser
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    qt_base = os.environ["QT_BASE_DIR"]
    qt_version = os.environ["QT_VERSION"]
    android_sdk = os.environ["ANDROID_SDK_ROOT"]
    android_ndk = os.environ["ANDROID_NDK_ROOT"]
    pyside_wheel = os.environ["PYSIDE_WHEEL"]
    shiboken_wheel = os.environ["SHIBOKEN_WHEEL"]
    arch = os.environ.get("ANDROID_ARCH", "arm64-v8a")
    api_level = os.environ.get("ANDROID_API_LEVEL", "34")

    qt_host = f"{qt_base}/{qt_version}/linux_gcc_64"
    qt_android = f"{qt_base}/{qt_version}/android_{arch.replace('-', '_')}"

    spec = configparser.ConfigParser()
    spec["app"] = {
        "title": config["app_name"],
        "project_dir": ".",
        "source_dir": ".",
        "input_file": "main.py",
        "exec_directory": ".",
    }
    spec["python"] = {
        "python_path": sys.executable,
        "packages": (
            "PySide6.QtCore,"
            "PySide6.QtGui,"
            "PySide6.QtQml,"
            "PySide6.QtQuick,"
            "PySide6.QtQuickControls2,"
            "PySide6.QtWebView"
        ),
        "android_packages": "",
    }
    spec["qt"] = {
        "qt_path": qt_host,
        "android_qt_path": qt_android,
        "modules": "Core,Gui,Qml,Quick,QuickControls2,WebView",
    }
    spec["android"] = {
        "wheel_pyside": pyside_wheel,
        "wheel_shiboken": shiboken_wheel,
        "ndk_path": android_ndk,
        "sdk_path": android_sdk,
        "arch": arch,
        "sdk_version": api_level,
        "package_name": config["package_name"],
    }

    spec_path = Path("pysidedeploy.spec")
    with open(spec_path, "w") as f:
        spec.write(f)

    print(f"=== Generated {spec_path} ===")
    spec_path.read_text() and print(spec_path.read_text())

    result = subprocess.run(
        [
            "pyside6-android-deploy",
            "-c", str(spec_path),
            "--wheel-pyside", pyside_wheel,
            "--wheel-shiboken", shiboken_wheel,
            "--ndk-path", android_ndk,
            "--sdk-path", android_sdk,
            "--verbose",
        ],
        check=False,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
