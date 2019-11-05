FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD Client/Client.py /usr/src/app/Client.py
ADD server/Server.py /usr/src/app/Server.py
ADD server/server_pb2.py /usr/src/app/server_pb2.py
ADD server/server_pb2_grpc.py /usr/src/app/server_pb2_grpc.py
ADD server/meterusage.csv /usr/src/app/meterusage.csv
# ADD run.sh /usr/local/bin/run.sh
ADD run.sh /usr/src/app/run.sh
RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install tornado
RUN chmod 777 /usr/src/app/run.sh
CMD /usr/src/app/run.sh

