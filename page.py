# -*- coding: utf-8 -*-
import random
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

    def goToUrl(self, url: str):
        assert isinstance(url, str)
        self.driver.get(url)
        sleep(random.uniform(1.0, 3.0))
        title = self.driver.title
        assert isinstance(title, str)
        return title

    def findAndAction(self,
                      xpathStr: str = None,
                      returnKey: bool = False,
                      click: bool = False,
                      stringToType: str = None):

        wait = WebDriverWait(self.driver, 10)
        if xpathStr is not None:
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpathStr)))
        else:
            element = self.driver.switch_to.active_element
        if click:
            element.click()

        if stringToType is not None:
            for key in stringToType:
                element.send_keys(key)
                sleep(random.uniform(0.02, 0.1))
        if returnKey:
            sleep(random.uniform(0.5, 0.7))
            element.send_keys(Keys.RETURN)
        sleep(random.uniform(2.0, 3.0))
        return element


class MailRu(BasePage):

    def login(self,
              MailRuUsername: str,
              MailRuPassword: str):
        assert isinstance(MailRuUsername, str)
        assert isinstance(MailRuPassword, str)
        # Вводим имя пользователя
        self.findAndAction(
            xpathStr='//input[@name="username"]',
            returnKey=True,
            stringToType=MailRuUsername)
        # Вводим пароль
        self.findAndAction(
            xpathStr='//input[@name="password"]',
            returnKey=True,
            stringToType=MailRuPassword)

        sleep(random.uniform(5.0, 7.0))
        title = self.driver.title
        assert isinstance(title, str)
        return title

    def findAndCountEmails(self, nameFrom: str):
        assert isinstance(nameFrom, str)

        self.findAndAction(
            xpathStr='//span[@class ="search-panel-button__text"]',
            click=True)

        self.findAndAction(
            xpathStr='//input',
            returnKey=True,
            stringToType=nameFrom)

        mails = self.driver.find_elements(By.XPATH, '//span[@class="ll-crpt"]')
        tags = self.driver.find_elements(By.XPATH, '//div[@class="ll-f"]')

        correctEmailsCount = 0
        i = 0
        for mail in mails:
            nameInTitle = nameFrom in mail.get_attribute("title")
            inbox = tags[i].get_attribute("title") == "Входящие"
            if nameInTitle and inbox:
                correctEmailsCount += 1
            i += 1
        sleep(random.uniform(3.0, 5.0))
        assert isinstance(correctEmailsCount, int)
        return correctEmailsCount

    def sendEmail(self, subject: str, textBody: str,
                  nameoOrAdress: str,
                  ):
        assert isinstance(subject, str)
        assert isinstance(textBody, str)
        assert isinstance(nameoOrAdress, str)

        self.findAndAction(
            xpathStr='//span[text() ="Написать письмо"]',
            click=True)

        self.findAndAction(
            returnKey=True,
            stringToType=nameoOrAdress)

        self.findAndAction(
            xpathStr='//input[@name = "Subject"]',
            returnKey=True,
            stringToType=subject)

        self.findAndAction(
            xpathStr='//div[@contenteditable = "true"]',
            returnKey=True,
            stringToType=textBody)

        self.findAndAction(
            xpathStr='//span[text() = "Отправить"]',
            click=True)

        sleep(random.uniform(3.0, 5.0))

        result = self.findAndAction(
            xpathStr='//a[text() = "Письмо отправлено"]')

        assert result is not None

        return True


class Gmail(BasePage):
    pass
