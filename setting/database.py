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


class TableBD:
    """
    Временная структура для описания таблицы
    """

    def __init__(self, name: str, fields: FieldDB, init_list, hookups='') -> None:
        super().__init__()
        self.fields = fields
        self.name = name
        self.hookups = hookups
        self.init_list = init_list


class DBManager:

    def __init__(self) -> None:
        super().__init__()
        self.conn = None
        self.cursor = None

    def db_connection(self):
        """
        Подключение к БД/Создание БД
        :return: Подключение к БД
        """
        if self.conn is None:
            db_name = os.environ.get('DB_NAME', 'default_db_name')
            self.conn = sqlite3.connect(db_name)
            self._init_db()
        return self.conn

    def db_cursor(self, conn=None):
        if self.cursor is None:
            if conn is None:
                conn = self.db_connection()
            self.cursor = conn.cursor()
        return self.cursor

    def _init_db(self):
        """
        Инициализируем БД для тестового задания. Что бы БД была не пустая

        """
        conn = self.db_connection()
        cursor = self.db_cursor()
        # todo: Костыльно, надо на модели переписать с нормальными типами
        tables = self._tables_list()
        for table in tables:  # type: TableBD
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

    def _tables_list(self):
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
        regions_table = TableBD('regions', regions_field_list, regions)

        cities = [
            ('Краснодар', 1),
            ('Ростов', 2),
            ('Ставрополь', 3),
        ]
        cities_field_list = [
            FieldDB('name', 'text'),
            FieldDB('region_id', 'integer'),
        ]
        cities_hookups = ', CONSTRAINT fk_regions ' \
                         'FOREIGN KEY (region_id) ' \
                         'REFERENCES regions(region_id) ' \
                         'ON DELETE CASCADE'
        cities_table = TableBD('regions', cities_field_list, cities, cities_hookups)

        comments = [
            ("first_name", "second_name", "last_name", "phone", "email", "test row"),
            ('Иванов', 'Иван', 'Иванович', '+98887776655', 'email@gmail.com', 'Понравилось'),
            ('Петров', 'Петр', 'Петрович', '+98887771111', 'email2@gmail.com', 'Не понравилось'),
        ]
        comments_field_list = [
            FieldDB('first_name', 'text'),
            FieldDB('second_name', 'text'),
            FieldDB('last_name', 'text'),
            FieldDB('phone', 'text'),
            FieldDB('email', 'text'),
            FieldDB('text', 'text'),
        ]
        comments_table = TableBD('comments', comments_field_list, comments)

        tables = [regions_table, cities_table, comments_table]
        return tables
