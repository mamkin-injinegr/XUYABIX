
#ТГ бот с исмп запросами и кол-вом фиксаций на скате

from pythonping import ping
from colorama import Fore, Back, Style
import datetime
import time
import os
import telebot
from telebot import types
import emoji	
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import datetime, timedelta

excel_data_df = pd.read_excel('name_ip_CKAT.xlsx')
ip = excel_data_df['Адрес в VPN'].tolist()
name = excel_data_df['Местоположение'].tolist()
CKAT_ip_list = dict(zip(ip,name))

excel_data_df = pd.read_excel('name_ip_AU.xlsx')
ip = excel_data_df['IP'].tolist()
name = excel_data_df['Расположение'].tolist()
AU_ip_list = dict(zip(ip,name))

excel_data_df = pd.read_excel('name_ip_KORDON.xlsx')
modem = excel_data_df['Модем'].tolist()
ip = excel_data_df['IP'].tolist()
name = excel_data_df['Расположение'].tolist()
n_m = (str(tup) for tup in zip(name, modem))
KORDON_ip_list = dict(zip(ip,n_m))

#обращение к таблице
excel_data_df = pd.read_excel('name_ip_CKAT11.xlsx')
ip = excel_data_df['Адрес в VPN'].tolist()
name = excel_data_df['Местоположение'].tolist()
CKAT11_ip_list = dict(zip(ip,name))
#Сегодняшня, вчерашняя дата
tod =datetime.today()
tod_str= tod.strftime("%Y-%m-%d ")
yest = datetime.today() - timedelta(days=1)
yest_str= yest.strftime("%Y-%m-%d ")
#Имитаця браузера-хз что
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}

#пароль логин
data = { "username": "root",
		 "password": "pass"}
#скиаты с другим пост запросом
excluded_list = ['192.168.245.58','192.168.245.59','192.168.245.47']

#Данные ПОСТ запроса для кол-ва фикциий, фиксаций нарушей в двух вариантах
dat={"method":"inf","desc":"true","order":"time","filter":{"time":{"from": yest_str+"00:00:00","to": tod_str +"00:00:00"},"undefined":{"undefined": tod_str +"00:00:00"}}}
dat_violation_1 = {"method":"inf","desc":'true',"order":"time","filter":{"time":{"from": yest_str+"00:00:00","to":tod_str +"00:00:00"},"undefined":{"undefined":tod_str +"00:00:00"},"events.type":{"in":["1.1","3","4","5","6","7"]}}}
dat_violation_nevski_kirova_ilinskiy = {"method":"inf","desc":"true","order":"time","filter":{"time":{"from": yest_str+"00:00:00","to":tod_str +"00:00:00"},"type":{"in":["1.1","3","4","6","7","8","10","15","20","W"]}}}


# Создаем бота
bot = telebot.TeleBot('5006471173:AAFVaE_yXD0HIV4MKXAfzhWlj49YY4hZjIQ')

# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
        
        # Добавляем две кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("СКАТ")
        item2=types.KeyboardButton("АВТОУРАГАН")
        item3=types.KeyboardButton("КОРДОН")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(m.chat.id, 'XUYABIX V1.1(betta)\n----------------------------\nВыбери тип проверки',  reply_markup=markup)



