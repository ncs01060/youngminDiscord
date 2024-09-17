import sqlite3

#db = sqlite3.connect("./db/youngmin.db")
#fishDB = sqlite3.connect("./db/fish.db")
#oreDB = sqlite3.connect("./db/ore.db")
#cur = db.cursor()
#fishCur = fishDB.cursor()
#oreCur = oreDB.cursor()



#oreCur.execute('''CREATE TABLE IF NOT EXISTS ore
            #(id text PRIMARY KEY,pic text,iron real,coal real,gold real,diamond real,blackstone real, stone real)''')


#cur.execute('''CREATE TABLE IF NOT EXISTS stocks
            #(id text PRIMARY KEY,job text, price real, exp real,level real,name text, playtime real,
             #fishingrod text)''')

#fishCur.execute('''CREATE TABLE IF NOT EXISTS fish
                #(id text PRIMARY KEY,mackerel real,cod real,shrimp real,salmon real,yeti real,mommoss real)''')


def select_ore(user_id,ore):
    db = sqlite3.connect("./db/ore.db")
    cur = db.cursor()
    cur.execute(f'SELECT {ore} FROM ore WHERE id = ?',(user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None


def update_ore(user_id,ore,num):
    db=sqlite3.connect("./db/ore.db")
    cur = db.cursor()
    cur.execute(f'UPDATE ore SET {ore} = ? WHERE id = ?', (num, user_id))
    db.commit()
    db.close()


def select_price(user_id):
    db = sqlite3.connect("./db/youngmin.db")
    cur = db.cursor()
    cur.execute('SELECT price FROM stocks WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None


def select_Rod(user_id):
    db = sqlite3.connect("./db/youngmin.db")
    cur = db.cursor()
    cur.execute('SELECT fishingrod FROM stocks WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    if result[0] == 'nomal':
        return ["기본 낚싯대",1]
    return result[0] if result else None


def select_cod(user_id):
    db = sqlite3.connect("./db/fish.db")
    cur = db.cursor()
    cur.execute('SELECT cod FROM fish WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None

def select_mackerel(user_id):
    db = sqlite3.connect("./db/fish.db")
    cur = db.cursor()
    cur.execute('SELECT mackerel FROM fish WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None

def select_Exp(user_id):
    db = sqlite3.connect("./db/youngmin.db")
    cur = db.cursor()
    cur.execute('SELECT exp FROM stocks WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None

def select_Level(user_id):
    db = sqlite3.connect("./db/youngmin.db")
    cur = db.cursor()
    cur.execute('SELECT level FROM stocks WHERE id = ?', (user_id,))
    result = cur.fetchone()
    db.close()
    return result[0] if result else None

def update_price(user_id, money):
    try:
        # 데이터베이스에 연결
        db = sqlite3.connect("./db/youngmin.db")
        cur = db.cursor()

        # 가격 업데이트
        cur.execute('UPDATE stocks SET price = ? WHERE id = ?', (money, user_id))
        db.commit()
    
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return None
    
    finally:
        # 커서와 데이터베이스 연결 닫기
        cur.close()
        db.close()

def update_fish(id,fish,num):
    fishDB = sqlite3.connect("./db/fish.db")
    fishCur = fishDB.cursor()
    fishCur.execute(f'UPDATE fish SET {fish} = ? WHERE id = ?', (num, id))
    fishDB.commit()
    fishDB.close()

def update_exp(id,num):
    db = sqlite3.connect('./db/youngmin.db')
    cur = db.cursor()
    cur.execute(f'UPDATE stocks SET exp = ? WHERE id = ?',(num,id))
    db.commit()
    db.close()


def update_level(id,num):
    db = sqlite3.connect('./db/youngmin.db')
    cur = db.cursor()
    cur.execute(f'UPDATE stocks SET level = ? WHERE id = ?',(num,id))
    db.commit()
    db.close()

def check_levelUp(id):
    exp = select_Exp(id)
    if int(exp) >= 10:
        update_exp(id,exp-10)
        update_level(id,int(select_Level())+1)