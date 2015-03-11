from gevent.wsgi import WSGIServer
from twidder import app
from twidder import WebsocketAppli
from geventwebsocket import WebSocketServer, Resource
import threading


def ws_app():
	WebSocketServer(
		('', 8000),
		Resource({'/websock': WebsocketAppli})
	).serve_forever()

ws_thread = threading.Thread(target = ws_app)
ws_thread.daemon = True
ws_thread.start()


app.debug = True
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()


