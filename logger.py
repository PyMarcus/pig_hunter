import logging


def save_log(chat: str) -> None:
    """Salva log de conversas com as horas para eventuais comparações"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s::%(levelname)s::%(message)s", filename="shark.log")
    logging.info(chat)
