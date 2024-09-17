import discord
import api

async def 광물보관함(interaction: discord.Interaction):
    id = interaction.user.id
    iron = api.select_ore(id,'iron')
    gold = api.select_ore(id,'gold')
    coal = api.select_ore(id,'coal')
    diamond = api.select_ore(id,'diamond')
    blackstone = api.select_ore(id,'blackstone')
    stone = api.select_ore(id,'stone')

    embed = discord.Embed(
        title=f"광물 보관함",
        color=discord.Color.green())
    embed.add_field(name="[일반]", value=f"[일반]철 {iron}개\n[일반]석탄 {coal}개\n[일반]돌 {stone}개", inline=False)
    embed.add_field(name="[희귀]", value=f"[희귀]금 {gold}개\n[희귀]블랙스톤 {blackstone}개", inline=False)
    embed.add_field(name="[레전드]", value=f"[레전드]다이아몬드 {diamond}개", inline=False)
    await interaction.response.send_message(embed=embed)

광물보관함.description = "인벤토리"