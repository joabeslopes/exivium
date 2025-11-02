from pydantic import BaseModel
from typing import Optional

class StartRecurso(BaseModel):
    token: str
    id: int
    recurso_alvo: str

class NovoRecurso(BaseModel):
    token: str
    nome: str
    tipo: str
    git_repo_url: Optional[str] = ""