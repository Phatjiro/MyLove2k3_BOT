import discord
from discord.ext import commands

import os
import asyncio
import youtube_dl
import time

def run_discord_bot():
    TOKEN = 'MTAyNDE4MjAwOTU0OTA0NTc3Mg.G6DKaR.KJGHKuwXkV1IEonef4HFm4T5AxNaJICKX1loHU'
    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    voice_clients = {}

    yt_dl_opts = {'format': 'bestaudio/best'}
    ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # # Get data about the user
        user_name = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel.name)

        # # Debug printing
        # print(f"{username} said: '{user_message}' ({channel})")

        if user_message.lower().startswith('kn!love'):
            await message.channel.send('Yêu Ngân 3000') 
            return

        if user_message.lower().startswith('kn!pin'):
            await message.channel.send('Phát iu Ngân :3')
            return

        if user_message.lower().startswith('kn!dinn'):
            await message.channel.send('Do iuu Ngân nhiềuuuu :>>')
            return

        if user_message.startswith('kn!link'):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as err:
                print(err)

            try:
                url = message.content.split()[1]
            
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

                voice_clients[message.guild.id].play(player)

            except Exception as err:
                print(err)

        if user_message.startswith('kn!p'):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as err:
                print(err)

            try:
                item = message.content.split(" ",1)[1]
                print(item)
                loop = asyncio.get_event_loop()
                data = ytdl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]

                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

                voice_clients[message.guild.id].play(player)

            except Exception as err:
                print(err)


        if message.content.startswith("kn!pause"):
            try:
                voice_clients[message.guild.id].pause()
            except Exception as err:
                print(err)

        # This resumes the current song playing if it's been paused
        if message.content.startswith("kn!resume"):
            try:
                voice_clients[message.guild.id].resume()
            except Exception as err:
                print(err)

        # This stops the current playing song
        if message.content.startswith("kn!s"):
            try:
                voice_clients[message.guild.id].stop()
                await voice_clients[message.guild.id].disconnect()
            except Exception as err:
                print(err)        

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)