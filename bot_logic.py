# импорты для конфигурации движка приложения
import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union
from datetime import datetime
import time
import calendar
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Message
TOKEN_API_KEY= os.getenv("TOKEN_API_KEY")
bot_id=os.getenv("bot_id")
moi_id=os.getenv("moi_id")
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bs4 import BeautifulSoup
import requests
from faststream.rabbit import RabbitBroker
projekt=[]
# для тестов
#projekt=[0,0,0,0,0,0,0,0,0,0,0,0]
#projekt[0]="закрепить доску на колёсики"
#projekt[1]="доска сводобно ездит на колёсиках по комнтате"
#projekt[2]="найти и купить вторую коляску"
#projekt[3]="отпилить колёсики у первой коляски"
#projekt[4]="отпилить колёсики у второй коляски"
#projekt[5]="измерить доски и рассчитать количество балок"
#projekt[6]="Купить и привезти из магазина первую часть балок"
#projekt[7]="Купить и привезти из магазина вторую часть балок"
#projekt[8]="Прикрепить балку к левой части доски"
#projekt[9]="Прикрепить балку к правой части доски"
#projekt[10]="Соединить балки с колесиками"
#projekt[11]="Уборка помещения"
projekt_long=[]
projekt_predstv_etapov=[]
etapy_projektov_svodka=[]
cislo_projekt_arhiv=0
id_projekt_arhiv=0
nov_id_projekt_arhiv=0
razovoje_delo=[]
razovoje_delo_long=[]
kalendarnoje=[]
zapis_kalendarnoje=0
validacija_kalendarnoje=0
kalendarnoje_DB=[]
privycka_long=[]
id_dela=0
id_kalendarnogo=1
nov_id_dela=0
kolvo_del=0
kolvo_privychek=0
kontrol_dney=0
id=1
id_zametki=1
id_privycki=0
nov_id_privycki=1
zapis=0
zapis_dela=0
zametka=[]
zametka_long=[]
zapis_zametk=0
validacija_zametki=0
validacija_projekta=0
validacija_dela=0
validacija_privycki=0
nov_id_zametki=0
kolvo_zametok=0
zametki_artikul=[]
nov_id_projekta=0
id_projekta=0
kolvo_projektov=0
projekti_artikul=0
privycka=[]
zapis_privycki=0
svodka_privychek=[]
kontrol_dney=1
proverka_1=0
proverka_2=0
proverka_3=0
proverka_4=0
proverka_5=0
naydennost=0
id_proverka_arhiv=1000
#работа с базой данных
from sqlalchemy import  DateTime, String, Float, Column, Integer, func, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
engine = create_async_engine(os.getenv("DBURL"),echo=True,max_overflow=5,pool_size=5)
session_factory = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
class Base(DeclarativeBase):
    pass
#class Ученики(Base):
#__tablename__="Ученики"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Фамилия: Mapped[str]=mapped_column(String(128), nullable=False)
#Имя: Mapped[str]=mapped_column(String(128), nullable=False)
#class Предметы(Base):
#__tablename__="Предметы"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Название_Предмета: Mapped[str]=mapped_column(String(32), nullable=False)
#class Даты(Base):
# __tablename__="Даты"
#id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Дата: Mapped[str]=mapped_column(String(128), nullable=False)
#class Ступени_Обучения(Base):
#__tablename__ = "Ступени_Обучения"
#id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
#Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
# отправить запрос системе управления
class Уроки(Base):
    __tablename__ = "Уроки"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Имя_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Предмет_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Имя_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_Проведения: Mapped[str] = mapped_column(String(128), nullable=False)
    Время_Начала: Mapped[str] = mapped_column(String(128), nullable=False)
    Длительность_Занятия_Мин: Mapped[int]
    Стоимость_Занятия_Центов: Mapped[int]
    Что_Делали_На_Уроке: Mapped[str] = mapped_column(Text, nullable=False)
    Задание_На_Дом: Mapped[str] = mapped_column(String(128), nullable=False)
    Примечание: Mapped[str] = mapped_column(Text, nullable=False)
class Уроки_Архив(Base):
    __tablename__ = "Уроки_Архив"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Имя_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Преподавателя: Mapped[str] = mapped_column(String(128), nullable=False)
    Предмет_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Имя_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Фамилия_Ученика: Mapped[str] = mapped_column(String(128), nullable=False)
    Ступень_Обучения: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_Проведения: Mapped[str] = mapped_column(String(128), nullable=False)
    Время_Начала: Mapped[str] = mapped_column(String(128), nullable=False)
    Длительность_Занятия_Мин: Mapped[int]
    Стоимость_Занятия_Центов: Mapped[int]
    Что_Делали_На_Уроке: Mapped[str] = mapped_column(Text, nullable=False)
    Задание_На_Дом: Mapped[str] = mapped_column(String(128), nullable=False)
    Примечание: Mapped[str] = mapped_column(Text, nullable=False)
class Календарные(Base):
    __tablename__ = "Календарные"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Название_События: Mapped[str] = mapped_column(String(128), nullable=False)
    Вид_События: Mapped[str] = mapped_column(String(128), nullable=False)
    Локация_События: Mapped[str]  = mapped_column(String(128), nullable=False)
    Участник_События: Mapped[str]  = mapped_column(String(128), nullable=False)
    Начало_События: Mapped[str]  = mapped_column(String(128), nullable=False)
    Окончание_События: Mapped[str]  = mapped_column(String(128), nullable=False)
    Отметка_Времени: Mapped[int]  = mapped_column(nullable=False)
#CREATE table Календарные (id BIGINT NOT NULL PRIMARY KEY, Название_События VARCHAR(128) NOT NULL, Вид_События VARCHAR(128) NOT NULL, Локация_События VARCHAR(128) NOT NULL,
#Участник_События VARCHAR(128) NOT NULL, Начало_События VARCHAR(128) NOT NULL, Окончание_События VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL);
class Привычки(Base):
    __tablename__ = "Привычки"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Требуемый_Навык: Mapped[str] = mapped_column(String(128), nullable=False)
    Главное_Препятствие: Mapped[str] = mapped_column(String(128), nullable=False)
    Помогающий_Человек: Mapped[str] = mapped_column(String(128), nullable=False)
    Триггер_Привычки: Mapped[str] = mapped_column(String(128), nullable=False)
    Награда_Привычки: Mapped[str] = mapped_column(String(128), nullable=False)
    Требование_Заказчика: Mapped[str] = mapped_column(String(128), nullable=False)
    Требование_Исполнителя: Mapped[str] = mapped_column(String(128), nullable=False)
    Целевое_Число_Повторений: Mapped[int]  = mapped_column(nullable=False)
    Выполненное_Число_Повторений: Mapped[int]  = mapped_column(nullable=False)
    Дата_Регистрации_Ритуала: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_Выполнения_Ритуала: Mapped[str] = mapped_column(String(128), nullable=False)
    Отметка_Времени: Mapped[int]  = mapped_column(nullable=False)
#CREATE table Привычки(id BIGINT NOT NULL PRIMARY KEY, Требуемый_Навык VARCHAR(128), Главное_Препятствие VARCHAR(128)
# NOT NULL, Помогающий_Человек VARCHAR(128) NOT NULL, Триггер_Привычки VARCHAR(128) NOT ULL, Награда_Привычки VARCHAR(128)
#NOT NULL, Требование_Заказчика VARCHAR(128) NOT NULL, Требование_Исполнителя VARCHAR(128) NOT NULL, Целевое_Число_Повторений
#BIGINT NOT NULL, Выполненное_Число_Повторений BIGINT NOT NULL, Дата_регистрации_ритуала VARCHAR(128) NOT NULL,
#Дата_выполнения_ритуала VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL)
class Заметки(Base):
    __tablename__ = "Заметки"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Текст_заметки: Mapped[str] = mapped_column(Text, nullable=False)
    Тема_1: Mapped[str] = mapped_column(String(128), nullable=False)
    Тема_2: Mapped[str] = mapped_column(String(128), nullable=False)
    Тема_3: Mapped[str] = mapped_column(String(128), nullable=False)
    Тема_4: Mapped[str] = mapped_column(String(128), nullable=False)
    Тема_5: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_регистрации: Mapped[str] = mapped_column(String(128), nullable=False)
    Отметка_Времени: Mapped[int]  = mapped_column(nullable=False)
#CREATE table Заметки(id BIGINT NOT NULL PRIMARY KEY, Текст_заметки TEXT NOT NULL, Тема_1 VARCHAR(128) NOT NULL, Тема_2
#VARCHAR(128) NOT NULL, Тема_3 VARCHAR(128) NOT NULL, Тема_4 VARCHAR(128) NOT NULL, Тема_5 VARCHAR(128) NOT NULL,
#Дата_регистрации VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL)
class Проект(Base):
    __tablename__ = "Проект"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Название_проекта: Mapped[str] = mapped_column(String(128), nullable=False)
    Критерий_завершенности: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершённость_проекта: Mapped[int]  = mapped_column(nullable=False)
    Этап_1: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_1: Mapped[int]  = mapped_column(nullable=False)
    Этап_2: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_2: Mapped[int]  = mapped_column(nullable=False)
    Этап_3: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_3: Mapped[int]  = mapped_column(nullable=False)
    Этап_4: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_4: Mapped[int]  = mapped_column(nullable=False)
    Этап_5: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_5: Mapped[int]  = mapped_column(nullable=False)
    Этап_6: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_6: Mapped[int]  = mapped_column(nullable=False)
    Этап_7: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_7: Mapped[int]  = mapped_column(nullable=False)
    Этап_8: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_8: Mapped[int]  = mapped_column(nullable=False)
    Этап_9: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_9: Mapped[int]  = mapped_column(nullable=False)
    Этап_10: Mapped[str] = mapped_column(String(128), nullable=False)
    Завершенность_Этап_10: Mapped[int]  = mapped_column(nullable=False)
    Дата_регистрации: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_изменения: Mapped[str] = mapped_column(String(128), nullable=False)
    Синхронизация: Mapped[int] = mapped_column(nullable=False)
class Проект_Архив(Base):
    __tablename__ = "Проект_Архив"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Название_проекта: Mapped[str] = mapped_column(String(128), nullable=False)
    Критерий_завершенности: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_1: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_2: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_3: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_4: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_5: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_6: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_7: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_8: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_9: Mapped[str] = mapped_column(String(128), nullable=False)
    Этап_10: Mapped[str] = mapped_column(String(128), nullable=False)
    Дата_внесения: Mapped[str] = mapped_column(String(128), nullable=False)
    Синхронизация: Mapped[int] = mapped_column(nullable=False)
#CREATE table Проект(id BIGINT NOT NULL PRIMARY KEY, Название_проекта VARCHAR(128) NOT NULL, Критерий_завершенности VARCHAR(128) NOT NULL,
#Завершённость_пректа INT NOT NULL, Этап_1 VARCHAR(128) NOT NULL, Завершенность_Этап_1 INT NOT NULL, Этап_2 VARCHAR(128)
#NOT NULL, Завершенность_Этап_2 INT NOT NULL, Этап_3 VARCHAR(128) NOT NULL, Завершенность_Этап_3 INT NOT NULL, Этап_4
#VARCHAR(128) NOT NULL, Завершенность_Этап_4 INT NOT NULL, Этап_5 VARCHAR(128) NOT NULL, Завершенность_Этап_5 INT NOT NULL,
#Этап_6 VARCHAR(128) NOT NULL, Завершенность_Этап_6 INT NOT NULL, Этап_7 VARCHAR(128) NOT NULL, Завершенность_Этап_7
#INT NOT NULL, Этап_8 VARCHAR(128) NOT NULL, Завершенность_Этап_8 INT NOT NULL, Этап_9 VARCHAR(128) NOT NULL,
#Завершенность_Этап_9 INT NOT NULL, Этап_10 VARCHAR(128) NOT NULL, Завершенность_Этап_10 INT NOT NULL, Дата_регистрации
#VARCHAR(128) NOT NULL, Дата_изменения VARCHAR(128) NOT NULL)'''
class Дело(Base):
    __tablename__ = "Дела"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    Трудовая_Задача: Mapped[str] = mapped_column(String(128), nullable=False)
    Одноразовое_Проект: Mapped[str] = mapped_column(String(32), nullable=False)
    Помошник: Mapped[str] = mapped_column(String(32), nullable=False)
    Группа_Задач: Mapped[str] = mapped_column(String(32), nullable=False)
    Срок_Выполнения: Mapped[str] = mapped_column(String(32), nullable=False)
    Отметка_времени : Mapped[str] = mapped_column(String(32), nullable=False)
    Синхронизация: Mapped[int]  = mapped_column(nullable=False)
