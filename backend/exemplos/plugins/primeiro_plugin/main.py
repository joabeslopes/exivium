from recurso_base import RecursoBase
import cv2
import sys
import numpy as np
import zmq
import time

#TODO variavel de ambiente
JPEG_QUALITY = 70
FPS = 30

class PrimeiroPlugin(RecursoBase):
    def __init__(self, id, recurso_alvo):
        super().__init__(id, recurso_alvo)
        self.init_recieve_socket()
        self.init_send_socket()

    def load_image(self):
        loaded = False
        try:
            topic, image = self.recieve_socket.recv_multipart(flags=zmq.NOBLOCK)
            frame_array = np.frombuffer(image, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            loaded, buffer = cv2.imencode(".jpg", gray_image, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            if loaded:
                self.image = buffer.tobytes()
        except zmq.Again:
            loaded = False
        except Exception as e:
            loaded = False
            self.close()

        return loaded

    def close(self):
        print(f"Parando plugin {self.id}")
        self.ativo = False
        self.send_socket.close()
        self.recieve_socket.close()


def main(id, target):
    print(f'Rodando plugin exemplo na camera {target}')

    reader = PrimeiroPlugin(id, target)
    while reader.ativo:
        try:
            if reader.load_image():
                reader.send_image()
        except zmq.Again:
            continue
        except KeyboardInterrupt:
            reader.close()
            break
        except Exception:
            continue
        time.sleep(1/FPS)

if __name__ == "__main__":
    id = sys.argv[1]
    target = sys.argv[2]
    main(id, target)