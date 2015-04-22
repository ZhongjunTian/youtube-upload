from PyQt4 import QtCore, QtGui, QtWebKit

CHECK_AUTH_JS = """
    var code = document.getElementById("code");
    var access_denied = document.getElementById("access_denied");
    var result;
    
    if (code) {
        result = {authorized: true, code: code.value};
    } else if (access_denied) {
        result = {authorized: false, message: access_denied.innerText};
    } else {
        result = {};
    }
    result;
"""

def _on_qt_page_load_finished(dialog, webview):
    to_s = lambda x: (str(x.toUtf8()) if isinstance(x, QtCore.QString) else x)
    frame = webview.page().currentFrame()
    jscode = QtCore.QString(CHECK_AUTH_JS)
    res = frame.evaluateJavaScript(jscode)
    authorization = dict((to_s(k), to_s(v)) for (k, v) in res.toPyObject().items())
    if authorization.has_key("authorized"):
        dialog.authorization_code = authorization.get("code")
        dialog.close()
   
def get_code(url, size=(640, 480), title="Google authentication"):
    """Open a QT webkit window and return the access code."""
    app = QtGui.QApplication([])
    dialog = QtGui.QDialog()
    dialog.setWindowTitle(title)
    dialog.resize(*size)
    webview = QtWebKit.QWebView()
    webpage = QtWebKit.QWebPage()
    webview.setPage(webpage)           
    webpage.loadFinished.connect(lambda: _on_qt_page_load_finished(dialog, webview))
    webview.setUrl(QtCore.QUrl.fromEncoded(url))
    layout = QtGui.QGridLayout()
    layout.addWidget(webview)
    dialog.setLayout(layout)
    dialog.authorization_code = None
    dialog.show()
    app.exec_()
    return dialog.authorization_code