#CREATE table Дела (id BIGINT NOT NULL PRIMARY KEY, Что_Cделать VARCHAR(128) NOT NULL, Одноразовое_Проект VARCHAR(128) NOT NULL,
#Помошник VARCHAR(128) NOT NULL, Группа_Задач VARCHAR(128) NOT NULL, Срок_Выполнения VARCHAR(128) NOT NULL,
#Отметка_времени VARCHAR(128) NOT NULL, Синхронизация BIGINT NOT NULL)
# импорты фреймворка
from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# импорты для машины конечных состояний
from aiogram.fsm.state import State, StatesGroup
from fsm_strategy import Sostavlenije_Zamekti, Poisk_ZametKi, Sbornik_ZametKi, Projekt_V_Arhiv, Projekt_Pokaz_Etapy
from aiogram.types import BotCommand
import psycopg2 as ps
from colorama import *
# импорты фреймворка
# этр образ бота в программе
Bot = Bot(TOKEN_API_KEY)
# это обьект для обработки сообщений
dp=Dispatcher()
# убрать зайца
#broker=RabbitBroker(url="amqp://guest:guest@localhost:5672/")
#@broker.subscriber("UROKI")
#async def get_uroki_fromFASTAPI(data: str):
#await Bot.send_message(chat_id=os.getenv('bot_id'), text='СООБЩЕНИЕ')
#await Bot.send_message(chat_id=os.getenv('bot_id'),text=data)
# Работа с заметками
class PrivyckaSvodka(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> None:
        text = event.text
        user_id = event.from_user.id
        global nov_id_privycki
        global id_privycki
        global kolvo_privychek
        global svodka_privychek
        if text =="привычка":
            kolvo_privychek = 0
            svodka_privychek=[]
            await self.bot.send_message(chat_id=user_id, text="Начинаем работать с привычками")
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * FROM Привычки;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    id = next_row[0]
                    kolvo_privychek = kolvo_privychek + 1
                    vypiska_privycki = []
                    vypiska_privycki.append(next_row[0])
                    vypiska_privycki.append(next_row[1])
                    vypiska_privycki.append(next_row[8])
                    svodka_privychek.append(vypiska_privycki)
                    if id > nov_id_privycki:
                        nov_id_privycki = id
                else:
                    break
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            id_privycki = nov_id_privycki + 1
            await self.bot.send_message(chat_id=user_id, text=f"{'Доступный артикул привычки: '}{id_privycki}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Всего привычек:'}{kolvo_privychek}")
            await self.bot.send_message(chat_id=user_id, text=f"{svodka_privychek}")
            return await handler(event, data)
        else:
            return await handler(event, data)
# Работа с заметками
class DelaSvodka(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> None:
        text = event.text
        user_id = event.from_user.id
        global nov_id_dela
        global id_dela
        global kolvo_del
        if text =="разовое дело":
            kolvo_del = 0
            await self.bot.send_message(chat_id=user_id, text="Начинаем работать с разовыми делами")
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * FROM Дела;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    id = next_row[0]
                    kolvo_del = kolvo_del + 1
                    if id > nov_id_dela:
                        nov_id_dela = id
                else:
                    break
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            id_dela = nov_id_dela + 1
            await self.bot.send_message(chat_id=user_id, text=f"{'Следующий доступный номер дела: '}{id_dela}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Всего дел:'}{kolvo_del}")
            return await handler(event, data)
        else:
            return await handler(event, data)
# Работа с заметками
class ZametkiSvodka(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> None:
        text = event.text
        user_id = event.from_user.id
        global nov_id_zametki
        global id_zametki
        global kolvo_zametok
        global zametki_artikul
        if text == "заметка":
            kolvo_zametok = 0
            zametki_artikul = []
            await self.bot.send_message(chat_id=user_id, text="Начинаем работать с заметками")
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * FROM Заметки;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    id = next_row[0]
                    kolvo_zametok = kolvo_zametok + 1
                    if id > nov_id_zametki:
                        nov_id_zametki = id
                else:
                    break
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            id_zametki = nov_id_zametki + 1
            await self.bot.send_message(chat_id=user_id, text=f"{'Следующий доступный номер заметки: '}{id_zametki}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Всего записей:'}{kolvo_zametok}")
            return await handler(event, data)
        else:
            return await handler(event, data)
class ProjektySvodka(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> None:
        text = event.text
        user_id = event.from_user.id
        global nov_id_projekta
        global id_projekta
        global kolvo_projektov
        global projekti_artikul
        global projekt_predstv_etapov
        global etapy_projektov_svodka
        global cislo_projekt_arhiv
        global id_projekt_arhiv
        global nov_id_projekt_arhiv
        if text == "проект":
            kolvo_projektov = 0
            cislo_projekt_arhiv = 0
            projekti_artikul = []
            etapy_projektov_svodka = []
            await self.bot.send_message(chat_id=user_id, text="Начинаем работать с проектами")
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"),
            password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * from Проект_Архив;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    cislo_projekt_arhiv = cislo_projekt_arhiv + 1
                    if next_row[0] > id_projekt_arhiv:
                        id_projekt_arhiv = next_row[0]
                else:
                    break
            # создание интерфейса для sql запроса
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            zapros = "SELECT * from Проект;"
            # отправить запрос системе управления
            cursor.execute(zapros)
            while True:
                next_row = cursor.fetchone()
                if next_row:
                    projekt_predstv_etapov = []
                    svjaz=[]
                    svjaz.append(next_row[0])
                    svjaz.append(next_row[1])
                    projekt_predstv_etapov.append(next_row[0])
                    projekt_predstv_etapov.append(next_row[1])
                    projekt_predstv_etapov.append(next_row[2])
                    prodvizenije=[]
                    for i in range (2,12):
                        prodvizenije.append(next_row[2*i+1])
                        projekt_predstv_etapov.append(next_row[2*i])
                    svjaz.append(prodvizenije)
                    pokazatel_uspecha=next_row[2*2+1]*1+next_row[3*2+1]*2+next_row[4*2+1]*3+next_row[5*2+1]*4+next_row[6*2+1]*5+next_row[7*2+1]*6
                    pokazatel_uspecha=pokazatel_uspecha+next_row[8*2+1]*7+next_row[9*2+1]*8+next_row[10*2+1]*9+next_row[11*2+1]*10+next_row[3]*100
                    svjaz.append(pokazatel_uspecha)
                    svjaz.append(next_row[3])
                    projekti_artikul.append(svjaz)
                    etapy_projektov_svodka.append(projekt_predstv_etapov)
                    id = next_row[0]
                    kolvo_projektov = kolvo_projektov + 1
                    if id > nov_id_projekta:
                        nov_id_projekta = id
                else:
                    break
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            id_projekta = nov_id_projekta + 1
            nov_id_projekt_arhiv=id_projekt_arhiv + 1
            await self.bot.send_message(chat_id=user_id, text=f"{'Следующий доступный номер проекта: '}{id_projekta}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Всего записей:'}{kolvo_projektov}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Проекты:'}{projekti_artikul}")
            await self.bot.send_message(chat_id=user_id, text=f"{'Проектов в архиве:'}{cislo_projekt_arhiv}")
            return await handler(event, data)
        else:
            return await handler(event, data)
dp.message.middleware(ZametkiSvodka(Bot))
dp.message.middleware(ProjektySvodka(Bot))
dp.message.middleware(DelaSvodka(Bot))
dp.message.middleware(PrivyckaSvodka(Bot))
from aiogram.types import BotCommand
private=[BotCommand(command="ready",description="запуск работы с органайзером"),
         BotCommand(command="vvod_projekta",description="ввод проекта"),
         BotCommand(command="proverka_bufera",description="проверяем, что записали в буфер"),
         BotCommand(command='ocistka_bufera',description='чистим буфер'),
         BotCommand(command="registracija_projekta",description="информация о создателе Секлетеи"),
        BotCommand(command="start",description="вывод приветственного сообщения"),
        BotCommand(command="stop",description="аварийный останов бота"),
        BotCommand(command="exit",description="отмена поискового запроса, выход из анкеты")]
klava_glav=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="проект"),KeyboardButton(text="разовое дело")],
    [KeyboardButton(text="привычка"),KeyboardButton(text="календарное событие")],
    [KeyboardButton(text="заметка"),KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Выберите, с какой трудовой задачей хотите поработать")
@dp.message((F.text.lower()=="/ready"))
@dp.message((F.text.lower()=="готов"))
async def organizer_glav(message: types.Message):
    await message.answer(text="Начало работы с органайзером",reply_markup=klava_glav)
    print("Начало работы с органайзером")
@dp.message((F.text.lower()=="/exit"))
@dp.message((F.text.lower()=="выход"))
async def vyhod_sbros(message: types.Message,state: FSMContext):
    await message.answer(text="Выход",reply_markup=ReplyKeyboardRemove())
    await state.clear()
# костыль для получения id фото в системе тг
class Vvod_Foto(StatesGroup):
    get_foto_id=State()
@dp.message((F.text.lower()=="скормить_фото"))
async def foto_avatara(message: types.Message, state: FSMContext):
    await message.answer(text="Получение id для фото")
    await state.set_state(Vvod_Foto.get_foto_id)
@dp.message(Vvod_Foto.get_foto_id, F.photo)
async def FotoSsyla(message: types.Message, state: FSMContext):
    await state.update_data(FotoAvatar=message.photo[-1].file_id)
    data=await state.get_data()
    await state.clear()
    await message.answer(text=f"{data}")
    print(data)
# СКРИПТ УПРАВЛЯЮЩИЙ ПРОЕКТАМИ
klava_projekt=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ввод проекта"),KeyboardButton(text="проверка проекта")],
    [KeyboardButton(text="регистрация проекта"),KeyboardButton(text="закрыть этап проекта")],
    [KeyboardButton(text="готовый проект в архив"),KeyboardButton(text="посмотреть этапы проекта")],
     [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Выберите, с каким аспектом проекта хотите поработать")
klava_alfavit_projektov=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="А"),KeyboardButton(text="Б"),KeyboardButton(text="В"),KeyboardButton(text="Г"),KeyboardButton(text="Д"),KeyboardButton(text="Е")],
    [KeyboardButton(text="Ё"),KeyboardButton(text="Ж"),KeyboardButton(text="З"),KeyboardButton(text="И"),KeyboardButton(text="Й"),KeyboardButton(text="К")],
    [KeyboardButton(text="Л"),KeyboardButton(text="М"),KeyboardButton(text="Н"),KeyboardButton(text="О"),KeyboardButton(text="П"),KeyboardButton(text="Р")],
    [KeyboardButton(text="С"),KeyboardButton(text="Т"),KeyboardButton(text="У"),KeyboardButton(text="Ф"),KeyboardButton(text="Х"),KeyboardButton(text="Ч")],
    [KeyboardButton(text="Ш"),KeyboardButton(text="Щ"),KeyboardButton(text="Ы"),KeyboardButton(text="Э"),KeyboardButton(text="Ю"),KeyboardButton(text="Я")]],
    resize_keyboard=True,input_field_placeholder="Начальная буква названия")
klava_nomera_etapov=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="1"),KeyboardButton(text="2"),KeyboardButton(text="3"),KeyboardButton(text="4"),KeyboardButton(text="5")],
    [KeyboardButton(text="6"),KeyboardButton(text="7"),KeyboardButton(text="8"),KeyboardButton(text="9"),KeyboardButton(text="10")],
    [KeyboardButton(text="проект завершен"),KeyboardButton(text="Выход")]],
    resize_keyboard=True,input_field_placeholder="Номер этапа проекта")
prodvizenije=[0,0,0,0,0,0,0,0,0,0,0,0]
prodvizenije[0]=0
prodvizenije[1]=1
prodvizenije[2]=1+2*1
prodvizenije[3]=1+2*1+3*1
prodvizenije[4]=1+2*1+3*1+4*1
prodvizenije[5]=1+2*1+3*1+4*1+5*1
prodvizenije[6]=1+2*1+3*1+4*1+5*1+6*1
prodvizenije[7]=1+2*1+3*1+4*1+5*1+6*1+7*1
prodvizenije[8]=1+2*1+3*1+4*1+5*1+6*1+7*1+8*1
prodvizenije[9]=1+2*1+3*1+4*1+5*1+6*1+7*1+8*1+9*1
prodvizenije[10]=1+2*1+3*1+4*1+5*1+6*1+7*1+8*1+9*1+10*1
prodvizenije[11]=1+2*1+3*1+4*1+5*1+6*1+7*1+8*1+9*1+10*1+100*1
@dp.message((F.text.lower()=="/projekt"))
@dp.message((F.text.lower()=="проект"))
async def segment_projekta(message: types.Message):
    await message.answer(text="Сегмент проекта",reply_markup=klava_projekt)
class Sostavlenije_Projekta(StatesGroup):
    nazvanije=State()
    kriterij_zaver=State()
    etap_1=State()
    etap_2=State()
    etap_3=State()
    etap_4=State()
    etap_5=State()
    etap_6=State()
    etap_7=State()
    etap_8=State()
    etap_9=State()
    etap_10=State()
class VypEtap_Projekta(StatesGroup):
    bukva_projekta=State()
    artikul_projekta = State()
    nomer_etapa = State()
@dp.message((F.text.lower()=="посмотреть этапы проекта"))
async def etapy_projekta_1(message: types.Message, state: FSMContext):
    await message.answer(text="Укажи первую букву, на которую начинается название проекта",reply_markup=klava_alfavit_projektov)
    await state.set_state(Projekt_Pokaz_Etapy.bukva_pokaz_projekta)
