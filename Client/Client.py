from __future__ import print_function

import grpc
import server_pb2_grpc

from json import JSONEncoder
import server_pb2

import tornado.ioloop
import tornado.web
import tornado.escape
import json

class Client(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

    def post(self):  # could be extended to send query to DB
        with grpc.insecure_channel('localhost:50050') as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            request = server_pb2.FetchRequest(s1="Test")
            readings = []
            for reading in stub.Fetch(request):
                readings.append(reading)
            result = {}
            result['readings'] = readings
            self.write(json.dumps(ReadingEncoder().encode(result), sort_keys=True, indent=3))


class ReadingEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, server_pb2.reading):
            dic = {"timestamp": object.timestamp, "usage": round(object.meterusage, 2)}
            return dic
        else:
            return json.JSONEncoder.default(self, object)

def make_app():
    return tornado.web.Application([
        (r"/", Client),
    ])

if __name__ == '__main__':
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
