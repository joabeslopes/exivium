from classes.db import Database
from classes.models import Usuario
from sqlalchemy import select
import jwt
from pwdlib import PasswordHash
import datetime
import os

class UserManager():
    def __init__(self, db: Database):
        self.db = db
        self.password_hash = PasswordHash.recommended()
        self.jwt_key = os.environ.get("JWT_SECRET_KEY")
        self.jwt_exp = int(os.environ.get("JWT_EXPIRE_MINUTES"))
        self.jwt_alg = os.environ.get("JWT_ALGORITHM")

        admin_email = os.environ.get("EXIVIUM_ADMIN_EMAIL")
        admin_password = os.environ.get("EXIVIUM_ADMIN_PASSWORD")
        self.cria_user("Admin", "", admin_email, admin_password)

    def cria_hash(self, senha):
        return self.password_hash.hash(senha)

    def get_user(self, email):
        query = select(Usuario).where(Usuario.email == email)
        return self.db.get_first(query)

    def del_user(self, id):
        query = select(Usuario).where(Usuario.id == id)
        dbUser = self.db.get_first(query)
        return self.db.delete(dbUser)

    def get_all(self):
        query = select(Usuario)
        return self.db.get_all(query)

    def valida_user(self, email, senha):
        dbUser = self.get_user(email)
        if not dbUser:
            return None

        if not self.password_hash.verify(senha, dbUser.senha_hash):
            return None
        return dbUser

    def cria_user(self, nome, telefone, email, senha) -> int:
        dbUser = self.get_user(email)
        if dbUser:
            return dbUser.id

        newUser = Usuario(nome=nome, telefone=telefone, email=email, senha_hash=self.cria_hash(senha))
        self.db.add(newUser)
        return newUser.id

    def cria_token(self, email):
        payload = {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=self.jwt_exp),
            "iat": datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_key, algorithm=self.jwt_alg)

    def valida_token(self, token) -> bool:
        try:
            payload = jwt.decode(token, self.jwt_key, algorithms=[self.jwt_alg])
            return True
        except Exception:
            return False
    
