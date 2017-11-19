from app import app

'''
if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
'''
app.run(host = '0.0.0.0',port = 8888,debug = True)