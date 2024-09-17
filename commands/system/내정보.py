import discord
import api

async def 내정보(interaction: discord.Interaction):
    
    id = interaction.user.id
    name = interaction.user.name
    
    # 프로필 사진 URL 가져오기
    profile = interaction.user.avatar.url if interaction.user.avatar else "https://cdn.discordapp.com/embed/avatars/0.png"
    
    # 데이터베이스에서 정보 가져오기
    price = api.select_price(id)
    level = api.select_Level(id)
    exp = api.select_Exp(id)
    
    # Embed 메시지 생성
    embed = discord.Embed(
        title=f"{name}님의 정보",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=profile)
    embed.add_field(name="돈", value=f"돈 : {price}", inline=False)
    embed.add_field(name="레벨 / exp", value=f"레벨 : {level} | 경험치 : {exp}", inline=False)
    
    # 메시지 전송
    await interaction.response.send_message(embed=embed)
