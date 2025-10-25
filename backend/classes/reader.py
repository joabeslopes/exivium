import zmq
from classes.recurso_base import RecursoBase

class Reader(RecursoBase):
    def __init__(self, recurso_alvo):
        super().__init__(0, recurso_alvo)
        self.init_sub_img()

    def load_image(self):
        loaded = False
        while self.active:
            try:
                topic, image = self.sub_img_socket.recv_multipart(flags=zmq.NOBLOCK)
                if image:
                    self.image = image
                    loaded = True
            except zmq.Again:
                break

        return loaded

    def close(self):
        self.active = False
        self.sub_img_socket.close()