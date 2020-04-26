import os
import discord
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

#permet de recupere l'emploi du temps et le retourne dans une phrase structuré
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

        print (url)
        
        message = ""
        
        for semaine in json_data['week'][jour]:
            message += "De "+semaine["start"]+" à "+semaine["end"]+" : \t\t"+semaine["subject"]+" en **"+semaine["room"]+ "**\n"
        return message


#pour faire un cog écrire les trois prochaine lignes
class bot_hugo(commands.Cog):
    
    #rajouter self aussi
    def __init__(self, client):
        self.client = client



    db_ref.search(Requete.name == "general")

    



    
    #remplacer .event par .Cog.listener
    @commands.Cog.listener()
    async def on_ready(self):
        print("bot edt ready!")
    
    #et enfin remplacer bot par commands
    @commands.command(brief=".id nom prenom id_du_channel")
    async def id(self, ctx, nom, prenom, identifiant):
        #identifiant = str(ctx.channel.id)
        
        # on scan la DB et on stock si u channel correspond
        res_requete = db_ref.search(Requete.channel==identifiant)
        
        # on verifie si la requete a un résultat ou non
        if len(res_requete) == 0:    
            db_ref.insert({"channel": identifiant, "nom": nom, "prenom": prenom})
            await ctx.send("nouvelle reference enregistré")
        else:
            db_ref.update({"channel": identifiant, "nom": nom, "prenom": prenom}, Requete.channel == identifiant)
            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPI", color=0xeee657)
            embed.add_field(name="cours", value="reference modifié")
            await ctx.author.send(embed = embed)
            #await ctx.send("reference modifié")

    #affiche la prochaine fois que l'on a un certain cours (ex.:python)
    @commands.command(brief="affiche le prochain cours (pour recup nom prochain cours -> .cours")
    async def prochain(self, ctx, *cours):
        date_prochain = ''
        
        #on récupere l'ID référent
        req_search = db_ref.search(Requete.channel == str(ctx.channel.id))
            
        print (req_search)
            
        ref_lastName = req_search[0]["nom"]
            
        ref_firstName = req_search[0]["prenom"]
            
        await ctx.send("referent : "+ref_firstName + " " + ref_lastName)
        
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
        
        data = requete.content
        
        json_data=json.loads(data)
        
        print (json_data)
        
        while(len(date_prochain) == 0):
            #my_date = datetime.datetime.now()
            
            for days in json_data['week']:
                for info in json_data['week'][days][0]:
                    if (json_data['week'][days][0][info] == cours):
                        date_prochain = json_data['week'][days][0]['date']
                        break
                    
        await ctx.send("le prochain cours de" + cours + "aura lieu le " + date_prochain)
        
    
    @commands.command(brief="affiche une liste de cours")
    async def cours(self, ctx):
        liste = ["PROJET INFRA", "TRE RECHERCHE STAGE", "COMMUNICATION ORALE", "METHODO", "PROJET PHYTON", "PHYTON", "PROJET MODELISATION", "SUITES ET SERIES NUM"]
        message =  ''
        for cours in liste:
            message += cours + "\n"
        await ctx.send(message)
    
    @commands.command()#renvoie simplement ce que l'utitilisateur a ecrit
    async def msg(self, ctx, *, message):
        await ctx.send(message)
    
    
    @commands.command(brief=".edt semaine/ojd/demain/mardi/mercredi/...")#envoie l'emploi du temps du jour selectionné
    async def edt(self, ctx, jour):
        liste = ["mardi", "mercredi", "jeudi", "vendredi"]
        
        print (ctx.channel.id)
        
        #on récupere l'ID référent
        req_search = db_ref.search(Requete.channel == str(ctx.channel.id))
        
        print (req_search)
        #on récupère le nom et prenom du referent
        ref_lastName = req_search[0]["nom"]
        
        ref_firstName = req_search[0]["prenom"]
        
        await ctx.send("referent : "+ref_firstName + " " + ref_lastName)

        #si l'utilisateur envoi semaine alors on montre toute la semaine
        if jour == "semaine":
            for day_liste in liste:
                message = recup_message_edt('', day_liste, ref_firstName, ref_lastName)
                embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPI", color=0xeee657)
                embed.add_field(name= day_liste, value= message)
                await ctx.author.send(embed = embed)
        #sinon on montre seulement le jour selectionné
        else:
            message = recup_message_edt('', jour, ref_firstName, ref_lastName)
            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPI", color=0xeee657)
            embed.add_field(name=jour, value= message)
            await ctx.author.send(embed = embed)
    
    #affiche l'heure
    @commands.command()
    async def time(self, ctx):
        await ctx.send(my_date)

#puis rajouter ca
def setup(client):
    client.add_cog(bot_hugo(client))

# ici le token du bot
#bot.run("Njg5NzgxNDU2ODk3MzEwODc4.XnjCcw.F8QKNou37q6b-1IbbQsnkUa8GN0")
