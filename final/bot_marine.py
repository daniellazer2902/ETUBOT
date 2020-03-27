#import discord


from discord.ext import commands


from tinydb import TinyDB, Query

#TOKEN = 'Njg5NzgxNDU2ODk3MzEwODc4.XnjCcw.F8QKNou37q6b-1IbbQsnkUa8GN0'

#bot = commands.Bot(command_prefix =';')



db_devoir = TinyDB("db_devoir.json")

#db_devoir.insert({"channel": "1234567890", "name": "general"})

#Requete = Query()

#db_devoir.update({'channel': 682221578393878561}, Requete.name == 'general')

#db_devoir.search(Requete.name == "general")

#db_devoir.insert({'date': '27 mars', 'matiere': 'francais', 'devoir': 'essai de 250 mots'})


class bot_marine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('bot marine ready!')

    @commands.command()
    async def dev(ctx, date, mat, dev):
       db_devoir.insert({'date': date, 'matiere': mat, 'devoir': dev,})

    @commands.command()
    async def test(ctx, date, mat, dev):
        db_devoir.all()

    @commands.command()
    async def devoir(ctx, date, matiere, devoir):
        await ctx.send('```Les devoirs sont : Pour le {} \nEn : {}\nFaire : {}```'.format(date, matiere, devoir))

def setup(bot):
    bot.add_cog(bot_marine(bot))

#bot.run(TOKEN)
