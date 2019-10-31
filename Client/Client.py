from __future__ import print_function

import grpc

import server_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50050')
    stub = server_pb2_grpc.ServerStub(channel)
    for reading in stub.Fetch('Fetch'):
        print(reading.timestamp + ":" + reading.meterusage)



if __name__ == '__main__':
    run()