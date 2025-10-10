import subprocess
import threading
import time
import sys
import zmq
from recurso_base import RecursoBase

# Configurações
FPS = 30
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 10  # menor = melhor qualidade no FFmpeg (1..31)

class FFmpegCamera(RecursoBase):
    def __init__(self, id, recurso_alvo):
        super().__init__(id, recurso_alvo)
        self.init_send_socket()

    def run_ffmpeg(self):
        """Executa o ffmpeg e pega os frames JPEG diretamente via stdout."""
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", self.recurso_alvo,
            "-vf", f"scale={FRAME_WIDTH}:{FRAME_HEIGHT}",
            "-r", str(FPS),
            "-f", "image2pipe",
            "-vcodec", "mjpeg",
            "-q:v", str(JPEG_QUALITY),
            "-"
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0  # saída sem buffer
        )

        buffer = bytearray()
        try:
            while self.ativo:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                buffer.extend(chunk)

                # Extrai frames JPEG completos (delimitadores FF D8 ... FF D9)
                while True:
                    start = buffer.find(b'\xff\xd8')
                    end = buffer.find(b'\xff\xd9', start + 2)
                    if start >= 0 and end > start:
                        jpeg = bytes(buffer[start:end + 2])
                        del buffer[:end + 2]
                        self.image = jpeg
                        self.send_image()
                    else:
                        # ainda não há frame completo
                        if len(buffer) > 1_000_000:
                            buffer.clear()
                        break
                    time.sleep(1 / FPS)
        except Exception as e:
            print("Erro no FFmpeg:", e)
        finally:
            process.terminate()
            process.wait(timeout=2)
            self.ativo = False

    def close(self):
        print(f"Parando camera {self.id}")
        self.ativo = False
        self.send_socket.close()

def main(id, recurso_alvo):
    print(f"Iniciando camera {id}")
    cam = FFmpegCamera(id, recurso_alvo)
    try:
        cam.run_ffmpeg()
    except Exception:
        pass
    finally:
        cam.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])