@dp.message(Projekt_Pokaz_Etapy.bukva_pokaz_projekta, F.text)
async def etapy_projekta_2(message: types.Message,state: FSMContext):
    text = message.text
    match_counter=0
    bukva_zapros = text.lower()
    for i in range(len(projekti_artikul)):
        katalog_projekta = projekti_artikul[i]
        nazv_projekta = katalog_projekta[1]
        bukva_projekta = nazv_projekta[0]
        peremycka=(" : ")
        if bukva_zapros == bukva_projekta.lower():
            await message.answer(text=f"{katalog_projekta[0]}{peremycka}{katalog_projekta[1]}")
        match_counter = match_counter + 1
    if match_counter == 0:
        await message.answer(text="На данную букву не нашлось не одного проекта")
        await state.clear()
    else:
        await message.answer(text="Укажи порядковый номер проекта для просмотра его этапов", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Projekt_Pokaz_Etapy.artikul_pokaz_projekta)
@dp.message(Projekt_Pokaz_Etapy.artikul_pokaz_projekta, F.text)
async def etapy_projekta_3(message: types.Message,state: FSMContext):
    try:
        artikul_projekta = message.text
        nomer_projekta_vvod = int(artikul_projekta)
    except ValueError:
        await message.answer(text="Введи артикул, который хотите завершить, корректно!")
        await state.set_state(Projekt_Pokaz_Etapy.artikul_pokaz_projekta)
    for i in range(len(etapy_projektov_svodka)):
        projekt_svedenije=etapy_projektov_svodka[i]
        nomer_projekta_baza=projekt_svedenije[0]
        if nomer_projekta_baza==nomer_projekta_vvod:
            await message.answer(text="Вот сведения по данному проекту")
            await message.answer(text=f"{projekt_svedenije}")
    await state.clear()
@dp.message((F.text.lower()=="/vvod_projekta"))
@dp.message((F.text.lower()=="ввод проекта"))
async def sostavjenie_projekta(message: types.Message, state: FSMContext):
    await message.answer(text="Напиши название проекта")
    await state.set_state(Sostavlenije_Projekta.nazvanije)
@dp.message(Sostavlenije_Projekta.nazvanije, F.text)
async def kriteriy_zaver(message: types.Message,state: FSMContext):
    await state.update_data(nazvanije_projekta=message.text)
    await message.answer(text="Укажи критерий завершенности")
    await state.set_state(Sostavlenije_Projekta.kriterij_zaver)
@dp.message(Sostavlenije_Projekta.kriterij_zaver, F.text)
async def etap_1(message: types.Message, state: FSMContext):
    await state.update_data(kriteriy_zavershennosti=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_1)
    await message.answer(text="Укажи первый этап проекта")
@dp.message(Sostavlenije_Projekta.etap_1, F.text)
async def etap_2(message: types.Message, state: FSMContext):
    await state.update_data(etap_1=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_2)
    await message.answer(text="Укажи второй этап проекта")
@dp.message(Sostavlenije_Projekta.etap_2, F.text)
async def etap_3(message: types.Message, state: FSMContext):
    await state.update_data(etap_2=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_3)
    await message.answer(text="Укажи третий этап проекта")
@dp.message(Sostavlenije_Projekta.etap_3, F.text)
async def etap_4(message: types.Message, state: FSMContext):
    await state.update_data(etap_3=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_4)
    await message.answer(text="Укажи четвертый этап проекта")
@dp.message(Sostavlenije_Projekta.etap_4, F.text)
async def etap_5(message: types.Message, state: FSMContext):
    await state.update_data(etap_4=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_5)
    await message.answer(text="Укажи пятый этап проекта")
@dp.message(Sostavlenije_Projekta.etap_5, F.text)
async def etap_6(message: types.Message, state: FSMContext):
    await state.update_data(etap_5=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_6)
    await message.answer(text="Укажи шестой этап проекта")
@dp.message(Sostavlenije_Projekta.etap_6, F.text)
async def etap_7(message: types.Message, state: FSMContext):
    await state.update_data(etap_6=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_7)
    await message.answer(text="Укажи седьмой этап проекта")
@dp.message(Sostavlenije_Projekta.etap_7, F.text)
async def etap_8(message: types.Message, state: FSMContext):
    await state.update_data(etap_7=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_8)
    await message.answer(text="Укажи восьмой этап проекта")
@dp.message(Sostavlenije_Projekta.etap_8, F.text)
async def etap_9(message: types.Message, state: FSMContext):
    await state.update_data(etap_8=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_9)
    await message.answer(text="Укажи девятый этап проекта")
@dp.message(Sostavlenije_Projekta.etap_9, F.text)
async def etap_10(message: types.Message, state: FSMContext):
    await state.update_data(etap_9=message.text)
    await state.set_state(Sostavlenije_Projekta.etap_10)
    await message.answer(text="Укажи последний этап проекта")
@dp.message(Sostavlenije_Projekta.etap_10, F.text)
async def final(message: types.Message, state: FSMContext):
    await state.update_data(etap_10=message.text)
    global projekt
    global zapis
    data=await state.get_data()
    projekt_nazv = data.get("nazvanije_projekta", None)
    projekt.append(projekt_nazv)
    await message.answer(text=f"{projekt_nazv}")
    kriteriy_zav = data.get("kriteriy_zavershennosti", None)
    projekt.append(kriteriy_zav)
    await message.answer(text=f"{kriteriy_zav}")
    etap1 = data.get("etap_1", None)
    await message.answer(text=f"{etap1}")
    projekt.append(etap1)
    etap2 = data.get("etap_2", None)
    await message.answer(text=f"{etap2}")
    projekt.append(etap2)
    etap3 = data.get("etap_3", None)
    await message.answer(text=f"{etap3}")
    projekt.append(etap3)
    etap4 = data.get("etap_4", None)
    await message.answer(text=f"{etap4}")
    projekt.append(etap4)
    etap5 = data.get("etap_5", None)
    await message.answer(text=f"{etap5}")
    projekt.append(etap5)
    etap6 = data.get("etap_6", None)
    await message.answer(text=f"{etap6}")
    projekt.append(etap6)
    etap7 = data.get("etap_7", None)
    await message.answer(text=f"{etap7}")
    projekt.append(etap7)
    etap8 = data.get("etap_8", None)
    await message.answer(text=f"{etap8}")
    projekt.append(etap8)
    etap9 = data.get("etap_9", None)
    await message.answer(text=f"{etap9}")
    projekt.append(etap9)
    etap10 = data.get("etap_10", None)
    await message.answer(text=f"{etap1}")
    projekt.append(etap10)
    await state.clear()
    await message.answer(text="Проект записан", reply_markup=klava_projekt)
    zapis=1
@dp.message((F.text.lower()=="/proverka_projekta"))
@dp.message((F.text.lower()=="проверка проекта"))
async def proverka_buf(message: types.Message):
    global projekt
    global validacija_projekta
    if len(projekt) == 0:
        await message.answer(text="Нет данных для показа")
    else:
        for i in range(len(projekt)):
            soobshenie=projekt[i]
            await message.answer(text = f"{soobshenie}")
        await message.answer(text="Вот сведения по записанному проекту, Госпожа",reply_markup=klava_glav)
        validacija_projekta=1
