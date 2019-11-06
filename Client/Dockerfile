FROM python:3

RUN mkdir -p /usr/src/app/Client
WORKDIR /usr/src/app/Client
ADD Client.py /usr/src/app/Client/Client.py
ADD server_pb2.py /usr/src/app/Client/server_pb2.py
ADD server_pb2_grpc.py /usr/src/app/Client/server_pb2_grpc.py
add index.html /usr/src/app/Client/index.html

RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install tornado
# RUN chmod 777 /usr/src/app/run.sh
CMD ["python","Client.py"]

