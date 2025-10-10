import os
import venv
import subprocess
import git
import atexit
import zmq
from classes.recurso_base import RecursoBase
import multiprocessing
import sys

class ResourceManager():
    def __init__(self):
        self.resources = {}
        base_path = os.path.dirname(sys.argv[0])
        self.plugins_path = os.path.join(base_path, 'plugins')
        self.cameras_path = os.path.join(base_path, 'cameras')
        self.proxy_process = multiprocessing.Process(target=self.start_proxy)
        self.proxy_process.start()
        atexit.register(self.stop_all)

    def start_proxy(self):
        self.base = RecursoBase(-1,-1)
        self.pub = self.base.context.socket(zmq.XPUB)
        self.pub.bind(self.base.zmq_url_out)
        self.sub = self.base.context.socket(zmq.XSUB)
        self.sub.bind(self.base.zmq_url_in)
        zmq.proxy(self.sub, self.pub)

    def create_dir(self, nome, tipo):
        dir = ""
        match tipo:
            case "camera":
                dir = os.path.join(self.cameras_path, nome)
            case "plugin":
                dir =  os.path.join(self.plugins_path, nome)
            case _:
                print("Tipo de recurso desconhecido")
                return ""

        # Se ja existir, nao cria de novo
        os.makedirs(dir, exist_ok=True)
        return dir

    def install_python(self, dir):
        if not os.path.exists(dir):
            print(f"Diretório {dir} não existe")
            return ""

        requirements_file = os.path.join(dir, 'requirements.txt')
        if not os.path.exists(requirements_file):
            print(f"{requirements_file} não encontrado")
            return ""

        venv_dir = os.path.join(dir, ".venv")
        python_file = ""
        if os.name == 'nt':
            python_file = os.path.join(venv_dir, 'Scripts', 'python.exe')
        else:
            python_file = os.path.join(venv_dir, 'bin', 'python')

        if not os.path.exists(python_file):
            venv.EnvBuilder(with_pip=True).create(venv_dir)
            print(f"Instalando dependências do {requirements_file}")
            subprocess.run([python_file, '-m', 'pip', 'install', '-r', requirements_file], check=True)

        return python_file

    def start_resource(self, id, nome, tipo, recurso_alvo, git_repo_url: str=""):
        if id in self.resources:
            self.stop_recource(id)

        dir = self.create_dir(nome, tipo)
        if dir == "":
            return ""

        if not git_repo_url == "":
            repo = git.Repo.clone_from(git_repo_url, dir)

        python_file = self.install_python(dir)

        self.resources[id] = subprocess.Popen(
            [python_file, os.path.join(dir, "main.py"), str(id), str(recurso_alvo)]
        )

    def stop_resource(self, id):
        if id in self.resources:
            try:
                print(f"parando recurso {id}")
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