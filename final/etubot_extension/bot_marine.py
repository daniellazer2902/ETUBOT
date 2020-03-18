#import discord


from discord.ext import commands


from tinydb import TinyDB, Query

TOKEN = 'Njg5NzgxNDU2ODk3MzEwODc4.XnH3nw.A1YG4a7xiFYfNeNziSYwf67tHuk'

bot = commands.Bot(command_prefix =';')



db_devoir = TinyDB("db_devoir.json")

#db_devoir.insert({"channel": "1234567890", "name": "general"})

Requete = Query()

db_devoir.update({'channel': 682221578393878561}, Requete.name == 'general')

#db_devoir.search(Requete.name == "general")

db_devoir.insert({'date': '27 mars', 'matiere': 'francais', 'devoir': 'essai de 250 mots'})


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

