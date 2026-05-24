from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    senha = Column(
        String,
        nullable=False
    )

    tipo = Column(
        String,
        nullable=False
    )


class Produto(Base):

    __tablename__ = "produtos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String,
        nullable=False
    )

    preco = Column(
        Float,
        nullable=False
    )

    estoque = Column(
        Integer,
        default=0
    )

    unidade = Column(
        String,
        nullable=False
    )


class Comanda(Base):

    __tablename__ = "comandas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    mesa = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String,
        default="ABERTA"
    )

    total = Column(
        Float,
        default=0
    )

    data = Column(
        DateTime,
        default=datetime.utcnow
    )

    itens = relationship(
        "ItemComanda",
        back_populates="comanda"
    )


class ItemComanda(Base):

    __tablename__ = "itens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id")
    )

    comanda_id = Column(
        Integer,
        ForeignKey("comandas.id")
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    # PREÇO SALVO NO MOMENTO DA VENDA
    preco_unitario = Column(
        Float,
        nullable=False
    )

    produto = relationship(
        "Produto"
    )

    comanda = relationship(
        "Comanda",
        back_populates="itens"
    )