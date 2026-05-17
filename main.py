"""AppWrapper – Python Android PWA wrapper using Kivy and Android WebView."""
import json
import os
from pathlib import Path

from kivy.app import App
from kivy.utils import platform


def load_config() -> dict:
    # Try multiple locations (Buildozer places assets differently per version)
    candidates = [
        Path(__file__).parent / "config.json",
        Path(os.environ.get("ANDROID_APP_PATH", ".")) / "config.json",
    ]
    for p in candidates:
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    # Hard fallback so the app doesn't crash silently
    return {"url": "https://essen.new-ages.de/", "app_name": "AppWrapper"}


CONFIG = load_config()


if platform == "android":
    from android.runnable import run_on_ui_thread  # type: ignore
    from jnius import autoclass  # type: ignore

    # Load classes once at module level (safer than inside a scheduled callback)
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    WebView = autoclass("android.webkit.WebView")
    WebViewClient = autoclass("android.webkit.WebViewClient")
    WebSettings = autoclass("android.webkit.WebSettings")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")

    @run_on_ui_thread
    def _create_webview(url):
        """Create and display the WebView, called directly on the Android UI thread."""
        activity = PythonActivity.mActivity
        wv = WebView(activity)
        settings = wv.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        settings.setBuiltInZoomControls(False)
        settings.setDisplayZoomControls(False)
        settings.setMixedContentMode(0)  # MIXED_CONTENT_ALWAYS_ALLOW
        settings.setCacheMode(WebSettings.LOAD_DEFAULT)

        suffix = CONFIG.get("user_agent_suffix", "")
        if suffix:
            ua = settings.getUserAgentString()
            settings.setUserAgentString(f"{ua} {suffix}")

        wv.setWebViewClient(WebViewClient())
        wv.loadUrl(url)

        # addContentView overlays on top of Kivy without destroying GL surface
        activity.addContentView(
            wv,
            LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT),
        )

    class AppWrapper(App):
        def build(self):
            from kivy.uix.widget import Widget
            # Schedule on the next frame so Kivy window is fully initialised
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: _create_webview(CONFIG["url"]), 1)
            return Widget()

else:
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label

    class AppWrapper(App):
        title = CONFIG.get("app_name", "AppWrapper")

        def build(self):
            box = BoxLayout(orientation="vertical")
            box.add_widget(Label(
                text=f"[b]{CONFIG.get('app_name', 'AppWrapper')}[/b]\n\n{CONFIG['url']}",
                markup=True,
                halign="center",
            ))
            return box


def main():
    AppWrapper().run()


if __name__ == "__main__":
    main()

