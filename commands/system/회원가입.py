import discord
import sqlite3

async def 회원가입(interaction: discord.Interaction):
    id = interaction.user.id
    name = interaction.user.name
    
    # 기존 DB 연결
    db = sqlite3.connect("db/youngmin.db")
    fishDB = sqlite3.connect("db/fish.db")
    oreDB = sqlite3.connect("db/ore.db")
    
    cur = db.cursor()
    fishCur = fishDB.cursor()
    oreCur = oreDB.cursor()

    try:
        # 기존 youngmin.db에 이미 id가 존재하는지 확인
        cur.execute("SELECT id FROM stocks WHERE id = ?", (id,))
        result = cur.fetchone()
        
        if result:
            oreCur.execute("SELECT id FROM ore WHERE id = ?",(id,))
            oreResult = oreCur.fetchone()
            if oreResult:
                await interaction.response.send_message(f"이미 회원가입된 아이디입니다.")
            else:
                oreCur.execute(f"INSERT INTO ore VALUES ('{id}','normal', 0, 0, 0, 0, 0, 0)")
                oreDB.commit()
                await interaction.response.send_message(f"이미 회원가입된 아이디입니다.")

        else:
            # 신규 회원인 경우만 stocks와 fish 테이블에 추가
            cur.execute(f"INSERT INTO stocks VALUES ('{id}', 'adventurer', 1000, 0, 0, '{name}', 0, 'nomal')")
            fishCur.execute(f"INSERT INTO fish VALUES ('{id}', 0, 0, 0, 0, 0, 0)")
            oreCur.execute(f"INSERT INTO ore VALUES ('{id}','normal', 0, 0, 0, 0, 0, 0)")
            db.commit()
            fishDB.commit()
            oreDB.commit()

        # ore.db에는 항상 삽입 시도
        

        await interaction.response.send_message(f"회원가입 완료 id:{id}, name:{name}")

    except sqlite3.IntegrityError as e:
        await interaction.response.send_message(f"오류 발생: {str(e)}")
    finally:
        # DB 연결 닫기
        db.close()
        fishDB.close()
        oreDB.close()
