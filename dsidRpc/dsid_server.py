# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time
import pickle

import grpc

import dsid_pb2
import dsid_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Aluno(object):
    """docstring for Aluno"""
    def __init__(self, notas, nome):
        super(Aluno, self).__init__()
        self.notas = notas
        self.nome = nome

    def getNome(self):
        return self.nome

    def getNotas(self):
        return self.notas

    def setNotas(self, notas):
        self.notas = notas

class Dsid(dsid_pb2_grpc.DsidServicer):

    def voidCall(self, request, context):
        return dsid_pb2.Empty()

    def longCall(self, request, context):
        return dsid_pb2.longReply(numberReply=request.numberRequest + 2)

    def eightLongCall(self, request, context):
        array = request.arrayRequest
        return dsid_pb2.eightLongReply(arrayReply=array)

    def stringCall(self, request, context):
        return dsid_pb2.stringReply(nameReply=request.nameRequest + " Bateu")

    def complexCall(self, request, context):
        aluno = pickle.loads(request.alunoRequest)
        aluno.setNotas(5)
        aluno2 = pickle.dumps(aluno)
        return dsid_pb2.complexReply(alunoReply=aluno2)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dsid_pb2_grpc.add_DsidServicer_to_server(Dsid(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
