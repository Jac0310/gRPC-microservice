from concurrent import futures
import time

import grpc

import server_pb2_grpc

filename = r"meterusage.csv"

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Server(server_pb2_grpc.ServerServicer):
    def Fetch(self, request, context):
        with open(filename) as f:
            lines = f.readlines()[1:]

        for line in lines:
            yield server_pb2.reading(line[0], float(line[1].strip()))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
