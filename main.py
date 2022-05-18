import sqlite3
import time

import telebot
from telebot import TeleBot
from telebot import types

db = sqlite3.connect('server.db', check_same_thread=False)
cr = db.cursor()

bot: TeleBot = telebot.TeleBot('5238036623:AAFIOXKc0HW5LeVGwXgVnAVHtEzc2ALfQj0')

#cr.execute(f"update users set roots = 'Admin' where user_id = '269112132'")

#cr.execute("drop table users")
#db.commit()

#cr.execute("drop table archive_docs")
#db.commit()

cr.execute("create table if not exists users (user_id int primary key, surname text, name text, roots text)")
db.commit()

cr.execute("create table if not exists docs (doc_id int primary key, name_doc text, discription text)")
db.commit()

#cr.execute("insert into docs (doc_id, name_doc) values(1,'Заявление на декрет')")
#db.commit()
#cr.execute("insert into docs (doc_id, name_doc) values(2,'Заявление на отпуск')")
#db.commit()
#cr.execute("insert into docs (doc_id, name_doc) values(3,'Заявление на больничный')")
#db.commit()

cr.execute("create table if not exists statuses (status_id int primary key, name_status text, discription text)")
db.commit()

cr.execute("create table if not exists archive_docs (id int primary key, datetime text, doc_id int, user_id int, status text)")
db.commit()






@bot.message_handler(commands=['start'])
def start(message):
    cr.execute(f"select * from users where user_id = '{message.chat.id}'")
    if cr.fetchone() is None:
        cr.execute("insert into users values(?, ?, ?, ?)", (message.chat.id, message.from_user.last_name, message.from_user.first_name, "User"))
        db.commit()
        k = 1
    else:
        rt_in = cr.execute(f"select roots from users where user_id = '{message.from_user.id}'").fetchone()
        if rt_in[0] == 'Admin':
            k = 3
        else:
            k = 2

    mess_for_new = f"Добро пожаловать, <b>{message.from_user.last_name} {message.from_user.first_name}</b>!\n" \
                   f"Это корпоративный бот компании 'Hopper IT'.Для Вашего удобства приведён список команд: " \
                   f"\n/help-список команд;" \
                   f"\n/status-узнать статус заявления;" \
                   f"\nИнформация о себе."
    mess_for_old = f"С возвращением, <b>{message.from_user.last_name} {message.from_user.first_name}</b>!\n" \
                   f"Напоминаем, что у бота есть следующие команды: " \
                   f"\n/help-список команд;" \
                   f"\n/status-узнать статус заявления."

    #mess_start = f"Привет, <b>{message.from_user.last_name} {message.from_user.first_name}</b>, это корпоративный бот компании Hopper IT.Для вашего удобства приведён список команд: " \
    #             f"\n/help-список команд;" \
    #             f"\n/status-узнать статус заявления\n\n"
    #bot.send_message(message.chat.id, mess_start, parse_mode='html')

    for vl in cr.execute("select * from users"):
        print(vl)
    print("---------------------------------------------------")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if k == 1:
        buttons_for_user(message)
    if k == 2:
        buttons_for_user(message)
    if k == 3:
        buttons_for_adm(message)


    #if (message.text == "👋 Поздороваться"):
    #    bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь статью!)")
    #elif (message.text == "❓ Задать вопрос"):
    #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #    btn1 = types.KeyboardButton("Как меня зовут?")
    #    btn2 = types.KeyboardButton("Что я могу?")
    #    back = types.KeyboardButton("Вернуться в главное меню")
    #    markup.add(btn1, btn2, back)
    #    bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    #elif (message.text == "Как меня зовут?"):
    #    bot.send_message(message.chat.id, "У меня нет имени..")

    #elif message.text == "Что я могу?":
    #    bot.send_message(message.chat.id, text="Поздороваться с читателями")

    #elif (message.text == "Вернуться в главное меню"):
    #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #    button1 = types.KeyboardButton("👋 Поздороваться")
    #    button2 = types.KeyboardButton("❓ Задать вопрос")
    #    markup.add(button1, button2)
    #    bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    #else:
    #    bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

