import rpyc
import random
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
    conn = rpyc.connect("35.231.207.252", 18861)
    for i in range(100):
        start_time = time.time() 
        conn.root.voidCall()
        matrixDeTestes[0][i] = (time.time() - start_time)

        start_time = time.time()
        longNumber = int(random.choice(range(0,1000000000000000000)))
        response = conn.root.longCall(longVar=longNumber)
        matrixDeTestes[1][i] = (time.time() - start_time)

        start_time = time.time()
        array = []
        for counter in range(8):
            array.append(int(random.choice(range(0,1000000000000000000))))
        response = conn.root.eightLongCall(longArray=array)
        matrixDeTestes[2][i] = (time.time() - start_time)
        
        start_time = time.time()
        stringC = "enviando"
        response = conn.root.stringCall(string=stringC)
        matrixDeTestes[3][i] = (time.time() - start_time)

        start_time = time.time()
        aluno = Aluno(random.choice(range(10)), "Joao")
        serializado = pickle.dumps(aluno)
        response = conn.root.complexCall(serializedObject=serializado)
        aluno2 = pickle.loads(response)
        matrixDeTestes[4][i] = (time.time() - start_time)
    
    df = pd.DataFrame(matrixDeTestes, index=("voidCall", "longCall", "eightLongCall", "stringCall", "complexCall"))
    df.to_csv("../Resultados/rpyc/rpyc_100exec_remoto_externo.csv")

if __name__ == '__main__':
    run()