@bot.message_handler(content_types=["text"])
def handle_text(message):
	global ip_list

	if(message.text == "СКАТ"):
		ip_list = CKAT_ip_list
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1=types.KeyboardButton("ICMP запрос всех")
		item2=types.KeyboardButton("ICMP запрос не рабочие")
		item3=types.KeyboardButton("Проверка фиксаций за вчерашний день по 11 контракту")
		back = types.KeyboardButton("Вернуться в главное меню")
		markup.add(item1)
		markup.add(item2)
		markup.add(item3)
		markup.add(back)
		bot.send_message(message.chat.id, text="Выбери режим", reply_markup=markup)
		answer = '...'

	elif(message.text == "АВТОУРАГАН"):
		ip_list = AU_ip_list
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1=types.KeyboardButton("ICMP запрос всех")
		item2=types.KeyboardButton("ICMP запрос не рабочие")
		back = types.KeyboardButton("Вернуться в главное меню")
		markup.add(item1)
		markup.add(item2)
		markup.add(back)
		bot.send_message(message.chat.id, text="Выбери режим", reply_markup=markup)
		answer = '...'

	elif(message.text == "КОРДОН"):
		ip_list = KORDON_ip_list
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1=types.KeyboardButton("ICMP запрос всех")
		item2=types.KeyboardButton("ICMP запрос не рабочие")
		back = types.KeyboardButton("Вернуться в главное меню")
		markup.add(item1)
		markup.add(item2)
		markup.add(back)
		bot.send_message(message.chat.id, text="Выбери режим", reply_markup=markup)
		answer = '...'

	elif (message.text == "ICMP запрос всех") :
		for key,value in ip_list.items():#Обращение к словарю айпишников
			now = datetime.now() #Нынешняя дата
			rt= now.strftime("%d.%m.%Y %H:%M:%S") #форматирование даты
			if ping(key, timeout=0.5).rtt_avg_ms < 500: #сам пинг, и опрделение доступа
				stat = rt + '\n------------------------------\n' + value + '\n------------------------------\n' + '\nOK ' + emoji.emojize(' :check_mark_button:')
				bot.send_message(message.chat.id, stat)
			else:
				stat = rt + '\n------------------------------\n' + value + '\n------------------------------\n' + '\nNO CONECTION ' + emoji.emojize(' :cross_mark:')
				bot.send_message(message.chat.id, stat)
		answer = 'Проверка с выводм всех результатов закончена.'
	# Кнопка 2
	elif (message.text == "ICMP запрос не рабочие"):
		for key,value in ip_list.items():#Обращение к словарю айпишников
			now = datetime.now() #Нынешняя дата
			rt= now.strftime("%d.%m.%Y %H:%M:%S") #форматирование даты
			if ping(key, timeout=0.5).rtt_avg_ms < 500: #сам пинг, и опрделение доступа
				y=1
			else:
				stat = rt + '\n------------------------------\n' + value + '\n------------------------------\n' + '\nNO CONECTION ' + emoji.emojize(' :cross_mark:')
				bot.send_message(message.chat.id, stat)
			answer = 'Проверка с выводм только не рабочих закончена.'
			
	elif (message.text == "Вернуться в главное меню"):
		markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1=types.KeyboardButton("СКАТ")
		item2=types.KeyboardButton("АВТАУРОГАН")
		item3=types.KeyboardButton("КОРДОН")
		markup.add(item1)
		markup.add(item2)
		markup.add(item3)
		bot.send_message(message.chat.id,text='XUYABIX V1.3(betta)\n-----------------------\nВыбери тип проверки', reply_markup=markup )
		answer = 'Вы вернулись в главное меню'

	elif (message.text == "Проверка фиксаций за вчерашний день по 11 контракту"):

		print("2")

		ip_list = CKAT11_ip_list

		for key,value in ip_list.items():#Обращение к словарю айпишников

			now = datetime.now() #Нынешняя дата
			rt= now.strftime("%d.%m.%Y %H:%M:%S")

			if ping(key, timeout=0.5).rtt_avg_ms < 500: #сам пинг, и опрделение доступа
				
				url = "http://"+key+"/?r=login"#url начальной страницы
			
				session = requests.Session()	#создание сессии

				session.headers.update(headers)  #включение имитации браузера

				POST_enter = session.post(url, data=data).text #отправка пароля логина
			
				if key in excluded_list : #определение типа ската

					dat_violation=dat_violation_nevski_kirova_ilinskiy 

				else:
					dat_violation=dat_violation_1

				url2 = "http://"+key+"/?r=targets_list" #url для запроса кол-ва фиксаций

				fix_s = requests.post(url2, data=json.dumps(dat)).text #запрос всех проездов

				violation_s = requests.post(url2, data=json.dumps(dat_violation)).text #запрос всех нарушений

				fix="".join(c for c in fix_s if  c.isdecimal()) #нормальный вид 

				violation="".join(c for c in violation_s if  c.isdecimal()) #нормальный вид 

				stat = rt + '\n------------------------------\n' + value + '\n------------------------------\n' + 'icmp - OK ' + emoji.emojize(' :check_mark_button:'+'\n' + "Колличество фиксаций за вчерашний день:"+fix +'\n' + "Колличество нарушений за вчерашний день:" + violation)

				bot.send_message(message.chat.id, stat)


			else:
				stat = rt + '\n------------------------------\n' + value + '\n------------------------------\n' + 'NO CONECTION ' + emoji.emojize(' :cross_mark:')
				

		ip_list = CKAT_ip_list

		answer ='Проверка фиксаций за вчерашний день по 11 контракту закончена'

	else:
		answer = 'Харош умничать, пользуйся кнопками! Я Для кого их сделал?!'
    # Отсылаем юзеру answer  в его чат
	bot.send_message(message.chat.id, answer)

# Запускаем бота
bot.polling(none_stop=True, interval=0)