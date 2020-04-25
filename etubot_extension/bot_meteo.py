import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup


class bot_meteo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot meteo connecte')

    @commands.command(brief="affiche la météo du jour")
    async def meteo(self, ctx):

        # recherche du code source de la météo de paris contenant les informations
        lien = "http://www.meteo-paris.com/"
        html = requests.get(lien)
        context = html.text
        soup = BeautifulSoup.BeautifulSoup(context, "html.parser")
        info = soup.select(".ac_bleu .ac_picto_ensemble")

        # initialisation du message
        embed = discord.Embed(title="ETUBOT", description="Best météo après celle de Gulli <3", color=0xeee657)
        embed.add_field(name="Date :",value= str(soup.select("#date_accueil")[1].text))

        desc = str(soup.select(".ac_com p")[0].text)
        desc = desc.replace("Ã©","é").replace("Ã¨","è").replace("Ã","à")

        embed.add_field(name="Descriptif :",value= desc)
        message = ""

        # récupération de chaque moment de la journée et le stock dans message
        for my_div in info:

            heure = my_div.select(".ac_etiquette")[0].text

            # traduction de l'utf8
            heure = heure.replace("Ã©","é").replace("Ã¨","è").replace("Ã","à")

            # suppression des espace lors des temps sinon illisible
            temp = my_div.select(".ac_temp")[0].text
            temp = "".join(temp.split())

            message += str(heure) + " - " + str(temp) + " °C\n"


        embed.add_field(name="Température :" ,value=message)

        #envoie du message
        await ctx.send(embed=embed)


        
        

def setup(bot):
    bot.add_cog(bot_meteo(bot))