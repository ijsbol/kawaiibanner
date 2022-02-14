import discord
import asyncio

from discord.ext import commands

botID = "your token here"
bot_status = "kb!info"
prefix = "kb!"

bot = commands.Bot(command_prefix = prefix, help_command=None, status=discord.Status.online, activity=discord.Game(bot_status)) # Initialising a Bot instance as "bot"

@bot.event
async def on_ready():
    print("Ready...") 

@bot.command()
async def info(ctx):
    await ctx.author.send("**This is the only command.**\n> This bot was made by `Scrumpy#0001`.\nIt automatically bans people across servers who are known raiders.\n**This is a selfhosted version, contact your local server owner for anything else.**")
    await ctx.send("Sent you a DM.")


async def ban_member(_id: int, guild, reason: str):
    try:
        await guild.ban(_id, reason=reason)
    except:
        pass


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, members: commands.Greedy[discord.Member], reason: str="KawaiiBanner Raid Prevention: Made a mistake."):
    await ctx.send(f"UNRIP **{len(members)}** users.")
    for member in members:
        bot.bans.remove(member.id)
        for guild in bot.guilds:
            try:
                await guild.unban(user=member.id, reason=reason)
            except:
                pass
    await ctx.send(f"Unbanned all of the **{len(members)}** users.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, members: commands.Greedy[discord.Member], reason: str="KawaiiBanner Raid Prevention: User is a known server-raider."):
    await ctx.send(f"RIP **{len(members)}** people.")

    ban_futures = [ban_member(member.id, guild, reason) for member in members for guild in bot.guilds]
    await asyncio.gather(ban_futures)
    await ctx.send(f"Banned all of the **{len(members)}** people.")

@bot.event
async def on_member_join(member):
    """Auto-Ban a member if they are in the ban list, when they join a server."""
    if member.id not in bot.bans:
        return

    try:
        await member.guild.ban(user=member, reason="KawaiiBanner Raid Prevention: User is a known server-raider.")
    except:
        pass

@bot.event
async def on_guild_join(guild):
    """Ban all members who are in the ban list when the bot joins a server."""
    ban_futures = [ban_member(member_id, guild, "KawaiiBanner Raid Prevention: User is a known server-raider.") for member_id in bot.bans if member_id in {m.id for m in guild.members}]
    await asyncio.gather(*ban_futures)


bot.bans = []
bot.run(botID)
