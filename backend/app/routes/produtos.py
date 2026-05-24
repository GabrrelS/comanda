from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Produto, ItemComanda
from app.permissoes import somente_admin

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


# ==========================
# CRIAR PRODUTO
# ==========================

@router.post("")
def criar_produto(
    produto: dict,
    db: Session = Depends(get_db),
    usuario=Depends(somente_admin)
):

    novo = Produto(
        nome=produto["nome"],
        preco=produto["preco"],
        estoque=produto["estoque"],
        unidade=produto["unidade"]
    )

    db.add(novo)

    db.commit()

    db.refresh(novo)

    return {
        "mensagem": "Produto criado",
        "id": novo.id
    }


# ==========================
# LISTAR PRODUTOS
# ==========================

@router.get("")
def listar_produtos(
    db: Session = Depends(get_db)
):

    produtos = db.query(
        Produto
    ).all()

    return produtos


# ==========================
# EXCLUIR PRODUTO
# ==========================

@router.delete("/{id}")
def excluir_produto(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(somente_admin)
):

    produto = db.query(
        Produto
    ).filter(
        Produto.id == id
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )


    # verifica se produto está sendo usado em alguma comanda
    item = db.query(
        ItemComanda
    ).filter(
        ItemComanda.produto_id == id
    ).first()


    if item:

        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir produto que já foi utilizado em comandas"
        )


    db.delete(produto)

    db.commit()

    return {
        "mensagem": "Produto removido com sucesso"
    }

# ==========================
# ALTERAR PRODUTO
# ==========================

@router.put("/{id}")
def atualizar_produto(
    id:int,
    dados:dict,
    db:Session=Depends(get_db),
    usuario=Depends(somente_admin)
):

    produto = db.query(
        Produto
    ).filter(
        Produto.id == id
    ).first()

    if not produto:

        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    produto.nome = dados["nome"]
    produto.preco = dados["preco"]
    produto.estoque = dados["estoque"]
    produto.unidade = dados["unidade"]

    db.commit()

    db.refresh(produto)

    return {
        "mensagem":"Produto atualizado"
    }