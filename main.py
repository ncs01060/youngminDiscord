import discord
import os
import importlib.util
import inspect
import asyncio
import types
import sqlite3
from dotenv import load_dotenv

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# 명령어를 로드하는 함수
def load_commands():
    commands_dir = "./commands"  # 명령어 파일이 있는 최상위 폴더

    for root, dirs, files in os.walk(commands_dir):  # 재귀적으로 하위 폴더까지 탐색
        for filename in files:
            if filename.endswith(".py"):  # 파이썬 파일만 로드
                module_name = filename[:-3]  # .py를 제외한 파일 이름
                module_path = os.path.join(root, filename)

                # 동적으로 모듈을 로드
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 각 모듈에 있는 명령어 함수들을 가져와 tree.command로 등록
                for attribute_name in dir(module):
                    if attribute_name.startswith("__") and attribute_name.endswith("__"):
                        continue

                    attribute = getattr(module, attribute_name)

                    # 비동기 함수 필터링
                    if isinstance(attribute, types.FunctionType) and inspect.iscoroutinefunction(attribute):
                        description = getattr(attribute, 'description', "설명이 없습니다")
                        command_name = attribute_name
                        
                        tree.command(name=command_name, description=description)(attribute)
                        print(f"명령어 {command_name}가 등록되었습니다. 설명: {description}")


async def send_announcements():
    await client.wait_until_ready()
    
    while not client.is_closed():
        conn = sqlite3.connect('db/announcement.db')
        cur = conn.cursor()
        
        # 데이터베이스에서 모든 서버의 공지 채널을 가져옴
        cur.execute("SELECT guild_id, channel_id FROM guild_settings")
        results = cur.fetchall()
        conn.close()
        
        for guild_id, channel_id in results:
            guild = client.get_guild(guild_id)
            if guild:
                channel = guild.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send("🔔 UpdateLog\n1.이제 낚시를 할 때 5초의 쿨타임이 생깁니다!\n2.이제 광질이 생겼습니다 마음껏 팔아보세요!!\n3.업데이트가 적용 된 뒤 회원가입을 다시 한 번 하셔야합니다!! 데이터는 안 날아가니 안심하세요!")
                        print(f"Sent announcement to {guild.name} in {channel.name}")
                    except Exception as e:
                        print(f"Failed to send message to {guild.name}: {e}")
        
        # 30분 대기
        await asyncio.sleep(1800)

# 봇 준비 완료 이벤트
@client.event
async def on_ready():
    print(f'{client.user}로 로그인했습니다.')
    load_commands()
    client.loop.create_task(send_announcements())
    await tree.sync()
    print("명령어가 동기화되었습니다.")


load_dotenv()

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
