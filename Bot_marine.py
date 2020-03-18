import discord


from discord.ext import commands


from tinydb import TinyDB, Query

TOKEN = 'NjgyMTgyMTQ2ODUyNzgyMDgy.XnHsyA.mAed8C9yfwvE5zqydk0AHiO0Bg0'

bot = commands.Bot(command_prefix =';')



db_devoir = TinyDB("db.json")

#db_devoir.insert({"channel": "1234567890", "name": "general"})

Requete = Query()

#db_devoir.update({'channel': 682221578393878561}, Requete.name == 'general')

db_devoir.search(Requete.name == "general")

db_devoir.insert({'date', 'matiere', 'devoir'})


@bot.event
async def on_ready():
    print('Je suis co !')

@bot.command()
async def dev(ctx, date, mat, dev):
   db_devoir.insert({'date': date, 'matiere': mat, 'devoir': dev,})

@bot.command()
async def test(ctx, date, mat, dev):
    db_devoir.all()

@bot.command()
async def devoir(ctx, date, matiere, devoir):
    await bot.get_channel(684798878649679965).send('```Les devoirs sont : Pour le {} \nEn : {}\nFaire : {}```'.format(date, matiere, devoir))


bot.run(TOKEN)

