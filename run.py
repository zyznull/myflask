from app import app
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)
app.run(host = '0.0.0.0',port = 8888,debug = True)