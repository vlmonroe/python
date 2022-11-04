from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path, Body
from schemas import Book, Author
import json
import socket
import threading
import random as rdm
import sqlite3
import datetime
import random
import string
import eel

# преобразование длинного URl в короткий

eel.init("web")

input_url = 'https://docs-python.ru/standart-library/modul-sqlite3-python/obekt-cursor-modulja-sqlite3/'
short_url = 'https://shu.ru/'
connection = sqlite3.connect('links.db')
cursor = connection.cursor()


# generate url
def gen_url():
    letters = string.ascii_lowercase
    new_url = ''.join(random.choice(letters) for i in range(5))
#    new_url = 'https://myclick.ru/li/' + new_url
#    print('gen_url', new_url)
    return new_url

#find url already exist in base and return paired url
def find_url(new_url, column):
    base = cursor.execute('''SELECT * FROM Links''')
    i = int(column == 'new')
#    print(base)
    for row in base.fetchall():
        if (new_url == row[i]):
            return row[1-i]
    return ''

# check new url already exist
def new_url():
    while(1):
        new_url = gen_url()
        if (find_url(new_url, 'new') == ''):
#            print('new_url', new_url)
            return new_url

# add urls in base
def add_url(iu, su):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Links(Incoming_url TEXT, Short_url TEXT, Date TEXT)''')
    tobase = '''INSERT INTO Links (Incoming_url, Short_url, Date) VALUES (?, ?, ?)'''
    cursor.execute(tobase,(iu, su, str(datetime.datetime.now())))
    connection.commit()
    frombase = '''SELECT Incoming_url FROM links WHERE Short_url=(?)'''
    cursor.execute(frombase,(su,))
    result = cursor.fetchall()

# clear the base of old records
def clear_base():
    base = cursor.execute('''SELECT * FROM Links''')
    clearold = '''DELETE from Links WHERE Date=(?)'''
    for row in base.fetchall():
        create_time = datetime.datetime.strptime(row[2],'%Y-%m-%d %H:%M:%S.%f')
        delta = datetime.datetime.now() - create_time
        if (delta.seconds > 100):
            cursor.execute(clearold,(str(create_time),))
            connection.commit()


add_url(input_url, new_url())
clear_base()
# print(row)


cursor.close()




'''def mywindow():
    layout = [
        [sg.Button('Камень', enable_events=True, key=1),
         sg.Button('ножнецы', enable_events=True, key=2),
         sg.Button('Бумага', enable_events=True, key=3)],
        [sg.Text("", k='out0')]
    ]

    window = sg.Window('Server', layout)
    count = 0

    while True:                             # The Event Loop
        event, values = window.read()       # рисуем читаем
        print(event, values) #debug
        comp_choise = rdm.randint(1, 3)
        if event in (None, 'Exit', 'Cancel'):
            break
        if event:


    window.Element('out0').update(val)
'''