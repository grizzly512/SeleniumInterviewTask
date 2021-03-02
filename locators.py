from selenium.webdriver.common.by import By


class MailRuLoginPageLocators(object):

    USER_NAME = (By.XPATH, '//input[@name="username"]')
    PASSWD = (By.XPATH, '//input[@name="password"]')


class MailRuSearchPageLocators(object):
    SEARCH_BUTTON = (By.XPATH, '//span[@class ="search-panel-button__text"]')
    SEARCH_FIELD = (By.XPATH, '//input')
    MAILS = (By.XPATH, '//span[@class="ll-crpt"]')
    TAGS = (By.XPATH, '//div[@class="ll-f"]')


class MailRuCreateEmailLocators(object):
    MAIL_CREATE_BUTTON = (By.XPATH, '//span[text() ="Написать письмо"]')
    MAIL_SUBJECT = (By.XPATH, '//input[@name = "Subject"]')
    MAIL_BODY = (By.XPATH, '//div[@contenteditable = "true"]')
    MAIL_SEND_BUTTON = (By.XPATH, '//span[text() = "Отправить"]')
    MAIL_SENDED = (By.XPATH, '//a[text() = "Письмо отправлено"]')
