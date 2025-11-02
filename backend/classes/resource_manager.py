import os
import venv
import subprocess
import signal
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

class ResourceManager():
    def __init__(self, db: Database):
        self.resources = {}
        base_path = os.path.join( os.path.dirname(sys.argv[0]), 'recursos' )
        self.plugins_path = os.path.join(base_path, 'plugins')
        self.cameras_path = os.path.join(base_path, 'cameras')
        self.proxy_process = multiprocessing.Process(target=self.start_proxy)
        self.proxy_process.start()
        self.db = db
        atexit.register(self.stop_all)
        self.start_db_resources()

    def start_db_resources(self):
        query = select(RecursoAtivo, Recurso).join(Recurso, RecursoAtivo.recurso_id == Recurso.id)
        resources = self.db.get_all(query)
        if resources:
            for ativo, recurso in resources:
                self._start(ativo.id, recurso.id, recurso.nome, recurso.tipo, ativo.recurso_alvo)

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

    def _start(self, id, recurso_id, nome, tipo, recurso_alvo, git_repo_url="") -> bool:
        if id in self.resources:
            return True
        dir = self.create_dir(nome, tipo)
        if dir == "":
            return False
        if not git_repo_url == "" and not os.listdir(dir):
            repo = git.Repo.clone_from(git_repo_url, dir)
        python_file = self.install_python(dir)

        log(f"Iniciando recurso ativo {id}")

        self.resources[id] = subprocess.Popen(
            [python_file, os.path.join(dir, "main.py"), str(id), str(recurso_alvo)]
        )

        return self.resources[id].poll() is None

    async def start_resource(self, recurso_id, recurso_alvo, git_repo_url: str=""):
        self.get_all() # Começa limpando recursos inativos

        # Busca recurso pelo id
        query_recurso = select(Recurso).where(Recurso.id == recurso_id)
        db_recurso = self.db.get_first(query_recurso)
        if not db_recurso:
            return False
        recurso = db_recurso[0]

        # Busca relaçao de recurso ativo
        recurso_ativo = None
        query_ativo = select(RecursoAtivo).where(RecursoAtivo.recurso_id == recurso_id).where(RecursoAtivo.recurso_alvo == recurso_alvo)
        db_ativo = self.db.get_first(query_ativo)
        if not db_ativo:
            recurso_ativo = RecursoAtivo(recurso_id=recurso_id, recurso_alvo=recurso_alvo)
            self.db.add(recurso_ativo)
        else:
            recurso_ativo = db_ativo[0]

        result = await asyncio.to_thread(self._start, recurso_ativo.id, recurso_id, recurso.nome, recurso.tipo, recurso_alvo, git_repo_url)
        return result

    def _stop(self, id):
        result = False
        if id in self.resources:
            try:
                log(f"Parando recurso {id}")
                process = self.resources[id]
                process.terminate()
                result = True
            except Exception as e:
                print(e)
            finally:
                self.get_all()
        return result

    async def stop_resource(self, id):
        result = await asyncio.to_thread(self._stop, id)
        return result

    def stop_all(self):
        for id in self.resources:
            self._stop(id)
        self.proxy_process.terminate()
        self.db.close()

    def get_all(self):
        ativos = []
        keys = list(self.resources.keys())

        for key in keys:
            proc = self.resources[key]
            if proc.poll() is None:
                ativos.append(key)
            else:
                del self.resources[key]
        return ativos