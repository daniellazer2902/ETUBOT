import discord


from discord.ext import commands


from tinydb import TinyDB, Query

TOKEN = 'NjgyMTgyMTQ2ODUyNzgyMDgy.Xn26JA.EzrkYx5zBd5JDwAIu3vmdRPed4g'

#bot = commands.Bot(command_prefix =';')



db_devoir = TinyDB("db_devoir.json")
all_dev = db_devoir.all()

Requete = Query()

db_devoir.update({'channel': 682221578393878561}, Requete.name == 'general')

db_devoir.search(Requete.name == "general")

#db_devoir.insert({'date': "27/05" , 'matiere': "Communication", 'devoir': "Faire un essai de 200 lignes"})
#db_devoir.insert({'date': "29/05" , 'matiere': "Logique", 'devoir': "Controle sur les probas"})

for item in db_devoir:
    print(item)



class bot_marine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Je suis co !')

    @commands.Cog.listener()
    async def db_ready(self):
        print(db_devoir)

    #@bot.command()
    #async def stock_dev(ctx, date_, matiere_, devoir_):
        #for dev in all_dev :
            #db_devoir.insert({'date': "date_", 'matiere': "matiere_", 'devoir': "devoir_"})


    @commands.command()
    async def list(self, ctx): 
        for dev in all_dev :
            await ctx.send(dev)

    @commands.command()
    async def search_matiere(self, ctx, mat_search):
        verif = False
        for dev in all_dev :
            if dev.get('matiere') == mat_search :
                verif = True
                await ctx.send(dev)
        if verif == False :
            await ctx.send("Pas de devoirs ! Veuillez verifier l'orthographe !")

    @commands.command()
    async def search_date(self, ctx, date_search):
        verif = False
        for dev in all_dev :
            if dev.get('date') == date_search :
                verif = True
                await ctx.send(dev)
        if verif == False :
            await ctx.send("Pas de devoirs pour cette date ! Veuillez verifier l'orthographe !")



    @commands.command()
    async def devoir(self, ctx, date, matiere, devoir):
        await ctx.send('```Les devoirs sont : Pour le {} \nEn : {}\nFaire : {}```'.format(date, matiere, devoir))


def setup(bot):
    bot.add_cog(bot_marine(bot))

#bot.run(TOKEN)

