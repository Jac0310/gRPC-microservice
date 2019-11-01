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
        self.render("index.html", function=self.post())

    def post(self):
        with grpc.insecure_channel('localhost:50050') as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            request = server_pb2.FetchRequest(s1="Test")
            readings = []
            for reading in stub.Fetch(request):
                readings.append(reading)
            self.write(ReadingEncoder().encode(readings))


class ReadingEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, server_pb2.reading):
            dic = {"timestamp": object.timestamp, "usage": object.meterusage}
            return dic
        else:
            return json.JSONEncoder.default(self, object)

def make_app():
    return tornado.web.Application([
        (r"/", Client),
    ])

# def formatresponse(time, usage)->str:
#     return "{" + 'timestamp:  "{time}", usage:  "{use}"'.format(time=time, use=str(usage)) + "}"
if __name__ == '__main__':
    app = make_app()
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(443)
    # tornado.ioloop.IOLoop.instance().start()

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()