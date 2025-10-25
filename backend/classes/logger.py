import zmq
from classes.recurso_base import RecursoBase
from functions.log import log
from threading import Thread
import time

class Logger(RecursoBase):
    def __init__(self):
        super().__init__(0, "")
        self.init_sub_log()
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        log("Iniciando logger")
        while self.active:
            try:
                btopic, btext = self.sub_log_socket.recv_multipart(flags=zmq.NOBLOCK)
                if btext:
                    topic = btopic.decode("utf-8")
                    text = btext.decode("utf-8")
                    log(f"{topic} - {text}")
            except zmq.Again:
                time.sleep(0.1)
                pass
            except Exception as e:
                print(e)
                return None

    def close(self):
        self.active = False
        self.thread.join(timeout=2)
        self.sub_log_socket.close()