import subprocess
import numpy as np
from threading import Thread
import cv2
import time
import sys
import zmq
from recurso_base import RecursoBase

#TODO variavel de ambiente
FPS = 30
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 70

class FFmpegCamera(RecursoBase):
    def __init__(self, id, recurso_alvo):
        super().__init__(id, recurso_alvo)
        self.init_send_socket()
        self.thread = Thread(target=self._run_ffmpeg)
        self.thread.start()

    def _run_ffmpeg(self):
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-fflags", "nobuffer",
            "-fflags", "discardcorrupt",
            "-flags", "low_delay",
            "-rtsp_flags", "prefer_tcp",
            "-use_wallclock_as_timestamps", "1",
            "-i", self.recurso_alvo,
            "-vf", f"scale={FRAME_WIDTH}:{FRAME_HEIGHT}",
            "-r", str(FPS),
            "-pix_fmt", "bgr24",
            "-f", "rawvideo",
            "-flush_packets", "1",
            "pipe:1"
        ]

        frame_size = FRAME_WIDTH * FRAME_HEIGHT * 3

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )

        try:
            while self.ativo:
                raw_frame = process.stdout.read(frame_size)
                if len(raw_frame) != frame_size:
                    break
                frame = np.frombuffer(raw_frame, np.uint8).reshape(
                    (FRAME_HEIGHT, FRAME_WIDTH, 3)
                )

                _, jpeg = cv2.imencode(
                    ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
                )
                self.image = jpeg.tobytes()
                self.send_image()
        except Exception as e:
            print(f"[{self.id}] Erro no FFmpeg:", e)
        finally:
            process.terminate()
            process.wait(timeout=2)
            self.ativo = False

    def close(self):
        print(f"Parando câmera {self.id}")
        self.ativo = False
        self.thread.join(timeout=2)
        self.send_socket.close()


def main(id, recurso_alvo):
    cam = FFmpegCamera(id, recurso_alvo)
    try:
        while cam.ativo:
            time.sleep(1)
    except KeyboardInterrupt:
        cam.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])