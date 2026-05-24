from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comanda

router = APIRouter(
    prefix="/comandas",
    tags=["Comandas"]
)


# ==========================
# LISTAR COMANDAS
# ==========================

@router.get("")
def listar_comandas(
    db: Session = Depends(get_db)
):
    return db.query(
        Comanda
    ).all()


# ==========================
# CRIAR COMANDA
# ==========================

@router.post("")
def criar_comanda(
    dados: dict,
    db: Session = Depends(get_db)
):

    nova = Comanda(
        mesa=dados["mesa"],
        status="ABERTA",
        total=0
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


# ==========================
# FECHAR COMANDA
# ==========================

@router.put("/{comanda_id}/fechar")
def fechar_comanda(
    comanda_id: int,
    db: Session = Depends(get_db)
):

    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == comanda_id
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )

    if comanda.status == "FINALIZADA":

        raise HTTPException(
            status_code=400,
            detail="Comanda já está fechada"
        )

    comanda.status = "FINALIZADA"

    db.commit()
    db.refresh(comanda)

    return {
        "mensagem": "Comanda fechada com sucesso",
        "comanda": comanda.id,
        "status": comanda.status
    }