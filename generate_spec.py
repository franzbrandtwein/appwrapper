"""
Generate buildozer.spec from config.json.
Run this before building or let the CI pipeline run it automatically.
"""
import json
from pathlib import Path


def main():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    pkg = config["package_name"]          # e.g. "de.newages.essen"
    parts = pkg.rsplit(".", 1)
    pkg_domain = parts[0] if len(parts) == 2 else "org.example"
    pkg_name = parts[-1].replace("-", "_")

    orientation = config.get("orientation", "portrait")
    fullscreen = "1" if config.get("fullscreen", False) else "0"
    version = config.get("version", "1.0.0")
    app_name = config["app_name"]

    spec = f"""[app]
title = {app_name}
package.name = {pkg_name}
package.domain = {pkg_domain}
version = {version}
source.dir = .
source.include_exts = py,json
requirements = python3==3.11.5,kivy==2.3.0,android,jnius
orientation = {orientation}
fullscreen = {fullscreen}
p4a.branch = v2024.01.21

[android]
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = False
android.enable_androidx = True
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 0
"""
    Path("buildozer.spec").write_text(spec)
    print(f"buildozer.spec generated for: {app_name} ({pkg})")


if __name__ == "__main__":
    main()
