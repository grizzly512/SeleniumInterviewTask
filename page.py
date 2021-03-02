# -*- coding: utf-8 -*-
import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from element import BasePageElement
from locators import MailRuLoginPageLocators
from locators import MailRuSearchPageLocators
from locators import MailRuCreateEmailLocators


class BasePage(object):
    """Базовый класс для страниц"""

    def __init__(self, driver):
        """Инициализация класса"""
        self.driver = driver

    def goToUrl(self, url: str) -> str:
        """Перейти к URL"""
        # Предусловия
        assert isinstance(url, str)
        self.driver.get(url)
        sleep(random.uniform(1.0, 3.0))
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str)
        return title


class LoginFormElement(BasePageElement):
    locator = MailRuLoginPageLocators.USER_NAME


class PasswordFormElement(BasePageElement):
    locator = MailRuLoginPageLocators.PASSWD


class MailRuLoginPage(BasePage):
    loginForm = LoginFormElement()
    passwordForm = PasswordFormElement()

    def login(self,
              MailRuUsername: str,
              MailRuPassword: str) -> str:
        """Логин на mail.ru"""
        # Предусловия
        assert isinstance(MailRuUsername, str)
        assert isinstance(MailRuPassword, str)
        # Вводим имя пользователя
        self.loginForm = [MailRuUsername, Keys.RETURN]
        WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(MailRuLoginPageLocators.PASSWD))
        # sleep(random.uniform(5.0, 7.0))
        # Вводим пароль
        self.passwordForm = [MailRuPassword, Keys.RETURN]
        # sleep(random.uniform(10.0, 10.0))
        WebDriverWait(self.driver, 100).until(
            EC.title_contains("Входящие - Почта Mail.ru"))
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str)
        return title


class SearchButtonElement(BasePageElement):
    locator = MailRuSearchPageLocators.SEARCH_BUTTON


class SearchFieldElement(BasePageElement):
    locator = MailRuSearchPageLocators.SEARCH_FIELD


class MailRuSearchPage(BasePage):
    searchButton = SearchButtonElement()
    searchField = SearchFieldElement()

    def findEmailsAndCount(self, nameFrom: str) -> int:
        assert isinstance(nameFrom, str)
        self.searchButton.click()
        sleep(random.uniform(1.0, 2.0))
        self.searchField = [nameFrom, Keys.RETURN]
        sleep(random.uniform(3.0, 5.0))
        emails = self.driver.find_elements(*MailRuSearchPageLocators.MAILS)
        tags = self.driver.find_elements(*MailRuSearchPageLocators.TAGS)

        correctEmailsCount = 0
        i = 0
        for mail in emails:
            nameInTitle = nameFrom in mail.get_attribute("title")
            inbox = tags[i].get_attribute("title") == "Входящие"
            if nameInTitle and inbox:
                correctEmailsCount += 1
            i += 1
        # Постусловия
        assert isinstance(correctEmailsCount, int)
        return correctEmailsCount


class EmailCreateElement(BasePageElement):
    locator = MailRuCreateEmailLocators.MAIL_CREATE_BUTTON


class EmailSubjectElement(BasePageElement):
    locator = MailRuCreateEmailLocators.MAIL_SUBJECT


class EmailBodyElement(BasePageElement):
    locator = MailRuCreateEmailLocators.MAIL_BODY


class EmailSendElement(BasePageElement):
    locator = MailRuCreateEmailLocators.MAIL_SEND_BUTTON


class EmailSendedElement(BasePageElement):
    locator = MailRuCreateEmailLocators.MAIL_SENDED


class MailRuSendPage(BasePage):
    emailCreate = EmailCreateElement()
    emailSubject = EmailSubjectElement()
    emailBody = EmailBodyElement()
    emailSend = EmailSendElement()
    emailSended = EmailSendedElement()

    def sendEmail(self, subject: str, textBody: str,
                  nameoOrAdress: str,
                  ) -> bool:
        """Отправить письмо"""
        # Предусловия
        assert isinstance(subject, str)
        assert isinstance(textBody, str)
        assert isinstance(nameoOrAdress, str)
        # Находим кнопку "Написать письмо" и кликаем на нее
        self.emailCreate.click()
        sleep(random.uniform(5.0, 7.0))
        adressForm = self.driver.switch_to.active_element
        adressForm.clear()
        adressForm.send_keys(nameoOrAdress)
        sleep(random.uniform(0.5, 1.0))
        adressForm.send_keys(Keys.RETURN)
        # Ищем поле с темой письма и вбиваем тему письма
        self.emailSubject = subject
        # Ищем поле для ввода текста и вбиваем текст письма
        self.emailBody = textBody
        # Нажимаем кнопку отправить
        self.emailSend.click()
        sleep(random.uniform(3.0, 5.0))
        # Постусловия
        result = self.emailSended
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
