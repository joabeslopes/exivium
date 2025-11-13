import os
import venv
import subprocess
import git
import atexit
import zmq
from classes.recurso_base import RecursoBase
import multiprocessing
import sys
from functions.log import log
import asyncio
from classes.db import Database
from classes.models import RecursoAtivo, Recurso
from sqlalchemy import select
import shutil

class ResourceManager():
    def __init__(self, db: Database):
        self.ativos = {}
        base_path = os.path.join( os.path.dirname(sys.argv[0]), 'recursos' )
        self.plugins_path = os.path.join(base_path, 'plugins')
        self.cameras_path = os.path.join(base_path, 'cameras')
        self.proxy_process = multiprocessing.Process(target=self.start_proxy)
        self.proxy_process.start()
        self.db = db
        atexit.register(self.stop_all)
        self.start_db_ativos()

    def get_db_recursos(self):
        query = select(Recurso)
        recursos = {}
        dbrecursos = self.db.get_all(query)
        for r in dbrecursos:
            recursos[r.id] = {
                "nome": r.nome,
                "tipo": r.tipo
            }
        return recursos

    def start_db_ativos(self):
        query = select(RecursoAtivo)
        ativos = self.db.get_all(query)
        if ativos:
            for a in ativos:
                self._start(a.recurso_id, a.recurso_alvo)

    def start_proxy(self):
        base = RecursoBase(-1,-1)

        pub = base.context.socket(zmq.XPUB)
        pub.bind(base.zmq_url_in)

        sub = base.context.socket(zmq.XSUB)
        sub.bind(base.zmq_url_out)

        zmq.proxy(pub, sub)

    def create_dir(self, nome, tipo):
        dir = ""
        match tipo:
            case "camera":
                dir = os.path.join(self.cameras_path, nome)
            case "plugin":
                dir =  os.path.join(self.plugins_path, nome)
            case _:
                log("Erro: tipo de recurso desconhecido")
                return ""

        # Se ja existir, nao cria de novo
        os.makedirs(dir, exist_ok=True)
        return dir

    def install_python(self, dir):
        if not os.path.exists(dir):
            log(f"Diretório {dir} não existe")
            return ""

        requirements_file = os.path.join(dir, 'requirements.txt')
        if not os.path.exists(requirements_file):
            log(f"{requirements_file} não encontrado")
            return ""

        venv_dir = os.path.join(dir, ".venv")
        python_file = ""
        if os.name == 'nt':
            python_file = os.path.join(venv_dir, 'Scripts', 'python.exe')
        else:
            python_file = os.path.join(venv_dir, 'bin', 'python')

        if not os.path.exists(python_file):
            venv.EnvBuilder(with_pip=True).create(venv_dir)
            log(f"Instalando dependências do {requirements_file}")
            subprocess.run([python_file, '-m', 'pip', 'install', '-r', requirements_file], check=True)

        return python_file

    def _create(self, nome, tipo, git_repo_url="") -> int:
        # Busca recurso pelo nome e tipo
        query_recurso = select(Recurso).where(Recurso.nome == nome).where(Recurso.tipo == tipo)
        db_recurso = self.db.get_first(query_recurso)
        if db_recurso:
            return db_recurso.id

        log(f"Criando recurso {nome}")

        dir = self.create_dir(nome, tipo)
        if dir == "":
            return 0
        if not git_repo_url == "" and not os.listdir(dir):
            repo = git.Repo.clone_from(git_repo_url, dir)
        python_file = self.install_python(dir)

        if python_file != "":
            recurso = Recurso(nome=nome, tipo=tipo, git_repo_url=git_repo_url)
            self.db.add(recurso)
            return recurso.id
        else:
            return 0

    async def create_resource(self, nome: str, tipo: str, git_repo_url: str="") -> int:
        result = await asyncio.to_thread(self._create, nome, tipo, git_repo_url)
        return result


    def _start(self, recurso_id, recurso_alvo) -> int:
        self.get_ativos() # Começa limpando recursos inativos

        # Busca recurso pelo id
        query_recurso = select(Recurso).where(Recurso.id == recurso_id)
        db_recurso = self.db.get_first(query_recurso)
        if not db_recurso:
            return 0
        recurso = db_recurso

        # Busca relaçao de recurso ativo
        recurso_ativo = None
        query_ativo = select(RecursoAtivo
        ).where(RecursoAtivo.recurso_id == recurso_id
        ).where(RecursoAtivo.recurso_alvo == recurso_alvo)

        dir = self.create_dir(recurso.nome, recurso.tipo)
        if dir == "":
            return 0

        git_repo_url = recurso.git_repo_url
        if git_repo_url and ( git_repo_url != "" and not os.listdir(dir) ):
            repo = git.Repo.clone_from(git_repo_url, dir)

        python_file = self.install_python(dir)
        if python_file == "":
            return 0

        db_ativo = self.db.get_first(query_ativo)
        if not db_ativo:
            recurso_ativo = RecursoAtivo(recurso_id=recurso_id, recurso_alvo=recurso_alvo)
            self.db.add(recurso_ativo)
        else:
            recurso_ativo = db_ativo

        id = recurso_ativo.id
        if id in self.ativos:
            return id

        log(f"Iniciando recurso ativo {id}")

        self.ativos[id] = subprocess.Popen(
            [python_file, os.path.join(dir, "main.py"), str(id), str(recurso_alvo)]
        )

        if self.ativos[id].poll() is None:
            return id
        else:
            return 0

    async def start_resource(self, recurso_id: int, recurso_alvo) -> int:
        result = await asyncio.to_thread(self._start, recurso_id, recurso_alvo)
        return result

    def _stop(self, id) -> bool:
        self.get_ativos() # Começa limpando recursos inativos

        result = False
        if id in self.ativos:
            try:
                log(f"Parando recurso {id}")
                process = self.ativos[id]
                process.terminate()
                result = True
            except Exception as e:
                print(e)
            finally:
                self.get_ativos()
        return result

    def _deleta_ativo(self, id):
        query = select(RecursoAtivo).where(RecursoAtivo.id == id)
        ativo = self.db.get_first(query)
        self.db.delete(ativo)

    async def stop_resource(self, id) -> bool:
        result = await asyncio.to_thread(self._stop, id)
        if result:
            await asyncio.to_thread(self._deleta_ativo, id)
        return result

    def _deleta_recurso(self, id):
        # Começa desativando todos que usam esse recurso
        query = select(RecursoAtivo).where(RecursoAtivo.recurso_id == id)
        ativos = self.db.get_all(query)
        if ativos:
            for ativo in ativos:
                interQuery = select(RecursoAtivo).where(RecursoAtivo.recurso_alvo == str(ativo.id))
                consumers = self.db.get_all(interQuery)
                if consumers:
                    for consumer in consumers:
                        self._stop(consumer.id)
                        self._deleta_ativo(consumer.id)
                self._stop(ativo.id)
                self._deleta_ativo(ativo.id)

        # Agora deleta de fato o recurso
        query = select(Recurso).where(Recurso.id == id)
        recurso = self.db.get_first(query)
        if recurso:
            dir = self.create_dir(recurso.nome, recurso.tipo)
            shutil.rmtree(dir, ignore_errors=True)
            self.db.delete(recurso)
            return True
        else:
            return False

    async def delete_resource(self, id) -> bool:
        result = await asyncio.to_thread(self._deleta_recurso, id)
        return result

    def stop_all(self):
        self.get_ativos() # Começa limpando recursos inativos

        keys = list(self.ativos.keys())

        for id in keys:
            self._stop(id)
        self.proxy_process.terminate()
        self.db.close()

    def get_ativos(self):
        ativos = []
        keys = list(self.ativos.keys())

        for id in keys:
            proc = self.ativos[id]
            if proc.poll() is None:
                ativos.append(id)
            else:
                self._deleta_ativo(id)
                del self.ativos[id]
        return ativos