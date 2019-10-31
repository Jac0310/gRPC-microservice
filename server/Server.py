from concurrent import futures
import time

import grpc

import server_pb2_grpc

#import server_pb2

filename = r"meterusage.csv"

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Server(server_pb2_grpc.ServerServicer):
    def Fetch(self, request, context):
        print("request.s1")

        with open(r"meterusage.csv") as f:
            lines = f.readlines()[1:]

        for line in lines:
            line = line.split(",")
            reading = self.getReading(line[0], float(line[1].strip()))
            print (reading.timestamp + " : " + str(reading.meterusage))
            yield reading

    def getReading(self, timestamp, reading):
        return server_pb2.reading(timestamp=timestamp, meterusage=reading)





    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServicer_to_server(Server(), server)
        server.add_insecure_port('localhost:50050')
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    server = Server()
    server.serve()
    #for reading in server.Fetch("", ""):
        #print(reading.timestamp + " : " + str(reading.meterusage))