@dp.message((F.text.lower()=="/registracija_projekta"))
@dp.message((F.text.lower()=="регистрация проекта"))
async def registracija_projekta(message: types.Message):
    await message.answer(text="Проверка условий записи")
    global zapis
    global projekt
    global projekt_long
    global id_projekta
    global validacija_projekta
    if zapis == 0:
        await message.answer(text="Данные в буфере по проекту отстутствуют, заполните буфер")
    if validacija_projekta == 0:
        await message.answer(text="Данные в буфере не прошли проверку, проверьте данные")
    if validacija_projekta == 1 and zapis == 1:
        projekt_long.append(id_projekta)
        for i in range(1,27):
            soobshenie=0
            projekt_long.append(soobshenie)
        for i in range(12):
            if i<2:
                projekt_long[i+1]=projekt[i]
            else:
                projekt_long[2*i]=projekt[i]
        tochnoje_vremja= str(datetime.now())
        projekt_long[24] = tochnoje_vremja[:-10]
        projekt_long[25] = tochnoje_vremja[:-10]
        projekt_long[26] = int(time.time())
        projekt_kartez = tuple(projekt_long)
        print(projekt_kartez)
        # импорт библиотеки для pq админ
        import psycopg2 as ps
        # создание подключения
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        query = '''INSERT INTO Проект (id, Название_проекта, Критерий_завершенности, Завершённость_проекта, Этап_1, Завершенность_Этап_1, Этап_2, Завершенность_Этап_2, Этап_3,
        Завершенность_Этап_3, Этап_4, Завершенность_Этап_4, Этап_5, Завершенность_Этап_5, Этап_6, Завершенность_Этап_6, Этап_7, Завершенность_Этап_7, Этап_8, Завершенность_Этап_8,
        Этап_9, Завершенность_Этап_9, Этап_10, Завершенность_Этап_10, Дата_регистрации, Дата_изменения, Синхронизация) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # подать запрос системе управления БД
        cursor.execute(query, projekt_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        print(Back.GREEN + Fore.BLACK + Style.BRIGHT + 'Вставка выполнена, моя Госпожа!')
        await message.answer(text="Регистрация проекта в БД выполнена",reply_markup=klava_glav)
        projekt.clear()
        projekt_long.clear()
        zapis = 0
        validacija_projekta = 0
        id_projekta = id_projekta + 1
@dp.message((F.text.lower()=="закрыть этап проекта"))
@dp.message((F.text.lower()=="zakr_etap_projekt"))
async def zakr_etap_projekta(message: types.Message,state: FSMContext):
    await message.answer(text="Сопоставь артикул проекта с его названием по первой букве",reply_markup=klava_alfavit_projektov)
    await state.set_state(VypEtap_Projekta.bukva_projekta)
@dp.message(VypEtap_Projekta.bukva_projekta, F.text.lower())
async def bukva_projekta(message: types.Message,state: FSMContext):
    await state.update_data(bukva=message.text)
    global projekti_artikul
    global naydennost
    text=message.text
    bukva_zapros=text.lower()
    for i in range(len(projekti_artikul)):
        katalog_projekta = projekti_artikul[i]
        nazv_projekta=katalog_projekta[1]
        bukva_projekta=nazv_projekta[0]
        if bukva_zapros == bukva_projekta.lower():
            await message.answer(text=f"{katalog_projekta}")
            naydennost=1
    if naydennost==1:
        await message.answer(text="Введи номер проекта, который хотите завершить",reply_markup=ReplyKeyboardRemove())
        await state.set_state(VypEtap_Projekta.artikul_projekta)
    else:
        await message.answer(text="На данную букву в базе проекты отсутсвуют",reply_markup=klava_projekt)
        await state.clear()
@dp.message(VypEtap_Projekta.artikul_projekta, F.text.lower())
async def poluch_artik_projekta(message: types.Message,state: FSMContext):
    text=message.text
    while True:
        try:
            artikul=int(text)
            await state.update_data(artikul=artikul)
            await message.answer(text="Введи этап проекта, который хотите завершить",
                                 reply_markup=klava_nomera_etapov)
            await state.set_state(VypEtap_Projekta.nomer_etapa)
            break
        except ValueError:
            await message.answer(text="Введи номер проекта, который хотите завершить, дятел")
            await state.set_state(VypEtap_Projekta.artikul_projekta)
            return
@dp.message(VypEtap_Projekta.nomer_etapa, F.text.lower())
async def proverka_i_registracija_etapa(message: types.Message,state: FSMContext):
    global projekti_artikul
    global proverka_1
    global proverka_2
    await message.answer(text="Проверка и регистрация этапа",reply_markup=ReplyKeyboardRemove())
    while True:
        try:
            await state.update_data(etap=message.text)
            data = await state.get_data()
            etap_vvod = data.get("etap", None)
            if etap_vvod=="проект завершен" or etap_vvod=="/projekt_zavershon":
                etap_poisk=100
                break
            else:
                etap_poisk=int(etap_vvod)
                break
        except ValueError:
            await message.answer(text="Введи этап проекта, который хотите завершить корректно, дятел",reply_markup=klava_nomera_etapov)
            await state.clear()
            return
    artikul_poisk= int(data.get("artikul", None))
    bukva_projekta_vvod =(data.get("bukva", None)).lower()
    for i in range(len(projekti_artikul)):
        artikul_svoistva=projekti_artikul[i]
        artikul_baza=artikul_svoistva[0]
        print(artikul_baza)
        print(artikul_poisk)
        if artikul_poisk == int(artikul_baza):
            await message.answer(text="Такой id есть в базе сверяю артикул по букве")
            nazvanije_projekta=artikul_svoistva[1]
            bukva_projekta_basa=(nazvanije_projekta[0]).lower()
            prodvizenije_fakt=artikul_svoistva[2]
            pokazatel_uspecha =artikul_svoistva[3]
            proverka_1=1
            await message.answer(text=f"{bukva_projekta_basa}")
            await message.answer(text=f"{bukva_projekta_vvod}")
            break
    if proverka_1==0:
        await message.answer(text="Такой id нет в базе")
        await state.clear()
        return
    if proverka_1 == 1:
        if bukva_projekta_basa == bukva_projekta_vvod:
            await message.answer(text="Буква в названии проекта совпадает с заявленной, проверяю соостветствие этапов")
            proverka_2 = 1
        else:
            await message.answer(text="Буква в названии не соотсветствует введенной")
            await state.clear()
            return
    if proverka_2 == 1 and proverka_1 == 1:
        if etap_poisk == 100:
            if prodvizenije_fakt[9] == 1 and pokazatel_uspecha == prodvizenije[10]:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершённость_проекта=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, проект завершён", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
            else:
                await message.answer(text="Проект и так уже был завершён, выполните архивацию проекта")
        elif pokazatel_uspecha == prodvizenije[(etap_poisk)-1] and etap_poisk == 1:
            await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            # создание интерфейса для sql запроса
            cursor = connection.cursor()
            edit = '''UPDATE Проект SET Завершенность_Этап_1=1 WHERE id=%s'''
            cursor.execute(edit,(artikul_poisk,))
            # синхронизация изменений, комит версии
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            await message.answer(text="Поздравляю, этап закрыт",reply_markup=klava_glav)
            proverka_1 = 0
            proverka_2 = 0
            await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk)-1] and etap_poisk == 2:
            if prodvizenije_fakt[(etap_poisk)-1-1]==1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_2=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 3:
            if prodvizenije_fakt[(etap_poisk)-1-1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_3=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт",reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 4:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_4=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 5:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_5=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 6:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_6=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 7:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_7=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 8:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_8=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 9:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_9=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
        elif pokazatel_uspecha == prodvizenije[(etap_poisk) - 1] and etap_poisk == 10:
            if prodvizenije_fakt[(etap_poisk) - 1 - 1] == 1:
                await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
                import psycopg2 as ps
                connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
                # создание интерфейса для sql запроса
                cursor = connection.cursor()
                edit = '''UPDATE Проект SET Завершенность_Этап_10=1 WHERE id=%s'''
                cursor.execute(edit, (artikul_poisk,))
                # синхронизация изменений, комит версии
                connection.commit()
                # закрытие соединенмя с ДБ для безопасности
                cursor.close()
                connection.close()
                await message.answer(text="Поздравляю, этап закрыт", reply_markup=klava_glav)
                proverka_1 = 0
                proverka_2 = 0
                await state.clear()
            else:
                await message.answer(text="bebebe")
        else:
            await message.answer(text="Этот этап уже и так закрыт")
@dp.message((F.text.lower()=="готовый проект в архив"))
async def projekt_arhiv_1(message: types.Message, state: FSMContext):
    await message.answer(text="Начинаем архивацию проекта")
    await message.answer(text="Выбери букву, на которую начинается название проекта",reply_markup=klava_alfavit_projektov)
    await state.set_state(Projekt_V_Arhiv.bukva_arhiv_projekta)
@dp.message(Projekt_V_Arhiv.bukva_arhiv_projekta, F.text.lower())
async def projekt_arhiv_2(message: types.Message,state: FSMContext):
    await state.update_data(bukva=message.text)
    global projekti_artikul
    text=message.text
    bukva_zapros=text.lower()
    for i in range(len(projekti_artikul)):
        katalog_projekta = projekti_artikul[i]
        nazv_projekta=katalog_projekta[1]
        bukva_projekta=nazv_projekta[0]
        if bukva_zapros == bukva_projekta.lower():
            await message.answer(text=f"{katalog_projekta}")
    await message.answer(text="Введи номер проекта, который хотите завершить",reply_markup=ReplyKeyboardRemove())
    await state.set_state(Projekt_V_Arhiv.artikul_arhiv_projekta)
@dp.message(Projekt_V_Arhiv.artikul_arhiv_projekta, F.text.lower())
async def projekt_arhiv_3(message: types.Message,state: FSMContext):
    global proverka_3
    global proverka_4
    global proverka_5
    await state.update_data(artikul=message.text)
    try:
        data = await state.get_data()
        artikul_vvod = data.get("artikul", None)
        artikul_poisk = int(artikul_vvod)
    except ValueError:
        await message.answer(text="Ошибка ввода. Введи артикул проекта заново")
        await state.set_state(Projekt_V_Arhiv.artikul_arhiv_projekta)
        return
    pozicija=0
    for i in range(len(etapy_projektov_svodka)):
        # выбор строчки конкретного проекта
        projekty_vybor = etapy_projektov_svodka[i]
        # выбор id конкретного проекта
        artikul_fakt = projekty_vybor[0]
        nazvanije_fakt = projekty_vybor[1]
        bukva_fakt = nazvanije_fakt[0]
        if artikul_poisk == artikul_fakt:
            projekt_v_arhiv=[]
            for j in range(len(projekty_vybor)):
                projekt_v_arhiv.append(projekty_vybor[j])
            tochnoje_vremja = str(datetime.now())
            projekt_v_arhiv.append(tochnoje_vremja[:-10])
            projekt_v_arhiv.append(int(time.time()))
            proverka_3=1
            pozicija=i
            await message.answer(text="Такой id есть в базе данных, сверяю артикул по букве")
            break
    if proverka_3==0:
        await message.answer(text="Проекта под данным id не обнаружено")
        await state.clear()
        return
    bukva_vvod=data.get("bukva", None)
    if bukva_vvod == bukva_fakt:
        await message.answer(text="Начальная буква проекта и id проекта совпадают, проивожу проверку завершенности проекта")
        proverka_4 = 1
    else:
        await message.answer(text="Начальная буква проекта и id проекта не совпадают")
        await state.clear()
        return
    vybor_projekta=projekti_artikul[int(pozicija)]
    zaverhennost=vybor_projekta[4]
    if zaverhennost == 1:
        await message.answer(text="Проверка успешности завершена, проивожу архивацию проекта")
        proverka_5 = 1
    else:
        await message.answer(text="Проект не доделан, пожалуйста, завершите все его этапы")
        await state.clear()
    if proverka_5 == 1 and proverka_4 == 1 and proverka_3 == 1:
        projekt_v_arhiv[0]=nov_id_projekt_arhiv
        projekt_eksempljar = Проект_Архив(id=projekt_v_arhiv[0], Название_проекта=projekt_v_arhiv[1], Критерий_завершенности=projekt_v_arhiv[2],
        Этап_1=projekt_v_arhiv[3], Этап_2=projekt_v_arhiv[4], Этап_3=projekt_v_arhiv[5], Этап_4=projekt_v_arhiv[6], Этап_5=projekt_v_arhiv[7],
        Этап_6=projekt_v_arhiv[8], Этап_7=projekt_v_arhiv[9], Этап_8=projekt_v_arhiv[10], Этап_9=projekt_v_arhiv[11], Этап_10=projekt_v_arhiv[12],
        Дата_внесения=projekt_v_arhiv[13], Синхронизация=projekt_v_arhiv[14])
        session = session_factory()
        session.add(projekt_eksempljar)
        await session.commit()
        await message.answer(text="запись в архив внесена")
        await session.close()
        import psycopg2 as ps
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        zapros = "DELETE FROM Проект WHERE id= %s;"
        # отправить запрос системе управления
        cursor.execute(zapros, (int(artikul_fakt),))
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        await message.answer(text="Готовый проект убран с рабочего стола")
    #global projekti_artikul
    #text=message.text
    #bukva_zapros=text.lower()
    #for i in range(len(projekti_artikul)):
    #katalog_projekta = projekti_artikul[i]
    #nazv_projekta=katalog_projekta[1]
    #bukva_projekta=nazv_projekta[0]
    #if bukva_zapros == bukva_projekta.lower():
    #await message.answer(text=f"{katalog_projekta}")
    #await message.answer(text="Введи номер проекта, который хотите завершить",reply_markup=ReplyKeyboardRemove())
    #await state.set_state(Projekt_V_Arhiv.artikul_arhiv_projekta)
########################################################################################################################
klava_zametok = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ввод заметки"), KeyboardButton(text="проверка заметки")],
    [KeyboardButton(text="регистрация заметки"), KeyboardButton(text="сброс введённой заметки")],
    [KeyboardButton(text="поиск заметки по теме"), KeyboardButton(text="получить мысли по теме")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True, input_field_placeholder="Как хотите поработать с заметками?")
@dp.message((F.text.lower()=="/zametka"))
@dp.message((F.text.lower()=="заметка"))
async def zametka_glav(message: types.Message):
    await message.answer(text="Начинаем работать с заметками",reply_markup=klava_zametok)
@dp.message((F.text.lower()=="/vvod_zametki"))
@dp.message((F.text.lower()=="ввод заметки"))
async def sostavjenie_zametki(message: types.Message, state: FSMContext):
    await message.answer(text="Напиши текст заметки")
    await state.set_state(Sostavlenije_Zamekti.tekst_zametki)
    print("Напиши текст заметки")
@dp.message(Sostavlenije_Zamekti.tekst_zametki, F.text)
async def tekst_zametki(message: types.Message,state: FSMContext):
    await state.update_data(tekst_zametki=message.text)
    await message.answer(text="Укажи первую тему заметки")
    await state.set_state(Sostavlenije_Zamekti.tema1_zametki)
@dp.message(Sostavlenije_Zamekti.tema1_zametki, F.text)
async def tema1_zametki(message: types.Message, state: FSMContext):
    await state.update_data(tema1_zametki=message.text)
    await message.answer(text="Укажи вторую тему заметки")
    await state.set_state(Sostavlenije_Zamekti.tema2_zametki)
@dp.message(Sostavlenije_Zamekti.tema2_zametki, F.text)
async def tema2_zametki(message: types.Message, state: FSMContext):
    await state.update_data(tema2_zametki=message.text)
    await message.answer(text="Укажи третью тему заметки")
    await state.set_state(Sostavlenije_Zamekti.tema3_zametki)
@dp.message(Sostavlenije_Zamekti.tema3_zametki, F.text)
async def tema3_zametki(message: types.Message, state: FSMContext):
    await state.update_data(tema3_zametki=message.text)
    await message.answer(text="Укажи четвёртую тему заметки")
    await state.set_state(Sostavlenije_Zamekti.tema4_zametki)
@dp.message(Sostavlenije_Zamekti.tema4_zametki, F.text)
async def tema4_zametki(message: types.Message, state: FSMContext):
    await state.update_data(tema4_zametki=message.text)
    await message.answer(text="Укажи пятую тему заметки")
    await state.set_state(Sostavlenije_Zamekti.tema5_zametki)
@dp.message(Sostavlenije_Zamekti.tema5_zametki, F.text)
async def tema3_zametki(message: types.Message, state: FSMContext):
    await state.update_data(tema5_zametki=message.text)
    global zametka
    global zapis_zametk
    data=await state.get_data()
    zametka_tekst= data.get("tekst_zametki", None)
    zametka.append(zametka_tekst)
    tema1_zametki= data.get("tema1_zametki", None)
    zametka.append(tema1_zametki)
    tema2_zametki = data.get("tema2_zametki", None)
    zametka.append(tema2_zametki)
    tema3_zametki = data.get("tema3_zametki", None)
    zametka.append(tema3_zametki)
    tema4_zametki = data.get("tema4_zametki", None)
    zametka.append(tema4_zametki)
    tema5_zametki = data.get("tema5_zametki", None)
    zametka.append(tema5_zametki)
    await state.clear()
    await message.answer(text=" Заметка записана",reply_markup=klava_zametok)
    zapis_zametk = 1
@dp.message((F.text.lower()=="/proverka_zametki"))
@dp.message((F.text.lower()=="проверка заметки"))
async def proverka_zametki(message: types.Message):
    global zametka
    global validacija_zametki
    if len(zametka) == 0:
        await message.answer(text="Нет данных для показа")
    else:
        for i in range(len(zametka)):
            soobshenie=zametka[i]
            await message.answer(text = f"{soobshenie}")
        await message.answer(text="Вот сведения по составленной заметке, Госпожа")
        validacija_zametki=1
@dp.message((F.text.lower()=="/registracija_zametki"))
@dp.message((F.text.lower()=="регистрация заметки"))
async def registracija_projekta(message: types.Message):
    await message.answer(text="Проверка условий записи заметки")
    global zapis_zametk
    global validacija_zametki
    if validacija_zametki == 1 and zapis_zametk== 1:
        global zametka
        global zametka_long
        global id_zametki
        zametka_long.append(id_zametki)
        for i in range(8):
            soobshenie=0
            zametka_long.append(soobshenie)
        for i in range(6):
            zametka_long[i+1]=zametka[i]
        tochnoje_vremja= str(datetime.now())
        zametka_long[7] = tochnoje_vremja[:-10]
        zametka_long[8] = int(time.time())
        zametka_kartez = tuple(zametka_long)
        # импорт библиотеки для pq админ
        import psycopg2 as ps
        # создание подключения
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        query = '''INSERT INTO Заметки (id, Текст_заметки, Тема_1,  Тема_2, Тема_3, 
        Тема_4, Тема_5, Дата_регистрации, Отметка_Времени) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # подать запрос системе управления БД
        cursor.execute(query, zametka_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        await message.answer(text="Регистрация заметки в БД выполнена")
        zapis_zametk = 0
        zametka.clear()
        zametka_long.clear()
        id_zametki = id_zametki + 1
        validacija_zametki = 0
        return
    elif zapis_zametk == 0:
        await message.answer(text="Данные по заметке отстутствуют, сделайте ввод данных")
    elif validacija_zametki == 0:
        await message.answer(text="Данные в буфере не прошли проверку, проверьте данные")
@dp.message((F.text.lower()=="/sbros"))
@dp.message((F.text.lower()=="сброс ввода заметки"))
@dp.message((F.text.lower()=="/sbros_vvoda_zametki"))
async def sbros_vvoda_zametki(message: types.Message, state: FSMContext):
    await message.answer(text="Сброс введенной заметки",reply_markup=klava_zametok)
    global zapis_zametk
    global validacija_zametki
    global vvod_zametki
    zametka.clear()
    zametka_long.clear()
    validacija_zametki = 0
    vvod_zametki = 0
    await state.clear()
@dp.message((F.text.lower()=="/poisk_zametki_po_temam"))
@dp.message((F.text.lower()=="поиск заметки по теме"))
async def poisk_zametki(message: types.Message, state: FSMContext):
    await message.answer(text="Поиск заметки по теме")
    await state.set_state(Poisk_ZametKi.tema_zametki)
    await message.answer(text="Укажи темы заметки")
@dp.message(Poisk_ZametKi.tema_zametki, F.text)
async def tema_zametki(message: types.Message, state: FSMContext):
    global validacija_zametki
    global vvod_zametki
    await state.update_data(tema_zametki=message.text)
    data=await state.get_data()
    await state.clear()
    zapros=str(data.get("tema_zametki"))
    print(zapros)
    import psycopg2 as ps
    connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
    # создание интерфейса для sql запроса
    cursor = connection.cursor()
    query = "SELECT * FROM Заметки WHERE Тема_1 = %s OR Тема_2 = %s OR Тема_3 = %s OR Тема_4 = %s OR Тема_5 = %s ORDER BY ID DESC;"
    cursor.execute(query, (zapros,zapros,zapros,zapros,zapros))
    while True:
        next_row = cursor.fetchone()
        if next_row:
            print(f"{next_row}")
            await message.answer(text = f"{next_row}")
        else:
            break
    # синхронизация изменений, комит версии
    connection.commit()
    # закрытие соединенмя с ДБ для безопасности
    cursor.close()
    connection.close()
@dp.message((F.text.lower()=="/mysli_po_temam"))
@dp.message((F.text.lower()=="получить мысли по теме"))
async def sbornik_zametok_po_temam(message: types.Message, state: FSMContext):
    await message.answer(text="Сборник заметок по темам")
    await state.set_state(Sbornik_ZametKi.tema_sbornika)
    await message.answer(text="Напиши тему, по которой хочешь получить сборник")
@dp.message(Sbornik_ZametKi.tema_sbornika, F.text)
async def polycajem_temu_sbornika(message: types.Message, state: FSMContext):
    await state.update_data(tema_sbornika=message.text)
    data = await state.get_data()
    await state.clear()
    mysli = str(data.get("tema_sbornika"))
    print(mysli)
    await message.answer(text="Собираю заметки по данному запросу")
    sbornik=[]
    import psycopg2 as ps
    connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
    # создание интерфейса для sql запроса
    cursor = connection.cursor()
    query = "SELECT * FROM Заметки WHERE Тема_1 = %s OR Тема_2 = %s OR Тема_3 = %s OR Тема_4 = %s OR Тема_5 = %s ORDER BY ID DESC;"
    cursor.execute(query, (mysli,mysli,mysli,mysli,mysli))
    while True:
        next_row = cursor.fetchone()
        if next_row:
            sbornik.append(next_row[1])
            await message.answer(text=f"{next_row[1]}")
        else:
            break
    # синхронизация изменений, комит версии
    connection.commit()
    # закрытие соединенмя с ДБ для безопасности
    cursor.close()
    connection.close()
    await message.answer(text=f"{sbornik}")
########################################################################################################################
#разовые дела
klava_delaO=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="создать дело"),KeyboardButton(text="проверка записи о деле")],
    [KeyboardButton(text="зарегистрировать дело"),KeyboardButton(text="отметить, что дело готово")],
    [KeyboardButton(text="найти дело"),KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Выберите, с какой трудовой задачей хотите поработать")
class Odnorazovoje_delo(StatesGroup):
    rabocaja_zadacha=State()
    projekt_odnorazovoje = State()
    pomoshnik_konsultant = State()
    rod_dejatelnosty=State()
    srok_vyponenija=State()
@dp.message((F.text.lower()=="разовое дело"))
@dp.message((F.text.lower()=="/odnorazovoje_delo"))
async def menu_dela(message: types.Message):
    await message.answer(text="разовое дело",reply_markup=klava_delaO)
@dp.message((F.text.lower()=="создать дело"))
@dp.message((F.text.lower()=="/sozdat_delo"))
async def odnorazovoje(message: types.Message, state: FSMContext):
    await message.answer(text="Опиши трудовую задачу")
    await state.set_state(Odnorazovoje_delo.rabocaja_zadacha)
@dp.message(Odnorazovoje_delo.rabocaja_zadacha, F.text)
async def truovaja_zadacha(message: types.Message, state: FSMContext):
    await state.update_data(trudovaja_zadacha=message.text)
    await state.set_state(Odnorazovoje_delo.projekt_odnorazovoje)
    await message.answer(text="Разовое действие или будет проект?")
@dp.message(Odnorazovoje_delo.projekt_odnorazovoje, F.text)
async def razovoje_projekt(message: types.Message, state: FSMContext):
    await state.update_data(razovoje_projekt=message.text)
    await state.set_state(Odnorazovoje_delo.pomoshnik_konsultant)
    await message.answer(text="Назначь помошника-консультанта при дилегированной отвественности")
@dp.message(Odnorazovoje_delo.pomoshnik_konsultant, F.text)
async def pomoshnik_konsultant(message: types.Message, state: FSMContext):
    await state.update_data(pomoshnik_konsultant=message.text)
    await state.set_state(Odnorazovoje_delo.rod_dejatelnosty)
    await message.answer(text="К какому виду деятельности относится данное дело?")
@dp.message(Odnorazovoje_delo.rod_dejatelnosty, F.text)
async def rod_dejatelnosty(message: types.Message, state: FSMContext):
    await state.update_data(rod_dejatelnosti=message.text)
    await state.set_state(Odnorazovoje_delo.srok_vyponenija)
    await message.answer(text="Обозначь срок выполнения")
@dp.message(Odnorazovoje_delo.srok_vyponenija, F.text)
async def srok_vypolnenyja(message: types.Message, state: FSMContext):
    await state.update_data(srok_vypolnenija=message.text)
    data=await state.get_data()
    await state.clear()
    global razovoje_delo
    global zapis_dela
    rabochaja_zadacha = data.get("trudovaja_zadacha", None)
    razovoje_delo.append(rabochaja_zadacha)
    await message.answer(text=f"{rabochaja_zadacha}")
    razovoje_projekt = data.get("razovoje_projekt", None)
    razovoje_delo.append(razovoje_projekt)
    await message.answer(text=f"{razovoje_projekt}")
    pomoshnik_konsultant = data.get("pomoshnik_konsultant", None)
    razovoje_delo.append(pomoshnik_konsultant)
    await message.answer(text=f"{pomoshnik_konsultant}")
    rod_dejatelnosti = data.get("rod_dejatelnosti", None)
    await message.answer(text=f"{rod_dejatelnosti}")
    razovoje_delo.append(rod_dejatelnosti)
    srok_vypolnenyja = data.get("srok_vypolnenija", None)
    await message.answer(text=f"{srok_vypolnenyja}")
    razovoje_delo.append(srok_vypolnenyja)
    zapis_dela = 1
    await message.answer(text=f"{data}")
@dp.message((F.text.lower()=="/proverka_zapisi_dela"))
@dp.message((F.text.lower()=="проверка записи о деле"))
async def proverka_dela(message: types.Message):
    global razovoje_delo
    global validacija_dela
    if len(razovoje_delo) == 0:
        await message.answer(text="Нет данных для показа")
    else:
        for i in range(len(razovoje_delo)):
            soobshenie=razovoje_delo[i]
            if soobshenie=="":
                await message.answer(text ="Данные повреждены")
                break
            else:
                await message.answer(text=f"{soobshenie}")
        await message.answer(text="Информация об деле проверена, данные готовы к записи")
        validacija_dela=1
@dp.message((F.text.lower()=="зарегистрировать дело"))
@dp.message((F.text.lower()=="/registacija_dela"))
async def registjacija_dela(message: types.Message):
    await message.answer(text="Проверка условий записи разового дела в БД")
    global validacija_dela
    global razovoje_delo
    global razovoje_delo_long
    global zapis_dela
    global id_dela
    if validacija_dela==1 and zapis_dela==1:
        razovoje_delo_long.append(id_dela)
        razovoje_delo_long.append(razovoje_delo[0])
        razovoje_delo_long.append(razovoje_delo[1])
        razovoje_delo_long.append(razovoje_delo[2])
        razovoje_delo_long.append(razovoje_delo[3])
        razovoje_delo_long.append(razovoje_delo[4])
        tochnoje_vremja = str(datetime.now())
        vremja_dizain = tochnoje_vremja[:-10]
        otnetka_vremeni = int(time.time())
        razovoje_delo_long.append(vremja_dizain)
        razovoje_delo_long.append(otnetka_vremeni)
        delovoy_kartez=tuple(razovoje_delo_long)
        await message.answer(text=f"{delovoy_kartez}")
        await message.answer(text="Правильность очередности этапов подтверждена выполняю вставку в БД")
        import psycopg2 as ps
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        insert = '''INSERT INTO Дела (id, Трудовая_Задача, Одноразовое_Проект, Помошник, Группа_Задач, Срок_Выполнения, Отметка_времени, Синхронизация)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(insert,delovoy_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        razovoje_delo.clear()
        zapis_dela=0
        validacija_dela=0
        razovoje_delo_long.clear()
        await message.answer(text="Вставка успешно проведена моя Госпожа")
    elif zapis_dela==0:
        await message.answer(text="Нечего вводить в БД")
        return
    elif validacija_dela==0:
        await message.answer(text="Данные не прошли валидацию, проверьте правильность данных записи")
        return
# СКРИПТ УПРАВЛЯЮЩИЙ ПРИВЫЧКАМИ
klava_privycek=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ввести запись о привычке"),KeyboardButton(text="проверить запись привычки")],
    [KeyboardButton(text="зарегистрировать привычку"),KeyboardButton(text="сбросить данные о привычке")],
    [KeyboardButton(text="отметить сделанный ритуал"),KeyboardButton(text="поиск привычки")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Как именно будем взаимодействовать с привычками?")
klava_alfavit_navykov=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="А"),KeyboardButton(text="Б"),KeyboardButton(text="В"),KeyboardButton(text="Г"),KeyboardButton(text="Д"),KeyboardButton(text="Е")],
    [KeyboardButton(text="Ё"),KeyboardButton(text="Ж"),KeyboardButton(text="З"),KeyboardButton(text="И"),KeyboardButton(text="Й"),KeyboardButton(text="К")],
    [KeyboardButton(text="Л"),KeyboardButton(text="М"),KeyboardButton(text="Н"),KeyboardButton(text="О"),KeyboardButton(text="П"),KeyboardButton(text="Р")],
    [KeyboardButton(text="C"),KeyboardButton(text="Т"),KeyboardButton(text="У"),KeyboardButton(text="Ф"),KeyboardButton(text="Х"),KeyboardButton(text="Ч")],
    [KeyboardButton(text="Ш"),KeyboardButton(text="Щ"),KeyboardButton(text="Ы"),KeyboardButton(text="Э"),KeyboardButton(text="Ю"),KeyboardButton(text="Я")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Начальная буква названия")
class Formulirovka_privycki(StatesGroup):
    zelaemyi_navyk=State()
    etap_preodolenija_sebja = State()
    kontroller_ispolnenija=State()
    trigger_privycki=State()
    nagrada_privycki=State()
    trebovanije_isponitelja=State()
    trebovanije_zakazcika=State()
    cislo_ritualov=State()
class Otmetka_Privycki(StatesGroup):
    nazvanije_navyka = State()
    artikul_navyka = State()
@dp.message((F.text.lower()=="/privychka"))
@dp.message((F.text.lower()=="привычка"))
@dp.message((F.text.lower()=="/behaviour"))
async def privycka_menu(message: types.Message):
    await message.answer(text="Начинаем работать с привычками",reply_markup=klava_privycek)
@dp.message((F.text.lower()=="ввести запись о привычке"))
@dp.message((F.text.lower()=="/vvod_privycki"))
@dp.message((F.text.lower()=="/vvod_patterna"))
async def vvod_privycki(message: types.Message, state: FSMContext):
    await message.answer(text="Начинаем запись привычки",reply_markup=ReplyKeyboardRemove())
    await state.set_state(Formulirovka_privycki.zelaemyi_navyk)
    await message.answer(text="Укажи навык, который будешь развивать с помощью привычки")
@dp.message(Formulirovka_privycki.zelaemyi_navyk, F.text)
async def zelamiy_navyk(message: types.Message, state: FSMContext):
    await state.update_data(navyk_ot_privycki=message.text)
    await state.set_state(Formulirovka_privycki.etap_preodolenija_sebja)
    await message.answer(text="Укажи главное препятствие, которое помешало бы началу выполнения привычки")
@dp.message(Formulirovka_privycki.etap_preodolenija_sebja, F.text)
async def etap_preodolenija(message: types.Message, state: FSMContext):
    await state.update_data(etap_preodolenija=message.text)
    await state.set_state(Formulirovka_privycki.kontroller_ispolnenija)
    await message.answer(text="Назови человека, который будет помогать вырабатывать привычку и контролировать выполнение ритуалов")
@dp.message(Formulirovka_privycki.kontroller_ispolnenija, F.text)
async def kontroller_ispolnenija(message: types.Message, state: FSMContext):
    await state.update_data(kontroller_ispolnenija=message.text)
    await state.set_state(Formulirovka_privycki.trigger_privycki)
    await message.answer(text="Укажи триггер, который запускал бы выполнение ритуала привычки")
@dp.message(Formulirovka_privycki.trigger_privycki, F.text)
async def trigger_privycki(message: types.Message, state: FSMContext):
    await state.update_data(trigger_privycki=message.text)
    await state.set_state(Formulirovka_privycki.nagrada_privycki)
    await message.answer(text="Укажи награду за выполнение ритуала привычки")
@dp.message(Formulirovka_privycki.nagrada_privycki, F.text)
async def nagrada_privycki(message: types.Message, state: FSMContext):
    await state.update_data(nagrada_privycki=message.text)
    await state.set_state(Formulirovka_privycki.trebovanije_isponitelja)
    await message.answer(text="Что нужно сделать абстрактному исполнителю для успеха выполнения привычки?")
@dp.message(Formulirovka_privycki.trebovanije_isponitelja, F.text)
async def trebovanije_ispolnitelja(message: types.Message, state: FSMContext):
    await state.update_data(trebovanije_isolnitelja=message.text)
    await state.set_state(Formulirovka_privycki.trebovanije_zakazcika)
    await message.answer(text="Что нужно сделать абстрактному заказчику для успеха выполнения привычки?")
@dp.message(Formulirovka_privycki.trebovanije_zakazcika, F.text)
async def trebovanije_zakazcika(message: types.Message, state: FSMContext):
    await state.update_data(trebovanije_zakazcika=message.text)
    await state.set_state(Formulirovka_privycki.cislo_ritualov)
    await message.answer(text="Укажи желаемое число повторений ритуалов привычки")
@dp.message(Formulirovka_privycki.cislo_ritualov, F.text)
async def cislo_ritualov(message: types.Message, state: FSMContext):
    await state.update_data(cislo_ritualov=message.text)
    global privycka
    global zapis_privycki
    data= await state.get_data()
    privycka_navyk = data.get("navyk_ot_privycki", None)
    privycka.append(privycka_navyk)
    glavnoje_prepjatstvije=data.get("etap_preodolenija", None)
    privycka.append(glavnoje_prepjatstvije)
    kontroller_ispolnenija=data.get("kontroller_ispolnenija", None)
    privycka.append(kontroller_ispolnenija)
    trigger_privycki = data.get("trigger_privycki", None)
    privycka.append(trigger_privycki)
    nagrada_privycki = data.get("nagrada_privycki", None)
    privycka.append(nagrada_privycki)
    trebovanije_zakazcika = data.get("trebovanije_zakazcika", None)
    privycka.append(trebovanije_zakazcika)
    trebovanije_ispolnitelja = data.get("trebovanije_isolnitelja", None)
    privycka.append(trebovanije_ispolnitelja)
    cislo_ritualov = data.get("cislo_ritualov", None)
    privycka.append(cislo_ritualov)
    await state.clear()
    await message.answer(text="Информация о привычке записана",reply_markup=klava_privycek)
    await message.answer(text=f"{privycka}")
    zapis_privycki = 1
@dp.message((F.text.lower()=="проверить запись привычки"))
@dp.message((F.text.lower()=="/proverka_privycki"))
@dp.message((F.text.lower()=="/kontrol_patterna"))
async def proverka_privycki(message: types.Message):
    await message.answer(text="Производим проверку записи привычки",reply_markup=ReplyKeyboardRemove())
    global privycka
    global validacija_privycki
    if len(privycka) == 0:
        await message.answer(text="Нет данных для показа",reply_markup=klava_privycek)
    else:
        for i in range(len(privycka)):
            soobshenie=privycka[i]
            if soobshenie=="":
                await message.answer(text ="Данные повреждены",reply_markup=klava_privycek)
                break
            else:
                await message.answer(text=f"{soobshenie}")
        await message.answer(text="Вот сведения по новой привычки, Госпожа",reply_markup=klava_privycek)
        validacija_privycki=1
@dp.message((F.text.lower()=="зарегистрировать привычку"))
@dp.message((F.text.lower()=="/registracija_privycki"))
@dp.message((F.text.lower()=="/registracija_patterna"))
async def registracija_privycki(message: types.Message):
    await message.answer(text="Регистрация привычки в БД",reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Проверка условий записи привычки в БД")
    global validacija_privycki
    global privycka
    global privycka_long
    global zapis_privycki
    global id_privycki
    if validacija_privycki==1 and zapis_privycki==1:
        privycka_long.append(id_privycki)
        for i in range(len(privycka)):
            privycka_long.append(privycka[i])
        ritualy=0
        privycka_long.append(ritualy)
        tochnoje_vremja = str(datetime.now())
        vremja_dizain = tochnoje_vremja[:-10]
        otnetka_vremeni = int(time.time())
        privycka_long.append(vremja_dizain)
        privycka_long.append(vremja_dizain)
        privycka_long.append(otnetka_vremeni)
        privycka_kartez=tuple(privycka_long)
        await message.answer(text="Выполняется запись в БД")
        import psycopg2 as ps
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        insert = '''INSERT INTO Привычки (id, Требуемый_Навык, Главное_Препятствие, Помогающий_Человек, Триггер_Привычки, 
        Награда_Привычки, Требование_Заказчика, Требование_Исполнителя, Целевое_Число_Повторений, Выполненное_Число_Повторений,
        Дата_Регистрации_Ритуала, Дата_Выполнения_Ритуала, Отметка_Времени) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(insert,privycka_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        privycka.clear()
        zapis_privycki=0
        validacija_privycki=0
        privycka_long.clear()
        await message.answer(text="Вставка успешно проведена моя Госпожа",reply_markup=klava_privycek)
    elif zapis_privycki==0:
        await message.answer(text="Нечего вводить в БД",reply_markup=klava_privycek)
        return
    elif validacija_privycki==0:
        await message.answer(text="Данные не прошли валидацию, проверьте правильность данных записи",reply_markup=klava_privycek)
        return
@dp.message((F.text.lower()=="сбросить данные о привычке"))
@dp.message((F.text.lower()=="/sbros_privycki"))
@dp.message((F.text.lower()=="/clear_pattern"))
async def sbros_privycki(message: types.Message):
    await message.answer(text="Сброс записи привычки, очистка буфера",reply_markup=ReplyKeyboardRemove())
@dp.message((F.text.lower()=="отметить сделанный ритуал"))
@dp.message((F.text.lower()=="/otmetka_rituala"))
@dp.message((F.text.lower()=="/mark_pattern"))
async def otmetka_rituala(message: types.Message,state: FSMContext):
    await message.answer(text="Отметить сделанный ритуал")
    await message.answer(text="Укажи первую букву тренируемого навыка в привычке",reply_markup=klava_alfavit_navykov)
    await state.set_state(Otmetka_Privycki.nazvanije_navyka)
@dp.message(Otmetka_Privycki.nazvanije_navyka, F.text)
async def bukva_rituala(message: types.Message, state: FSMContext):
    await state.update_data(bukva_navyka=message.text)
    global svodka_privychek
    podhodasije_navyki=[]
    bukva_navyka_grand=message.text
    bukva_navyka_polzovatel=bukva_navyka_grand.lower()
    for i in range(len(svodka_privychek)):
        svedenija_privycka=svodka_privychek[i]
        print(svedenija_privycka)
        formolirovka_navyka=svedenija_privycka[1]
        print(formolirovka_navyka)
        bukva_navyka_bazaGR = formolirovka_navyka[0]
        print(bukva_navyka_bazaGR)
        bukva_navyka_baza=bukva_navyka_bazaGR.lower()
        print(bukva_navyka_baza)
        if bukva_navyka_baza==bukva_navyka_polzovatel:
            nuzni_navyk=[]
            nuzni_navyk.append(svedenija_privycka[0])
            nuzni_navyk.append(svedenija_privycka[1])
            podhodasije_navyki.append(nuzni_navyk)
    if len(podhodasije_navyki)==0:
        await message.answer(text="На данную букву не обнаружено не одной привычки")
        await message.answer(text="Попробуй найти подходящие навыки по начальной букве заново", reply_markup=klava_alfavit_navykov)
        await state.set_state(Otmetka_Privycki.nazvanije_navyka)
        return
    else:
        await message.answer(text="Найдены следующие навыки на данную букву")
        await message.answer(text=f"{podhodasije_navyki}")
        await message.answer(text="Теперь сопоставь начальную букву навыка с артикулом записи привычки", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Otmetka_Privycki.artikul_navyka)
@dp.message(Otmetka_Privycki.artikul_navyka, F.text)
async def artukul_navyka(message: types.Message, state: FSMContext):
    await state.update_data(artikul_navyka=message.text)
    data=await state.get_data()
    print(data)
    await state.clear()
    global svodka_privychek
    proverka_navyka_1=0
    bukva_vvod_GR = data.get("bukva_navyka", None)
    bukva_vvod=bukva_vvod_GR.lower()
    artikul_vvod = int(data.get("artikul_navyka", None))
    for i in range(len(svodka_privychek)):
        svedenija_privycka = svodka_privychek[i]
        artikul_fakt =int(svedenija_privycka[0])
        if artikul_vvod ==artikul_fakt:
            await message.answer(text="Привычка с таким артикулом действительно существует")
            await message.answer(text="Проводим проверку сооствествия введенного порядкового номера привычки и сооствествующего навыка",reply_markup=klava_privycek)
            zadacha_navyka_fakt=svedenija_privycka[1]
            celevoje_kolichestvo=svedenija_privycka[2]
            bukva_fakt_GR=zadacha_navyka_fakt[0]
            bukva_fakt=bukva_fakt_GR.lower()
            proverka_navyka_1=1
            print(bukva_fakt)
            print(bukva_vvod)
            break
        else:
            await message.answer(text="Под введенным порядковым номером не числится ни одна привычка")
            await message.answer(text="Проверьте данные и попробуйте ещё раз",reply_markup=klava_alfavit_navykov)
            await state.set_state(Otmetka_Privycki.nazvanije_navyka)
            return
    if proverka_navyka_1==1:
        if  bukva_fakt==bukva_vvod:
            await message.answer(text="Порядковый номер и название навыка соотвествуют друг другу")
            await message.answer(text="Делаю отметку об выполненном ритуале в базе данных")
            # берем предыдущее количество ритуалов
            import psycopg2 as ps
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            cursor = connection.cursor()
            edit = ''' SELECT * FROM Привычки WHERE id=%s'''
            cursor.execute(edit, (artikul_fakt,))
            row = cursor.fetchone()
            kolicestvo_ritualov = row[9]
            data_obrashenija = row[10]
            await message.answer(text=f"{"Количество повторений привычки до настоящего времени:"}{" "}{kolicestvo_ritualov}")
            await message.answer(text=f"{"Привычка последний раз выполнялась:"}{" "}{data_obrashenija}")
            # синхронизация изменений, комит версии
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            kolicestvo_ritualov = kolicestvo_ritualov + 1
            tochnoje_vremja= str(datetime.now())
            vremja_zapolnenija = tochnoje_vremja[:-10]
            otmetka_vremeni = int(time.time())
            connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
            cursor = connection.cursor()
            edit = ''' UPDATE Привычки SET   Выполненное_Число_Повторений=%s, Дата_выполнения_ритуала=%s, Отметка_Времени=%s WHERE id=%s'''
            cursor.execute(edit, (kolicestvo_ritualov, vremja_zapolnenija, otmetka_vremeni,artikul_fakt))
            # синхронизация изменений, комит версии
            connection.commit()
            # закрытие соединенмя с ДБ для безопасности
            cursor.close()
            connection.close()
            await message.answer(text="Отметка выполения привычки выполнена, моя Госпожа!")
            koefficent_vypolnenija_long=str(kolicestvo_ritualov/celevoje_kolichestvo*100)
            koefficent_vypolnenija =koefficent_vypolnenija_long[:-14]
            await message.answer(text=f"{"От целевого показателя выполнено"}{" "}{koefficent_vypolnenija}{"%"}",reply_markup=klava_privycek          )
        else:
            await message.answer(text="Выявлено несоовествие порядкового номера и названия навыка")
            await message.answer(text="Проверьте данные и попробуйте ещё раз",reply_markup=klava_alfavit_navykov)
            await state.set_state(Otmetka_Privycki.nazvanije_navyka)
            return
@dp.message((F.text.lower()=="поиск привычки"))
@dp.message((F.text.lower()=="/poisk_privyvki"))
@dp.message((F.text.lower()=="/search_pattern"))
async def poisk_privycki(message: types.Message):
    await message.answer(text="Поиск сведений о привычке",reply_markup=ReplyKeyboardRemove())
# СКРИПТ УПРАВЛЯЮЩИЙ КАЛЕНДАРНЫМИ ДЕЛАМИ
klava_kalendarnyh=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="записать дело в календарь"),KeyboardButton(text="проверка календарного дела")],
    [KeyboardButton(text="регистрация календарного дела"),KeyboardButton(text="сброс календарного дела")],
    [KeyboardButton(text="поиск календарного дела"),KeyboardButton(text="удаление календарного дела")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Что хотите сделать с календарными событиями?")
klava_minuty=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="00"),KeyboardButton(text="05"),KeyboardButton(text="10"),KeyboardButton(text="15")],
    [KeyboardButton(text="20"),KeyboardButton(text="25"),KeyboardButton(text="30"),KeyboardButton(text="35")],
    [KeyboardButton(text="40"),KeyboardButton(text="45"),KeyboardButton(text="50"),KeyboardButton(text="55")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Минуты отметки времени начала/завершения события")
klava_chasy=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="00"),KeyboardButton(text="01"),KeyboardButton(text="02"),KeyboardButton(text="03"),KeyboardButton(text="04"),KeyboardButton(text="05")],
    [KeyboardButton(text="06"),KeyboardButton(text="07"),KeyboardButton(text="08"),KeyboardButton(text="09"),KeyboardButton(text="10"),KeyboardButton(text="11")],
    [KeyboardButton(text="12"),KeyboardButton(text="13"),KeyboardButton(text="14"),KeyboardButton(text="15"),KeyboardButton(text="16"),KeyboardButton(text="17")],
    [KeyboardButton(text="18"),KeyboardButton(text="19"),KeyboardButton(text="20"),KeyboardButton(text="21"),KeyboardButton(text="22"),KeyboardButton(text="23")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Часы отметки времени начала/завершения события")
klava_cisla=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="01"),KeyboardButton(text="02"),KeyboardButton(text="03"),KeyboardButton(text="04"),KeyboardButton(text="05"),KeyboardButton(text="06")],
    [KeyboardButton(text="07"),KeyboardButton(text="08"),KeyboardButton(text="09"),KeyboardButton(text="10"),KeyboardButton(text="11"),KeyboardButton(text="12")],
    [KeyboardButton(text="13"),KeyboardButton(text="14"),KeyboardButton(text="15"),KeyboardButton(text="16"),KeyboardButton(text="17"),KeyboardButton(text="18")],
    [KeyboardButton(text="19"),KeyboardButton(text="20"),KeyboardButton(text="21"),KeyboardButton(text="22"),KeyboardButton(text="23"),KeyboardButton(text="24")],
    [KeyboardButton(text="25"),KeyboardButton(text="26"),KeyboardButton(text="27"),KeyboardButton(text="28"),KeyboardButton(text="29"),KeyboardButton(text="30")],
    [KeyboardButton(text="31"),KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Число события")
klava_mesjacy=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Январь"),KeyboardButton(text="Февраль"),KeyboardButton(text="Март")],
    [KeyboardButton(text="Апрель"),KeyboardButton(text="Май"),KeyboardButton(text="Июнь")],
    [KeyboardButton(text="Июль"),KeyboardButton(text="Август"),KeyboardButton(text="Сентябрь")],
    [KeyboardButton(text="Октябрь"),KeyboardButton(text="Ноябрь"),KeyboardButton(text="Декабрь")],
    [KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Месяц события")
@dp.message((F.text.lower()=="календарное событие"))
@dp.message((F.text.lower()=="/timetable action"))
async def kalendarnoje_sobytije(message: types.Message):
    await message.answer(text="календарное событие",reply_markup=klava_kalendarnyh)
class Vvod_kalendarnogo(StatesGroup):
    nazvanije_sobytija = State()
    vid_sobityja = State()
    lokacija_sobityja = State()
    ucastnik_sobityja = State()
    data_sobityjaMnMn= State()
    data_sobitijaDD = State()
    nacalo_sobityjaChCh = State()
    nacalo_sobityjaMinMin = State()
    konec_sobityjaChCh = State()
    konec_sobityjaMinMin = State()
@dp.message((F.text.lower() == "записать дело в календарь"))
@dp.message((F.text.lower()=="/kalender_enter"))
async def vvod_kalendarnogo(message: types.Message, state: FSMContext):
    await message.answer(text="Начинаем ввод календарного события")
    await message.answer(text="Запиши название календарного события")
    await state.set_state(Vvod_kalendarnogo.nazvanije_sobytija)
@dp.message(Vvod_kalendarnogo.nazvanije_sobytija, F.text)
async def nazvanije_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(nazvanije_sobytija=message.text)
    await message.answer(text="Что за вид события состоится?")
    await state.set_state(Vvod_kalendarnogo.vid_sobityja)
@dp.message(Vvod_kalendarnogo.vid_sobityja, F.text)
async def vid_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(vid_sobytija=message.text)
    await message.answer(text="Укажи локацию данного события")
    await state.set_state(Vvod_kalendarnogo.lokacija_sobityja)
@dp.message(Vvod_kalendarnogo.lokacija_sobityja, F.text)
async def locacija_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(lokacija_sobytija=message.text)
    await message.answer(text="Назови участника данного события")
    await state.set_state(Vvod_kalendarnogo.ucastnik_sobityja)
@dp.message(Vvod_kalendarnogo.ucastnik_sobityja, F.text)
async def ucastnik_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(ucastnik_sobytija=message.text)
    await message.answer(text="Укажи месяц, когда состоится событие",reply_markup=klava_mesjacy)
    await state.set_state(Vvod_kalendarnogo.data_sobityjaMnMn)
@dp.message(Vvod_kalendarnogo.data_sobityjaMnMn, F.text)
async def mesjac_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(mecjac_sobytija=message.text)
    await message.answer(text="Укажи день, когда состоится событие",reply_markup=klava_cisla)
    await state.set_state(Vvod_kalendarnogo.data_sobitijaDD)
@dp.message(Vvod_kalendarnogo.data_sobitijaDD, F.text)
async def den_sobytija(message: types.Message, state: FSMContext):
    await state.update_data(den_sobytija=message.text)
    await message.answer(text="Укажи часы отметки времени, когда начнется событие",reply_markup=klava_chasy)
    await state.set_state(Vvod_kalendarnogo.nacalo_sobityjaChCh)
@dp.message(Vvod_kalendarnogo.nacalo_sobityjaChCh, F.text)
async def chasy_nacsobytija(message: types.Message, state: FSMContext):
    await state.update_data(chasy_nacsobytija=message.text)
    await message.answer(text="Укажи минуты отметки времени, когда начнется событие",reply_markup=klava_minuty)
    await state.set_state(Vvod_kalendarnogo.nacalo_sobityjaMinMin)
@dp.message(Vvod_kalendarnogo.nacalo_sobityjaMinMin, F.text)
async def minuty_nacsobytija(message: types.Message, state: FSMContext):
    await state.update_data(minuty_nacsobytija=message.text)
    await message.answer(text="Укажи часы отметки времени, когда закончится событие",reply_markup=klava_chasy)
    await state.set_state(Vvod_kalendarnogo.konec_sobityjaChCh)
@dp.message(Vvod_kalendarnogo.konec_sobityjaChCh, F.text)
async def chasy_okonsobytija(message: types.Message, state: FSMContext):
    await state.update_data(chasy_okonsobytija=message.text)
    await message.answer(text="Укажи минуты отметки времени, когда закончится событие",reply_markup=klava_minuty)
    await state.set_state(Vvod_kalendarnogo.konec_sobityjaMinMin)
@dp.message(Vvod_kalendarnogo.konec_sobityjaMinMin, F.text)
async def minuty_okonsobytija(message: types.Message, state: FSMContext):
    await state.update_data(minuty_okonsobytija=message.text)
    data=await state.get_data()
    await state.clear()
    global kalendarnoje
    global zapis_kalendarnoje
    data_nach_sobytija=[]
    data_okon_sobytija=[]
    vrm_nach_sobytija=[]
    vrm_okon_sobytija=[]
    sobytiynoje1 = []
    sobytiynoje2 = []
    nomer_mesjaca=0
    nazvanije_sobytija = data.get("nazvanije_sobytija", None)
    kalendarnoje.append(nazvanije_sobytija)
    vid_sobytija = data.get("vid_sobytija", None)
    kalendarnoje.append(vid_sobytija)
    locacija_sobytija = data.get("lokacija_sobytija", None)
    kalendarnoje.append(locacija_sobytija)
    ucastnik_sobytija = data.get("ucastnik_sobytija", None)
    kalendarnoje.append(ucastnik_sobytija)
    # работа с датой события
    data_tekush=str(datetime.now())
    god_tekush=data_tekush[:-22]
    data_nach_sobytija.append(god_tekush)
    data_okon_sobytija.append(god_tekush)
    mesjac_sobytija = str(data.get("mecjac_sobytija", None))
    kalendarnoje.append(mesjac_sobytija)
    if mesjac_sobytija == "Январь":
        nomer_mesjaca= 1
    elif mesjac_sobytija == "Февраль":
        nomer_mesjaca = 2
    elif mesjac_sobytija == "Март":
        nomer_mesjaca = 3
    elif mesjac_sobytija == "Апрель":
        nomer_mesjaca = 4
    elif mesjac_sobytija == "Май":
        nomer_mesjaca= 5
    elif mesjac_sobytija == "Июнь":
        nomer_mesjaca = 6
    elif mesjac_sobytija == "Июль":
        nomer_mesjaca = 7
    elif mesjac_sobytija == "Август":
        nomer_mesjaca = 8
    elif mesjac_sobytija == "Сентябрь":
        nomer_mesjaca = 9
    elif mesjac_sobytija == "Октябрь":
        nomer_mesjaca = 10
    elif mesjac_sobytija == "Ноябрь":
        nomer_mesjaca = 11
    elif mesjac_sobytija == "Декабрь":
        nomer_mesjaca = 12
    nomer_mesjacaF= str(nomer_mesjaca)
    data_nach_sobytija.append(nomer_mesjacaF)
    data_okon_sobytija.append(nomer_mesjacaF)
    den_sobytija = str(data.get("den_sobytija", None))
    kalendarnoje.append(den_sobytija)
    data_nach_sobytija.append(den_sobytija)
    data_okon_sobytija.append(den_sobytija)
    chasy_nacsobytija = str(data.get("chasy_nacsobytija", None))
    kalendarnoje.append(chasy_nacsobytija)
    vrm_nach_sobytija.append(chasy_nacsobytija)
    minuty_nacsobytija = str(data.get("minuty_nacsobytija", None))
    kalendarnoje.append(minuty_nacsobytija)
    vrm_nach_sobytija.append(minuty_nacsobytija)
    chasy_okonsobytija = str(data.get("chasy_okonsobytija", None))
    kalendarnoje.append(chasy_okonsobytija)
    vrm_okon_sobytija.append(chasy_okonsobytija)
    minuty_okonsobytija = str(data.get("minuty_okonsobytija", None))
    kalendarnoje.append(minuty_okonsobytija)
    vrm_okon_sobytija.append(minuty_okonsobytija)
    sobytiynoje_nach1="-".join(data_nach_sobytija)
    sobytiynoje_okon1="-".join(data_okon_sobytija)
    sobytiynoje_nach2=":".join(vrm_nach_sobytija)
    sobytiynoje_okon2=":".join(vrm_okon_sobytija)
    sobytiynoje1.append(sobytiynoje_nach1)
    sobytiynoje1.append(sobytiynoje_nach2)
    sobytiynoje2.append(sobytiynoje_okon1)
    sobytiynoje2.append(sobytiynoje_okon2)
    sobytiynoje_nach3=" ".join(sobytiynoje1)
    sobytiynoje_okon3 = " ".join(sobytiynoje2)
    kalendarnoje.append(nomer_mesjacaF)
    kalendarnoje.append(sobytiynoje_nach3)
    kalendarnoje.append(sobytiynoje_okon3)
    kalendarnoje.append(god_tekush)
    await message.answer(text=f"{kalendarnoje}")
    await message.answer(text=f"{sobytiynoje_nach3}")
    await message.answer(text=f"{sobytiynoje_okon3 }")
    zapis_kalendarnoje=1
    await message.answer(text="Данные о календарном событии получены",reply_markup=ReplyKeyboardRemove())
@dp.message((F.text.lower()=="проверка календарного дела"))
@dp.message((F.text.lower()=="/timetable_check"))
async def kalendarnoje_сheck(message: types.Message):
    await message.answer(text="проверка календарного дела")
    global kalendarnoje
    global kontrol_dney
    global validacija_kalendarnoje
    if len(kalendarnoje) == 0:
        await message.answer(text="Нет данных для проверки, введите календарное событие",reply_markup=klava_kalendarnyh)
        return
    else:
        await message.answer(text=f"{kalendarnoje}")
    den_cislo=kalendarnoje[4]
    den_cislo2 = kalendarnoje[5]
    den_cislo3 = kalendarnoje[13]
    await message.answer(text=f"{den_cislo}")
    await message.answer(text=f"{ den_cislo2}")
    await message.answer(text=f"{den_cislo3}")
    if kalendarnoje[4] == "Февраль":
        if calendar.isleap(int(kalendarnoje[13])):
            if int(kalendarnoje[5])>29:
                await message.answer(text="Данное мероприятие на несуществующую дату, превышено количество дней в месяце",reply_markup=klava_kalendarnyh)
            else:
                await message.answer(text="Данное мероприятие на существующую дату, количество дней в месяце соответствует дате",reply_markup=klava_kalendarnyh)
                kontrol_dney=1
        else:
            if int(kalendarnoje[5])>28:
                await message.answer(text="Данное мероприятие на несуществующую дату, превышено количество дней в месяце",reply_markup=klava_kalendarnyh)
            else:
                await message.answer( text="Данное мероприятие на существующую дату, количество дней в месяце соответствует дате",reply_markup=klava_kalendarnyh)
                kontrol_dney=1
    elif kalendarnoje[4] == "Сентябрь" or "Ноябрь" or "Апрель" or "Июнь":
        if int(kalendarnoje[5])>30:
            await message.answer(text="Данное мероприятие на несуществующую дату, превышено количество дней в месяце",reply_markup=klava_kalendarnyh)
        else:
            await message.answer(
                text="Данное мероприятие на существующую дату, количество дней в месяце соответствует дате",reply_markup=klava_kalendarnyh)
            kontrol_dney=1
    elif kalendarnoje[4] == "Январь" or "Март" or "Май" or "Июль" or "Август" or "Октябрь" or "Декабрь":
        if int(kalendarnoje[5])>31:
            await message.answer(text="Данное мероприятие на несуществующую дату, превышено количество дней в месяце",reply_markup=klava_kalendarnyh)
        else:
            await message.answer(
                text="Данное мероприятие на существующую дату, количество дней в месяце соответствует дате",reply_markup=klava_kalendarnyh)
            kontrol_dney=1
    if kontrol_dney == 1:
        for i in range(len(kalendarnoje)):
            if kalendarnoje[i] =="":
                await message.answer(text="Данные повреждены",reply_markup=klava_kalendarnyh)
                break
            else:
                validacija_kalendarnoje = 1
    if kontrol_dney == 1 and validacija_kalendarnoje == 1:
        await message.answer(text="Данные проверены и готовы к записи",reply_markup=klava_kalendarnyh)
@dp.message((F.text.lower()=="регистрация календарного дела"))
@dp.message((F.text.lower()=="/timetable_register"))
async def registacija_kalendarnogo(message: types.Message):
    await message.answer(text="запись календарного дела в БД",reply_markup=ReplyKeyboardRemove())
    global kalendarnoje
    global kalendarnoje_DB
    global validacija_kalendarnoje
    global kontrol_dney
    global zapis_kalendarnoje
    global id_kalendarnogo
    if validacija_kalendarnoje == 1 and zapis_kalendarnoje == 1 and kontrol_dney == 1:
        kalendarnoje_DB.append(id_kalendarnogo)
        for i in range (4):
            kalendarnoje_DB.append(kalendarnoje[i])
        kalendarnoje_DB.append(kalendarnoje[11])
        kalendarnoje_DB.append(kalendarnoje[12])
        otmetka_vremeni=time.time()
        otmetka_vremeniFR=str(otmetka_vremeni)
        otmetka_vremeniFR2=int(otmetka_vremeniFR[:-8])
        kalendarnoje_DB.append(otmetka_vremeniFR2)
        await message.answer(text=f"{kalendarnoje_DB}")
        kalendarny_kartez = tuple(kalendarnoje_DB)
        # импорт библиотеки для pq админ
        import psycopg2 as ps
        # создание подключения
        connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
        # создание интерфейса для sql запроса
        cursor = connection.cursor()
        query = '''INSERT INTO Календарные (id, Название_События, Вид_События, Локация_События, Участник_События, Начало_События, Окончание_События, Отметка_Времени)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
        # подать запрос системе управления БД
        cursor.execute(query, kalendarny_kartez)
        # синхронизация изменений, комит версии
        connection.commit()
        # закрытие соединенмя с ДБ для безопасности
        cursor.close()
        connection.close()
        await message.answer(text="Запись о календарном событии в БД выполнена")
        kalendarnoje_DB=[]
        kalendarnoje=[]
        zapis_kalendarnoje=0
        validacija_kalendarnoje=0
        id_kalendarnogo=id_kalendarnogo+1
    elif zapis_kalendarnoje == 0:
        await message.answer(text="Запись о календарном событии отстуствует, введите такую запись и попробуйте ещё раз")
    elif validacija_kalendarnoje == 0:
        await message.answer(text="Запись о календарном событии не прошла проверку перед вводом в базу данных, проведите проверку календарного события")
@dp.message((F.text.lower()=="/admin"))
@dp.message((F.text.lower()=="админ"))
@dp.message((F.text.lower()=="developer"))
async def poisk1(message: types.Message):
    await message.answer(text="начальник пришёл")
    print("начальник пришёл")
@dp.message((F.text.lower()=="/exit"))
@dp.message((F.text.lower()=="отмена"))
@dp.message((F.text.lower()=="выход"))
@dp.message((F.text.lower()=="сброс"))
@dp.message((F.text.lower()=="Выход"))
async def poisk1(message: types.Message, state: FSMContext):
    await message.answer(text="выход")
    await state.clear()
    print("выход")
@dp.message((F.text.lower()=="/description"))
@dp.message((F.text.lower()=="описание"))
async def poisk1(message: types.Message):
    await message.answer(text="информация о создателе бота")
    print("информация о создателе бота")
@dp.message((F.text.lower()=="/start"))
@dp.message((F.text.lower()=="старт"))
@dp.message((F.text.lower()=="пуск"))
async def start_command(message: types.Message):
    await message.answer(text="Наливай,поехали!!!")
    print("Uiiiiiiiiiiiiiiiiiiiii")
@dp.message((F.text.lower()=="/stop"))
@dp.message((F.text.lower()=="авария"))
async def stop(message: types.Message, state:FSMContext):
        await state.clear()
        await message.answer("Моя остановочка")
        print("Bota ripnuli")
        raise KeyboardInterrupt
klava_start=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/ready"),KeyboardButton(text="/start")],
    [KeyboardButton(text="/stop"),KeyboardButton(text="/description")],
    [KeyboardButton(text="архив сделанных проектов"),KeyboardButton(text="выход")]],
    resize_keyboard=True,input_field_placeholder="Начальная буква названия")
def kostyly_DB():
    # создать таблицу
    print(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(Back.GREEN + Fore.BLACK + Style.BRIGHT + 'Надо создать таблицу')
    # создание подключения
    import psycopg2 as ps
    connection = ps.connect(host=os.getenv("DBHOST"), database=os.getenv("DBNAME"), user=os.getenv("DBUSER"), password=os.getenv("DBPASSWORD"))
    # создание интерфейса для sql запроса
    cursor = connection.cursor()
    # здесь пиши SQL запрос для БД для вставки строк CREATE TABLE название (строки данные ограничения, первичный ключ)
    query = '''CREATE table Календарные (id BIGINT NOT NULL PRIMARY KEY, Название_События VARCHAR(128) NOT NULL, Вид_События VARCHAR(128) NOT NULL, Локация_События VARCHAR(128) NOT NULL, 
           Участник_События VARCHAR(128) NOT NULL, Начало_События VARCHAR(128) NOT NULL, Окончание_События VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL);
    CREATE table Привычки (id BIGINT NOT NULL PRIMARY KEY, Требуемый_Навык VARCHAR(128), Главное_Препятствие VARCHAR(128) NOT NULL,
    Помогающий_Человек VARCHAR(128) NOT NULL, Триггер_Привычки VARCHAR(128) NOT NULL, Награда_Привычки VARCHAR(128) NOT NULL, Требование_Заказчика VARCHAR(128) NOT NULL,
    Требование_Исполнителя VARCHAR(128) NOT NULL, Целевое_Число_Повторений BIGINT NOT NULL, Выполненное_Число_Повторений BIGINT NOT NULL,
    Дата_регистрации_ритуала VARCHAR(128) NOT NULL, Дата_выполнения_ритуала VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL);
    CREATE table Заметки (id BIGINT NOT NULL PRIMARY KEY, Текст_заметки TEXT NOT NULL, Тема_1 VARCHAR(128) NOT NULL,  Тема_2 VARCHAR(128) NOT NULL, Тема_3 VARCHAR(128) NOT NULL,
    Тема_4 VARCHAR(128) NOT NULL, Тема_5 VARCHAR(128) NOT NULL, Дата_регистрации VARCHAR(128) NOT NULL, Отметка_Времени BIGINT NOT NULL);
    CREATE table Дела (id BIGINT NOT NULL PRIMARY KEY, Что_Cделать VARCHAR(128) NOT NULL, Одноразовое_Проект VARCHAR(128) NOT NULL, Помошник VARCHAR(128) NOT NULL, Группа_Задач VARCHAR(128) NOT NULL, Срок_Выполнения VARCHAR(128) NOT NULL,
    Отметка_времени VARCHAR(128) NOT NULL, Синхронизация BIGINT NOT NULL);
    CREATE table Проект (id BIGINT NOT NULL PRIMARY KEY, Название_проекта VARCHAR(128) NOT NULL,
    Критерий_завершенности VARCHAR(128) NOT NULL, Завершённость_пр4екта INT NOT NULL, Этап_1 VARCHAR(128) NOT NULL,
    Завершенность_Этап_1 INT NOT NULL, Этап_2 VARCHAR(128) NOT NULL, Завершенность_Этап_2 INT NOT NULL, Этап_3 VARCHAR(128) NOT NULL,
    авершенность_Этап_3 INT NOT NULL, Этап_4 VARCHAR(128) NOT NULL, Завершенность_Этап_4 INT NOT NULL, Этап_5 VARCHAR(128) NOT NULL,
    Завершенность_Этап_5 INT NOT NULL, Этап_6 VARCHAR(128) NOT NULL, Завершенность_Этап_6 INT NOT NULL, Этап_7 VARCHAR(128) NOT NULL,
    Завершенность_Этап_7 INT NOT NULL, Этап_8 VARCHAR(128) NOT NULL, Завершенность_Этап_8 INT NOT NULL, Этап_9 VARCHAR(128) NOT NULL,
    Завершенность_Этап_9 INT NOT NULL, Этап_10 VARCHAR(128) NOT NULL,Завершенность_Этап_10 INT NOT NULL, Дата_регистрации VARCHAR(128) NOT NULL, Дата_изменения VARCHAR(128) NOT NULL)'''
    # подать запрос системе управления БД
    cursor.execute(query)
    # синхронизация изменений, комит версии
    connection.commit()
    # закрытие соединенмя с ДБ для безопасности
    cursor.close()
    connection.close()
    print(Back.GREEN + Fore.BLACK + Style.BRIGHT + 'Таблица создана, моя Госпожа!!!')
async def create_tably():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
async def main():
#заяц выкл
#async with broker:
#await broker.start()
# CRUD костыль на создание таблиц
    #kostyly_DB()
# ORM на таблицу по ученикам
    scheduler.start()
    await create_tably()
    init(autoreset=True)
    await Bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await Bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(Bot)
async def dni_pamjati():
    response = requests.get("https://azbyka.ru/days/")
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("div", class_="text day__text")
    svjatcy = ""
    for div in data:
        strofa = div.text
        svjatcy  += str(strofa)
    imena = svjatcy [65:-2]
    result = imena.split(")")
    for i in range(len(result)):
        result[i] = result[i] + ")"
    response2 = requests.get("https://www.elering.ee")
    soup2 = BeautifulSoup(response2.text, "html.parser")
    data2 = soup2.find_all("div", class_="live_prices_card__graph--column")
    elektro = []
    for div in data2:
        price = div.text
        elektro.append(price)
    electricity = []
    for i in range(24):
        sokrash = elektro[i]
        netprobelov = sokrash.replace("\n", "")
        sorkash = netprobelov[17:-45]
        electricity.append(sorkash)
    response3 = requests.get("https://www.yr.no/en/forecast/hourly-table/2-588409/Estonia/Harju/Tallinn/Tallinn?i=1")
    soup3 = BeautifulSoup(response3.text, "html.parser")
    data3 = soup3.find_all("div", class_="hourly-weather-table")
    result31 = []
    for div in data3:
        pogoda = div.text
        result31.append(pogoda)
    result32 = pogoda[90:]
    result33 = result32.split("m/s")
    temperature = []
    for j in range(len(result33)):
        if len(result33[j]) == 24:
            vspom31 = result33[j]
            vspom32 = vspom31[:-17]
            result33[j] = vspom32
        if len(result33[j]) == 20:
            vspom33 = result33[j]
            vspom34 = vspom33[:-13]
            result33[j] = vspom34
    for j in range(len(result33) - 49):
        vspom35 = result33[3 * j]
        vspom36 = vspom35[2:-3]
        temperature.append(vspom36)
    await Bot.send_message(chat_id=os.getenv('moi_id'),text='Божией помощи на день! Дни памяти святых:')
    await Bot.send_message(chat_id=os.getenv('moi_id'), text=f"{result}")
    await Bot.send_message(chat_id=os.getenv('moi_id'), text='Цены на электричество EUR/MWH:')
    await Bot.send_message(chat_id=os.getenv('moi_id'), text=f"{electricity}")
    await Bot.send_message(chat_id=os.getenv('moi_id'), text='Температура воздуха в Таллинне по часам:')
    await Bot.send_message(chat_id=os.getenv('moi_id'), text=f"{temperature}")
scheduler = AsyncIOScheduler()
scheduler.add_job(dni_pamjati, 'cron', hour=2, minute=30, timezone='Europe/Kiev')
if __name__ == "__main__":
    asyncio.run(main())
