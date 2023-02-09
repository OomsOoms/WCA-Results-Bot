import nextcord
from nextcord.ext import commands
from datetime import datetime
import os
import dataframes

from cmds import init_cmds

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

init_cmds(bot)


@bot.event
async def on_ready():
    message = f"Results Bot Online: {datetime.now()}"[
        :35].replace("-", "/")

    print(message)

    await bot.change_presence(activity=nextcord.Activity(type=5, name="Thing"))

    os.system(
        f'curl https://notify.run/09ItsXhIlJ0Z6PBXVqd7 -d "{message}" > /null 2>&1')


bot.run("MTA0MDcyMzIxODQzODI5OTcwOQ.GCMjKq.8Ne_-eAIz_P7uUG-Gog9uuAAhMyyEZA9YRi-lc")
