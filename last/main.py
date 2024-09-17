import discord
import discord.ext
import sqlite3
import api
import random
import asyncio
from enum import Enum

class Select_fish(Enum):
  고등어="mackerel"
  대구="cod"

# setting up the bot
intents = discord.Intents.all() 
# if you don't want all intents you can do discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

db = sqlite3.connect("youngmin.db")
fishDB = sqlite3.connect("fish.db")
cur = db.cursor()
fishCur = fishDB.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS stocks
            (id text PRIMARY KEY,job text, price real, exp real,name text, playtime real,
             fishingrod text)''')

fishCur.execute('''CREATE TABLE IF NOT EXISTS fish
                (id text PRIMARY KEY,mackerel real,cod real,shrimp real,salmon real,yeti real,mommoss real)''')


# sync the slash command to your server
@client.event
async def on_ready():
    await tree.sync()
    # print "ready" in the console when the bot is ready to work
    print("ready")

# make the slash command
@tree.command(name="회원가입", description="회원가입")
async def slash_command(interaction: discord.Interaction):
    id = interaction.user.id
    name = interaction.user.name
    db = sqlite3.connect("youngmin.db")
    cur = db.cursor()
    try:
        cur.execute(f"INSERT INTO stocks VALUES ('{id}','adventurer',1000,0,'{name}',0,'nomal')")
        fishCur.execute(f"INSERT INTO fish VALUES ('{id}',0,0,0,0,0,0)")
        db.commit()
        fishDB.commit()
    except sqlite3.IntegrityError:
        await interaction.response.send_message(f"이미 회원가입된 아이디입니다")
    await interaction.response.send_message(f"회원가입 완료 id:{id}")

@tree.command(name="도박", description="도박하기")
async def dobak(interaction: discord.Interaction,money:int):
    id = interaction.user.id
    price = api.select_price(id)
    if money <= int(price):
        if random.randrange(1,100) >= 50:
            update_price = price + money*2
            cur.execute('UPDATE stocks SET price = ? WHERE id = ?', (update_price, id))
            db.commit()
            await interaction.response.send_message(f"도박에 성공하여 2배로 돈을 받습니다!\n가진 돈 : {update_price}")
        else:
            update_price = price-money
            cur.execute('UPDATE stocks SET price = ? WHERE id = ?', (update_price, id))
            db.commit()
            await interaction.response.send_message(f"도박에 실패하여 가진 돈을 잃었습니다!\n가진 돈 : {update_price}")
    else:
        await interaction.response.send_message(f"도박에 필요한 돈이 부족합니다!!")


@tree.command(name="돈", description="가진 돈을 봅니다")
async def show_money(interaction: discord.Interaction):
    id = interaction.user.id
    k = api.select_price(id)
    await interaction.response.send_message(f"가진 돈 : {k}")


@tree.command(name="낚시", description="낚시를 합니다")
async def show_money(interaction: discord.Interaction):
    id = interaction.user.id
    name = interaction.user.name
    k = api.select_Rod(id)
    await interaction.response.send_message(f"가지고 있는 낚싯대 : {k[0]}")
    await interaction.channel.send(f"낚시중....")
    await asyncio.sleep(2)
    
    if k[1] == 1:
        fish = ['[일반]고등어','[일반]대구']
        if random.randrange(1,10) < 3:
            result = fish[1]
            cod_fish = api.select_cod(id)
            api.update_fish(id,"cod",cod_fish+1)
            img_url = "https://i.ibb.co/tmn9YRv/Raw-Cod.webp"
        else:
            makerel = api.select_mackerel(id)
            api.update_fish(id,"mackerel",makerel+1)
            img_url = "https://i.ibb.co/tmn9YRv/Raw-Cod.webp"
            result = fish[0]

    embed = discord.Embed(
        title=f"{name}님의 낚시",
        color=discord.Color.green())
    embed.set_thumbnail(url=img_url)
    embed.add_field(name="결과", value=f"🐠{result}를 잡았습니다!!", inline=False)
    await interaction.followup.send(embed=embed)


@tree.command(name="낚시확률", description="낚시 확률을 표시합니다")
async def show_money(interaction: discord.Interaction):
    id = interaction.user.id
    embed = discord.Embed(
        title=f"낚시 확률표",
        color=discord.Color.green())
    embed.add_field(name="보통 낚싯대", value=f"[일반]고등어 30%\n[일반]대구 70%", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="낚시보관함", description="보관함을 엽니다")
async def show_money(interaction: discord.Interaction):
    id = interaction.user.id
    makerel = api.select_mackerel(id)
    cod = api.select_cod(id)
    embed = discord.Embed(
        title=f"낚시 확률표",
        color=discord.Color.green())
    embed.add_field(name="보관함", value=f"[일반]고등어 {makerel}마리\n[일반]대구 {cod}마리", inline=False)
    await interaction.response.send_message(embed=embed)

#상점
@tree.command(name="상점", description="보관함을 엽니다")
async def show_money(interaction: discord.Interaction,물고기:Select_fish):
    id = interaction.user.id
    fish = 물고기.value
    price = api.select_price(id)
    if fish == "cod":
        cod = api.select_cod(id)
        money = int(cod) * 10
        api.update_price(id,price+money)
        api.update_fish(id,"cod",0)
        embed = discord.Embed(title=f"상점",color=discord.Color.green())
        embed.add_field(name=f"+{money}원", value=f"대구를 다 팔았습니다!", inline=False)
        await interaction.response.send_message(embed=embed)
    elif fish == "mackerel":
        makerel = api.select_mackerel(id)
        money = int(makerel) * 15
        api.update_price(id,price+money)
        api.update_fish(id,"mackerel",0)
        fishDB.commit()
        embed = discord.Embed(title=f"상점",color=discord.Color.green())
        embed.add_field(name=f"+{money}원", value=f"고등어를 다 팔았습니다!", inline=False)
        await interaction.response.send_message(embed=embed)
