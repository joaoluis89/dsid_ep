import rpyc

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_voidCall(self, request, context):
        return dsid_pb2.Empty()

    def exposed_longCall(self, request, context):
        return dsid_pb2.longReply(numberReply=request.numberRequest + 2)

    def exposed_eightLongCall(self, request, context):
        array = request.arrayRequest
        return dsid_pb2.eightLongReply(arrayReply=array)

    def exposed_stringCall(self, request, context):
        return dsid_pb2.stringReply(nameReply=request.nameRequest + " Bateu")

    def exposed_complexCall(self, request, context):
        aluno = pickle.loads(request.alunoRequest)
        aluno.setNotas(5)
        aluno2 = pickle.dumps(aluno)
        return dsid_pb2.complexReply(alunoReply=aluno2)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()
