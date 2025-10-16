from pydantic import BaseModel

class NovoRecurso(BaseModel):
    token: str
    id: int
    nome: str
    tipo: str
    recurso_alvo: str