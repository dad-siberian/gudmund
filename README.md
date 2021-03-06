# gudmund
Проект, созданный для скачивания снимков планеты Земля, снимков космоса и фотографий с запусков летательных аппаратов Space X.
Скрипт может быть использован для публикации фотографий в Telegram канале.

## Приступая к работе
 1. Склонировать проект:
```
git clone https://github.com/dad-siberian/gudmund.git
cd gudmund
```

2. Создать виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости:
```
pip install -r requirements.txt
```

4. Создать в корне проекта переменную окружения .env и внести настройки. Подробнее в разделе настройка переменной окружения.

## Предварительные условия
Для работы скрипта у вас должен быть установлен python версии 3.8 и выше. 

## Настройка переменной окружения
```
NASA_API={nasa api}
TELEGRAM_API={telegram api key}
TIMEOUT={время в секундах}
CHAT_ID={@telegram_channel_id}
```

Nasa api можно сгенерировать заполнив форму на сайте [NASA Open APIs](https://api.nasa.gov/). Необходимо для скачивания снимков NASA.

Для публикации фотографий в телеграм канале необходимо:
- создать телеграм бота у [@BotFather](https://telegram.me/BotFather) ([инструкция](https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/)).  Полученный token api необходимо присвоить переменной TELEGRAM_API. 
- добавить бота в канал и предоставить ему права администратора.
- присвоить переменной CHAT_ID ссылку на телеграм канал, например @gudmund198

Бот будет публиковать фотографии с переодичностью,  указанной в переменной TIMEOUT. Время указывается в секундах (3600  для 1 часа,  86400 для 1 суток)

## Использование

Для скачивания фотографии Земли (папка EPIC) и снимков космоса (папка NASA) запустить `fetch_nasa.py`.
Для скачивания фотографий с последнего запуска SpaceX запустить `fetch_nasa.py`.
Для публикации фотографий в канал запустить `gudmund_bot.py`

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков  [dvmn.org](https://dvmn.org/)






