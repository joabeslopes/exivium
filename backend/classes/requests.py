from pydantic import BaseModel
from typing import Optional

class StartRecurso(BaseModel):
    token: str
    recurso_id: int
    recurso_alvo: str

class NovoRecurso(BaseModel):
    token: str
    nome: str
    tipo: str
    git_repo_url: Optional[str] = ""

class NovoUsuario(BaseModel):
    token: str
    nome: str
    telefone: Optional[str] = ""
    email: str
    senha: str

class ObtemToken(BaseModel):
    email: str
    senha: str