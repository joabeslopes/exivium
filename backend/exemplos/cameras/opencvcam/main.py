import cv2
import sys
from recurso_base import RecursoBase
import time

#TODO variavel de ambiente
JPEG_QUALITY = 70
FRAME_WIDTH = 640
FRAME_HEIGHT = 360
FPS = 30

class OpencvCam(RecursoBase):
    def __init__(self, id, recurso_alvo):
        super().__init__(id, recurso_alvo)

        if recurso_alvo.isdigit():
            recurso_alvo = int(recurso_alvo)
        self.cap = cv2.VideoCapture(recurso_alvo)
        self.active = self.cap.isOpened()

        if not self.active:
            self.send_log(f"Camera {recurso_alvo} invalida")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.size_offset = 0
        real_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        real_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if (real_width != FRAME_WIDTH or real_height != FRAME_HEIGHT):
            if (real_width > FRAME_WIDTH or real_height > FRAME_HEIGHT):
                self.size_offset = 1
            else:
                self.size_offset = -1

        self.init_pub_img()
        self.init_pub_log()

    def load_image(self):
        if not self.active:
            return False

        readed, frame = self.cap.read()
        if readed:
            match self.size_offset:
                case 1: # Downscale 
                    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT), interpolation=cv2.INTER_AREA)
                case -1: # Upscale
                    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT), interpolation=cv2.INTER_LINEAR )
        else:
            return False

        try:
            encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
            if encoded:
                self.image = buffer.tobytes()
            return encoded
        except Exception as e:
            self.close()
            return False

    def close(self):
        self.send_log(f"Parando camera opencv {self.id}")
        self.active = False
        if hasattr(self, "pub_img_socket"):
            self.pub_img_socket.close()
        if hasattr(self, "pub_log_socket"):
            self.pub_log_socket.close()
        if hasattr(self, "cap"):
            self.cap.release()

def main(id, recurso_alvo):
    try:
        cam = OpencvCam(id, recurso_alvo)
        cam.send_log(f"Rodando camera opencv {id}")
        while cam.active:
            if cam.load_image():
                cam.send_image()
            time.sleep(1 / FPS)
    except Exception:
        pass
    finally:
        cam.close()


if __name__ == "__main__":
    id = sys.argv[1]
    target = sys.argv[2]
    main(id, target)