from fastapi import APIRouter

router = APIRouter(prefix="/comandas")

@router.get("/")
def listar_comandas():
    return {"mensagem": "rota funcionando"}