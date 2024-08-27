from models.models import session, Categoria


def get_categoria_by_nome(nome: str) -> Categoria:
    categoria = (
        session.query(Categoria).filter(Categoria.nome.like(f"%{nome}%")).first()
    )
    return categoria


def get_all_categorias() -> list:
    categorias = session.query(Categoria).all()
    return categorias


def save_categoria(categoria: str):
    nova_categoria = Categoria(nome=categoria)
    session.add(nova_categoria)
    session.commit()
