from pydantic import BaseModel
from typing import Optional

class NovoRecurso(BaseModel):
    token: str
    id: int
    nome: str
    tipo: str
    recurso_alvo: str
    git_repo_url: Optional[str] = ""