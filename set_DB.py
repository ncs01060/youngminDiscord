import sqlite3

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('./db/announcement.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER
                )''')
    conn.commit()
    conn.close()

init_db()  #