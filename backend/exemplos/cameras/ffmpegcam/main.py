import subprocess
import numpy as np
from threading import Thread
import cv2
import time
import sys
import zmq
from recurso_base import RecursoBase
import os

FPS = int( os.environ.get("FPS") )
FRAME_WIDTH = int( os.environ.get("FRAME_WIDTH") )
FRAME_HEIGHT = int( os.environ.get("FRAME_HEIGHT") )
JPEG_QUALITY = int( os.environ.get("JPEG_QUALITY") )

class FFmpegCamera(RecursoBase):
    def __init__(self, id, recurso_alvo):
        super().__init__(id, recurso_alvo)
        self.init_pub_img()
        self.init_pub_log()
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
            while self.active:
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
            self.active = False

    def close(self):
        self.send_log(f"Parando camera ffmpeg {self.id}")
        self.active = False
        self.thread.join(timeout=2)
        self.pub_img_socket.close()
        self.pub_log_socket.close()


def main(id, recurso_alvo):
    cam = FFmpegCamera(id, recurso_alvo)
    cam.send_log(f"Rodando camera ffmpeg {id}")
    try:
        while cam.active:
            time.sleep(1)
    except KeyboardInterrupt:
        cam.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])