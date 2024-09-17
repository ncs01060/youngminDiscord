import discord
from discord.ui import Button, View
import api
from enum import Enum

class Select_fish(Enum):
    고등어 = "mackerel"
    대구 = "cod"

class FishShopView(View):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="고등어 팔기", style=discord.ButtonStyle.primary, custom_id="sell_mackerel")
    async def sell_mackerel(self, interaction: discord.Interaction, button: Button):
        await self.handle_fish_sale(interaction, "mackerel")

    @discord.ui.button(label="대구 팔기", style=discord.ButtonStyle.primary, custom_id="sell_cod")
    async def sell_cod(self, interaction: discord.Interaction, button: Button):
        await self.handle_fish_sale(interaction, "cod")

    async def handle_fish_sale(self, interaction: discord.Interaction, fish: str):
        price = api.select_price(self.user_id)
        if fish == "cod":
            cod = api.select_cod(self.user_id)
            money = int(cod) * 10
            api.update_price(self.user_id, price + money)
            api.update_fish(self.user_id, "cod", 0)
            embed = discord.Embed(title="상점", color=discord.Color.green())
            embed.add_field(name=f"+{money}원", value="대구를 다 팔았습니다!", inline=False)
        elif fish == "mackerel":
            mackerel = api.select_mackerel(self.user_id)
            money = int(mackerel) * 15
            api.update_price(self.user_id, price + money)
            api.update_fish(self.user_id, "mackerel", 0)
            embed = discord.Embed(title="상점", color=discord.Color.green())
            embed.add_field(name=f"+{money}원", value="고등어를 다 팔았습니다!", inline=False)

        await interaction.response.edit_message(embed=embed, view=None)


class OreShopView(View):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="돌 팔기", style=discord.ButtonStyle.primary, custom_id="sell_stone")
    async def sell_stone(self, interaction: discord.Interaction, button: Button):
        await self.sell_ore(interaction, "stone")

    @discord.ui.button(label="철 팔기", style=discord.ButtonStyle.primary, custom_id="sell_iron")
    async def sell_iron(self, interaction: discord.Interaction, button: Button):
        await self.sell_ore(interaction, "iron")

    @discord.ui.button(label="석탄 팔기", style=discord.ButtonStyle.primary, custom_id="sell_coal")
    async def sell_coal(self, interaction: discord.Interaction, button: Button):
        await self.sell_ore(interaction, "coal")

    async def sell_ore(self, interaction: discord.Interaction, ore: str):
        ore_p = {"stone": 10, "iron": 100, "coal": 50}
        price = api.select_price(self.user_id)
        ore_full = api.select_ore(self.user_id, ore)
        sell_price = ore_p.get(ore, 0)
        money = int(ore_full) * sell_price
        api.update_price(self.user_id, price + money)
        api.update_ore(self.user_id, ore, 0)
        embed = discord.Embed(title="상점", color=discord.Color.green())
        embed.add_field(name=f"+{money}원", value=f"{ore}을 다 팔았습니다!", inline=False)

        await interaction.response.edit_message(embed=embed, view=None)

class SelectView(View):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
    
    @discord.ui.button(label="팔기", style=discord.ButtonStyle.danger, custom_id="select_sell")
    async def select_sell(self, interaction: discord.Interaction, button: Button):
        view = MainShopView(self.user_id)
        embed = discord.Embed(title="상점", color=discord.Color.green())
        embed.add_field(name="무엇을 파시겠습니까?", value="광물 또는 물고기를 선택하세요.", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="사기", style=discord.ButtonStyle.success, custom_id="select_buy")
    async def select_buy(self, interaction: discord.Interaction, button: Button):
        view = BuyShopView(self.user_id)
        embed = discord.Embed(title="상점", color=discord.Color.green())
        embed.add_field(name="무엇을 사시겠습니까?", value="아무거나 사세요!", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class BuyShopView(View):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
    
    @discord.ui.button(label="아무거나 사기", style=discord.ButtonStyle.success, custom_id="buy_test")
    async def buy_item_button(self, interaction: discord.Interaction, button: Button):
        await self.buy_item(interaction)
    
    async def buy_item(self, interaction: discord.Interaction):
        await interaction.response.send_message("테스트중입니다.")

class MainShopView(View):
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="광물 팔기", style=discord.ButtonStyle.primary, custom_id="select_ore")
    async def select_ore(self, interaction: discord.Interaction, button: Button):
        view = OreShopView(self.user_id)
        embed = discord.Embed(title="광물 상점", color=discord.Color.green())
        embed.add_field(name="광물을 팔 수 있습니다.", value="돌, 철, 석탄 등을 판매하세요.", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="물고기 팔기", style=discord.ButtonStyle.primary, custom_id="select_fish")
    async def select_fish(self, interaction: discord.Interaction, button: Button):
        view = FishShopView(self.user_id)
        embed = discord.Embed(title="물고기 상점", color=discord.Color.green())
        embed.add_field(name="물고기를 팔 수 있습니다.", value="고등어, 대구 등을 판매하세요.", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

async def 상점(interaction: discord.Interaction):
    user_id = interaction.user.id
    embed = discord.Embed(title="상점", color=discord.Color.green())
    embed.add_field(name="무엇을 하시겠습니까?", value="사기 혹은 팔기를 선택하세요!", inline=False)

    view = SelectView(user_id)
    await interaction.response.send_message(embed=embed, view=view)

상점.description = "상점"
