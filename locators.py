from selenium.webdriver.common.by import By


class MailRuLoginPageLocators(object):
    """Локаторы для страницы входа"""

    USER_NAME = (By.XPATH, '//input[@name="username"]')
    PASSWD = (By.XPATH, '//input[@name="password"]')
    INCORRECT_PASSWORD = (
        By.XPATH, '//small[text() = "Неверный пароль, попробуйте ещё раз"]')


class MailRuSearchPageLocators(object):
    """Локаторы для страницы поиска"""

    SEARCH_BUTTON = (By.XPATH, '//span[@class ="search-panel-button__text"]')
    SEARCH_FIELD = (By.XPATH, '//input')
    MAILS = (By.XPATH, '//span[@class="ll-crpt"]')
    TAGS = (By.XPATH, '//div[@class="ll-f"]')


class MailRuCreateEmailLocators(object):
    """Локаторы для страницы отправки письма"""

    MAIL_CREATE_BUTTON = (By.XPATH, '//span[text() ="Написать письмо"]')
    MAIL_SUBJECT = (By.XPATH, '//input[@name = "Subject"]')
    MAIL_BODY = (By.XPATH, '//div[@contenteditable = "true"]')
    MAIL_SEND_BUTTON = (By.XPATH, '//span[text() = "Отправить"]')
    MAIL_SENDED = (By.XPATH, '//a[text() = "Письмо отправлено"]')
