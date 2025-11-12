from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from classes.reader import Reader
from classes.resource_manager import ResourceManager
from classes.logger import Logger
from functions.log import log
from functions.tokens import get_token_info
from fastapi.middleware.cors import CORSMiddleware
from functions.mjpeg import gen_frame
from classes.requests import StartRecurso, NovoRecurso
from fastapi import Depends
from classes.db import Database

app = FastAPI(root_path="/api")
logger = Logger()
db = Database()
resource_manager = ResourceManager(db)

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

    ativos = resource_manager.get_ativos()
    if not id in ativos:
        raise HTTPException(status_code=500, detail="Video nao disponivel")

    reader = Reader(id)
    return StreamingResponse(gen_frame(request, reader), media_type="multipart/x-mixed-replace; boundary=--boundary")

@app.get("/ativos")
async def get_recursos_ativos(token: str):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    return resource_manager.get_ativos()

@app.post("/ativo")
async def ativa_recurso(request: StartRecurso):
    info = await get_token_info(request.token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.start_resource(request.recurso_id, request.recurso_alvo)
    return result

@app.delete("/ativo/{id}")
async def desativa_recurso(token: str, id: int):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.stop_resource(id)
    return result

@app.get("/recursos")
async def get_recursos(token: str):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    return resource_manager.get_db_recursos()

@app.post("/recurso")
async def cria_recurso(request: NovoRecurso):
    info = await get_token_info(request.token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.create_resource(request.nome, request.tipo, request.git_repo_url)
    return result

@app.delete("/recurso/{id}")
async def deleta_recurso(token: str, id: int):
    info = await get_token_info(token)
    if not info:
        log("[ERRO] Token invalido")
        raise HTTPException(status_code=401, detail="Token invalido")

    result = await resource_manager.delete_resource(id)
    return result