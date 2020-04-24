import discord
from discord.ext import commands
import datetime
from datetime import timedelta
import json
import requests

client = discord.Client()

#recuperer l'emploi du temps du prochain cours
def recup_message_edt(jour, ref_firstName, ref_lastName):
    liste = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    my_date = datetime.datetime.now()
    url = "https://api-calendar.calendz.app/v1/week/"

    #on rajoute le mois
    if my_date.month<10:
        url +="0"
        
    url += str(my_date.month)
        
    url += "-"
    #si on est le week-end on rajoute deux jours pour passer a la semaine suivante
    if my_date.weekday==5 or my_date.weekday==6:
        my_date.day = my_date.day+2
        
    if my_date.day<10:
        url +="0"
        
    #on rajoute le jour
    url += str(my_date.day)
    url +="-20?token=imasecret&firstname=" + ref_firstName + "&lastname=" + ref_lastName
        
    requete = requests.get(url)
        
    data =requete.content
        
    json_data=json.loads(data)
        
    #remplacer le nombre par le jour
    if jour == 'ajd':
        jour=liste[int(my_date.weekday())]
        
    if jour == 'demain':
        jour=liste[int(my_date.weekday())+1]

    message = ""
    heure_actuelle = ""

    if my_date.hour < 9:
        heure_actuelle = "09:00" 

    if 9 < my_date.hour < 11:
        heure_actuelle = "11:00"

    if 11 < my_date.hour < 14:
        heure_actuelle = "14:00" 

    if 14 < my_date.hour < 16:
        heure_actuelle = "16:00" 

    if my_date.hour >= 17:
        heure_actuelle = "09:00" 

    for semaine in json_data['week'][jour]:
        if semaine["start"] == heure_actuelle:
            message += "De "+semaine["start"]+" à "+semaine["end"]+" : \t\t"+ semaine["subject"]+" en **" + semaine["room"]+ "**\n"
    return message

class my_bot (commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.command("Envoyer l'emploi du temps sur le tchat")
    async def edt(self,ctx):
        message = recup_message_edt("jeudi","olivier","tanguy")
        print(message)
        await ctx.send(message)

    @commands.command("Envoyer l'emploi du temps en DM à l auteur")
    async def mon_edt(self,ctx):
        message = recup_message_edt("jeudi","olivier","tanguy")
        await ctx.author.send(message)    
     
    @commands.command("Envoyer l'emploi du temps en DM à l ou plusieurs membres ")
    async def my_edt(self,ctx,message):
            message = recup_message_edt("jeudi","olivier","tanguy")    
            name=message.content.split(" ")[1]
            
            if (name == "all"):
                for member in message.guild.members:
                    await member.send(message)

            else:
                member= discord.utils.get(message.guild.members, name=name)
                await member.send(message)

def setup (bot):
    bot.add_cog(my_bot(bot))
