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
        result = {}
        result['readings'] = self.getReadings()
        self.write(ReadingEncoder().encode(result))

    def getReadings(self):
        with grpc.insecure_channel('127.0.0.1:50050') as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            request = server_pb2.FetchRequest(s1="Test")
            readings = []
            for reading in stub.Fetch(request):
                readings.append(reading)
            return readings


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


def create_client():
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    start_client()

def start_client():
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    create_client()