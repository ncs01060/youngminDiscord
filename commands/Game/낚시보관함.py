import discord
import api

async def 낚시보관함(interaction: discord.Interaction):
    id = interaction.user.id
    makerel = api.select_mackerel(id)
    cod = api.select_cod(id)
    embed = discord.Embed(
        title=f"낚시 보관함",
        color=discord.Color.green())
    embed.add_field(name="보관함", value=f"[일반]고등어 {makerel}마리\n[일반]대구 {cod}마리", inline=False)
    await interaction.response.send_message(embed=embed)

낚시보관함.description = "인벤토리"