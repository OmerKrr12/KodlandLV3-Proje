import sqlite3
import os

class DB_Manager:
    def __init__(self, database):
        self.database = database
        if not  os.path.exists(self.database): 
            self.create_tables()
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE FAQs (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            text TEXT NOT NULL,
                            response TEXT,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 
            conn.execute('''CREATE TABLE not_in_FAQs (
                            id INTEGER,
                            user_id INTEGER,
                            text TEXT NOT NULL,
                            response TEXT
                            times_asked INTEGER DEFAULT 1,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()

    def insert_faq(self, user_id, text, response):
        sql_check_faqs = '''SELECT response FROM FAQs WHERE text = ?'''
        faq_result = self.__select_data(sql_check_faqs, (text,))
        if faq_result:
            return faq_result[0][0]

        sql_check_not_in_faqs = '''SELECT id, times_asked FROM not_in_FAQs WHERE text = ?'''
        result = self.__select_data(sql_check_not_in_faqs, (text,))
        if result:
            faq_id = result[0][0]
            times_asked = result[0][1] if result[0][1] is not None else 0
            sql_update = '''UPDATE not_in_FAQs SET times_asked = ? WHERE id = ?'''
            self.__executemany(sql_update, [(times_asked + 1, faq_id)])
            return None  

        sql_insert = '''INSERT INTO not_in_FAQs (user_id, text, response, times_asked) VALUES (?, ?, ?, 1)'''
        data = (user_id, text, response)
        self.__executemany(sql_insert, [data])
        return None 

