
from server.Server import *
from Client.Client import *

import threading

app = create_client()
server = get_server()

def setUp():
    serverThread = threading.Thread(target=server.serve)
    serverThread.start()


def testServer1(server):
    assert server.data[0][1] == 55.09
    assert server.data[4][1] == 55.77
    assert server.data[4][0] == '2019-01-01 01:15:00'

def testServer2(server):
    assert isinstance(server_pb2.reading, server.getReading('2019-01-01 05:15:00', 63.52))


def testServerClient():
    ## go to http://localhost:8888/
    ## ensure JSON data is pulled when button is pressed
    assert True

if __name__ == '__main__':
    setUp()
    testServer1(server)
    testServer2(server)
    testServerClient()
    stop_client()
    server.stop()

