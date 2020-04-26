import discord
from discord.ext import commands
from tinydb import TinyDB, Query

#TOKEN = ''
#bot = commands.Bot(command_prefix =';')


db_devoir = TinyDB("db_devoir.json")

#db_devoir.purge()

req = Query()

db_devoir.update({'channel': 682221578393878561}, req.name == 'general')
db_devoir.search(req.name == "general")

#db_devoir.insert({'date': "27/05" , 'matiere': "Communication", 'devoir': "Faire un essai de 200 lignes"})
#db_devoir.insert({'date': "29/05" , 'matiere': "Logique", 'devoir': "Controle sur les probas"})

for item in db_devoir:
    print(item)


class bot_marine(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Je suis co !') #Affiche quand le bot est co !

    @commands.Cog.listener()
    async def db_ready(self):
        print(db_devoir) #Affiche les données présente dans la base de donnée db_devoir

    @commands.command(brief="liste tout les devoirs")
    async def list_dev(self, ctx): 
        all_dev = db_devoir.all()
        for dev in all_dev :
            await ctx.send(dev) #Affiche tout les devoirs présents dans la base de donnée

    @commands.command(brief="search_matiere [matiere]")
    async def search_matiere(self, ctx, mat_search):
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

    @commands.command()
    async def search_date(self, ctx, date_search):
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

    @commands.command()
    async def enter_dev(self, ctx, date, matiere, devoir):
        db_devoir.insert({'date': date, 'matiere': matiere, 'devoir': devoir})
        await ctx.send("Vous venez de rajouter pour le {} \n {} : {} ".format(date, matiere, devoir)) #Commande qui permet de rentrer les devoirs sur discord pour la base de donnée

    @commands.command()
    async def rem_dev(self, ctx, date, mat_search):

        all_dev = db_devoir.all()
        for dev in all_dev:

            if dev.get('matiere').casefold() == mat_search.casefold() :
                mat_search = dev.get('matiere')
                db_devoir.remove((req.date == date) & (req.matiere == mat_search))
                await ctx.send('Vous venez de supprimer les devoirs du {} en {}'.format(date, mat_search)) #Retire des devoirs de la base de donnée en fonction de la date et de la matière
                break

def setup(client):
    client.add_cog(bot_marine(client))

#bot.run(TOKEN)

