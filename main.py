import json
import random
import discord
from discord import *
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import *
from discord import *
import time
import datetime
import asyncio
from discord.ext import tasks

botID = "TOKEN HERE OK?"

bot_status = "kb!info"

prefix = "kb!"

Client = discord.Client() # Setting up "Client"
bot = commands.Bot(command_prefix = prefix) # Initialising "Client" as "bot"

bot.remove_command("help")

@bot.event
async def on_ready():
      print("Ready...")
      game = discord.Game(bot_status)
      changeStatus = await bot.change_presence(status=discord.Status.online, activity=game)
      bot.bans = []

@bot.command()
async def info(ctx):
      await ctx.send("Sending...")
      await ctx.author.send("**This is the only command.**\n> This bot was made by `Megumin#1234`.\nIt automatically bans people across servers who are known raiders.\n**This is a selfhosted version, contact your local server owner for anything else.**")

@commands.has_permissions(administrator=True)
@bot.command()
async def unban(ctx, *, members):
      members = members.split(" ")
      await ctx.send("UNRIP **%s** users." % (len(members)))
      for id_ in members:
            for guild in bot.guilds:
                  try:
                        await guild.unban(user=discord.Object(id=id_), reason="KawaiiBanner Raid Prevention: Made a mistake.")
                  except:
                        pass
      await ctx.send("Unbanned all of the **%s** users." % (len(members)))

@commands.has_permissions(administrator=True)
@bot.command()
async def ban(ctx, *, members):
      members = members.split(" ")
      await ctx.send("RIP **%s** people." % (len(members)))
      for id_ in members:
            for guild in bot.guilds:
                  try:
                        bot.bans.append(int(id_))
                  except:
                        pass
      await ctx.send("Banned all of the **%s** people." % (len(members)))

@bot.event
async def on_member_ban(guild, member):
      if member.id in bot.bans:
            pass
      else:
            bot.bans.append(member.id)
            for guild_ in bot.guilds:
                  if guild_ == guild:
                        pass
                  else:
                        try:
                              await guild_.ban(user=member, reason="KawaiiBanner Raid Prevention: User has been approved as a known server-raider.")
                        except:
                              pass
bot.run(botID)
