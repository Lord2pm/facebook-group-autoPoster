from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///db.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)
    grupos = relationship("GruposFacebook", back_populates="categoria")


class GruposFacebook(Base):
    __tablename__ = "grupos_facebook"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_grupo = Column(String, nullable=False, unique=True)
    data_cadastro = Column(DateTime, default=datetime.now())
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="grupos")


class LoginData(Base):
    __tablename__ = "login_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
