import discord
from discord.ext import commands, tasks
import json
import requests
import bs4 as BeautifulSoup
import time
from tinydb import TinyDB, Query

db_art = TinyDB('db_article.json')



class bot_article(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    def cog_unload(self):
        self.update.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
            print('Bot article connecté')



    #============================================
    #                COMMANDES
    #============================================

    # permet de rajouter un abonnement et de l'insérer dans la BDD
    @commands.command(brief="addnews url \".class1 .class2\" ")
    async def addnews(self, ctx, user_link, user_selector):
        db_art.insert({'link': user_link, 'selector': user_selector, 'history': ''})
        print(user_link + '  ' + user_selector)
        await ctx.send('Vous venez de vous abonner à ce fil d\'actualité')



    # liste tout les abonnements du serveur
    @commands.command(brief="affiche tout les abonnements")
    async def listnews(self, ctx):
        i = 1
        lien = " ```Liste des articles \n"
        articles = db_art.all()

        for my_article in articles:
            lien += "Articles " + str(i) + " : " + my_article.get('link') + "\n"
            lien += "Selecteur : " + my_article.get('selector') + "\n\n"
            i += 1
        lien += "```" 
        await ctx.send(lien)



    # supprime un article de la BDD en prenant son lien
    @commands.command(brief="remnews url")
    async def remnews(self, ctx, lien):
        req = Query()
        print(lien)
        db_art.remove(req.link == lien)
        await ctx.send('Vous venez de supprimer l\'article ' + lien)



    #===========================================
    #                   LOOP
    #===========================================

    @tasks.loop(seconds=5.0)
    async def update(self):

        #===========================================
        #              LOOP - articles
        #===========================================
        
        articles = db_art.all()
        for my_article in articles:
            # {'link': user_link, 'selector': user_selector, 'history': ''}

            lien = my_article.get('link')
            mon_selector = my_article.get('selector')
            history = my_article.get('history')


            #============================================
            #           On envoie en traitement 
            # -> on recupere un BOOL
            # si vrai alors on actualise l'historique
            # puis on envoie le message dans le channel
            #============================================

            resultat = traitement_article(lien, mon_selector, history)
            
            if resultat != "none":
                my_article['history'] = resultat
                db_art.write_back(articles)
                await self.bot.get_channel(687254822428475412).send('https://'+resultat)


#============================================
#                FONCTIONS
#============================================


def traitement_article(lien, mon_selector, history):

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
    bot.add_cog(bot_article(bot))