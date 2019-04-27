import os
import sqlite3


class FieldDB:
    """
    Временное описание полей таблицы
    """

    def __init__(self, name: str, type: str) -> None:
        super().__init__()
        self.name = name
        self.type = type


class TableDB:
    """
    Временная структура для описания таблицы
    """

    def __init__(self, name: str, fields: FieldDB, init_list=[], hookups='') -> None:
        super().__init__()
        self.fields = fields
        self.name = name
        self.hookups = hookups
        self.init_list = init_list


class DBManager:

    @staticmethod
    def select(table_name: str, fields=[], filter=None):
        sql = f'SELECT {", ".join(fields) or "*"} FROM {table_name}'
        if filter:
            sql += f' WHERE {filter}'
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def create(table_name, fields, values):
        sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(values)})"
        print(cursor.execute(sql))
        conn.commit()
        print(cursor.fetchone())

    @staticmethod
    def delete(table_name, filter):
        sql = f"DELETE FROM {table_name} WHERE {filter}"
        cursor.execute(sql)
        conn.commit()

    @staticmethod
    def run(sql):
        cursor.execute(sql)
        return cursor.fetchall()

    def init_db(self):
        """
        Инициализируем БД для тестового задания. Что бы БД была не пустая
        """
        # todo: Костыльно, надо на модели переписать с нормальными типами
        tables = self._tables_list()
        for table in tables:  # type: TableDB
            fields_with_type = ", ".join([f'{field.name} {field.type}' for field in table.fields])
            sql = f'create table if not exists {table.name} (id integer, {fields_with_type}, PRIMARY KEY (id){table.hookups})'
            cursor.execute(sql)
            cursor.execute(f'SELECT * FROM {table.name}')
            exists = cursor.fetchone()
            if exists is None:
                fields = ", ".join([field.name for field in table.fields])
                values = ", ".join(['?' for _ in range(len(table.fields))])
                cursor.executemany(f"INSERT INTO {table.name} ({fields}) VALUES ({values})", table.init_list)

        conn.commit()

    @staticmethod
    def _tables_list():
        """
        Таблицы для бд
        (Вынесены что бы не пугали сильно)
        """
        regions = [
            ('Краснодарский край',),
            ('Ростовская область',),
            ('Ставропольский край',),
        ]
        regions_field_list = [
            FieldDB('name', 'text'),
        ]
        regions_table = TableDB('regions', regions_field_list, regions)

        cities = [
            ('Краснодар', 1),
            ('Кропоткин', 1),
            ('Славянск', 1),
            ('Ростов', 2),
            ('Шахты', 2),
            ('Батайск', 2),
            ('Ставрополь', 3),
            ('Пятигорск', 3),
        ]
        cities_field_list = [
            FieldDB('name', 'text'),
            FieldDB('region_id', 'integer'),
        ]
        cities_hookups = ', CONSTRAINT fk_regions ' \
                         'FOREIGN KEY (region_id) ' \
                         'REFERENCES regions(region_id) ' \
                         'ON DELETE CASCADE'
        cities_table = TableDB('cities', cities_field_list, cities, cities_hookups)

        comments = [
            ("Рудин", "Стив", "Петрович", "98887771111", "email1@gmail.com", "Комментарии бывают двух видов: комментарии к постам и ответные комментарии. И каждый вид пишется в своём окне. С комментариями к постам ни у кого проблем нет. А вот с ответными  у некоторых наших друзей есть.", 1, 1),
            ('Нвапа', 'Майкл', 'Петрович', '+98887776655', 'email2@gmail.com', 'К любому посту для нас открыто окно для комментария. Написанный здесь комментарий предназначен АВТОРУ поста. И не важно, пишется он к чужому посту или к своему. Другими словами, если кто-то пишет комментарий в этом уже открытом окне в своём дневнике, то он пишет его самому себе! И тот, кому это писалось, не получит сообщения о нём.', 1, 1),
            ('Махонин', 'Вася', 'Петрович', '+98887771112', 'email2@gmail.com', 'Чтобы написать ответный комментарий, надо нажать "ответить" под комментарием того человека, которому вы желаете ответить. Откроется новое окно, предназначенное для ответного коммента. В этом случае ваш комментарий будет расположен сразу после исходного.', 3, 8),
            ('Апджян', 'Вася', 'Петрович', '+98887771113', 'email2@gmail.com', 'Можно воспользоваться и уже открытым окном, но надо нажать "обратиться" под комментарием того, кому вы отвечаете. Это не совсем удобно, если идёт диалог. Потому что он будет расположен не под комментарием того, кому вы отвечаете, а "в порядке очереди".', 1, 1),
            ('Бырыкин', 'Джино', 'Петрович', '+98887771114', 'email2@gmail.com', 'Сообщения о комментариях мы получаем на почту. Чтобы не получать сообщения обо всех комментариях к посту, в котором мы отметились, убираем галочку в квадратике у слов "подписка на комментарии". И тогда будут получены только ответные, то есть предназначенные именно нам.', 1, 1),
            ('Мухамедова', 'Виктория', 'Петрович', '+98887775111', 'email2@gmail.com', 'Кончились советы. Пора свои писать', 1, 1),
            ('Марроу', 'Наташа', 'Петрович', '+98887771611', 'email2@gmail.com', 'Не понравилось увиденное', 2, 5),
            ('Кузьмина', 'Лидия', 'Петрович', '+98887777111', 'email2@gmail.com', 'Безупречно, лучше нигде нету', 2, 4),
            ('Ярмоленко', 'Лиза', 'Петрович', '+98887771811', 'email2@gmail.com', 'Сыроватенько', 3, 7),
            ('Лёвочкина', 'Марина', 'Петрович', '+98887771911', 'email2@gmail.com', 'Очень страшно такое поддерживать', 3, 8),
            ('Певзнер', 'Макс', 'Петрович', '+98887771221', 'email2@gmail.com', 'Надеюсь то скоро кончится', 3, 8),
            ('Сафина', 'Виктор', 'Петрович', '+98887773311', 'email2@gmail.com', 'У меня 2 кота. Ня ня ня)', 2, 6),
            ('Минцковская', 'Петя', 'Петрович', '+98887771144', 'email2@gmail.com', 'Один рыжка', 2, 4),
            ('Полотнянчиков', 'Гриша', 'Петрович', '+98887775511', 'email2@gmail.com', 'Другой пушка', 1, 1),
            ('Петров', 'Рома', 'Петрович', '+98886671111', 'email2@gmail.com', 'Ну и под конец ещ один комментари средней длины. нууу жу ещё чуть чуть. Ну думаю хватит', 1, 2),
        ]
        comments_field_list = [
            FieldDB('first_name', 'text'),
            FieldDB('second_name', 'text'),
            FieldDB('last_name', 'text'),
            FieldDB('phone', 'text'),
            FieldDB('email', 'text'),
            FieldDB('text', 'text'),
            FieldDB('region_id', 'integer'),
            FieldDB('city_id', 'integer'),
        ]
        comments_hookups = ', CONSTRAINT fk_regions ' \
                           'FOREIGN KEY (region_id) ' \
                           'REFERENCES regions(region_id) ' \
                           'ON DELETE SET NULL' \
                           ', CONSTRAINT fk_cities ' \
                           'FOREIGN KEY (city_id) ' \
                           'REFERENCES cities(city_id) ' \
                           'ON DELETE SET NULL'
        comments_table = TableDB('comments', comments_field_list, comments)

        tables = [regions_table, cities_table, comments_table]
        return tables


DB_NAME = os.environ.get('DB_NAME', 'default_db_name')
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
DBManager().init_db()
