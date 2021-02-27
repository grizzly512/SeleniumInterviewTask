# -*- coding: utf-8 -*-

import os
import unittest
import pytest
import allure
from envparse import env
from selenium import webdriver
from selenium_stealth import stealth
from page import MailRu

currentDir = os.path.dirname(os.path.abspath(__file__))
env.read_envfile(currentDir + '/.env')

MAILRU_LOGIN_LINK = os.environ['MAILRU_LOGIN_LINK']
MAILRU_USERNAME = os.environ['MAILRU_USERNAME']
MAILRU_PASSWORD = os.environ['MAILRU_PASSWORD']
NAME_FROM = os.environ['NAME_FROM']
STUDENT_NAME = os.environ['STUDENT_NAME']

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

WEBDRIVER = webdriver.Chrome(
    options=options,
    executable_path="/usr/bin/chromedriver")

stealth(WEBDRIVER,
        languages=["ru-RU", "ru"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


class MailRuTest(unittest.TestCase):

    def setUp(self):
        self.driver = WEBDRIVER
        self.page = MailRu(self.driver)

    def test_Mail(self):
        with allure.step("Загрузка сайта"):
            self.load_site(MAILRU_LOGIN_LINK)
        with allure.step("Логин"):
            self.login(MAILRU_USERNAME, MAILRU_PASSWORD)
        with allure.step("Счёт писем"):
            emailsCount = self.findAndCountEmails(NAME_FROM)

        body = "От вас пришло писем - {}".format(emailsCount)
        subject = "Тестовое задание {}".format(STUDENT_NAME)
        with allure.step("Отправка письма"):
            self.sendEmail(NAME_FROM, body, subject)

    def load_site(self, url: str):
        titleLogin = self.page.goToUrl(url)
        self.assertEqual(titleLogin, "Авторизация")

    def login(self, userName, passwrd):
        titleMail = self.page.login(userName, passwrd)
        self.assertRegex(titleMail, "Входящие - Почта Mail.ru")

    def findAndCountEmails(self, fromWho):
        countEmails = self.page.findAndCountEmails(fromWho)
        self.assertGreater(countEmails, 0)
        return countEmails

    def sendEmail(self, toWho, body, subject):
        result = self.page.sendEmail(nameoOrAdress=toWho,
                                     textBody=body,
                                     subject=subject)
        self.assertTrue(result)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
