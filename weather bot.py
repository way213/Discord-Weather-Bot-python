import discord
from discord import app_commands
from discord.ext import commands
import json
import requests
import os
from dotenv import load_dotenv


intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def sync(ctx):
    await ctx.channel.send("Syncing...")
    try:
        synced = await bot.tree.sync()
        await ctx.channel.send(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@bot.command()
async def exit(ctx):
    await ctx.channel.send("Logging off...")
    quit()

@bot.tree.command(name='hello')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey {interaction.user.mention}! this is a slash command!', ephemeral=True)

API_KEY = '401d98b9c12fc72c8a630aaf4a18498e'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@bot.tree.command(name='weather')
@app_commands.describe(city = 'Check the weather of a city!')
async def weather(interaction: discord.Interaction, city: str):
    request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"                                                                          #f string to format our request
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        temperature = round(data['main']['temp'] - 273.15, 2)                                                                       #round to 2 decimals 
        temperature_feels_like = round(data['main']['feels_like'] - 273.15, 2)                                                      #round to 2 decimals 
        weather_main = data['weather'][0]['main']
        weather_description = data['weather'][0]['description']
        await interaction.response.send_message('The temperature in ' + city + ' is ' + str(temperature)  + ' and it feels like ' + str(temperature_feels_like)
         + ', the weather condition is ' + weather_main  + ' and its ' + weather_description)
        await interaction.response.send_message()
    else:
        await interaction.response.send_message('An error occured')
load_dotenv()                                                     #environment variables
KEY = os.getenv("TOKEN")                                          #get token
bot.run(KEY)                                                   #run the bot