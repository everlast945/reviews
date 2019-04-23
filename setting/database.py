import os
import sqlite3

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
            self.init_db()
        return self.conn

    def db_cursor(self, conn=None):
        if self.cursor is None:
            if conn is None:
                conn = self.db_connection()
            self.cursor = conn.cursor()
        return self.cursor

    def init_db(self):
        """
        Инициализируем БД для тестового задания. Что бы БД была не пустая
        """
        conn = self.db_connection()
        cursor = self.db_cursor()
        tables = {
            'regions': [
                'name text',
            ],
            'cities': [
                'name text',
                'region_id integer',
                'CONSTRAINT fk_regions '
                'FOREIGN KEY (region_id)'
                'REFERENCES regions(region_id)'
                'ON DELETE CASCADE'],
            'comments': [
                'first_name text',
                'second_name text',
                'last_name text',
                'phone text',
                'email text',
                'text text'
            ],
        }
        for table_name, fields in tables.items():
            sql = f'create table if not exists {table_name} ({", ".join(fields)})'
            cursor.execute(sql)
        # create regions
        regions = [
            ('Краснодарский край',),
            ('Ростовская область',),
            ('Ставропольский край',),
        ]
        cursor.executemany("INSERT INTO regions VALUES (?)", regions)
        # create cities
        cities = [
            ('Краснодар', 1),
            ('Ростов', 2),
            ('Ставрополь', 3),
        ]
        cursor.executemany("INSERT INTO cities VALUES (?,?)", cities)

        # create comments
        cursor.execute('SELECT * FROM comments')
        exists = cursor.fetchone()
        if exists is None:
            comments = [
                ("first_name", "second_name", "last_name", "phone", "email", "text"),
                ('Клиент', 'Плохой', '', '', '', 'Очень плохой комментарий'),
                ('Клиент', 'Получше', 'С отчеством', '', '', 'Комментарий'),
            ]
            cursor.executemany("INSERT INTO comments VALUES (?,?,?,?,?,?)", comments)


        conn.commit()
