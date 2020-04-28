#réalisé par Marine RICO, Olivier TANGUY, Daniel GAVRILINE, Hugo CABARET

import discord
from discord.ext import commands
import json
import requests
import bs4 as BeautifulSoup


class bot_df(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot df connecte')

    @commands.command(pass_context=True, brief="df ordinateur ")
    async def df(self, ctx, mot):

        # récupération du code source en fonction du mot
        lien = "https://www.larousse.fr/dictionnaires/francais/" + mot
        html = requests.get(lien)
        context = html.text
        soup = BeautifulSoup.BeautifulSoup(context, "html.parser")

        # test pour savoir si on parvient à récupérer la définition de la page
        # si oui, alors on envoie le message avec la définition obtenu
        # si non, alors on a une erreur d'index et donc on liste les suggestions proposé par le site
        try:
            if soup.select(".Definitions")[0].text:

                # récupération des différentes donnés utiles
                definition = soup.select(".Definitions")[0].text
                mot =  soup.select(".AdresseDefinition")[0].text
                mot = mot[1:]
                author = ctx.message.author

                # préparation du message de réponse 
                embed = discord.Embed(title="ETUBOT", description="Les définitions les plus sûre de ta région", color=0xeee657)
                embed.add_field(name="Mot :",value=mot)
                embed.add_field(name="Définition :",value=definition)
                embed.add_field(name="Par :",value=author)
                await ctx.send(embed=embed)

        except IndexError:

            # préparation du message avec toute les suggestions ressemblante à notre requête
            message = "__Vouliez vous plutot chercher __ :\n"
            for proposition in soup.select(".corrector ul li"):
                message += "**°** " + proposition.text + "\n"

            await ctx.send(message)

def setup(bot):
    bot.add_cog(bot_df(bot))
