
import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup



bot = commands.Bot(command_prefix='$')
guild = 682156076342312960



@bot.event
async def on_ready():
    print('Je suis co !')

#@bot.command()
#async def text(ctx, pseudo, temps, *, reason):
#    await ctx.send(reason)

#@bot.command()
#async def ping(ctx):
#    await ctx.send(':ok_hand:')



    
html = requests.get('https://overwatch.judgehype.com/')
context = html.text
soup = BeautifulSoup.BeautifulSoup(context, "html.parser")

for link in soup.find_all(class_="gallerynobind", limit=1):
    last_thread = link.get('href')
print(last_thread)

bot.run('Njg0NzYxOTE1NTg2OTA0MDg1.XmfVVg.AU94SP045cs02ibx50vB3G6IbWc')



