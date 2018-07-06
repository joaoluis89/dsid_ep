import rpyc
import pickle

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

class Servico(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_voidCall(self):
        pass

    def exposed_longCall(self, longVar):
        return longVar + 2

    def exposed_eightLongCall(self, longArray):
        array = longArray
        return array

    def exposed_stringCall(self, string):
        return string + " Bateu"

    def exposed_complexCall(self, serializedObject):
        aluno = pickle.loads(serializedObject)
        aluno.setNotas(5)
        aluno2 = pickle.dumps(aluno)
        return aluno2

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Servico, port=18861)
    t.start()
