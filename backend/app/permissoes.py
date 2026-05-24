from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario


# TEMPORÁRIO:
# pega o primeiro usuário do banco
# depois trocamos por JWT/login real

def usuario_logado(
    db: Session = Depends(get_db)
):

    usuario = db.query(
        Usuario
    ).first()

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Nenhum usuário encontrado"
        )

    return usuario


def somente_admin(
    usuario=Depends(usuario_logado)
):

    if usuario.tipo != "admin":

        raise HTTPException(
            status_code=403,
            detail="Apenas admin"
        )

    return usuario


def admin_ou_garcom(
    usuario=Depends(usuario_logado)
):

    if usuario.tipo not in [
        "admin",
        "garcom"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Sem permissão"
        )

    return usuario


def admin_ou_caixa(
    usuario=Depends(usuario_logado)
):

    if usuario.tipo not in [
        "admin",
        "caixa"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Sem permissão"
        )

    return usuario