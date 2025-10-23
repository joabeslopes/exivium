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

class ResourceManager():
    def __init__(self):
        self.resources = {}
        base_path = os.path.join( os.path.dirname(sys.argv[0]), 'recursos' )
        self.plugins_path = os.path.join(base_path, 'plugins')
        self.cameras_path = os.path.join(base_path, 'cameras')
        self.proxy_process = multiprocessing.Process(target=self.start_proxy)
        self.proxy_process.start()
        atexit.register(self.stop_all)

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

    def _start(self, id, nome, tipo, recurso_alvo, git_repo_url) -> bool:
        if id in self.resources:
            return True
        dir = self.create_dir(nome, tipo)
        if dir == "":
            return False
        if not git_repo_url == "":
            repo = git.Repo.clone_from(git_repo_url, dir)
        python_file = self.install_python(dir)
        log(f"Iniciando recurso {id}")
        self.resources[id] = subprocess.Popen(
            [python_file, os.path.join(dir, "main.py"), str(id), str(recurso_alvo)]
        )

        return self.resources[id].poll() is None

    async def start_resource(self, id, nome, tipo, recurso_alvo, git_repo_url: str=""):
        result = await asyncio.to_thread(self._start, id, nome, tipo, recurso_alvo, git_repo_url)
        return result

    def stop_resource(self, id):
        if id in self.resources:
            try:
                log(f"Parando recurso {id}")
                process = self.resources[id]
                process.terminate()
            except Exception:
                pass

    def stop_all(self):
        for id in self.resources:
            self.stop_resource(id)
        self.proxy_process.terminate()

    def get_all(self):
        return list(self.resources.keys())