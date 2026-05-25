from fastapi import FastAPI
from app.database import engine
from app.models import Base

print(">>> MAIN PY CARREGADO")

from app.routes import (
    produtos,
    relatorios,
    auth_routes,
    users,
    comandas,
    itens
)

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
        "status": "online",
        "mensagem": "API Sistema de Comandas funcionando"
    }

print("ROTAS REGISTRADAS:")
for r in app.routes:
    print(r.path)