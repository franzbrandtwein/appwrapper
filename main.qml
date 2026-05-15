import QtQuick
import QtQuick.Controls.Material
import QtWebView

ApplicationWindow {
    id: root
    visible: true
    width: 400
    height: 800
    title: appName

    // Properties set from Python via setInitialProperties
    property string initialUrl: "about:blank"
    property string appName: "AppWrapper"
    property bool allowNavigation: true
    property bool fullscreen: false
    property string statusBarColor: "#000000"
    property string userAgentSuffix: ""

    visibility: fullscreen ? Window.FullScreen : Window.AutomaticVisibility

    Material.theme: Material.Dark
    Material.primary: statusBarColor

    WebView {
        id: webView
        anchors.fill: parent
        url: initialUrl

        onLoadingChanged: function(loadRequest) {
            if (loadRequest.status === WebView.LoadFailedStatus) {
                errorView.visible = true
                errorText.text = "Fehler beim Laden:\n" + loadRequest.errorString
            } else {
                errorView.visible = false
            }
        }

        onUrlChanged: {
            if (!allowNavigation) {
                // Block external navigation, stay on initial URL
                var currentHost = new URL(url.toString()).hostname
                var initialHost = new URL(initialUrl).hostname
                if (currentHost !== initialHost) {
                    webView.url = initialUrl
                }
            }
        }
    }

    // Error overlay
    Rectangle {
        id: errorView
        visible: false
        anchors.fill: parent
        color: "#1a1a2e"

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                id: errorText
                color: "white"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                width: root.width * 0.8
            }

            Button {
                text: "Erneut versuchen"
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    errorView.visible = false
                    webView.url = initialUrl
                }
            }
        }
    }

    // Loading indicator
    Rectangle {
        id: loadingOverlay
        anchors.fill: parent
        color: "#1a1a2e"
        visible: webView.loading

        BusyIndicator {
            anchors.centerIn: parent
            running: parent.visible
        }

        Text {
            anchors {
                top: parent.verticalCenter
                topMargin: 50
                horizontalCenter: parent.horizontalCenter
            }
            text: "Wird geladen…"
            color: "white"
            font.pixelSize: 14
        }
    }
}
