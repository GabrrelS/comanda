from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ItemComanda, Produto, Comanda
from app.permissoes import admin_ou_garcom

print(">>> ITENS ROUTER IMPORTADO")

router = APIRouter(
    prefix="/itens",
    tags=["itens"]
)


@router.post("/")
def adicionar_item(
    dados: dict,
    db: Session = Depends(get_db),
    usuario=Depends(admin_ou_garcom)
):

    produto = db.query(
        Produto
    ).filter(
        Produto.id == dados["produto_id"]
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    comanda = db.query(
        Comanda
    ).filter(
        Comanda.id == dados["comanda_id"]
    ).first()

    if not comanda:

        raise HTTPException(
            status_code=404,
            detail="Comanda não encontrada"
        )


    if comanda.status=="FINALIZADA":

        raise HTTPException(
            status_code=400,
            detail="Comanda já fechada"
        )


    quantidade=dados["quantidade"]


    if produto.estoque<quantidade:

        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente"
        )


    produto.estoque-=quantidade


    item=ItemComanda(

        produto_id=dados["produto_id"],

        comanda_id=dados["comanda_id"],

        quantidade=quantidade,

        preco_unitario=produto.preco
    )


    comanda.total+=(
        item.preco_unitario*
        quantidade
    )


    db.add(item)

    db.commit()

    db.refresh(item)

    return{

        "mensagem":"Item adicionado",

        "preco_vendido":
        item.preco_unitario,

        "estoque_restante":
        produto.estoque
    }


@router.get("/")
def listar_itens(
    db:Session=Depends(get_db)
):

    itens=db.query(
        ItemComanda
    ).all()

    resultado=[]

    for i in itens:

        resultado.append({

            "id":i.id,

            "produto":i.produto.nome,

            "quantidade":i.quantidade,

            "preco_unitario":
            i.preco_unitario,

            "subtotal":
            i.preco_unitario*
            i.quantidade
        })

    return resultado