import discord
import api
import asyncio
import random
import time

cooldowns = {}


async def 낚시(interaction: discord.Interaction):
    id = interaction.user.id
    name = interaction.user.name

    cooldown_time = 5
    current_time = time.time()

    if id in cooldowns:
        last_used = cooldowns[id]
        if current_time - last_used < cooldown_time:
            remaining_time = int(cooldown_time - (current_time - last_used))
            await interaction.response.send_message(f"쿨타임이 끝나지 않았습니다. {remaining_time}초 후에 다시 시도하세요.", ephemeral=True)
            return

    # 쿨타임 갱신
    cooldowns[id] = current_time


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
            api.update_exp(id,1)
            api.check_levelUp(id)
        else:
            makerel = api.select_mackerel(id)
            api.update_fish(id,"mackerel",makerel+1)
            img_url = "https://i.ibb.co/tmn9YRv/Raw-Cod.webp"
            result = fish[0]
            api.update_exp(id,1)
            api.check_levelUp(id)

    embed = discord.Embed(
        title=f"{name}님의 낚시",
        color=discord.Color.green())
    embed.set_thumbnail(url=img_url)
    embed.add_field(name="결과", value=f"🐠{result}를 잡았습니다!!", inline=False)
    await interaction.followup.send(embed=embed)

낚시.description = "낚시"