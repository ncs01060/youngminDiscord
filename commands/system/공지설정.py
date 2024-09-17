import discord
import sqlite3

async def 공지채널설정(ctx:discord.Interaction, channel: discord.TextChannel):
    guild_id = ctx.guild.id
    channel_id = channel.id
    
    # 데이터베이스에 채널 ID 저장
    conn = sqlite3.connect('db/announcement.db')
    cur = conn.cursor()
    cur.execute("REPLACE INTO guild_settings (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
    conn.commit()
    conn.close()
    
    await ctx.response.send_message(f"공지 채널이 {channel.mention}으로 설정되었습니다.")