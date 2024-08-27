from models.models import session, LoginData


def save_login_data(email: str, senha: str):
    old_login_data = session.query(LoginData).first()

    if old_login_data:
        session.delete(old_login_data)
        session.commit()

    login_data = LoginData(email=email, senha=senha)
    session.add(login_data)
    session.commit()
