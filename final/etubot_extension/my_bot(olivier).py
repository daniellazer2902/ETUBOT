import discord
from discord.ext import commands
import datetime
from datetime import timedelta

#bot = commands.Bot(command_prefix='%')


class donnees:
    def __init__(self, date,start_time,end_time,subject,professor,room):
        self.date=date
        self.start_time=start_time
        self.end_time=end_time
        self.subject=subject
        self.professor=professor
        self.room=room

    def __str__(self):
        return " \n Aujourd'hui le  " + str(self.date) + " : le cours de " + str(self.start_time) + " heures jusqu'à " + str(self.end_time) + " heures est un cours de " + self.subject + " , administré par " + self.professor + " en salle " + self.room
 
class emploi_du_temps:
    def __init__(self,nom):
        self.nom=nom
        self.list=[]

    def add(self,date,start_time,end_time,subject,professor,room):
        self.list.append(donnees(date,start_time,end_time,subject,professor,room))

    def __str__(self):
        return self.nom

class bot_olivier(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot readax')

    @commands.command()
    async def private_message(ctx,message):   
        if (message.content.startswith("edt")):
            member = discord.utils.get(message.guild.members,name=message.content.split(" ")[1])
            await member.send("semaine 17 mars")

    @commands.command()
    async def edt(ctx, arg= 0):
        await ctx.send("Voici, votre emploi du temps de la journée:", emploi_du_temps_list[0].list[1])

if __name__ == "__main__":
    emploi_du_temps_list=[]
       
    emploi_du_temps_list.append(emploi_du_temps("edt 17 mars"))
    emploi_du_temps_list[0].add("17 mars",9,11,"projet transversal","Epesse Yves Manfred","C212-VP(Chasseur)")
    emploi_du_temps_list[0].add("17 mars",11,13,"projet transversal","Epesse Yves Manfred","C212-VP(Chasseur)")
    emploi_du_temps_list[0].add("17 mars",14,16,"HEP inside","Magnan De Bellevue","C211-VP(Chasseur)")
    emploi_du_temps_list[0].add("17 mars",16,18,"HEP inside","Magnan De Bellevue","C211-VP(Chasseur)")
         
    for i in range(0,4):
        print(emploi_du_temps_list[0].list[i])

print("--------------------------------------\n")

datetime_today = datetime.now()
print(datetime_today)
print("--------------------------------------\n")

my_delta = timedelta(minutes= 30)
new_date = datetime_today - my_delta
print(new_date)

if new_date.hours == 8:
    print(emploi_du_temps_list[0].list[0])

def setup(client):
    client.add_cog(bot_olivier(client))
    

#bot.run('Njg0NzYxNjQyNzYwMDExODA3.Xmig4g.mnMqdVi7jGFMCpXkQFLUuF1rOeE')
