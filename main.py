import sys
import json
import os
from pathlib import Path

from PySide6.QtCore import QUrl, Qt, QCoreApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWebView import QtWebView


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    QtWebView.initialize()

    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Material")

    config = load_config()

    QCoreApplication.setApplicationName(config.get("app_name", "AppWrapper"))
    QCoreApplication.setApplicationVersion(config.get("version", "1.0.0"))

    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.setInitialProperties({
        "initialUrl": config.get("url", "about:blank"),
        "appName": config.get("app_name", "AppWrapper"),
        "allowNavigation": config.get("allow_navigation", True),
        "fullscreen": config.get("fullscreen", False),
        "statusBarColor": config.get("status_bar_color", "#000000"),
        "userAgentSuffix": config.get("user_agent_suffix", ""),
    })

    qml_file = Path(__file__).parent / "main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
