import logging


logging.basicConfig(
    filename="facebook_post_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_post_shared(group_name, post_url):
    logging.info(f"Post compartilhado no grupo '{group_name}': {post_url}")


def log_post_shared_error(group_name, post_url):
    logging.error(f"Erro ao compartilhar no grupo '{group_name}': {post_url}")


def read_log_file(log_file):
    with open(log_file, "r") as file:
        logs = file.readlines()
    return logs
