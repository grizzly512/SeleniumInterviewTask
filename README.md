## Тестовое задание на вакансию Разработчик в теестировании:
1. Использовать Python, подключить библиотеку Selenium Webdriver;
2. С помощью Selenium открыть браузер, открыть ~~gmail.com~~ mail.ru (c gmail сейчас проблемы), авторизоваться, зайти на почту;
3. С помощью Selenium определить, сколько нашлось писем от заданного адресата;
4. С помощью Selenium и интерфейса почты автоматически написать и отправить письмо заданному адресату, в тексте которого указать найденное в шаге 3 количество писем. Указать тему письма "Тестовое задание <Фамилия>".
5. Оформить эти действия в виде теста.

## Для запуска (Linux):
1. Скачайте selenium server c [офф.сайта](https://www.selenium.dev/downloads/).
2. Положите его в ./selenium/selenium-server.jar
3. Дайте права на исполнение sh скриптам: 
    ```sh
    chmod +x runHub.sh runServer.sh runTest.sh
    ```
4. Создайте виртуальное окружение:
    ```sh
    virtualenv ./venv
    ```
5. Активируйте окружение и установите зависимости:
    ```sh
    source ./venv/bin/activate
    pip install -r requirements.txt
    ```
6. Запустите Hub
    ```sh
    sh ./runHub.sh
    ```
7. Запустите Server
    ```sh
    sh ./runServer.sh
    ```
8. Запустите Test
    ```sh
    sh ./runTest.sh
    ```
9. При необходимости можно отредактировать runTest.sh для запуска пяти тестов одновременно:
    ```sh
    source ./venv/bin/activate
    python -m pytest main.py --alluredir ./results &
    python -m pytest main.py --alluredir ./results &
    python -m pytest main.py --alluredir ./results &
    python -m pytest main.py --alluredir ./results &
    python -m pytest main.py --alluredir ./results
    ```
10. [Установите Allure](https://docs.qameta.io/allure/)
11. Для просмотра отчетов:
    ```sh
    allure serve ./results/
    ```