import streamlit as st
import pandas as pd
from pathlib import Path

from scripts.PublishFacebookGroup import PublishFacebookGroup
from utils.desktop_messages import show_message
from utils.manage_logs import read_log_file
from services.dados_login_services import save_login_data
from services.categorias_services import (
    save_categoria,
    get_categoria_by_nome,
    get_all_categorias,
)
from services.grupos_services import (
    get_all_grupos,
    get_grupo_by_link,
    save_grupo,
    get_grupos_by_categoria,
)


def main():
    st.set_page_config(page_title="Bot para Facebook - Rede Industrial")
    st.title("Bot para Facebook")
    st.text(
        "Economize tempo! Partilhe suas publicações em milhares de grupos num estalar de dedos"
    )

    menu = st.tabs(
        [
            "Home",
            "Meus Grupos",
            "Minhas categorias",
            "Configurar Dados de Login",
            "Logs",
        ]
    )

    with menu[0]:
        categorias = get_all_categorias()
        categorias_nomes = [categoria.nome for categoria in categorias]
        post_link_input = st.text_input(label="Link do seu Post")
        group_category = st.selectbox(
            label="Categoria dos grupos", options=categorias_nomes, key="group-category"
        )
        share_button = st.button("Partilhar Publicação", key="share-button")

        if share_button:
            if post_link_input and group_category:
                groups_list = get_grupos_by_categoria(group_category)
                publish_facebook_group = PublishFacebookGroup(groups_list)

                if publish_facebook_group.start(post_link_input):
                    st.success("Post partilhado em todos os grupos")
                    show_message("Post partilhado em todos os grupos")
            else:
                st.error("Preencha devidamente todos os campos")

    with menu[1]:
        categorias = get_all_categorias()
        categorias_nomes = [categoria.nome for categoria in categorias]
        st.header("Novo grupo")
        group_link_input = st.text_input(label="Link do Grupo")
        group_category = st.selectbox(
            label="Categoria do grupo", options=categorias_nomes
        )
        save_group_button = st.button("Salvar Grupo", key="save-group-button")

        if save_group_button:
            if group_link_input and group_category:
                if "facebook.com/groups" in group_link_input:
                    grupo = get_grupo_by_link(group_link_input)
                    if not grupo:
                        save_grupo(group_link_input, group_category)
                        st.success("Link salvo com sucesso")
                    else:
                        st.error("Link já cadastrado")
                else:
                    st.error("Link inválido")
            else:
                st.error("Preencha devidamente todos os campos")

        st.divider()

        st.header("Lista de grupos")

        grupos = get_all_grupos()
        dados_grupos = [
            {
                "Link do Grupo": grupo.link_grupo,
                "Categoria": grupo.categoria.nome,
                "Data de Cadastro": grupo.data_cadastro,
            }
            for grupo in grupos
        ]
        df_grupos = pd.DataFrame(dados_grupos)
        st.table(df_grupos)

    with menu[2]:
        st.header("Nova categoria")
        category_input = st.text_input(label="Nome da categoria")
        save_category_button = st.button("Salvar Categoria", key="save-category-button")

        if save_category_button:
            if category_input:
                categoria = get_categoria_by_nome(category_input)
                if not categoria:
                    save_categoria(category_input)
                    show_message(f"Categoria {category_input} salva com sucesso")
                    st.rerun()
                else:
                    st.error("Categoria já cadastrada")
            else:
                st.error("Preencha devidamente todos os campos")

    with menu[3]:
        user_email = st.text_input(label="Seu e-mail ou número de telefone")
        user_password = st.text_input(label="Sua senha", type="password")
        save_login_data_button = st.button(
            "Salvar Dados de Login", key="save-login-data-button"
        )

        if save_login_data_button:
            if user_email and user_password:
                save_login_data(user_email, user_password)
                st.success("Dados de Login salvos com sucesso")
            else:
                st.error("Preencha devidamente todos os campos")

    with menu[4]:
        log_file = "facebook_post_log.log"
        logs = read_log_file(log_file)

        st.title("Logs de Postagens no Facebook")
        st.text_area("Logs", value="".join(logs), height=400)
