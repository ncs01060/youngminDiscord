import discord
import api
import random



async def 도박(interaction: discord.Interaction, money: int):
    id = interaction.user.id
    price = api.select_price(id)
    if money <= int(price) and money >= 0:
        if random.randrange(1, 100) >= 50:
            update_price = price + money * 2
            api.update_price(id,update_price)
            await interaction.response.send_message(f"도박에 성공하여 2배로 돈을 받습니다!\n가진 돈 : {update_price}")
        else:
            update_price = price - money
            api.update_price(id,update_price)
            await interaction.response.send_message(f"도박에 실패하여 가진 돈을 잃었습니다!\n가진 돈 : {update_price}")
    else:
        await interaction.response.send_message(f"도박에 필요한 돈이 부족합니다!!")

도박.description = "인생은 한 방"