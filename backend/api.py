from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from classes.reader import Reader
from classes.resource_manager import ResourceManager
from classes.logger import Logger
from functions.log import log
from functions.tokens import get_token_info
from fastapi.middleware.cors import CORSMiddleware
from functions.mjpeg import gen_frame
from classes.requests import NovoRecurso

app = FastAPI(root_path="/api")
resource_manager = ResourceManager()
logger = Logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/video/{id}")
async def mjpeg_stream(request: Request, token: str, id: int):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    if not id in resource_manager.resources:
        raise HTTPException(status_code=500, detail="Video nao disponivel")

    reader = Reader(id)
    return StreamingResponse(gen_frame(request, reader), media_type="multipart/x-mixed-replace; boundary=--boundary")

@app.get("/recursos")
async def get_all_cameras(token: str):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    return resource_manager.get_all()

@app.post("/recurso")
async def cria_recurso(request: NovoRecurso):
    info = await get_token_info(request.token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.start_resource(request.id, request.nome, request.tipo, request.recurso_alvo, request.git_repo_url)
    return result

@app.delete("/recurso/{id}")
async def para_recurso(token: str, id: int):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.stop_resource(id)
    return result