# -*- coding: utf-8 -*-
import random
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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
        assert isinstance(url, str), "URL должен быть str"
        self.driver.get(url)
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str), "Тайтл должен быть str"
        return title


class LoginFormElement(BasePageElement):
    """Поле для ввода логина"""
    locator = MailRuLoginPageLocators.USER_NAME


class PasswordFormElement(BasePageElement):
    """Поле для ввода пароля"""
    locator = MailRuLoginPageLocators.PASSWD


class MailRuLoginPage(BasePage):
    """Страница логина"""
    loginForm = LoginFormElement()
    passwordForm = PasswordFormElement()

    def login(self,
              MailRuUsername: str,
              MailRuPassword: str) -> str:
        """Логин на mail.ru"""
        # Предусловия
        assert isinstance(MailRuUsername, str), "Логин должен быть str"
        assert isinstance(MailRuPassword, str), "Пароль должен быть str"
        # Вводим имя пользователя
        self.loginForm = [MailRuUsername, Keys.RETURN]
        # Вводим пароль
        self.passwordForm = [MailRuPassword, Keys.RETURN]
        try:
            self.driver.find_element(
                *MailRuLoginPageLocators.INCORRECT_PASSWORD)
            raise AssertionError("Логин и пароль не совпадают!")
        except NoSuchElementException:
            pass
        # Ждем, пока загрузится страница
        WebDriverWait(self.driver, 100).until(
            EC.title_contains("Входящие - Почта Mail.ru"))
        # Постусловия
        title = self.driver.title
        assert isinstance(title, str), "Тайтл должен быть str"
        return title


class SearchButtonElement(BasePageElement):
    """Кнопка вызова поля поиска"""
    locator = MailRuSearchPageLocators.SEARCH_BUTTON


class SearchFieldElement(BasePageElement):
    """Поле поиска"""
    locator = MailRuSearchPageLocators.SEARCH_FIELD


class MailRuSearchPage(BasePage):
    """Страница поиска"""
    searchButton = SearchButtonElement()
    searchField = SearchFieldElement()

    def findEmailsAndCount(self, nameFrom: str) -> int:
        """Найти и посчитать эл.письма"""
        # Предусловия
        assert isinstance(nameFrom, str), "Имя или Адрес должены быть str"
        self.searchButton.click()
        self.searchField = [nameFrom, Keys.RETURN]
        sleep(random.uniform(3.0, 5.0))

        emails = self.driver.find_elements(*MailRuSearchPageLocators.MAILS)
        tags = self.driver.find_elements(*MailRuSearchPageLocators.TAGS)
        # Считаем входящие сообщения
        correctEmailsCount = 0
        i = 0
        for mail in emails:
            nameInTitle = nameFrom in mail.get_attribute("title")
            inbox = tags[i].get_attribute("title") == "Входящие"
            if nameInTitle and inbox:
                correctEmailsCount += 1
            i += 1
        # Постусловия
        assert isinstance(correctEmailsCount, int), "Кол-во должно быть int"
        return correctEmailsCount


class EmailCreateElement(BasePageElement):
    """Кнопка Написать сообщение"""
    locator = MailRuCreateEmailLocators.MAIL_CREATE_BUTTON


class EmailSubjectElement(BasePageElement):
    """Поле для ввода темы"""
    locator = MailRuCreateEmailLocators.MAIL_SUBJECT


class EmailBodyElement(BasePageElement):
    """Поле для ввода текста письма"""
    locator = MailRuCreateEmailLocators.MAIL_BODY


class EmailSendElement(BasePageElement):
    """Кнопка отправки сообщения"""
    locator = MailRuCreateEmailLocators.MAIL_SEND_BUTTON


class EmailSendedElement(BasePageElement):
    """Проверка на успех отправки эл. письма"""
    locator = MailRuCreateEmailLocators.MAIL_SENDED


class MailRuSendPage(BasePage):
    """Страница отправки письма"""
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
        assert isinstance(subject, str), "Тема должена быть str"
        assert isinstance(textBody, str), "Текст письма должен быть str"
        assert isinstance(nameoOrAdress, str), "Имя или Адрес должены быть str"
        # Находим кнопку "Написать письмо" и кликаем на нее
        self.emailCreate.click()
        WebDriverWait(self.driver, 100).until(
            EC.visibility_of_element_located(
                MailRuCreateEmailLocators.MAIL_SUBJECT))
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
        # Постусловия
        result = self.emailSended
        assert result is not None, "Не получено подтверждение об отправке"
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
