import zmq
from classes.recurso_base import RecursoBase
from functions.log import log

class Reader(RecursoBase):
    def __init__(self, recurso_alvo):
        super().__init__(0, recurso_alvo)
        self.init_recieve_socket()

    def load_image(self):
        loaded = False
        try:
            topico, image = self.recieve_socket.recv_multipart(flags=zmq.NOBLOCK)
            if image:
                self.image = image
                loaded = True
        except Exception as e:
            loaded = False

        return loaded

    def close(self):
        log(f"Encerrando reader {self.id}")
        self.ativo = False
        self.recieve_socket.close()