# Скрипт для создания коротких ссылок

При вводе полной ссылки выводится сокращенная ссылка. При вводе сокращенной ссылки показывается количество переходов по ней.

## Цели проекта

* Создать консольную утилиту, сокращающую ссылки.
* Добавить возможность считать количество переходов по введенной короткой ссылке.
> Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

### Пример работы

![Пример](https://github.com/etokosmo/bitlinks/blob/main/github/bitly_example.gif)

## Конфигурации

* Python version: 3.10
* Libraries: requirements.txt

## Запуск

- Скачайте код
- Установите библиотеки командой:
```bash
pip install -r requirements.txt
```
- Запишите переменные окружения в файле `.env`
```bash
TOKEN=... #Токен полученный на https://app.bitly.com/
```
- Запустите утилиту командой 
```bash
python3 main.py <link> #где <link> ваша полная ссылка
```
