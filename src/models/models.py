from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Definir a URL do banco de dados
DATABASE_URL = "sqlite:///db.db"

# Criar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Definir a base para os modelos
Base = declarative_base()


# Definir o modelo para a tabela `Categoria`
class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True)

    # Relacionamento com GruposFacebook
    grupos = relationship("GruposFacebook", back_populates="categoria")


# Definir o modelo para a tabela `grupos_facebook`
class GruposFacebook(Base):
    __tablename__ = "grupos_facebook"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_grupo = Column(String, nullable=False, unique=True)
    data_cadastro = Column(DateTime, default=datetime.now())

    # Chave estrangeira para a tabela `Categoria`
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)

    # Relacionamento com Categoria
    categoria = relationship("Categoria", back_populates="grupos")


# Definir o modelo para a tabela `login_data`
class LoginData(Base):
    __tablename__ = "login_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)


# Criar todas as tabelas no banco de dados
Base.metadata.create_all(engine)

# Configurar a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de como adicionar uma nova categoria e um grupo relacionado
# nova_categoria = Categoria(nome="Tecnologia")
# novo_grupo = GruposFacebook(link_grupo="https://facebook.com/grupo1", categoria=nova_categoria)
# session.add(nova_categoria)
# session.add(novo_grupo)
# session.commit()
