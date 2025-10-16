import os
import zmq
import atexit

class RecursoBase():
    def __init__(self, id, recurso_alvo):
        self.id = id
        self.recurso_alvo = recurso_alvo
        if os.name == 'nt':  # Windows
            self.zmq_url_in = "tcp://localhost:5555"
            self.zmq_url_out = "tcp://localhost:5556"
        else:
            self.zmq_url_in = "ipc:///tmp/exivium_camera_in.sock"
            self.zmq_url_out = "ipc:///tmp/exivium_camera_out.sock"
        self.context = zmq.Context()
        self.image = None
        self.ativo = True
        atexit.register(self.close)

    def init_send_socket(self):
        self.send_socket = self.context.socket(zmq.PUB)
        self.send_socket.connect(self.zmq_url_in)
        self.send_topic = f"recurso.{self.id}.image".encode()
        self.send_socket.setsockopt(zmq.CONFLATE, 1)
        self.send_socket.setsockopt(zmq.LINGER, 0)
        self.send_socket.setsockopt(zmq.SNDHWM, 2)

    def init_recieve_socket(self):
        self.recieve_socket = self.context.socket(zmq.SUB)
        self.recieve_socket.connect(self.zmq_url_out)
        self.recieve_topic = f"recurso.{self.recurso_alvo}.image".encode()
        self.recieve_socket.setsockopt(zmq.SUBSCRIBE, self.recieve_topic)
        self.recieve_socket.setsockopt(zmq.CONFLATE, 1)
        self.recieve_socket.setsockopt(zmq.LINGER, 0)
        self.recieve_socket.setsockopt(zmq.RCVHWM, 2)

    def load_image(self):
        pass

    def get_image(self):
        return self.image

    def send_image(self):
        self.send_socket.send_multipart([self.send_topic, self.image])

    def close(self):
        self.ativo = False
