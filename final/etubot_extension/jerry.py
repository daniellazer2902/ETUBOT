import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup
import time
from tinydb import TinyDB, Query


bot = commands.Bot(command_prefix='$')
guild = 682156076342312960
db = TinyDB('db_art.json')



#============================================
#                COMMANDES
#============================================

@bot.command()
async def addnews(ctx, user_link, user_selector):
        #db.insert({'link': user_link, 'selector': user_selector, 'history': ''})
        print(user_link + '  ' + user_selector)
        await ctx.send('Vous venez de vous abonner à ce fil d\'actualité')


@bot.command()
async def ping(ctx):
    await ctx.send(':ok_hand:')


#============================================
#                FONCTIONS
#============================================


def traitement(lien, mon_selector, history):

    #============================================
    #           obtention d'un article
    #============================================

    html = requests.get(lien)
    context = html.text
    soup = BeautifulSoup.BeautifulSoup(context, "html.parser")

    for link in soup.find_all(class_=mon_selector, limit=1):
        last_thread = link.get('href')



        #============================================
        #      filtrage du lien pour avoir www.*
        #============================================

        good = True
        while good == True:
            if last_thread.startswith('www.'):
                good = False

            else:
                last_thread = last_thread[1:]


        #============================================
        #      comparaison avec l'ancien article
        #============================================

        if last_thread != history:
            print('Un article a ajoute')
            print(last_thread)
            return last_thread
        else:
            #print('Aucun article recent')
            return "none"







#============================================
#           A LA CONNEXION DU BOT
#============================================


@bot.event
async def on_ready():
    print('Je suis co !')

    time.time()
    while True:


    #================================================
    #          RECUPERATION DU DERNIER ARTICLE
    #================================================
        articles = db.all()
        for my_article in articles:

            lien = my_article.get('link')
            mon_selector = my_article.get('selector')
            history = my_article.get('history')


            #============================================
            #           On envoie en traitement 
            # -> on recupere un BOOL
            # si vrai alors on actualise l'historique
            # puis on envoie le message dans le channel
            #============================================

            resultat = traitement(lien, mon_selector, history)
            
            if resultat != "none":
                my_article['history'] = resultat
                db.write_back(articles)
                await bot.get_channel(687254822428475412).send('https://'+resultat)


        time.sleep(5 - time.time() % 5)
