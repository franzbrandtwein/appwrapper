"""
Generate buildozer.spec from config.json.
Run this before building or let the CI pipeline run it automatically.

Environment variables (set automatically on GitHub Actions runner):
  ANDROIDSDK  - path to pre-installed Android SDK (e.g. /usr/local/lib/android/sdk)
  ANDROIDNDK  - path to pre-installed NDK
If set, these are written into the spec so Buildozer uses the already-licensed
SDK instead of downloading its own.
"""
import json
import os
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

    # If a pre-licensed SDK is available (CI), pin it in the spec so Buildozer
    # won't download its own SDK and hit an interactive license prompt.
    sdk_path = os.environ.get("ANDROIDSDK", "")
    ndk_path = os.environ.get("ANDROIDNDK", "")
    sdk_lines = ""
    if sdk_path:
        sdk_lines += f"\nandroid.sdk_path = {sdk_path}"
        print(f"  → using pre-installed SDK: {sdk_path}")
    if ndk_path:
        sdk_lines += f"\nandroid.ndk_path = {ndk_path}"
        print(f"  → using pre-installed NDK: {ndk_path}")

    spec = f"""[app]
title = {app_name}
package.name = {pkg_name}
package.domain = {pkg_domain}
version = {version}
source.dir = .
source.include_exts = py,json
requirements = python3==3.11.0,kivy==2.3.0,android,jnius
orientation = {orientation}
fullscreen = {fullscreen}

[android]
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = False
android.enable_androidx = True
android.release_artifact = apk{sdk_lines}

[buildozer]
log_level = 2
warn_on_root = 0
"""
    Path("buildozer.spec").write_text(spec)
    print(f"buildozer.spec generated for: {app_name} ({pkg})")


if __name__ == "__main__":
    main()
