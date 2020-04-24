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
        message = " ```La météo de Daniel du " + str(soup.select("#date_accueil")[1].text) + "\n\n"
        message += str(soup.select(".ac_com p")[0].text) + "\n\n"


        # récupération de chaque moment de la journée et le stock dans message
        for my_div in info:

            heure = my_div.select(".ac_etiquette")[0].text
            temp = my_div.select(".ac_temp")[0].text
            temp = "".join(temp.split())

            message += str(heure) + " - " + str(temp) + "\n"

        # traduction de l'utf8 + envoie du message 
        message += "\nRisque de pluie - " + soup.select(".pourcent")[0].text
        message += "```"
        message = message.replace("Ã©","é").replace("Ã¨","è").replace("Ã","à")

        await ctx.send(message)

def setup(bot):
    bot.add_cog(bot_meteo(bot))