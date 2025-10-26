import asyncio
from classes.reader import Reader
from fastapi import Request
import os

FPS = int( os.environ.get("FPS") )

async def gen_frame(request: Request, reader: Reader):
    try:
        while reader.active:
            if await request.is_disconnected():
                break

            if reader.load_image():
                image = reader.get_image()
                yield ( b'--boundary\r\n'+
                        b'Content-Type: image/jpeg\r\n' +
                        b'Content-Length: ' + str(len(image)).encode() + b'\r\n\r\n' +
                        image + 
                        b'\r\n')
            await asyncio.sleep(1 / FPS)
    except Exception as e:
        print(e)
    finally:
        reader.close()