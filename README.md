# tea_store
Проект интернет-магазина Чая - "Tea Shop"

### Технологии

    Django==4.2
    Bootstrap ~5
    Python ~3.11
    PostgreSQL 16.0

---

###  Установка и использование

+ Клонируйте репозиторий: git clone git@github.com:nataliadudina/catalog.git
+ Перейдите в каталог проекта: cd catalog
+ Создайте (python3 -m venv env) и активируйте  (.\env\Scripts\activate) виртуальное окружение
+ Активируйте виртуальное окружение: source env/bin/activate (Linux/Mac) или .\env\Scripts\activate (Windows)
+ Установите зависимости: poetry install (требуется предварительная установка poetry)
+ Примените миграции: python manage.py migrate
+ Запустите сервер: python manage.py runserver

Для работы с базой данных необходимо создать файл .env с параметрами доступа к базе данных PostgresSQL. 
Пример содержимого файла:
```
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_PORT=1111
POSTGRES_DB=postgres

```
---

### Структура проекта

    Проект "Tea Shop" состоит из трёх приложений:
    1) main: модели TeaProduct, TeaCategory, Version
    2) store_blog: модель Article
    3) users: модель User
---

### Структура сайта

#### Меню состоит: 
    
+ Ссылки "На главную"
+ Выпадающего меню - ссылки на категории товаров. 
  Пользователи, входящие в группу moderator, также видят ссылки на форму добавления товара и админ-панель.
+ Обратной связи - отправленные данные записываются в json-файл
+ Кнопок авторизации/профиля и регистрации/выхода

#### Футер (6 ссылок):

- Ссылка на блог (Tea Stories)
- 4 ссылки-заглушки
- Обратная связь
- Кнопка "наверх"

#### Приложение main

- Главная страница состоит из карусели и карточек 4 случайных продуктов в наличии, которые содержат название, изображение и начало описания.
  Есть ссылка на страницу со списком категорий/видов чая.

- На странице каждой категории представлен список товаров в наличии.
- Страница-карточка отдельного товара выводит всю информацию о выбранном товаре из Базы Данных. Для удобства в карточку добавлены ссылки для перехода к списку товаров данной категории и к списку категорий. 
  У пользователей, входящих в группу moderator, есть возможность редактировать и удалять товар, создавать версии продукта (устанавливать спец.предложения).

#### Blog app

- Основная страница - список статей и ссылка на форму "написать статью". Любой зарегистрированный пользователь может создать пост.
- Страница просмотра статьи с отображением автора, количества просмотров, даты создания. Только состоящие в группе контент-менеджер и автор статьи могут править или удалять пост.

#### Users app

* Регистрация: почта и пароль (обязательные поля) или через соцсеть (GitHub)
* Авторизация: по username или email, или через соцсеть (GitHub)
  Авторизованные пользователи могут постить статьи и редактировать или удалять свои посты. Все права для раздела blog есть также у пользователь с группой доступа content-manager.
  Пользователю со статусом is_staff и с группой доступа moderator доступен функционал создания и редактирования продукта через админ-панель и интерфейс сайта. 
  Для пользователей без необходимого доступа все функциональные кнопки скрыты.

---
    
### Дополнительно

Есть кастомная команда, которая умеет заполнять данные в базу данных, при этом предварительно зачищать ее от старых данных.

Созданы фикстуры для таблиц main_teaproduct и store_blog_article.

Реализованы пользовательские теги, контекстный процессор.

Есть пользовательский менеджер модели и перечисляемые поля (TextChoices).

Динамически создаются адреса, состоящие из слагов связанных моделей.

Настроена админ-панель с возможностью фильтрации, сортировки, поиска, выбора действия.

Есть обработчик ошибки 404.
