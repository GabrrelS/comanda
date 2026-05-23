from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Usuario(Base):

    __tablename__="usuarios"

    id=Column(Integer,primary_key=True,index=True)
    nome=Column(String)
    email=Column(String,unique=True)
    senha=Column(String)
    tipo=Column(String)

class Produto(Base):

    __tablename__="produtos"

    id=Column(Integer,primary_key=True,index=True)
    nome=Column(String)
    preco=Column(Float)
    estoque=Column(Integer)
    unidade=Column(String)

class Comanda(Base):

    __tablename__="comandas"

    id=Column(Integer,primary_key=True,index=True)
    mesa=Column(Integer)
    status=Column(String)
    total=Column(Float,default=0)
    data=Column(DateTime,default=datetime.utcnow)

class ItemComanda(Base):

    __tablename__="itens"

    id=Column(Integer,primary_key=True,index=True)

    produto_id=Column(
        Integer,
        ForeignKey("produtos.id")
    )

    comanda_id=Column(
        Integer,
        ForeignKey("comandas.id")
    )

    quantidade=Column(Integer)

    produto=relationship("Produto")