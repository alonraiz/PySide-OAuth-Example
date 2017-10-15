import sys
from urllib import urlencode
from PySide import QtCore
from PySide import QtWebKit
from PySide.QtGui import QApplication

ClientId = ''
ClientSecret = ''
RedirectUrl = 'localhost/callback'
RedirectScheme = 'http://'
Scopes = ['user_read', 'channel_subscriptions', 'channel_check_subscription', 'user_subscriptions', 'channel_editor',
          'chat_login']

ResponseType = 'code'

Headers = {'client_id': ClientId, 'redirect_uri': RedirectScheme+RedirectUrl, 'response_type': ResponseType,
           'scope': str.join(' ', Scopes)}

AuthUrl = 'https://api.twitch.tv/kraken/oauth2/authorize?{headers}'.format(
    headers=urlencode(Headers))

class LoginWindow(QtWebKit.QWebView):


    def __init__(self, app):
        super(LoginWindow, self).__init__()

        self.nam = self.page().networkAccessManager()
        self.nam.finished.connect(self.checkResponse)
        self.app = app
        self.load(QtCore.QUrl(AuthUrl))
        self.show()

    def checkResponse(self, reply):
        request = reply.request()
        print request.url()

        if (request.url().host()+request.url().path()) == RedirectUrl:
            for item in request.url().queryItems():
                if item[0] == 'code':
                    print('OAuth code is {code}'.format(code=item[1]))
                    self.app.quit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = LoginWindow(app)
