## Telegram bot для записи к врачу

**Telegram bot для ГУЗ СГКБ 10.**

- Запись к врачу
- Вызов врача на дом
- Отмена записи

### Стек технологий:

- `Python`
- `Aiogram`

## Содержание

<details>
<summary>Инструкция по развертыванию проекта</summary>

#### 1. Установите зависимости из файла requirements.txt

#### 2. Настройте переменные окружения:

1. Создайте файл `.env` в корневой директории
2. Скопируйте в него содержимое файла `.env_example` и подставьте свои значения

</details>

<details>
<summary>Использование</summary>

#### 1. Создание бота:

Перед началом использования приложения у вас должен быть ID Telegram бота, который нужно подставить в переменные
окружения (файл .env).

#### 2. Создание группы:

Также необходимо создать группу в телеграм, куда будут отправляться сообщения от бота. ID этой группы нужно подставить в
переменные окружения (файл .env) со знаком "-".

#### 3. Принцип работы:

1. Бот задает вопрос пользователю, что он хочет: записаться к врачу, вызвать врача на дом или отменить запись.
2. Далее спрашивает нужные данные.
3. Отправляет это сообщение от пользователя в группу Телеграм, где это сообщение обрабатывает сотрудник учреждения (
   регистратор).

</details>
