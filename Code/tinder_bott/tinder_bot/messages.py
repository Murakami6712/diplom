text = {
    'UK 🇺🇦': {
        'select_lang': "Обери мову",
        'report': "На вас надійшла скарга! Перевірте свій профіль!",
        'contacts': "Тримай посилання на профіль:\n",
        'like_you': "Користувач поставив тобі лайк!",
        'no_in_town': "Нажаль більше немає користувачів з вашого міста",
        'my_btns': (
                "Редагувати анкету",
                "Дивитись анкети",
                "Не показувати мою анкету",
                "Показувати мою анкету",
                "Змінити фото",
                "Змінити опис"),
        'your_anketa': "Так виглядає твоя анкета:",
        'select_target': "Чиї анкети тобі показувати\n🧔🏻‍♂️ Чоловіків 👩🏼 Жінок \n🧔🏻‍♂️ 👩🏼 Усіх",
        'select_gender': "Яка твоя стать\n🧔🏻‍♂️ Чоловік 👩🏼 Жінка",
        'select_about': "Напиши декілька слів про себе",
        'select_city': "В якому ти місті?",
        'select_photo': "Надішли своє фото",
        'incorect_input': "Немає такого варіанту відповіді.",
        'select_name': "Давай заповнимо твою анкету!\nНапиши своє ім'я",
        'no_username': "Для того щоб користуватися ботом необхідно створити ім'я користувача телеграм.",


    },
    'RU 🏳️': {
        'select_lang': "Выбери язык",
        'report': "На вас поступила жалоба! Проверьте свой профиль!",
        'contacts': "Держи ссылку на профиль\n",
        'like_you': "Пользователю понравилась твоя анкета",
        'no_in_town': "К сожалению, больше нет пользователей из вашего города",
        'my_btns': (
                "Редактировать анкету",
                "Смотреть анкеты",
                "Не показывать мою анкету",
                "Показывать мою анкету",
                "Изменить фото",
                "Изменить описание"),
        'your_anketa': "Так выглядит твоя анкета:",
        'select_target': "Чьи анкеты тебе показывать\n🧔🏻‍♂️ Мужчин 👩🏼 Женщин \n🧔🏻‍♂️ 👩🏼 Всех",
        'select_gender': "Какой твой пол\n🧔🏻‍♂️ Мужчина 👩🏼 Женщина",
        'select_about': "Напиши немного о себе",
        'select_city': "Из какого ты города",
        'select_photo': "Пришли свою фотографию",
        'incorect_input': "Нет такого варианта ответа.",
        'select_name': "Давай заполним твою анкету!\nНапишите ваше имя",
        'no_username': "Для того чтобы пользоваться ботом, необходимо создать имя пользователя телеграмм.",
        
    },
    'EN 🇬🇧': {
        'select_lang': "Choose your language",
        'report': "You have received a complaint! Check your profile!",
        'contacts': "Keep a link to the user profile\n",
        'like_you': "The user liked your profile",
        'no_in_town': "Sorry, there are no more users from your city",
        'my_btns': (
                "Edit",
                "Search",
                "Disable",
                "Enable"
                "Edit photo",
                "Edit description"),
        'your_anketa': "This is how your profile looks like:",
        'select_target': "Whose profiles to show you\n🧔🏻‍♂️ Man 👩🏼 Woman \n🧔🏻‍♂️ 👩🏼 All",
        'select_gender': "What's your gender\n🧔🏻‍♂️ Man 👩🏼 Woman",
        'select_about': "Tell me about yourself",
        'select_city': "What is your city?",
        'select_photo': "Send you photo",
        'incorect_input': "No such answer.",
        'select_name': "Let's fill out your questionnaire!\nWrite your name",
        'no_username': "In order to use the bot, you need to create a Telegram username.",
        
    }
}



def get_lang_list() -> tuple:

    return tuple(text.keys())


def get_text(lang: str, item: str) -> str:

    try:
        return text[lang][item]
    except Exception as e:
        print(e)
        return None