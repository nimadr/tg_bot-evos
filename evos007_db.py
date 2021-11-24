import sqlite3


class Datebase:
    def __init__(self):
        self.db_name = 'evos catalog.db'
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS 'BIG_CATALOG'(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL ,
            parent_id INTEGER ,
            FOREIGN KEY (parent_id)
            REFERENCES BIG_CATALOG(id)
             ON UPDATE CASCADE
             ON DELETE CASCADE   
        )    
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS 'catalog_table'(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL 
        )
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS 'catalog_product'(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL ,
        price INTEGER NOT NULL,
        description TEXT NOT NULL,
        photo TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        FOREIGN KEY (category_id)
        REFERENCES BIG_CATALOG(id)
             ON UPDATE CASCADE
             ON DELETE CASCADE,       
        FOREIGN KEY (type_id)
        REFERENCES catalog_table(id)
             ON UPDATE CASCADE
             ON DELETE CASCADE       
        )
        """)
        self.conn.commit()

    def null_catalog(self):
        a = self.conn.execute("""
        SELECT id,name FROM 'BIG_CATALOG'
        WHERE parent_id is null
        """).fetchall()
        return a

    def callback_query(self, key):
        a = self.conn.execute('''
        SELECT id,name FROM BIG_CATALOG
        WHERE parent_id  = ?
        ''', [key]).fetchall()
        return a

    # def data_sp(self,category,parient,numbers):


    def savatcha(self, produkt_id):
        a = self.conn.execute("""
        SELECT * FROM catalog_product
        WHERE type_id = ? 
        """, [produkt_id]).fetchone()
        return a

    def get_product(self, ctg_id, type_id):
        a = self.conn.execute("""
        SELECT * FROM catalog_product
        WHERE category_id = ? and type_id = ?
        """, [ctg_id, type_id]).fetchone()
        return a

    def get_type(self, ctg_id):
        a = self.conn.execute("""
        SELECT ct.name,ct.id FROM catalog_product as cp
        INNER JOIN catalog_table as ct
        ON cp.type_id = ct.id
        WHERE cp.category_id = ?
        """, [ctg_id]).fetchall()
        return a

    def add_catalog(self):
        ctg = [
            (1, '🌯Lavash', None),
            (2, '🍲shaurma', None),
            (3, '🥙Donar', None),
            (4, '🍔Gamburger', None),
            (5, '🌭Xot-Dog', None),
            (6, '🍰Disertlar', None),
            (7, '☕️Ichimliklar', None),
            (8, '🍟Gazaklar', None),
            (9, 'G`oshtli lavsh', 1),
            (10, 'G`oshtli lavsh pishloqli', 1),
            (11, 'Toviqli lavash', 1),
            (12, 'Toviqli lavash pshloqli', 1),
            (13, 'Qalampir lavash', 1),
            (14, 'Filter', 1),
            (15, 'G`oshtli shourma', 2),
            (16, 'G`oshtli shourma achchiq', 2),
            (17, 'Tovuqli shourma', 2),
            (18, 'Tovuqli shourma achchiq', 2),
            (19, 'Go`shtli', 3),
            (20, 'Tovuqli', 3),
            (21, 'Gamburger', 4),
            (22, 'Chizburger', 4),
            (23, 'Klassik hotdog', 5),
            (24, 'Oddiy', 5),
            (25, 'Shohona', 5),
            (26, 'Asalm', 8),
            (27, 'Chizkeyk', 8),
            (28, 'Choko', 8),
            (29, 'Fri', 7),
            (30, 'Стрипсы', 7),
            (31, 'Qish.Kartoshkasi', 7),
            (32, 'Salat', 7),
            (33, 'Souslar', 7),
            (34, 'Guruch', 7)

        ]
        self.conn.executemany("""
            INSERT INTO 'BIG_CATALOG'(id,name,parent_id)
            Values (?,?,?)
        """, ctg)
        self.conn.commit()

    # def discrptsipn(self):
