import discord
import api
import asyncio
import random
import time  # 시간 추적을 위해 사용

# 사용자별로 마지막 광질 시각을 저장할 사전
cooldowns = {}

async def 광질(interaction: discord.Interaction):
    id = interaction.user.id
    name = interaction.user.name
    
    # 쿨타임 설정 (초 단위)
    cooldown_time = 10

    # 현재 시간
    current_time = time.time()

    # 마지막 광질 시간 확인 및 쿨타임 체크
    if id in cooldowns:
        last_used = cooldowns[id]
        if current_time - last_used < cooldown_time:
            remaining_time = int(cooldown_time - (current_time - last_used))
            await interaction.response.send_message(f"쿨타임이 끝나지 않았습니다. {remaining_time}초 후에 다시 시도하세요.", ephemeral=True)
            return

    # 쿨타임 갱신
    cooldowns[id] = current_time

    await interaction.channel.send(f"광질 중....")
    await asyncio.sleep(2)  # 시뮬레이션을 위한 대기 시간
    
    pix = api.select_ore(id, "pic")
    ore = ["[일반]철", "[일반]돌", "[일반]석탄", "[희귀]금", "[희귀]블랙스톤", "[레전더리]다이아몬드"]
    txt = "무언가를 발견하지 못했습니다."  # 기본 텍스트
    image_url = "https://cdn.discordapp.com/embed/avatars/0.png"
    if pix == "normal":
        rnd = random.randint(0, 9)  # 0부터 9까지의 랜덤 정수 생성
        if rnd == 1:
            iron = api.select_ore(id, 'iron')
            api.update_ore(id, 'iron', iron + 1)
            txt = ore[0]  # "[일반]철"
            image_url = "https://i.ibb.co/b1HRk95/Iron-Ore-JE2-BE2.png"
        elif rnd >= 5:
            stone = api.select_ore(id, 'stone')
            api.update_ore(id, 'stone', stone + 1)
            txt = ore[1]  # "[일반]돌"
            image_url = "https://i.ibb.co/wWsfpPN/Stone.png"
        else:
            coal = api.select_ore(id, 'coal')
            api.update_ore(id, 'coal', coal + 1)
            txt = ore[2]  # "[일반]석탄"
            image_url = "https://i.ibb.co/hdZXrbq/Coal-Ore-JE5-BE4.png"
    elif pix == "rare":
        rnd = random.randint(0, 100)
        if rnd == 1:
            blackstone = api.select_ore(id, 'blackstone')
            api.update_ore(id, 'blackstone', blackstone + 1)
            txt = ore[4]  # "[희귀]블랙스톤"
        elif rnd <= 20:
            gold = api.select_ore(id, 'gold')
            api.update_ore(id, 'gold', gold + 1)
            txt = ore[3]  # "[희귀]금"
        elif rnd <= 30:
            iron = api.select_ore(id, 'iron')
            api.update_ore(id, 'iron', iron + 1)
            txt = ore[0]  # "[일반]철"
        elif rnd >= 60:
            stone = api.select_ore(id, 'stone')
            api.update_ore(id, 'stone', stone + 1)
            txt = ore[1]  # "[일반]돌"
        elif rnd >= 40:
            coal = api.select_ore(id, 'coal')
            api.update_ore(id, 'coal', coal + 1)
            txt = ore[2]  # "[일반]석탄"

    embed = discord.Embed(
        title=f"{name}님의 광질",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=image_url)
    embed.add_field(name="결과", value=f"{txt} 광석을 캤습니다.", inline=False)
    
    await interaction.response.send_message(embed=embed)

광질.description = "광질"
