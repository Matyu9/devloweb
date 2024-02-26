import sqlite3
import time


class DevloBDD:
    def __init__(self):
        self.conn = sqlite3.connect('devloweb.db')
        self.cursor = self.conn.cursor()
        # Creation de la base de donnée utilisateur
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(ja_id TEXT NOT NULL, email TEXT NOT NULL, password 
        TEXT NOT NULL, date INT NOT NULL, active INT DEFAULT 0)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS verification(ja_id TEXT NOT NULL, code TEXT NOT NULL, 
        date TEXT DEFAULT CURRENT_TIMESTAMP)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS security(ip TEXT NOT NULL,try INT DEFAULT 1, 
        first TEXT DEFAULT CURRENT_TIMESTAMP, last TEXT DEFAULT CURRENT_TIMESTAMP, punition TEXT DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.commit()



    def inscire_ja(self, ja_id, email, password):
        date = time.time()
        self.cursor.execute("INSERT INTO users(ja_id, email, password, date) VALUES (?, ?, ?, ?)", (ja_id, email, password, date))
        self.conn.commit()

    def ja_exists(self, ja_id: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE ja_id = ?", (ja_id,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def activer_ja(self, ja_id: int):
        self.cursor.execute("UPDATE users SET active = 1 WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def is_active(self, ja_id: int) -> bool:
        self.cursor.execute("SELECT active FROM users WHERE ja_id = ?", (ja_id,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False


    """
    Partie Code de Vérification
    """
    def store_code(self, ja_id, code):
        self.cursor.execute("INSERT INTO verification(ja_id, code) VALUES (?, ?)", (ja_id, code))
        self.conn.commit()

    def code_exists(self, code: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM verification WHERE code = ?", (code,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    """
    Partie sécurité :
    -> try
    """
    def init_try(self, ip):
        self.cursor.execute("INSERT INTO security(ip) VALUES (?)", (ip,))
        self.conn.commit()

    def has_try(self, ip: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM security WHERE ip = ?", (ip,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def update_try(self, ip: str):
        self.cursor.execute("UPDATE security SET try = try + 1 WHERE ip = ?", (ip,))
        self.conn.commit()

    def add_try(self, ip: str):
        if self.has_try(ip):
            self.update_try(ip)
        else:
            self.init_try(ip)

    def quit_bdd(self):
        self.conn.close()

    def get_try(self, ip: str):
        self.cursor.execute("SELECT * FROM security WHERE ip = ?", (ip,))
        self.conn.commit()

    def reset_try(self, ip: str):
        self.cursor.execute("UPDATE security SET try = 0 WHERE ip = ?", (ip,))



if __name__ == '__main__':
    bdd = DevloBDD()
    print(bdd.is_active(8166))