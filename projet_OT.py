import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print('Bot readax')

@bot.command()
async def bonjour(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def edt(ctx,member= discord.Member,*):
    await ctx.send("Bonjour {member}, je vous envoie votre emploi du temps de la semaine")

bot.run('Njg0NzYxNjQyNzYwMDExODA3.Xl-0OQ.Dky5L4TMoRbn8qSp0wY3wi3GT4I')
