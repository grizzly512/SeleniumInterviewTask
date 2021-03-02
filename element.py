from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePageElement(object):
    """Базовый элемент"""

    def __set__(self, obj, value):
        """Ждем, пока элемент появится, после посылаем текст"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located(self.locator))
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Ждем, пока элемент появится, после возвращаем элемент"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located(self.locator))
        element = driver.find_element(*self.locator)
        return element
