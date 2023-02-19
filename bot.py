import discord
from discord.ext import tasks
import json
import requests

# API keys
APOD_KEY = ''
BOT_KEY = ''

# Discord Guild/Server's Channel you want to send APOD notifications to
CHANNEL_NOTIFICATIONS = -1

apod_message = ""
my_intents = discord.Intents.default()
client = discord.Client(intents=my_intents)

@client.event
async def on_ready():
	call_nasa_api()
	daily_astronomy_pictures.start()
	print("APOD Bot is online")

@client.event
async def on_connect():
	print("APOD Bot has connected to Discord")

@client.event
async def on_disconnect():
	print("APOD Bot has disconnected from Discord")

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	call_nasa_api()

	# DM for personal APOD
	if message.content.startswith('!space'):
		print("Send APOD to DM")
		await message.channel.send(apod_message)
		return

@tasks.loop(seconds=86400) # 86400 seconds = 24 hours
async def daily_astronomy_pictures():
    call_nasa_api()
    channel = client.get_channel(CHANNEL_NOTIFICATIONS)
    print("Send APOD to server")
    await channel.send(apod_message)

# Gets NASA's APOD and resets it everytime the function is called
def call_nasa_api():
	# API stuff
	global apod_message
	response_API = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + APOD_KEY)
	data = response_API.text
	parse_json = json.loads(data)
	apod_message = "> **{title}**\n> *{date}*\n> {text}\n{img}\n".format(title = parse_json['title'], date = parse_json['date'], text = parse_json['explanation'], img = parse_json['url'])

client.run(BOT_KEY)