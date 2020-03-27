import discord
from discord.ext import commands
import datetime
from datetime import timedelta
import json
import requests

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print('Bot readax')

chn_id =682156076342312960

@bot.command()
async def edt(ctx,arg=0):
    await ctx.send("Voici, votre emploi du temps de la journée:", emploi_du_temps_list[0].list[1])
    
def recup_message_edt(self, jour, ref_firstName, ref_lastName):
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
        if jour == 'ojd':
            jour=liste[int(my_date.weekday())]
        
        if jour == 'demain':
            jour=liste[int(my_date.weekday())+1]
        
        
        message = ""
        
        for semaine in json_data['week'][jour]:
            message += "De "+semaine["start"]+" à "+semaine["end"]+" : \t\t"+semaine["subject"]+" en **"+semaine["room"]+ "**\n"
        return message

if __name__ == "__main__":

    message = recup_message_edt('','vendredi','olivier','tanguy')
    print(message)

print("--------------------------------------\n")

my_date = datetime.datetime.now()
print(my_date)
print("--------------------------------------\n")

my_delta = timedelta(hours= 1)
new_date = my_date - my_delta
print(new_date)  


bot.run('token')
