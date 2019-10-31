from __future__ import print_function

import grpc

import logging

import server_pb2_grpc

import server_pb2

class Client():
    def run(self):
        with grpc.insecure_channel('localhost:50050') as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            request = server_pb2.FetchRequest(s1="Test")
            for reading in stub.Fetch(request):
                print(reading.timestamp + ":" + reading.meterusage)


if __name__ == '__main__':
    client = Client()
    client.run()