"""AppWrapper – Python Android PWA wrapper using Kivy and Android WebView."""
import json
from pathlib import Path

from kivy.app import App
from kivy.utils import platform


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()


if platform == "android":
    from android.runnable import run_on_ui_thread  # type: ignore
    from jnius import autoclass  # type: ignore

    class AppWrapper(App):
        def build(self):
            from kivy.clock import Clock
            from kivy.uix.widget import Widget
            Clock.schedule_once(self._start_webview, 0)
            return Widget()

        @run_on_ui_thread
        def _start_webview(self, dt):
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            WebView = autoclass("android.webkit.WebView")
            WebViewClient = autoclass("android.webkit.WebViewClient")
            WebSettings = autoclass("android.webkit.WebSettings")

            activity = PythonActivity.mActivity
            wv = WebView(activity)
            settings = wv.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setLoadWithOverviewMode(True)
            settings.setUseWideViewPort(True)
            settings.setBuiltInZoomControls(False)
            settings.setDisplayZoomControls(False)
            settings.setCacheMode(WebSettings.LOAD_DEFAULT)

            suffix = CONFIG.get("user_agent_suffix", "")
            if suffix:
                ua = settings.getUserAgentString()
                settings.setUserAgentString(f"{ua} {suffix}")

            wv.setWebViewClient(WebViewClient())
            wv.loadUrl(CONFIG["url"])
            activity.setContentView(wv)

else:
    # Desktop preview (not the Android target, just for quick testing)
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

