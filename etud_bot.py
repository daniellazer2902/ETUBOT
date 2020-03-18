import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'etubot_extension.{extension}')
    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'etubot_extension.{extension}')
    
for filename in os.listdir('./etubot_extension'):
    if filename.endswith('.py'):
        bot.load_extension(f'etubot_extension.{filename[:-3]}')


bot.run("Njg5NzgxNDU2ODk3MzEwODc4.XnH3nw.A1YG4a7xiFYfNeNziSYwf67tHuk")
