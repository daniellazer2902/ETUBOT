
import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup
import os
import time



bot = commands.Bot(command_prefix='$')
guild = 682156076342312960




#@bot.command()
#async def text(ctx, pseudo, temps, *, reason):
#    await ctx.send(reason)

#@bot.command()
#async def ping(ctx):
#    await ctx.send(':ok_hand:')




@bot.event
async def on_ready():
    print('Je suis co !')





    starttime=time.time()
    while True:


        #================================================
        #          RECUPERATION DU DERNIER ARTICLE
        #================================================

                #============================================
                #           obtention d'un article
                #============================================

        lien = 'https://www.01net.com/actualites/applis-logiciels/'
        mon_selector = "table-cell-middle padding-inside-all"

        html = requests.get(lien)
        context = html.text
        soup = BeautifulSoup.BeautifulSoup(context, "html.parser")

        for link in soup.find_all(class_=mon_selector, limit=1):
            last_thread = link.get('href')
            #print(last_thread)

                #============================================
                #      filtrage du lien pour avoir www.*
                #============================================

        good = True
        while good == True:
            if last_thread.startswith('www.'):
                good = False

            else:
                last_thread = last_thread[1:]

        print(last_thread)

                #============================================
                #      comparaison avec l'ancien article
                #============================================


        art_r = open('./article_appli.txt', 'r')
        content = art_r.read()
        art_r.close()

        if last_thread != content:
            art_w = open('./article_appli.txt', 'w')
            art_w.write(last_thread)
            art_w.close() 
            print('Un article a ajoute')
            await bot.get_channel(687254822428475412).send('https://'+last_thread)
        else:
            print('Aucun article recent')

        time.sleep(5 - time.time() % 5)

bot.run('')



