import discord


async def 낚시확률(interaction: discord.Interaction):
    id = interaction.user.id
    embed = discord.Embed(
        title=f"낚시 확률표",
        color=discord.Color.green())
    embed.add_field(name="보통 낚싯대", value=f"[일반]고등어 30%\n[일반]대구 70%", inline=False)
    await interaction.response.send_message(embed=embed)


낚시확률.description = "확률조작"