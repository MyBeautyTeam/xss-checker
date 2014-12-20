# XSS CHECKER

Курсовой проект по курсу "Анализ защищенности" 
Технопарк@mail.ru МГТУ им. Баумана


***

Перед запуском необходимо: 

1) Убедиться, что установлен Firefox WebDriver https://code.google.com/p/selenium/wiki/FirefoxDriver

2) Запустить Selenium Server из папки Seleniun:
`java -jar selenium-server-standalone-2.43.1.jar`


***
Запуск командой
`python main.py http://www.example.ru/`

Флаги:
-o   -    проверять всего одну страницу
-l   -    перед началом сдедать задержку в 30 секунд на авторизацию

----
**Внимание**, по урлам:
* * http://beautyteam.cloudapp.net/scriptlet.html
* * http://beautyteam.cloudapp.net/xss.css
* * http://beautyteam.cloudapp.net/xssmoz.xml
* * http://beautyteam.cloudapp.net/xss.jpg
* * http://beautyteam.cloudapp.net/xss.js
содержится код

`location.hash="SMILE"`

Перед запуском рекомендуется проверить доступность этих файлов. Если необходимо - заменить в исходном коде в файле XssChecker.py на доступные, для повышения эффективности программы.
