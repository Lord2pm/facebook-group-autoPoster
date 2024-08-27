from models.models import session, GruposFacebook
from services.categorias_services import get_categoria_by_nome


def get_grupos_by_categoria(categoria: str) -> list:
    categoria = get_categoria_by_nome(categoria)
    lista_grupos = (
        session.query(GruposFacebook).filter_by(categoria_id=categoria.id).all()
    )
    return lista_grupos


def get_grupo_by_link(link_grupo: str) -> GruposFacebook:
    grupo = session.query(GruposFacebook).filter_by(link_grupo=link_grupo).first()
    return grupo


def save_grupo(link_grupo: str, categoria: str):
    categoria = get_categoria_by_nome(categoria)
    grupo = GruposFacebook(link_grupo=link_grupo, categoria_id=categoria.id)
    session.add(grupo)
    session.commit()


def get_all_grupos() -> list:
    return session.query(GruposFacebook).all()