def buttons_for_user(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заяв. на декрет")
    item2 = types.KeyboardButton("Заяв. на отпуск")
    item3 = types.KeyboardButton("Заяв. на больничный")
    item4 = types.KeyboardButton("Информация о себе")
    item5 = types.KeyboardButton("Мои заявления")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Выберите что вам надо, пользователь', reply_markup=markup)




def buttons_for_adm(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Заяв. на декрет")
    item2 = types.KeyboardButton("Заяв. на отпуск")
    item3 = types.KeyboardButton("Заяв. на больничный")
    item4 = types.KeyboardButton("Информация о себе")
    item5 = types.KeyboardButton("Все заявления")
    item6 = types.KeyboardButton("Все пользователи")
    item7 = types.KeyboardButton("Очистить базу заявлений")
    item8 = types.KeyboardButton("Очистить базу пользователей")
    item9 = types.KeyboardButton("Назначить админом")
    item10 = types.KeyboardButton("Назначить пользователем")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
    bot.send_message(message.chat.id, 'Выберите что вам надо, админ', reply_markup=markup)

@bot.message_handler(commands=['commandlist'])
def button(message):
    mess_command = f"Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, это список команд, которые можно использовать:" \
                 f"\nДекрет - получить заявление на декретный отпуск;" \
                 f"\nОтпуск - получить заявление на отпуск;" \
                 f"\nБольничный - получить заявление на больничный"
    bot.send_message(message.chat.id, mess_command, parse_mode='html')

id_doc = 0

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    global id_doc
    mess_text_user = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}, а также известный как {message.from_user.username}</b>'


    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, mess_text_user, parse_mode='html')


    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой id, <b>{message.from_user.id}</b>", parse_mode='html')


    elif (message.text == "Заяв. на декрет"):
        id_doc = 1
        dek = cr.execute(f"select * from archive_docs where doc_id = '{id_doc}' and user_id = '{message.from_user.id}' "
                         f"and status = 'Принято'").fetchall()
        if len(dek) == 0:
            doc = open('Заявление на декрет.doc', 'rb')
            bot.send_document(message.chat.id, doc)
        else:
            bot.send_message(message.chat.id, f"Вы уже подали заявление на декрет. Оно находится на стадии рассмотрения. Дождитесь решения по его утверждению.", parse_mode='html')


    elif (message.text == "Заяв. на отпуск"):
        id_doc = 2
        otp = cr.execute(f"select * from archive_docs where doc_id = '{id_doc}' and user_id = '{message.from_user.id}' "
                         f"and status = 'Принято'").fetchall()
        if len(otp) == 0:
            doc = open('Заявление на отпуск.doc', 'rb')
            bot.send_document(message.chat.id, doc)
        else:
            bot.send_message(message.chat.id, f"Вы уже подали заявление на отпуск. Оно находится на стадии рассмотрения. Дождитесь решения по его утверждению.", parse_mode='html')


    elif (message.text == "Заяв. на больничный"):
        id_doc = 3
        bol = cr.execute(f"select * from archive_docs where doc_id = '{id_doc}' and user_id = '{message.from_user.id}' "
                         f"and status = 'Принято'").fetchall()
        if len(bol) == 0:
            doc = open('Заявление на больничный.doc', 'rb')
            bot.send_document(message.chat.id, doc)
        else:
            bot.send_message(message.chat.id, f"Вы уже подали заявление на больничный. Оно находится на стадии рассмотрения. Дождитесь решения по его утверждению.", parse_mode='html')


    elif (message.text == "Информация о себе"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        info = cr.execute(f"select * from users where user_id = '{message.from_user.id}'").fetchall()
        for i in info:
            bot.send_message(message.chat.id,
                         "Информация о Вас:\nID: "
                         +str(i[0])+"\nФамилия: "
                         +str(i[1])+"\nИмя: "
                         +str(i[2])+"\nУровень доступа: "
                         +str(i[3])+"\n", reply_markup=markup)


    elif (message.text == "Мои заявления"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        st = "Вами поданные заявления:\n\n--Дата время--Тип документа--Статус\n"
        info = cr.execute(f"select a.datetime, d.name_doc, a.status "
                          f"from archive_docs a, docs d "
                          f"where user_id = '{message.from_user.id}'"
                          f"and a.doc_id = d.doc_id").fetchall()
        for i in info:
            st += str(i[0])+"--"+str(i[1])+"--"+str(i[2])+"\n"
        bot.send_message(message.chat.id, st, reply_markup=markup)





    elif message.text.lower() == "изменить статус заявления":
        sz = cr.execute(f"select roots from users where user_id = '{message.from_user.id}'").fetchone()
        if sz[0] == 'Admin':
            stzayav = cr.execute(f'select id, datetime, doc_id, user_id, status from archive_docs').fetchall()
            if len(stzayav) == 0:
                bot.send_message(message.chat.id, "В базе пусто", parse_mode='html')
            else:
                bot.send_message(message.chat.id, f"Выберите нужное заявление (в качестве ответа "
                                                  f"отправьте ID записи):\n\n"
                                                  f"--ID записи--Дата Время--ID документа"
                                                  f"--ID пользователя--Статус заявления--", parse_mode='html')
                for row in stzayav:
                    bot.send_message(message.chat.id, str(row[0]) + "--" + str(row[1]) + "--" + str(row[2])
                                     + str(row[3]) + "--" + str(row[4]), parse_mode='html')
                get_adm_id(message)


        else:
            bot.send_message(message.chat.id, 'Эта функция доступна только админам.', parse_mode='html')


    elif message.text == "Все пользователи":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        rt = cr.execute(f"select roots from users where user_id = '{message.from_user.id}'").fetchone()
        if rt[0] == 'Admin':
            st = "--ID--Surname--Name--Roots\n\n"
            rec = cr.execute(f'select user_id, surname, name, roots from users').fetchall()
            if len(rec) == 0:
                bot.send_message(message.chat.id, "В базе пусто", reply_markup=markup)
            else:
                for row in rec:
                    st += str(row[0])+"--"+str(row[1])+"--"+str(row[2])+"--"+str(row[3])+"\n"
                bot.send_message(message.chat.id, str(st), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Эта функция доступна только админам.', parse_mode='html')


    elif (message.text == "Все заявления"):
        rt = cr.execute(f"select roots from users where user_id = '{message.from_user.id}'").fetchone()
        if rt[0] == 'Admin':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(back)
            st = "--ID записи--Дата Время--ID документа--ID пользователя--Статус заявления--\n\n"
            arch = cr.execute(f'select * from archive_docs').fetchall()
            for row in arch:
                print(str(row[0])+"--"+str(row[1])+"--"+str(row[2])+
                                 "--"+str(row[3])+"--"+str(row[4]))
                st += str(row[0])+"--"+str(row[1])+"--"+str(row[2])+"--"+str(row[3])+"--"+str(row[4])+"\n"
            bot.send_message(message.chat.id,st, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Эта функция доступна только админам.', parse_mode='html')

    elif (message.text == "Очистить базу заявлений"):
        cr.execute('delete from archive_docs where id != 1')


    elif (message.text == "Вернуться в главное меню"):
            back_to_main_menu(message)


    elif (message.text == "Назначить админом"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        rec = cr.execute(f'select user_id, surname, name, roots from users').fetchall()
        if len(rec) == 0:
            bot.send_message(message.chat.id, "В базе пусто", reply_markup=markup)
        else:
            st = "Список пользователей:\n\n--ID--Surname--Name--Roots\n"
            #bot.send_message(message.chat.id, "Список пользователей:\n\n--ID--Surname--Name--Roots")
            for row in rec:
                st += str(row[0]) + "--" + str(row[1]) + "--" + str(row[2]) + "--" + str(row[3])+"\n"
            bot.send_message(message.chat.id, st, reply_markup=markup)
            btns_for_give_adm(message)


    elif (message.text == "Назначить пользователем"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(back)
        rec = cr.execute(f'select user_id, surname, name, roots from users').fetchall()
        if len(rec) == 0:
            bot.send_message(message.chat.id, "В базе пусто", reply_markup=markup)
        else:
            st = "Список пользователей:\n\n--ID--Surname--Name--Roots\n"
            for row in rec:
                st += str(row[0]) + "--" + str(row[1]) + "--" + str(row[2]) + "--" + str(row[3])+"\n"
            bot.send_message(message.chat.id, st, reply_markup=markup)
            btns_for_give_user(message)



    else:
        bot.send_message(message.chat.id, "Неизвестная команда, ознакомьтесь со споском команд.", parse_mode='html')

def back_to_main_menu(message):
    #bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id,
    #                             reply_markup='')
    #bot.delete_message(message.chat.id, message.message_id-1)
    #bot.delete_message(message.chat.id, message.message_id - 2)
    rt = cr.execute(f"select roots from users where user_id = '{message.from_user.id}'").fetchone()
    if rt[0] == 'Admin':
        buttons_for_adm(message)
    else:
        buttons_for_user(message)

def btns_for_give_adm(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    row = cr.execute(f'select user_id from users').fetchall()
    for rw in row:
        btn = types.InlineKeyboardButton(text=f'{str(rw[0])}', callback_data=f'{str(rw[0])+" "+str(1)}')
        kb.add(btn)
    bot.send_message(message.chat.id, 'Выберите нужного пользователя для назначения админом:', reply_markup=kb)

def btns_for_give_user(message):
    kb = types.InlineKeyboardMarkup(row_width=2)
    row = cr.execute(f'select user_id from users').fetchall()
    for rw in row:
        btn = types.InlineKeyboardButton(text=f'{str(rw[0])}', callback_data=f'{str(rw[0])+" "+str(0)}')
        kb.add(btn)
    bot.send_message(message.chat.id, 'Выберите нужного пользователя для назначения пользователем:',reply_markup=kb)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_cb_data(callback):
    print(callback.data[10])
    if callback.data[10] == str(1):
        bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id,
                                      reply_markup='') #удаляет привязанную к сообщению клавиатуру
        upd = cr.execute(f"update users set roots = 'Admin' where user_id = '{callback.data[0:9]}'")
        db.commit()
        bot.send_message(callback.message.chat.id, f'Пользователь с ID {callback.data[0:9]} назначен администратором.')



    elif callback.data[10] == str(0):
        bot.edit_message_reply_markup(callback.message.chat.id, message_id=callback.message.message_id,
                                      reply_markup='') #удаляет привязанную к сообщению клавиатуру
        upd = cr.execute(f"update users set roots = 'User' where user_id = '{callback.data[0:9]}'")
        db.commit()
        bot.send_message(callback.message.chat.id, f'Пользователь с ID {callback.data[0:9]} назначен пользователем.')



def get_adm_id(message):
    cid = cr.execute(f'select min(id), max(id) from archive_docs').fetchall()
    for ccid in cid:
        minid = ccid[0]
        maxid = ccid[1]
    if int(message.text) > maxid or int(message.text) < minid:
        bot.send_message(message.chat.id, "Некорректный ID!", parse_mode='html')

@bot.message_handler(content_types=['document'])
def get_user_doc(message):
    global id_doc
    tconv = lambda x: time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(x))
    max_id = cr.execute("select max(id) from archive_docs").fetchone()
    cr.execute("""insert into archive_docs values(?, ?, ?, ?, ?)""",
               (int(max_id[0])+1, tconv(message.date), id_doc, message.from_user.id, "Принято"))
    db.commit()
    bot.send_message(message.chat.id, "Ваше заявление было принято на обработку", parse_mode='html')
    id_doc = 0
    for vl in cr.execute("select * from archive_docs"):
        print(vl)
    print("---------------------------------------------------")


#@bot.message_handler(commands=['button'])
#def button(message):
#    markup = types.InlineKeyboardMarkup()
#    markup.add(types.InlineKeyboardButton("Посетить веб", url="http://www.pdd24.com/pdd-onlain"))
#    bot.send_message(message.chat.id, "Кнопка работает", reply_markup=markup)

@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка 1")
    item2 = types.KeyboardButton("Кнопка 2")
    item3 = types.KeyboardButton("Кнопка 3")
    item4 = types.KeyboardButton("Кнопка 4")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Кнопка":
        bot.send_message(message.chat.id,"https://habr.com/ru/users/lubaznatel/")


bot.infinity_polling()

# @bot.message_handler(commands=['help'])
# def button(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     button1 = types.KeyboardButton("button1")
#     button2 = types.KeyboardButton("button2")
#     markup.add(button1, button2)
#     bot.send_message(message.chat.id, "Кнопка работает", reply_markup=markup)





bot.polling(none_stop=True)
