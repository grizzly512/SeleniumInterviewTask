# -*- coding: utf-8 -*-

import os
import unittest
import allure
from envparse import env
from selenium import webdriver
# from selenium_stealth import stealth
from page import MailRu
# Читаем данные из окружения
currentDir = os.path.dirname(os.path.abspath(__file__))
env.read_envfile(currentDir + '/.env')
# Константы из окружения, можно определить здесь:
# Ссылка на страницу входа mail.ru
MAILRU_LOGIN_LINK = os.environ['MAILRU_LOGIN_LINK']
# Логин mail.ru
MAILRU_USERNAME = os.environ['MAILRU_USERNAME']
# Пароль mail.ru
MAILRU_PASSWORD = os.environ['MAILRU_PASSWORD']
# Адрес или имя адресата
NAME_FROM = os.environ['NAME_FROM']
# Фамилия студента
STUDENT_SNAME = os.environ['STUDENT_SNAME']

# Настройки локального драйвера. просто оставлю тут, на всякий случай

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# WEBDRIVER_LOCAL = webdriver.Chrome(
#     options=options,
#     executable_path="/usr/bin/chromedriver")
# stealth(WEBDRIVER_LOCAL,
#         languages=["ru-RU", "ru"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )

# Удаленный вэбдрайвер
desiredCapabilities = {"browserName": "chrome"}
WEBDRIVER_REMOTE = webdriver.Remote(desired_capabilities=desiredCapabilities)


class MailRuTest(unittest.TestCase):
    """
    Класс тестов с mail.ru
    inheritance: unittest.TestCase
    methods:
        public:
            setUp
            test_Mail
            load_site
            login
            findAndCountEmails
            sendEmail
            tearDown
    """

    def setUp(self):
        """
        Настройка тестов
        """
        self.driver = WEBDRIVER_REMOTE
        self.driver.maximize_window()
        self.page = MailRu(self.driver)

    def test_Mail(self):
        """
        Входной тест с шагами allure
        """
        with allure.step("Загрузка сайта"):
            self.load_site(MAILRU_LOGIN_LINK)
        with allure.step("Логин"):
            self.login(MAILRU_USERNAME, MAILRU_PASSWORD)
        with allure.step("Счёт писем"):
            emailsCount = self.findAndCountEmails(NAME_FROM)

        body = "От вас пришло писем - {}".format(emailsCount)
        subject = "Тестовое задание {}".format(STUDENT_SNAME)
        with allure.step("Отправка письма"):
            self.sendEmail(NAME_FROM, body, subject)

    def load_site(self, url: str):
        """
        Загрузка сайта
        arguments:
            url: str - адрес страницы
        returns:
            None
        """
        # Предусловия в self.page.goToUrl()
        titleLogin = self.page.goToUrl(url)
        # Постусловия
        self.assertEqual(titleLogin, "Авторизация")

    def login(self, userName, passwrd):
        """
        Логин на mail.ru
        arguments:
            userName: str, - логин mail.ru
            passwrd: str, - пароль mail.ru
        """
        # Предусловия в self.page.login()
        titleMail = self.page.login(userName, passwrd)
        # Постусловия
        self.assertRegex(titleMail, "Входящие - Почта Mail.ru")

    def findAndCountEmails(self, fromWho):
        """
        Найти и посчитать входящие электронные письма от адресата
        arguments:
            fromWho: str, - имя или адрес
        returns:
            countEmails: str - количесто эл. писем
        """
        # Предусловия в self.page.findAndCountEmails()
        countEmails = self.page.findAndCountEmails(fromWho)
        # Постусловия
        self.assertGreater(countEmails, 0)
        return countEmails

    def sendEmail(self, toWho, body, subject):
        """
        Отправить письмо
        arguments:
            subject: str, - Тема письма
            body: str, - Текст письма
            toWho: str, - Имя или адрес
        """
        result = self.page.sendEmail(nameoOrAdress=toWho,
                                     textBody=body,
                                     subject=subject)
        # Постусловия
        self.assertTrue(result)

    def tearDown(self):
        """
        Действия по завершению
        """
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
