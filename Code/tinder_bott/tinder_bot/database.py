import sqlite3
from mtranslate import translate


class Users:


    def __init__(self, filename: str) -> None: #инициирует класс
        
        self.filename = filename
        self.timeout = 5
        self.create_table()

    
    def create_table(self) -> None: #создает таблицу в базе данных о профиле? ДА

        sql = ''' 
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY UNIQUE,
        user_name STRING,
        first_name STRING,
        name STRING DEFAULT NULL,
        photo STRING DEFAULT NULL,
        city STRING DEFAULT NULL,
        about STRING DEFAULT NULL,
        gender STRING DEFAULT NULL,
        target STRING DEFAULT NULL,
        status INTEGER DEFAULT 0,
        city_ru STRING DEFAULT NULL);'''

        with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
            cursor = connect.cursor()
            cursor.execute(sql)
            connect.commit()


    def get_pair(self, user_id: int, state: set) -> tuple: #Делает пару используя данные из бд

        my_profile = self.get_profile(user_id)
        
        if my_profile is None:
            return -1
        
        city_ru = my_profile[10]
        targets = my_profile[8].split()

        sql = '''SELECT * FROM users WHERE id <> ? AND status = 1 AND city_ru = ?;'''
        data = (user_id, city_ru,)
        with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
            cursor = connect.cursor()
            cursor.execute(sql, data)
            result = cursor.fetchall()

        for user in result:
            if user[0] not in state:
                for target in targets:
                    if target == user[7]:
                        return user
        return None


    def add_user(self, user_id: str, user_name: str, first_name: str) -> None: #добавляет пользователя? Да

        sql = '''
        INSERT INTO users (id, user_name, first_name) VALUES (?, ?, ?);'''
        data = (user_id, user_name, first_name,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def enable_user(self, user_id: int) -> None: #одобрение пользователя? Да
        
        sql = '''
            UPDATE users
            SET status = 1
            WHERE id = ?;'''
        data = (user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def disable_user(self, user_id: int) -> None: #удаление пользователя
        
        sql = '''
            UPDATE users
            SET status = 0
            WHERE id = ?;'''
        data = (user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
            
        except Exception as e:
            print(e)


    def add_target(self, user_id: int, target: str) -> None: #Выбирает цель поиска (парень/девушка)

        sql = '''
            UPDATE users
            SET target = ?
            WHERE id = ?;'''
        data = (target, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
            self.enable_user(user_id)
        except Exception as e:
            print(e)


    def add_gender(self, user_id: int, gender: str) -> None: #создает гендер в БД

        sql = '''
            UPDATE users
            SET gender = ?
            WHERE id = ?;'''
        data = (gender, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def add_about(self, user_id: int, about: str) -> None: #создает описание в БД

        sql = '''
            UPDATE users
            SET about = ?
            WHERE id = ?;'''
        data = (about, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)
    

    def add_city(self, user_id: int, city: str) -> None: #создает город в БД

        sql = '''
            UPDATE users
            SET city = ?, city_ru = ?
            WHERE id = ?;'''
        city_ru = city
        try:
            city_ru = translate(city, 'ru')
        except Exception as e:
            print(e)
        data = (city, city_ru, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def add_name(self, user_id: int, name: str) -> None: #имя в БД

        sql = '''
            UPDATE users
            SET name = ?
            WHERE id = ?;'''
        data = (name, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def add_photo(self, user_id: int, photo_id: str) -> None: #фото в БД

        sql = '''
            UPDATE users
            SET photo = ?
            WHERE id = ?;'''
        data = (photo_id, user_id,)
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
        except Exception as e:
            print(e)


    def get_profile(self, user_id: int) -> list: #Получает профиль из бд

        sql = '''SELECT * FROM users WHERE id = ? LIMIT 1;'''
        data = (user_id, )
        with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
            cursor = connect.cursor()
            cursor.execute(sql, data)
            result = cursor.fetchone()
        return result
    

    def do_something(self, sql: str, data: tuple) -> None: #функция для тестов

        with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
            cursor = connect.cursor()
            cursor.execute(sql, data)
            result = cursor.fetchall()
            connect.commit()
        return result




class Languages:


    def __init__(self, filename: str) -> None: #языки? Да их инициализация в классе
        
        self.filename = filename
        self.timeout = 5
        self.create_table()


    def create_table(self) -> None: # создает бд с языками

        sql = '''
        CREATE TABLE IF NOT EXISTS lenguages
        (id INTEGER PRIMARY KEY UNIQUE,
        language_code STRING DEFAULT "UK 🇺🇦" NOT NULL);'''
        with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
            cursor = connect.cursor()
            cursor.execute(sql)
            connect.commit()


    def add_user(self, user_id: int) -> bool: # добавляет язык юзера

        sql = '''
            INSERT INTO lenguages(id)
            VALUES(?);'''
        data = (user_id, )
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
            return True
        except Exception as e:
            return False


    def update_lang(self, user_id: int, lang: str) -> bool: # обновляет язык пользователя

        self.add_user(user_id)
        sql = '''
            UPDATE lenguages
            SET language_code = ?
            WHERE id = ?;'''
        data = (lang, user_id, )
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                connect.commit()
            return True
        except Exception as e:
            return False


    def get_lang(self, user_id: int) -> str: # получает язык пользователя

        lang = 'uk'
        sql = '''SELECT language_code FROM lenguages WHERE id = ? LIMIT 1;'''
        data = (user_id, )
        try:
            with sqlite3.connect(self.filename, timeout=self.timeout) as connect:
                cursor = connect.cursor()
                cursor.execute(sql, data)
                result = cursor.fetchone()
            if result is not None:
                lang = result[0]
        except Exception as e:
            print(e)
        
        return lang



if __name__ == "__main__": # запуск главной программы

    db_fname = "users.db"
    users = Users(db_fname)
    #users.add_user(12345678)