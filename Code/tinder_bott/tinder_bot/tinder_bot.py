import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from database import Users, Languages
from messages import get_text, get_lang_list



# API_TOKEN = "6076424344:AAEXBVhWjOiNCAIdEJQIjVqEtQnCYz3EzBI" # poraction
API_TOKEN = '6224620838:AAFoituXzckVTAVHQ7u8jJO8DpuxpiaTMpA'
users_db_filename = 'users.db'
lang_db_filename = 'languages.db'

users = Users(users_db_filename)
lang_db = Languages(lang_db_filename)

lang_list = get_lang_list()
gender_list = ('🧔🏻‍♂️', '👩🏼')
show_next_btn = ("🔍🌎")

bot = telebot.TeleBot(token=API_TOKEN, num_threads=15)


def chek_command(message: telebot.types.Message) -> bool: #Команды через слеш

    text = message.text
    if text is not None:
        if text == '/start' or text == "/language":
            select_lang(message)
            return True
        elif text == '/myprofile':
            myprofile(message)
            return True
        elif text == '/edit_profile':
            edit_profile(message)
            return True
    
    return False


def is_correct_gender(gender: str) -> bool: #Код гендеровв

    if gender is None or not gender.strip():
        return False
    genders = gender.split()
    for g in genders:
        if g not in gender_list:
            return False
    return True


def get_gender_markup() -> ReplyKeyboardMarkup: #Гендер лист

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*gender_list)
    return markup


def get_target_gender_markup() -> ReplyKeyboardMarkup: #Гендер кнопки

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*gender_list, ' '.join(gender_list))
    return markup


def lang_markup() -> ReplyKeyboardMarkup: # не знаю

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*lang_list)
    return markup


def show_next_keyboard() -> ReplyKeyboardMarkup: #Показывает следующие кнопки

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(show_next_btn)
    return markup


def gen_markup(*args) -> ReplyKeyboardMarkup: # создает клавиатуру

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*args)
    return markup


def first_inline_markup(ref_id: int) -> InlineKeyboardMarkup: #Привязывает смайлики к репорту и лайк/дизлайк +

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton("❤️", callback_data=f'like {ref_id}'),
        InlineKeyboardButton("❌", callback_data=f'dislike {ref_id}'))
    keyboard.add(InlineKeyboardButton("‼️", callback_data=f'report {ref_id} 1'))
    
    return keyboard


def like_inline_markup(ref_id: int) -> InlineKeyboardMarkup: #тоже самое по логике

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton("❤️", callback_data=f'both_like {ref_id}'),
        InlineKeyboardButton("❌", callback_data=f'dislike {ref_id}'))
    keyboard.add(InlineKeyboardButton("‼️", callback_data=f'report {ref_id} 2'))
    
    return keyboard


def my_inline_markup(lang_code: str, status: int) -> InlineKeyboardMarkup: #Кнопки профиля и т.д

    btns = get_text(lang_code, 'my_btns')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(btns[0], callback_data='edit_profile'),
        InlineKeyboardButton(btns[1], callback_data='show'))
    keyboard.add(
        InlineKeyboardButton(btns[4], callback_data='edit_photo'),
        InlineKeyboardButton(btns[5], callback_data='edit_desc'))
    if status:
        keyboard.add(InlineKeyboardButton(btns[2], callback_data='disable'))
    else:
        keyboard.add(InlineKeyboardButton(btns[3], callback_data='enable'))

    return keyboard


def report_keyboard(rep_id, rep_type) -> InlineKeyboardMarkup: #Кнопки репорта

    reasons = ['Spam', 'Violence', 'Pornography', 'Other']
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(reasons[0], callback_data=f'ban {rep_id} {reasons[0]}'),
        InlineKeyboardButton(reasons[1], callback_data=f'ban {rep_id} {reasons[1]}'))
    keyboard.add(
        InlineKeyboardButton(reasons[2], callback_data=f'ban {rep_id} {reasons[2]}'),
        InlineKeyboardButton(reasons[3], callback_data=f'ban {rep_id} {reasons[3]}'))
    
    keyboard.add(InlineKeyboardButton("Cancel", callback_data=f'cancel_report {rep_id} {rep_type}'))
    return keyboard


def send_profile(user_id: int, info: tuple,  who: str='my') -> None: #Отправка профиля другому юзеру при лайке и дизлайке

    name = info[3]
    photo = info[4]
    city = info[5]
    about = info[6]
    gender = info[7]
    target = info[8]
    status = info[9]
    lang_code = lang_db.get_lang(user_id)
    
    if who == 'my':
        markup = my_inline_markup(lang_code, status)
        txt_1 = get_text(lang_code, 'your_anketa')
        bot.send_message(user_id, txt_1, reply_markup=show_next_keyboard())

    elif who == 'first':
        markup = first_inline_markup(info[0])

    elif who == 'like':
        markup = like_inline_markup(info[0])
        txt_1 = get_text(lang_code, 'like_you')
        bot.send_message(user_id, txt_1, reply_markup=show_next_keyboard())
    else:
        return
    
    txt = f"{name}, {gender}, {city}\n"
    txt += f"{about}"
    txt = txt[:1024]
    bot.send_photo(user_id, photo, caption=txt, reply_markup=markup)


