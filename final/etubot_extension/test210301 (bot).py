import os
from discord.ext import commands
import json
import requests
import datetime
from tinydb import TinyDB, Query

#prochain cours que l'on demande, et un jour special

# il faut penser a changer le token (dernière ligne) et le channel (ligne 13) pour faire bouger le code dans un autre bot

bot = commands.Bot(command_prefix='.')

# ici le numero du channel dans lequel le bot répond
chn_id = 684798996996423860
my_date = datetime.datetime.now()

db = TinyDB("db_referent.json")

#db.insert({"channel": "1234567890", "name": "general"})

Requete = Query()

#db.update({'channel': 682221578393878561}, Requete.name == 'general')

db.search(Requete.name == "general")

def recup_message_edt(jour, ref_firstName, ref_lastName):
    liste = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    
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

def write_file(text, nom, lien):
	os.chdir(lien)
	fichier_a = open(nom, "a")
	fichier_a.write(text)
	fichier_a.close()

@bot.event
async def on_ready():
    print("logged in as :",bot.user.name)
    print("ID: ",bot.user.id)


@bot.command()
async def id(ctx, nom, prenom):
    identifiant = str(ctx.channel.id)
    res_requete = db.search(Requete.channel==identifiant)       # on scan la DB et on stock si u channel correspond
    if len(res_requete) == 0:     # on verifie si la requete a un résultat ou non
        db.insert({"channel": identifiant, "nom": nom, "prenom": prenom})
        await bot.get_channel(ctx.channel.id).send("nouvelle reference enregistré")
    else:
        db.update({"channel": identifiant, "nom": nom, "prenom": prenom}, Requete.channel == identifiant)
        await bot.get_channel(ctx.channel.id).send("reference modifié")

@bot.command()
async def msg(ctx, *, message):
    await bot.get_channel(chn_id).send(message)


@bot.command()
async def edt(ctx, jour):
    liste = ["mardi", "mercredi", "jeudi", "vendredi"]
    
    print (ctx.channel.id)
    
    #on récupere l'ID référent dans la DB
    req_search = db.search(Requete.channel == str(ctx.channel.id))
    
    print (req_search)
    
    ref_lastName = req_search[0]["nom"]
    
    ref_firstName = req_search[0]["prenom"]
    
    await bot.get_channel(chn_id).send("referent : "+ref_firstName + " " + ref_lastName)
    
    if jour == "semaine":
        for day_liste in liste:
            await bot.get_channel(chn_id).send(day_liste+" : ")
            message = recup_message_edt(day_liste, ref_firstName, ref_lastName)
            await bot.get_channel(chn_id).send(message)
    else:
        message = recup_message_edt(jour, ref_firstName, ref_lastName)
        await bot.get_channel(chn_id).send(message)


@bot.command()
async def time(ctx):
    await bot.get_channel(chn_id).send(my_date)

# ici le token du bot
