from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comanda

router=APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)

@router.get("")
def relatorio(
    db:Session=Depends(get_db)
):

    comandas=db.query(
        Comanda
    ).filter(
        Comanda.status=="FINALIZADA"
    ).all()

    resultado=[]

    for c in comandas:

        resultado.append({

            "comanda":c.id,
            "mesa":c.mesa,
            "valor":c.total,
            "status":c.status
        })

    return resultado