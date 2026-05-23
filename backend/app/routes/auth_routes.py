from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.auth import verificar

router=APIRouter()

@router.post("/login")
def login(
    dados:dict,
    db:Session=Depends(get_db)
):

    usuario=db.query(
        Usuario
    ).filter(
        Usuario.email==dados["email"]
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Usuário inválido"
        )

    if not verificar(
        dados["senha"],
        usuario.senha
    ):

        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    return{

        "tipo":usuario.tipo,
        "nome":usuario.nome
    }