def send_report_to_user(user_id: int, report_type: str) -> None: #отправка репорта

    lang_code = lang_db.get_lang(user_id)
    text = get_text(lang_code, 'report')
    text += f'\nReport type: ({report_type})'
    msg = bot.send_message(user_id, text=text)


def show_my_profile(info: tuple, message: telebot.types.Message): #показывает мой профиль

    user_id = message.from_user.id
    name = info[3]
    photo = info[4]
    city = info[5]
    about = info[6]
    gender = info[7]
    target = info[8]
    status = info[9]
    for item in (name, photo, city, about, gender, target):
        if item is None:
            edit_profile(message)
            return
    send_profile(user_id, info, 'my')


def set_lang(message: telebot.types.Message) -> None: #установка языка

    if chek_command(message):
        return
    
    text = message.text
    user_id = message.from_user.id
    if text is not None:
        text = text.strip()
        if text in lang_list:
            lang_db.update_lang(user_id, text)
            myprofile(message)
            return

    lang_code = lang_db.get_lang(user_id)
    text = get_text(lang_code, 'incorect_input')
    msg = bot.send_message(user_id, text=text)
    bot.register_next_step_handler(msg, set_lang)


def input_target(message: telebot.types.Message) -> None: #выбор пола логическая конструкция

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    target = message.text

    if not is_correct_gender(target):
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_target)
    else:
        users.add_target(user_id, target)
        myprofile(message)


def input_gender(message: telebot.types.Message) -> None: #вводим свой гендер? Да

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    gender = message.text
    if gender is None or gender not in gender_list:
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_gender)
    else:
        users.add_gender(user_id, gender)
        text = get_text(lang_code, 'select_target')
        target_markup = get_target_gender_markup()
        msg = bot.send_message(user_id, text=text, reply_markup=target_markup)
        bot.register_next_step_handler(msg, input_target)


def input_about(message: telebot.types.Message) -> None: #вводим инфу о себе

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    about = message.text
    if about is None:
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_about)
    else:
        users.add_about(user_id, about)
        text = get_text(lang_code, 'select_gender')
        gender_markup = get_gender_markup()
        msg = bot.send_message(user_id, text=text, reply_markup=gender_markup)
        bot.register_next_step_handler(msg, input_gender)


def input_about_only(message: telebot.types.Message) -> None: #для получения информации об пользователе и сохранения ее в базу данных

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    about = message.text
    if about is None:
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_about_only)
    else:
        users.add_about(user_id, about)
        myprofile(message)


def input_city(message: telebot.types.Message) -> None: #вводим город

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    city = message.text
    if city is None:
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_city)
    else:
        city = city.strip().capitalize()
        users.add_city(user_id, city)
        text = get_text(lang_code, 'select_about')
        msg = bot.send_message(user_id, text=text, reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_about)


def input_photo(message: telebot.types.Message) -> None: #вводим фото

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    if message.content_type != "photo":
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_photo)
    else:
        photo_id = message.photo[-1].file_id
        users.add_photo(user_id, photo_id)
        text = get_text(lang_code, 'select_city')
        msg = bot.send_message(user_id, text=text, reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_city)


def input_photo_only(message: telebot.types.Message) -> None: # Если пользователь отправил не фотографию, то функция отправляет сообщение об ошибке и ожидает повторного сообщения, содержащего фотографию. 

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    if message.content_type != "photo":
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text)
        bot.register_next_step_handler(msg, input_photo_only)
    else:
        photo_id = message.photo[-1].file_id
        users.add_photo(user_id, photo_id)
        myprofile(message)


def input_name(message: telebot.types.Message) -> None: #вводим имя

    if chek_command(message):
        return
    
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    if first_name is not None:
        markup = gen_markup(first_name)
    else:
        markup = ReplyKeyboardRemove()
    lang_code = lang_db.get_lang(user_id)
    name = message.text
    if name is None:
        text = get_text(lang_code, 'incorect_input')
        msg = bot.send_message(user_id, text=text, reply_markup=markup)
        bot.register_next_step_handler(msg, input_name)
    else:
        users.add_name(user_id, name)
        text = get_text(lang_code, 'select_photo')
        msg = bot.send_message(user_id, text=text, reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_photo)


def search_users(message: telebot.types.Message) -> None: #поиск пользователей

    user_id = message.from_user.id
    state = bot.get_state(user_id=user_id)
    if state is None:
        state = set()
    pair = users.get_pair(user_id, state)
    if pair is None:
        lang_code = lang_db.get_lang(user_id)
        text = get_text(lang_code, 'no_in_town')
        bot.send_message(user_id, text=text)
    elif pair == -1:
        edit_profile(message)
    else:
        send_profile(user_id, pair, 'first')
        state.add(pair[0])
        bot.set_state(user_id=user_id, state=state)


