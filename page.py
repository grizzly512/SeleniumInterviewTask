# -*- coding: utf-8 -*-
import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class BasePage(object):
    """
    Базовый класс для страниц
    init: driver - Selenium web driver
    methods:
        public:
            goToUrl
        private:
            findAndAaction
    """

    def __init__(self, driver):
        """Инициализация класса"""
        self.driver = driver

    def goToUrl(self, url: str) -> str:
        """
        Перейти к URL
        arguments:
            url: str - адрес страницы
        returns:
            title: str - тайтл полученной страницы
        """
        # Предусловия
        assert isinstance(url, str)
        self.driver.get(url)
        sleep(random.uniform(1.0, 3.0))
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str)
        return title

    def _findAndAction(self,
                       xpathStr: str = None,
                       returnKey: bool = False,
                       click: bool = False,
                       stringToType: str = None) -> WebElement:
        """
        Найти элемент по локатору и выполнить действия над ним
        arguments:
            xpathStr: str = None, - xpath локатор
            returnKey: bool = False, - нажимать ли пробел?
            click: bool = False, - кликать на элемент?
            stringToType: str = None - текст для печати в форму
        returns:
            element: selemium.webdriver.WebElement
        """
        # Предусловия
        xpathStrAssert = (
            isinstance(xpathStr, str) or xpathStr is None)
        stringToTypeAssert = (
            isinstance(stringToType, str) or stringToType is None)
        assert xpathStrAssert
        assert stringToTypeAssert
        assert isinstance(returnKey, bool)
        assert isinstance(click, bool)
        # Находим элемент по локатору, если xpathStr не None
        wait = WebDriverWait(self.driver, 10)
        if xpathStr is not None:
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpathStr)))
        # Либо назначаем текущий элемент активным
        else:
            element = self.driver.switch_to.active_element
        # Кликаем, если нужно
        if click:
            element.click()
        # Вписываем текст, если нужно
        if stringToType is not None:
            for key in stringToType:
                element.send_keys(key)
                sleep(random.uniform(0.02, 0.1))
        # Нажимаем пробел, если нужно
        if returnKey:
            sleep(random.uniform(0.5, 0.7))
            element.send_keys(Keys.RETURN)
        sleep(random.uniform(2.0, 3.0))
        # Постусловия
        assert isinstance(element, WebElement)
        return element


# TODO: Мультиязычность.
# TODO: Стабильная работа при уменьшении размера окна.
class MailRu(BasePage):
    """
    Класс работы с mail.ru
    inheritance: BasePage
    init: driver - Selenium web driver
    methods:
        public:
            goToUrl
            login
            findAndCountEmails
            sendEmail
        private:
            findAndAaction
    """

    def login(self,
              MailRuUsername: str,
              MailRuPassword: str) -> str:
        """
        Логин на mail.ru
        arguments:
            MailRuUsername: str, - логин mail.ru
            MailRuPassword: str, - пароль mail.ru
        returns:
            title: str - тайтл полученной страницы
        """
        # Предусловия
        assert isinstance(MailRuUsername, str)
        assert isinstance(MailRuPassword, str)
        # Вводим имя пользователя
        self._findAndAction(
            xpathStr='//input[@name="username"]',
            returnKey=True,
            stringToType=MailRuUsername)
        # Вводим пароль
        self._findAndAction(
            xpathStr='//input[@name="password"]',
            returnKey=True,
            stringToType=MailRuPassword)

        sleep(random.uniform(5.0, 7.0))
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str)
        return title

    def findAndCountEmails(self, nameFrom: str) -> int:
        """
        Найти и посчитать входящие электронные письма от адресата
        arguments:
            nameFrom: str, - имя или адрес
        returns:
            correctEmailsCount: int - количество входящих сообщений
        """
        # Предусловия
        assert isinstance(nameFrom, str)
        # Находим и кликаем на кнопку поиска
        self._findAndAction(
            xpathStr='//span[@class ="search-panel-button__text"]',
            click=True)
        # Находим строку поиска и вводим имя отправителя
        # TODO: Победить infinite scroll
        self._findAndAction(
            xpathStr='//input',
            returnKey=True,
            stringToType=nameFrom)
        # Считаем письма и тэги
        mails = self.driver.find_elements(By.XPATH, '//span[@class="ll-crpt"]')
        tags = self.driver.find_elements(By.XPATH, '//div[@class="ll-f"]')
        # Считаем только необходимые письма
        # TODO: Считать не только входящие, но и исходящие
        correctEmailsCount = 0
        i = 0
        for mail in mails:
            nameInTitle = nameFrom in mail.get_attribute("title")
            inbox = tags[i].get_attribute("title") == "Входящие"
            if nameInTitle and inbox:
                correctEmailsCount += 1
            i += 1
        sleep(random.uniform(3.0, 5.0))
        # Постусловия
        assert isinstance(correctEmailsCount, int)
        return correctEmailsCount

    def sendEmail(self, subject: str, textBody: str,
                  nameoOrAdress: str,
                  ) -> bool:
        """
        Отправить письмо
        arguments:
            subject: str, - Тема письма
            textBody: str, - Тескт письма
            nameoOrAdress: str, - Имя или адрес
        returns:
            True
        """
        # Предусловия
        assert isinstance(subject, str)
        assert isinstance(textBody, str)
        assert isinstance(nameoOrAdress, str)
        # Находим кнопку "Написать письмо" и кликаем на нее
        self._findAndAction(
            xpathStr='//span[text() ="Написать письмо"]',
            click=True)
        # Фокус переходит на строку адреса, поэтому не нужно ее искать,
        # просто вводим имя получателя и нажимаем Enter
        self._findAndAction(
            returnKey=True,
            stringToType=nameoOrAdress)
        # Ищем поле с темой письма и вбиваем тему письма
        self._findAndAction(
            xpathStr='//input[@name = "Subject"]',
            returnKey=True,
            stringToType=subject)
        # Ищем поле для ввода текста и вбиваем текст письма
        self._findAndAction(
            xpathStr='//div[@contenteditable = "true"]',
            returnKey=True,
            stringToType=textBody)
        # Нажимаем кнопку отправить
        self._findAndAction(
            xpathStr='//span[text() = "Отправить"]',
            click=True)

        sleep(random.uniform(3.0, 5.0))
        # Постусловия
        result = self._findAndAction(
            xpathStr='//a[text() = "Письмо отправлено"]')

        assert result is not None
        # Если нашли result, то возвращаем True, если нет, то
        # assert все равно не пропустит
        return True


class Gmail(BasePage):
    """
    Потратил много времени на поиск обходного пути на gmail
    пробовал скрываться, входить через сторонние сайты,
    на 28.02.21 действующих способов не нашел.
    """
    pass
