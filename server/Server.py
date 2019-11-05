from concurrent import futures
import time

import grpc

import server_pb2_grpc

import server_pb2

filename = r"meterusage.csv"

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()[1:]
    return [format(line) for line in lines]

def format(line) -> str:
    line = line.strip()
    line = line.split(",")
    line[1] = round(float(line[1]), 2)
    return line

class Server(server_pb2_grpc.ServerServicer):
    def __init__(self, data):
        self.data = data
        self.running = True

    def Fetch(self, request, context):
        #request not currently used but could be extended to query an InfluxDB instance
        for item in self.data:
            reading = self.getReading(item[0], (item[1]))
            yield reading

    def getReading(self, timestamp, reading):
        return server_pb2.reading(timestamp=timestamp, meterusage=reading)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServicer_to_server(Server(self.data), server)
        server.add_insecure_port('localhost:50050')
        server.start()
        try:
            while self.running:
                time.sleep(5)
        except KeyboardInterrupt:
            server.stop(0)

    def stop(self):
        self.running = False

def get_server():
    return Server(read_data(filename))


if __name__ == '__main__':
    get_server().serve()
