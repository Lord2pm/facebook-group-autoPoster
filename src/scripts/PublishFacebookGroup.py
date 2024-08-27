from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st
from typing import NoReturn
from time import sleep

from scripts.config import load_driver_config
from models.models import LoginData, GruposFacebook, session
from utils.manage_logs import log_post_shared, log_post_shared_error


class PublishFacebookGroup:
    def __init__(self, facebook_groups: list) -> NoReturn:
        self.facebook_url = "https://web.facebook.com"
        self.facebook_groups = facebook_groups
        service, options = load_driver_config()
        self.driver = webdriver.Chrome(service=service, options=options)

    def login(self, email: str, senha: str) -> bool:
        try:
            self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input",
            ).send_keys(email)
            self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input",
            ).send_keys(senha)
            sleep(1)
            self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button",
            ).click()
            sleep(60)
            return True
        except:
            return False

    def post_in_group(self, post_link) -> NoReturn:
        for facebook_group in self.facebook_groups:
            try:
                self.driver.get(facebook_group.link_grupo)
                sleep(10)
                self.driver.find_element(
                    By.XPATH,
                    "//span[normalize-space()='Write something...']",
                ).click()
                sleep(10)
                self.driver.find_element(
                    By.XPATH, "//div[@class='_1mf _1mj']"
                ).send_keys(post_link)
                sleep(2)
                self.driver.find_element(
                    By.XPATH,
                    "//div[@aria-label='Post']//div[@class='x6s0dn4 x78zum5 xl56j7k x1608yet xljgi0e x1e0frkt']",
                ).click()
                log_post_shared(facebook_group.link_grupo, post_link)
                sleep(30)
            except:
                log_post_shared_error(facebook_group.link_grupo, post_link)
                ...

    def start(self, post_link: str) -> bool:
        self.driver.get(self.facebook_url)
        login_data = session.query(LoginData).first()

        if login_data:
            sleep(15)
            if self.login(login_data.email, login_data.senha):
                self.post_in_group(post_link)
                return True
            else:
                st.error("Erro ao fazer login")
        else:
            st.error("Não existem dados de login cadastrados")

        return False


if __name__ == "__main__":
    publish_facebook_group = PublishFacebookGroup()
    publish_facebook_group.start()
