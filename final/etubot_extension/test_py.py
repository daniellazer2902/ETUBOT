import os
from discord.ext import commands
import json
import requests
import datetime
from tinydb import TinyDB, Query

# il faut penser a changer le token (dernière ligne) et le channel (ligne 13) pour faire bouger le code dans un autre bot

bot = commands.Bot(command_prefix =';')

# ici le numero du channel dans lequel le bot répond
chn_id = 684798996996423860

my_date = datetime.datetime.now()

db_ref = TinyDB("db_referent.json")

#db.insert({"channel": "1234567890", "name": "general"})

Requete = Query()
#db.update({'channel': 682221578393878561}, Requete.name == 'general')

def recup_message_edt(self, jour, ref_firstName, ref_lastName):
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


#pour faire un cog écrire les trois prochaine lignes
class bot_hugo(commands.Cog):
    
    #rajouter self aussi
    def __init__(self, client):
        self.client = client



    db_ref.search(Requete.name == "general")

    



    
    #remplacer .event par .Cog.listener
    @commands.Cog.listener()
    async def on_ready(self):
        print("bot hugo ready!")
    
    #et enfin remplacer bot par commands
    @commands.command()
    async def id(self, ctx, nom, prenom, identifiant):
        #identifiant = str(ctx.channel.id)
        
        # on scan la DB et on stock si u channel correspond
        res_requete = db_ref.search(Requete.channel==identifiant)
        
        # on verifie si la requete a un résultat ou non
        if len(res_requete) == 0:    
            db_ref.insert({"channel": identifiant, "nom": nom, "prenom": prenom})
            await bot.get_channel(ctx.channel.id).send("nouvelle reference enregistré")
        else:
            db_ref.update({"channel": identifiant, "nom": nom, "prenom": prenom}, Requete.channel == identifiant)
            await bot.get_channel(ctx.channel.id).send("reference modifié")
    
    @commands.command()
    async def msg(self, ctx, *, message):
        await bot.get_channel(chn_id).send(message)
    
    
    @commands.command()
    async def edt(self, ctx, jour):
        liste = ["mardi", "mercredi", "jeudi", "vendredi"]
        
        print (ctx.channel.id)
        
        #on récupere l'ID référent
        req_search = db_ref.search(Requete.channel == str(ctx.channel.id))
        
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
    
    
    @commands.command()
    async def time(self, ctx):
        await bot.get_channel(chn_id).send(my_date)

#puis rajouter ca
def setup(client):
    client.add_cog(bot_hugo(client))

# ici le token du bot
#bot.run("Njg5NzgxNDU2ODk3MzEwODc4.XnjCcw.F8QKNou37q6b-1IbbQsnkUa8GN0")
