from buggypedia import app
from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    # Development
    app.run(host='0.0.0.0', port = 6000, debug = True)

    # Production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()