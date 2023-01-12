import discord
import os
from discord.ext import commands
from PIL import Image, ImageSequence
import requests
import uuid

TOKEN = TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=".", intents=intents)

#height of the image you want to resize to
img_height = 130
right_boundary = 130
v_height = 30

@client.event
async def on_ready():
    print(f'The Bot is ready!')
    
    
@client.command()
async def gif(ctx):
    gifName = str(uuid.uuid4()) + '.gif'
    imageName = "inputImg.jpg"
    #downloads the image from the discord chat
    await ctx.message.attachments[0].save(imageName)
    
    image = Image.open(imageName).convert("RGBA")
    #changing the size of the image to fit in the gif
    i = int(image.width * (img_height / image.height))
    if i > right_boundary:
        i = right_boundary
    imsize = (i,img_height)
    image = image.resize(imsize)
    gif = Image.open("scared_resize.gif")
    new_image = Image.new("RGB", gif.size)

    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy()
        frame.paste(image, (right_boundary - image.width, v_height), image)
        frames.append(frame)
    file_loc = f'output\{gifName}'
    frames[0].save(file_loc, save_all=True, append_images=frames[1:])
    print("Image converted")
    await ctx.send(file=discord.File(file_loc))
    
    
client.run(TOKEN)