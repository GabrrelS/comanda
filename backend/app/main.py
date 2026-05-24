from fastapi import FastAPI
from app.database import engine
from app.models import Base

from app.routes import produtos
from app.routes import relatorios
from app.routes import auth_routes
from app.routes import users
from app.routes import comandas
from app.routes import itens

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Comandas"
)

app.include_router(produtos.router)
app.include_router(relatorios.router)
app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(comandas.router)
app.include_router(itens.router)

@app.get("/")
def home():
    return {
        "status":"online",
        "mensagem":"API Sistema de Comandas funcionando"
    }