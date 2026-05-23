from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto

router=APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)

@router.post("")
def criar_produto(
    produto:dict,
    db:Session=Depends(get_db)
):

    novo=Produto(
        nome=produto["nome"],
        preco=produto["preco"],
        estoque=produto["estoque"],
        unidade=produto["unidade"]
    )

    db.add(novo)
    db.commit()

    return{
        "mensagem":"Produto criado"
    }

@router.get("")
def listar_produtos(
    db:Session=Depends(get_db)
):

    return db.query(
        Produto
    ).all()

@router.delete("/produtos/{id}")
def excluir_produto(
    id:int,
    db:Session=Depends(get_db)
):

    produto=db.query(
        Produto
    ).filter(
        Produto.id==id
    ).first()

    if not produto:

        return {
            "erro":"Produto não encontrado"
        }

    db.delete(
        produto
    )

    db.commit()

    return {
        "mensagem":"Produto removido"
    }