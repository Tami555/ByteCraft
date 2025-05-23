# Интернет-магазин компьютерной техники "ByteCraft"

Flask-приложение для интернет-магазина компьютерных комплектующих с полным циклом работы: от каталога товаров до обработки заказов.

## 🔧 Технологии
- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: API Yandex Maps, Email API, RESTful API
- **База данных**: SQLite с SQLAlchemy ORM

## 🌟 Основные функции
- **Каталог товаров** с фильтрацией по категориям
- **Система пользователей** (регистрация, авторизация, профили)
-**Пополнение баланса карты пользователя**
- **Корзина и избранное**
- **Оформление заказов** с выбором способа доставки
- **Система отзывов** о товарах

## 🗃️ Структура БД
- Пользователи (учетные записи, профили)
- Товары (категории, характеристики, остатки)
- Корзина (корзина пользователя)
- Избранные (избранные пользователя)
- Заказы (корзины, статусы, история)
- Отзывы и рейтинги
- Способы доставки

## 📊 Особенности
- Адаптивный дизайн
- Поиск по каталогу
- Отправка сообщений на почту пользователя при успешном заказе

## 🚀 Установка
1. Клонировать репозиторий
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt

## Важно ❗
- Для того, чтобы работала карта, при оформелии заказа, выборе адреса курьером,
 замените в файле external_API/yandex_map_api.py все API ключи на ваши
  (GeoCode_Api_Key -> https://yandex.ru/maps-api/docs/geocoder-api/quickstart.html 
  StaticMape_Server -> https://yandex.ru/maps-api/docs/static-api/quickstart.html
  )
- Для того чтобы работала отправка сообщений пользователю на почту при успешном заказе
   замените в файле send_email.py все API ключи на ваши
   (login, password, sender_email)


более подробную информацию о структуре проекта смотрите в презентации