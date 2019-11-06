FROM python:3

RUN mkdir -p /usr/src/app/Server
WORKDIR /usr/src/app/Server
ADD Server.py /usr/src/app/Server/Server.py
ADD server_pb2.py /usr/src/app/Server/server_pb2.py
ADD server_pb2_grpc.py /usr/src/app/Server/server_pb2_grpc.py
add meterusage.csv /usr/src/app/Server/meterusage.csv

RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install tornado

CMD ["python","Server.py"]

