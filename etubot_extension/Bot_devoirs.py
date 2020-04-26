import discord
from discord.ext import commands
from tinydb import TinyDB, Query

TOKEN = 'NjgyMTgyMTQ2ODUyNzgyMDgy.XqRM_g.K-x8U4OoLBuxTDkhdDd1mnn-nc8'
bot = commands.Bot(command_prefix =';')


db_devoir = TinyDB("db_devoir.json")

#db_devoir.purge()

req = Query()

db_devoir.update({'channel': 682221578393878561}, req.name == 'general')
db_devoir.search(req.name == "general")

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

@bot.command(brief="liste tout les devoirs")
async def list_dev(ctx): 
    all_dev = db_devoir.all()
    for dev in all_dev :
        await ctx.send(dev) #Affiche tout les devoirs présents dans la base de donnée

@bot.command(brief="search_matiere [matiere]")
async def search_matiere(ctx, mat_search):
    all_dev = db_devoir.all()
    verif = False
    for dev in all_dev :
        if dev.get('matiere').casefold() == mat_search.casefold() :
            verif = True

            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPSI", color=0xeee657) #Permet d'obtenir une plus belle présentation des devoirs 
            embed.add_field(name="DATE", value= dev.get('date'))
            embed.add_field(name="MATIERE", value= dev.get('matiere'))
            embed.add_field(name="DEVOIRS A FAIRE", value= dev.get('devoir'))

            await ctx.author.send(embed = embed)

    if verif == False :
        await ctx.send("Pas de devoirs ! Veuillez verifier l'orthographe !") #Affiche précisement les devoirs recherchés dans une matière en particulier et dis si ce n'est pas trouvable

@bot.command()
async def search_date(ctx, date_search):
    all_dev = db_devoir.all()
    verif = False
    for dev in all_dev :
        if dev.get('date') == date_search :
            verif = True

            embed = discord.Embed(title="ETUBOT", description="Meilleur BOT de l'EPSI", color=0xeee657) #Permet d'obtenir une plus belle présentation des devoirs 

            embed.add_field(name="DATE", value= dev.get('date'))

            embed.add_field(name="MATIERE", value= dev.get('matiere'))
            
            embed.add_field(name="DEVOIRS A FAIRE", value= dev.get('devoir')) 

            await ctx.author.send(embed = embed)

    if verif == False :
        await ctx.send("Pas de devoirs pour cette date ! Veuillez verifier l'orthographe !") #Affiche précisement les devoirs recherchés pour une date en particulier et dis si il n'y a pas de devoirs à cette date

@bot.command()
async def enter_dev(ctx, date, matiere, devoir):
    db_devoir.insert({'date': date, 'matiere': matiere, 'devoir': devoir})
    await ctx.send("Vous venez de rajouter pour le {} \n {} : {} ".format(date, matiere, devoir)) #Commande qui permet de rentrer les devoirs sur discord pour la base de donnée

@bot.command()
async def rem_dev(ctx, date, mat_search):

    all_dev = db_devoir.all()
    for dev in all_dev:

        if dev.get('matiere').casefold() == mat_search.casefold() :
            mat_search = dev.get('matiere')
            db_devoir.remove((req.date == date) & (req.matiere == mat_search))
            await ctx.send('Vous venez de supprimer les devoirs du {} en {}'.format(date, mat_search)) #Retire des devoirs de la base de donnée en fonction de la date et de la matière
            break



bot.run(TOKEN)

