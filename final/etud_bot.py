import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'etubot_extension.{extension}')
    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'etubot_extension.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'etubot_extension.{extension}')
    bot.load_extension(f'etubot_extension.{extension}')

if __name__ == "__main__":
    
    for filename in os.listdir('./etubot_extension'):
        if filename.endswith('.py'):
            bot.load_extension(f'etubot_extension.{filename[:-3]}')


bot.run("")
#bot.run("NjgyMjIxNDAxOTE0MzQzNDQ0.Xm9YHQ.PxYpZyCm7-EsQ_sHXGmBqsxjtvA")
