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
        
    print(url)

    requete = requests.get(url)
        
    data =requete.content
        
    json_data=json.loads(data)

    print("json_data : "+str(json_data))
        
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

    if 14 < my_date.hour < 18:
        heure_actuelle = "16:00" 

    if my_date.hour >= 19:
        heure_actuelle = "09:00" 

    for semaine in json_data['week'][jour]:
        if semaine["start"] == heure_actuelle:
            message += "De "+semaine["start"]+" à "+semaine["end"]+" : \t\t"+ semaine["subject"]+" en **" + semaine["room"]+ "**\n"
    print("message : "+str(message))

    if not message:
        message="la journée est terminée"

    return message


class my_bot (commands.Cog):

    def __init__(self,bot):
        self.bot=bot



    @commands.command(brief="Envoyer l'emploi du temps sur le tchat")
    async def rappel(self,ctx, jour):
        message = recup_message_edt(jour,"olivier","tanguy")
        print("message : "+message)
        await ctx.send(message)



    @commands.command(brief="Envoyer l'emploi du temps en DM à l auteur")
    async def mon_rappel(self,ctx, jour):
        message = recup_message_edt(jour,"olivier","tanguy")
        await ctx.author.send(message)    
     

    @commands.command(brief="Envoyer l'emploi du temps en DM à l ou plusieurs membres ")
    async def mes_rappels(self,ctx,jour, destinataire):

        message = recup_message_edt(jour,"olivier","tanguy")    
    
        # cherche si l'utisateur rentré existe ou non
        # si oui, lui envoie un mp avec les salles
        # si non, message erreur

        if destinataire == "all" :
            print("à tous")

            for member in ctx.guild.members:
                await member.send(message)


        else:
            verif = True
            for member in ctx.guild.members:

                if member.display_name == destinataire:
                    await member.send(message)
                    verif = False
                    break

                elif member.name == destinataire:
                    await member.send(message)
                    verif = False
                    break

            if verif:
                await ctx.send(message)



def setup (bot):
    bot.add_cog(my_bot(bot))
