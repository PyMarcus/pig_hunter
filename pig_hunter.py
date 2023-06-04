import sys
import time
import typing
from logger import save_log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from dataclasses import dataclass


@dataclass
class Bot:

    __site: str = "site/chat.html"

    def __connect(self) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(executable_path="caminho_para_o_chromedriver.exe")  # Substitua pelo caminho correto
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def __access(self) -> webdriver.Chrome:
        driver = self.__connect()
        driver.get(self.__site)
        return driver

    def __find_elements(self, driver: WebDriver) -> tuple[WebElement | None, WebElement | None, WebDriver]:
        """Encontra elementos html na pagina"""
        try:
            driver.implicitly_wait(10)
            btn_end: WebElement | None = driver.find_element(by=By.ID, value="btnend")
            write: WebElement | None = driver.find_element(by=By.ID, value="chatinput")
            return btn_end, write, driver
        except Exception as e:
            ...

    def __chat(self) -> None:
        drive = self.__access()
        text: typing.List[str] = ["lista de conversas"]
        while True:
            try:
                btn_end, write, driver = self.__find_elements(drive)
                btn_send: WebElement | None = driver.find_element(by=By.ID, value="btnsend")
                their_msg: WebElement | None = driver.find_element(by=By.CLASS_NAME, value="theirmsg")
                next_chat: WebElement | None = driver.find_element(By.ID, value="btnnext")
                for word in text:
                    time.sleep(6)
                    if write.is_enabled():
                        write.send_keys(word)
                        btn_send.click()
                    if not btn_end.is_enabled():
                        next_chat.click()
                if their_msg:
                    save_log(their_msg.text)
            except Exception:
                pass

    def run(self) -> None:
        self.__chat()
        input("[+]Pressione Enter para fechar o bot...")
        sys.exit(0)


if __name__ == '__main__':
    try:
        bot: Bot = Bot()
        bot.run()
    except KeyboardInterrupt:
        ...
