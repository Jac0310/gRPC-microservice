from concurrent import futures
import time

import grpc

import os

import server_pb2_grpc

import server_pb2

filename = r"meterusage.csv"

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()[1:]
    return lines

def format(line) -> str:
    line = line.strip()
    return line.split(",")

class Server(server_pb2_grpc.ServerServicer):

    def __init__(self, data):
        self.data = data

    def Fetch(self, request, context):
        for item in self.data:
            item = format(item)
            reading = self.getReading(item[0], float(item[1]))
            yield reading

    def getReading(self, timestamp, reading):
        return server_pb2.reading(timestamp=timestamp, meterusage=reading)



    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServicer_to_server(Server(self.data), server)
        server.add_insecure_port('localhost:50050')
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    # cwd = os.getcwd()
    # files = os.listdir(cwd)  # Get all the files in that directory
    # print("Files in %r: %s" % (cwd, files))
    server = Server(read_data(r"server/meterusage.csv"))
    server.serve()



