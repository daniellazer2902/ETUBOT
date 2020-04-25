import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.command(brief="load extension | charge une extension")
async def load(ctx, extension):
    bot.load_extension(f'etubot_extension.{extension}')
    
@bot.command(brief="unload extension | décharge une extension")
async def unload(ctx, extension):
    bot.unload_extension(f'etubot_extension.{extension}')

@bot.command(brief="reload extension | recharge une extension")
async def reload(ctx, extension):
    bot.unload_extension(f'etubot_extension.{extension}')
    bot.load_extension(f'etubot_extension.{extension}')

if __name__ == "__main__":
    
    for filename in os.listdir('./etubot_extension'):
        if filename.endswith('.py'):
            bot.load_extension(f'etubot_extension.{filename[:-3]}')


bot.run("")