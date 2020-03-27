import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup
import time
from tinydb import TinyDB, Query


#bot = commands.Bot(command_prefix='$')
guild = 682156076342312960
db_art = TinyDB('db_art.json')


class bot_daniel(commands.Cog):
        def __init__(self, bot):
                self.bot = bot

        #============================================
        #                COMMANDES
        #============================================

        @commands.command()
        async def addnews(ctx, user_link, user_selector):
                #db.insert({'link': user_link, 'selector': user_selector, 'history': ''})
                print(user_link + '  ' + user_selector)
                await ctx.send('Vous venez de vous abonner à ce fil d\'actualité')


        @commands.command()
        async def ping(self, ctx):
            await ctx.send(':ok_hand:')


        #============================================
        #           A LA CONNEXION DU BOT
        #============================================


        @commands.Cog.listener()
        async def on_ready(self):
            print('Je suis co !')

            time.time()
            #putain de boucle infini DANIELLLL !!!
            while False:


            #================================================
            #          RECUPERATION DU DERNIER ARTICLE
            #================================================
                articles = db_art.all()
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
                        db_art.write_back(articles)
                        await ctx.send('https://'+resultat)


                time.sleep(5 - time.time() % 5)


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








def setup(bot):
        bot.add_cog(bot_daniel(bot))

#bot.run("Njg5NzgxNDU2ODk3MzEwODc4.XnjCcw.F8QKNou37q6b-1IbbQsnkUa8GN0")
