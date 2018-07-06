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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import grpc
import random
import dsid_pb2
import dsid_pb2_grpc
import pickle
import numpy as np
import pandas as pd
import time

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


def run():
    numOfTestes = 100
    numOfCalls = 5
    matrixDeTestes = np.zeros((numOfCalls,numOfTestes), dtype=np.float)
    channel = grpc.insecure_channel('localhost:50051')
    for i in range(100):
        start_time = time.time() 
        stub = dsid_pb2_grpc.DsidStub(channel)
        response = stub.voidCall(dsid_pb2.Empty())
        matrixDeTestes[0][i] = (time.time() - start_time)

        start_time = time.time()
        longNumber = int(random.choice(range(0,1000000000000000000)))
        response = stub.longCall(dsid_pb2.longRequest(numberRequest=longNumber))
        matrixDeTestes[1][i] = (time.time() - start_time)

        start_time = time.time()
        array = []
        for counter in range(8):
            array.append(int(random.choice(range(0,1000000000000000000))))
        response = stub.eightLongCall(dsid_pb2.eightLongRequest(arrayRequest=array))
        matrixDeTestes[2][i] = (time.time() - start_time)
        
        start_time = time.time()
        string = "enviando"
        response = stub.stringCall(dsid_pb2.stringRequest(nameRequest=string))
        matrixDeTestes[3][i] = (time.time() - start_time)

        start_time = time.time()
        aluno = Aluno(random.choice(range(10)), "Joao")
        serializado = pickle.dumps(aluno)
        response = stub.complexCall(dsid_pb2.complexRequest(alunoRequest=serializado))
        aluno2 = pickle.loads(response.alunoReply)
        matrixDeTestes[4][i] = (time.time() - start_time)
    df = pd.DataFrame(matrixDeTestes, index=("voidCall", "longCall", "eightLongCall", "stringCall", "complexCall"))
    df.to_csv("../Resultados/grpc/grpc_100exec_local.csv")

if __name__ == '__main__':
    run()