def send_who_like(user_id: int, partner_id: int) -> None: #показывает кто лайкнул

    profile = users.get_profile(user_id)
    if profile is not None:
        send_profile(partner_id, profile,  'like')
        try:
            state = bot.get_state(user_id=user_id)
            if state is None:
                state = set()
            state.add(partner_id)
            bot.set_state(user_id=user_id, state=state)

            state = bot.get_state(user_id=partner_id)
            if state is None:
                state = set()
            state.add(user_id)
            bot.set_state(user_id=partner_id, state=state)

        except Exception as e:
            print(e)
            print('in send_who_like()')
        

def send_contacts(user_id: int, partner_id: int) -> None: #отправка контактов человека при взаимном лайке

    prifile_1 = users.get_profile(user_id)
    partner_profile = users.get_profile(partner_id)
    for profile, chat_id in ((prifile_1, partner_id), (partner_profile, user_id)):
        if profile is None:
            continue
        try:
            lang_code = lang_db.get_lang(chat_id)
            text = get_text(lang_code, 'contacts')
            name = profile[3]
            city = profile[5]
            gender = profile[7]
            username = profile[1]
            text += f"{name} {gender}, {city} \n@{username}"
            bot.send_message(chat_id, text, reply_markup=show_next_keyboard())
        except Exception as e:
            print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_process(call: telebot.types.CallbackQuery): #обработка запросов сложный процесс...

    data = call.data
    msg_id = call.message.id
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    lang_code = lang_db.get_lang(user_id)
    if data is None:
        return
    elif data == "edit_profile":
        edit_profile(call)

    elif data == "edit_photo":
        text = get_text(lang_code, 'select_photo')
        msg = bot.send_message(user_id, text=text, reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_photo_only)
    elif data == "edit_desc":
        text = get_text(lang_code, 'select_about')
        msg = bot.send_message(user_id, text=text, reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, input_about_only)
    
    elif data == "disable":
        users.disable_user(user_id)
        markup = my_inline_markup(lang_code, 0)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=markup)
    elif data == "enable":
        users.enable_user(user_id)
        markup = my_inline_markup(lang_code, 1)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=markup)
    elif data == "show":
        search_users(call)

    if data.startswith("like") or data.startswith("dislike") or data.startswith("both_like"):
        command, partner_id = data.split()[:2]
        if command == "like":
            try:
                send_who_like(user_id, partner_id)
            except Exception as e:
                print(e)
            search_users(call)
        elif command == "both_like":
            send_contacts(user_id, partner_id)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
    elif data.startswith('report'):
        rep_id = data.split()[1]
        rep_type = data.split()[2]
        markup = report_keyboard(rep_id, rep_type)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=markup)
    elif data.startswith('ban'):
        bot.answer_callback_query(call.id, 'Done', cache_time=2)
        bot.delete_message(chat_id, msg_id)
        rep_id = data.split()[1]
        report_type = data.split()[2]
        send_report_to_user(rep_id, report_type)
    elif data.startswith("cancel_report"):
        rep_id = data.split()[1]
        rep_type = data.split()[2]
        if rep_type == '1':
            markup = first_inline_markup(rep_id)
        else:
            markup = like_inline_markup(rep_id)
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=markup)
    bot.answer_callback_query(call.id, 'Ok')



@bot.message_handler(commands=['start', 'language'], chat_types=['private'])
def select_lang(message: telebot.types.Message): # не знаю

    user_id = message.from_user.id
    lang_db.add_user(user_id)
    lang_code = lang_db.get_lang(user_id)

    text = get_text(lang_code, 'select_lang')
    if text is not None:
        markup = lang_markup()
        msg = bot.send_message(user_id, text=text, reply_markup=markup)
        bot.register_next_step_handler(msg, set_lang)



@bot.message_handler(func=lambda message: message.from_user.username is None, chat_types=['private'])
def no_username(message: telebot.types.Message): # не знаю

    user_id = message.from_user.id
    lang_code = lang_db.get_lang(user_id)
    text = get_text(lang_code, 'no_username')
    bot.send_message(user_id, text)


@bot.message_handler(commands=['edit_profile'], chat_types=['private'])
def edit_profile(message: telebot.types.Message): # создание профиля? Его изменения
    
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    users.add_user(user_id, user_name, first_name)
    lang_code = lang_db.get_lang(user_id)
    if first_name is not None:
        markup = gen_markup(first_name)
    else:
        markup = None
    txt = get_text(lang_code, 'select_name')
    msg = bot.send_message(user_id, txt, reply_markup=markup)
    bot.register_next_step_handler(msg, input_name)

    

@bot.message_handler(commands=['myprofile'], chat_types=['private'])
def myprofile(message: telebot.types.Message): #показывает мой профиль? Да

    user_id = message.from_user.id
    username = message.from_user.username
    
    if username is None:
        no_username(message)
    else:
        profile = users.get_profile(user_id)
        if profile is not None:
            show_my_profile(profile, message)
        else:
            edit_profile(message)


@bot.message_handler(content_types=['text'], chat_types=['private'])
def no_username(message: telebot.types.Message): #Когда нету юзернейма у пользователя такое бывает

    text = message.text
    if text is not None:
        if text == show_next_btn:
            search_users(message)


bot.infinity_polling()