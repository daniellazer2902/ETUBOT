import discord

from discord.ext import commands


from tinydb import TinyDB, Query

TOKEN = 'NjgyMTgyMTQ2ODUyNzgyMDgy.Xobi8w.1fXiAX-_B5fhTuOVEyfnk2pZuzU'

bot = commands.Bot(command_prefix =';')


db_devoir = TinyDB("db_devoir.json")
all_dev = db_devoir.all()

#db_devoir.purge()

Requete = Query()

db_devoir.update({'channel': 682221578393878561}, Requete.name == 'general')

db_devoir.search(Requete.name == "general")

#db_devoir.insert({'date': "27/05" , 'matiere': "Communication", 'devoir': "Faire un essai de 200 lignes"})
#db_devoir.insert({'date': "29/05" , 'matiere': "Logique", 'devoir': "Controle sur les probas"})

for item in db_devoir:
    print(item)


@bot.event
async def on_ready():
    print('Je suis co !') #Affiche quand le bot est co !

@bot.event
async def db_ready():
    print(db_devoir) #Affiche les données présente dans la base de donnée db_devoir

@bot.command()
async def list(ctx): 
    for dev in all_dev :
        await ctx.send(dev) #Affiche tout les devoirs présents dans la base de donnée

@bot.command()
async def search_matiere(ctx, mat_search):
    verif = False
    for dev in all_dev :
        if dev.get('matiere') == mat_search :
            verif = True

            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPSI", color=0xeee657) #Permet d'obtenir une plus belle présentation des devoirs 

            embed.add_field(name="MATIERE", value= dev.get('matiere'))

            await ctx.author.send(embed = embed)

    if verif == False :
        await ctx.send("Pas de devoirs ! Veuillez verifier l'orthographe !") #Affiche précisement les devoirs recherchés dans une matière en particulier et dis si ce n'est pas trouvable

@bot.command()
async def search_date(ctx, date_search):
    verif = False
    for dev in all_dev :
        if dev.get('date') == date_search :
            verif = True

            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPSI", color=0xeee657) #Permet d'obtenir une plus belle présentation des devoirs 

            embed.add_field(name="DATE", value=dev.get('date'))

            await ctx.author.send(embed = embed)

    if verif == False :
        await ctx.send("Pas de devoirs pour cette date ! Veuillez verifier l'orthographe !") #Affiche précisement les devoirs recherchés pour une date en particulier et dis si il n'y a pas de devoirs à cette date

@bot.command()
async def enter_dev(self, ctx, date, matiere, desc):
    db_devoir.insert({'date': date, 'matiere': matiere, 'devoir': desc})
    await ctx.send("Vous venez de rajouter pour le {} \n {} : {} ".format(date, matiere, desc)) #Commande qui permet de rentrer les devoirs sur discord pour la base de donnée

@commands.command()
async def rem_dev(self, ctx, date, matiere):
    req = Query()
    db_devoir.remove((req.date == date) & (req.matiere == matiere))
    await ctx.send('Vous venez de supprimer les devoirs du {} en {}'.format(date, matiere)) #Retire des devoirs de la base de donnée en fonction de la date et de la matière

bot.run(TOKEN)

