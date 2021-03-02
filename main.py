# -*- coding: utf-8 -*-

import os
import unittest
import allure
from envparse import env
from selenium import webdriver
# from selenium_stealth import stealth
from page import MailRuLoginPage, MailRuSearchPage, MailRuSendPage

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
    """Класс тестов с mail.ru"""

    def setUp(self):
        """
        Настройка тестов
        """
        self.driver = WEBDRIVER_REMOTE
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.loginPage = MailRuLoginPage(self.driver)
        self.searchPage = MailRuSearchPage(self.driver)
        self.sendPage = MailRuSendPage(self.driver)

    def test_Mail(self):
        """
        Входной тест с шагами allure
        """
        with allure.step("Загрузка сайта"):
            titleLogin = self.loginPage.goToUrl(MAILRU_LOGIN_LINK)
            self.assertEqual(titleLogin, "Авторизация")
        with allure.step("Логин"):
            titleMail = self.loginPage.login(MAILRU_USERNAME,
                                             MAILRU_PASSWORD)
            self.assertRegex(titleMail, "Входящие - Почта Mail.ru")
        with allure.step("Поиск и счйт писем"):
            countEmails = self.searchPage.findEmailsAndCount(NAME_FROM)
            self.assertGreater(countEmails, 0)

        body = f"От вас пришло писем - {countEmails}"
        subject = f"Тестовое задание {STUDENT_SNAME}"

        with allure.step("Отправка письма"):
            result = self.sendPage.sendEmail(subject, body, NAME_FROM)
            self.assertTrue(result)

    def tearDown(self):
        """Действия по завершению"""
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
