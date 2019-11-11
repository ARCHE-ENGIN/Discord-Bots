# -*-coding = cp1252 -*-


# Importation of the modules

import os
import discord
import asyncio
import time
import sys
import emoji
import random
import requests
import json
from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO

TOKEN = os.environ["TOKEN"]

DiscordClient = discord.Client()    # Creation of the discord client

# PARAMETERS

DiscordClient.CallCommand = "$zep "

try :

    DiscordClient.Admins = os.environ["ADMINS"].split(" ")

except :

    DiscordClient.Admins = None

DiscordClient.IsRunning = False

try :

    Infos = os.environ["MSG"].split(" ")

    Channel = DiscordClient.get_channel(Infos[0][2:-1])

    Msg = DiscordClient.get_message(Channel, Msg[1])

    DiscordClient.Msg_Watch = Msg

    Server = DiscordClient.get_guild("591314616647417868")

    DiscordClient.IsRunning = True

    on_reaction(Server)

except :

    DiscordClient.Msg_Watch = None

try :
    
    DiscordClient.DefaultChannel = DiscordClient.get_channel(os.environ["DEFAULT-CHANNEL"])

except :

    DiscordClient.DefaultChannel = None

# Welcome image parameters

DiscordClient.AvatarSize = 500
DiscordClient.ContourRadius = 260
DiscordClient.ContourColor = (239,210,66)
DiscordClient.TxtSize = 120
DiscordClient.Padding = 360
DiscordClient.MsgColor = (255,255,255)

DiscordClient.Font = ImageFont.truetype("Font.ttf",DiscordClient.TxtSize)
DiscordClient.Welcome = Image.open("Land.jpg")
DiscordClient.Goodbye = Image.open("Grave.jpg")

#####################################################################################

def create_Welcome_Image () :

    DiscordClient.Mask = Image.new("L", (DiscordClient.AvatarSize,DiscordClient.AvatarSize), 0)   #Create an image mask for the avatar
    DiscordClient.Draw = ImageDraw.Draw(DiscordClient.Mask) #Draw on the mask
    DiscordClient.Draw.ellipse((0,0) + (DiscordClient.AvatarSize,DiscordClient.AvatarSize), fill = 255)   #Draw a circle of the avatar's tall

    DiscordClient.AvatarCenter = (int(DiscordClient.Welcome.size[0] / 2 - DiscordClient.AvatarSize / 2),int(DiscordClient.Welcome.size[1] / 2 - DiscordClient.AvatarSize / 2))
    DiscordClient.CircleCenter = (DiscordClient.Welcome.size[0] / 2 - DiscordClient.ContourRadius, DiscordClient.Welcome.size[1] / 2 - DiscordClient.ContourRadius, DiscordClient.Welcome.size[0] / 2 + DiscordClient.ContourRadius, DiscordClient.Welcome.size[1] / 2 + DiscordClient.ContourRadius)

    DiscordClient.DrawingHello = ImageDraw.Draw(DiscordClient.Welcome)    # Create a draw of the background
    DiscordClient.DrawingHello.ellipse(DiscordClient.CircleCenter, fill = DiscordClient.ContourColor, outline = "black", width = 5)   # Draw a circle on the background

def create_Goodbye_Image () :

    DiscordClient.Mask = Image.new("L", (DiscordClient.AvatarSize,DiscordClient.AvatarSize), 0)   #Create an image mask for the avatar
    DiscordClient.Draw = ImageDraw.Draw(DiscordClient.Mask) #Draw on the mask
    DiscordClient.Draw.ellipse((0,0) + (DiscordClient.AvatarSize,DiscordClient.AvatarSize), fill = 255)   #Draw a circle of the avatar's tall

    DiscordClient.AvatarCenter = (int(DiscordClient.Goodbye.size[0] / 2 - DiscordClient.AvatarSize / 2),int(DiscordClient.Goodbye.size[1] / 2 - DiscordClient.AvatarSize / 2))
    DiscordClient.CircleCenter = (DiscordClient.Goodbye.size[0] / 2 - DiscordClient.ContourRadius, DiscordClient.Goodbye.size[1] / 2 - DiscordClient.ContourRadius, DiscordClient.Goodbye.size[0] / 2 + DiscordClient.ContourRadius, DiscordClient.Goodbye.size[1] / 2 + DiscordClient.ContourRadius)

    DiscordClient.DrawingBye = ImageDraw.Draw(DiscordClient.Goodbye)    # Create a draw of the background
    DiscordClient.DrawingBye.ellipse(DiscordClient.CircleCenter, fill = DiscordClient.ContourColor, outline = "black", width = 5)   # Draw a circle on the background

create_Welcome_Image()

create_Goodbye_Image()

#####################################################################################

def reload_Files () :

    DiscordClient.Font = ImageFont.truetype("Font.ttf",DiscordClient.TxtSize)
    DiscordClient.Welcome = Image.open("Land.jpg")
    DiscordClient.Goodbye = Image.open("Grave.jpg")

    create_Welcome_Image()
    create_Goodbye_Image()

#####################################################################################

async def send_Welcome (user) :

    Target = await DiscordClient.get_user_info(user.id)

    Content = ":beginner:Welcome <@" + str(user.id) + "> in the Averuv server !\nIf you want the complete access of the server *** don't forget to accept the rules in the channel rules-and-infos.***\n\nWe wish you to have fun on it !"

    await DiscordClient.send_message(Target,Content)

#####################################################################################

async def send_Welcome_Image (member,channel = None) :

    try :

        Img = requests.get(member.avatar_url)   #Get the avatar url

    except :

        Img = requests.get("https://i.ibb.co/6Rd33Fw/Default.png")

    Avatar = Image.open(BytesIO(Img.content)).resize((DiscordClient.AvatarSize,DiscordClient.AvatarSize)) #Open the avatar image and resize it

    Avatar.putalpha(DiscordClient.Mask)

    Content = "Welcome " + str(member) + " in the new world !"

    Txt_Size = DiscordClient.Draw.textsize(Content, font = DiscordClient.Font) # Get the size of the welcome msg with the font
    
    DiscordClient.TextCenter = (int(DiscordClient.Welcome.size[0] / 2 - Txt_Size[0] / 2)) , (int(DiscordClient.Welcome.size[1] / 2 - Txt_Size[1] / 2)) + DiscordClient.Padding   # Get the center of the background image for the text

    DiscordClient.DrawingHello.text(DiscordClient.TextCenter,Content,fill = DiscordClient.MsgColor, font = DiscordClient.Font)  # Write the text on the background image

    DiscordClient.Welcome.paste(Avatar, DiscordClient.AvatarCenter, Avatar) # Paste the avatar image on the background image

    DiscordClient.Welcome.save("Welcome.png")  # Save the image to send

    if channel == None :

        Channel = DiscordClient.DefaultChannel

    else :

        Channel = channel

    await DiscordClient.send_file(Channel,"Welcome.png")    # Send the image in channel

    reload_Files()

#####################################################################################

async def send_Goodbye_Image (member,channel = None) :

    try :

        Img = requests.get(member.avatar_url)   #Get the avatar url

    except :

        Img = requests.get("https://i.ibb.co/6Rd33Fw/Default.png")

    Avatar = Image.open(BytesIO(Img.content)).resize((DiscordClient.AvatarSize,DiscordClient.AvatarSize)) #Open the avatar image and resize it

    Avatar.putalpha(DiscordClient.Mask)

    Content = str(member) + " has just left us, repose in peace."

    Txt_Size = DiscordClient.Draw.textsize(Content, font = DiscordClient.Font) # Get the size of the welcome msg with the font
    
    DiscordClient.TextCenter = (int(DiscordClient.Goodbye.size[0] / 2 - Txt_Size[0] / 2)) , (int(DiscordClient.Goodbye.size[1] / 2 - Txt_Size[1] / 2)) + DiscordClient.Padding   # Get the center of the background image for the text

    DiscordClient.DrawingBye.text(DiscordClient.TextCenter,Content,fill = DiscordClient.MsgColor, font = DiscordClient.Font)  # Write the text on the background image

    DiscordClient.Goodbye.paste(Avatar, DiscordClient.AvatarCenter, Avatar) # Paste the avatar image on the background image

    DiscordClient.Goodbye.save("Goodbye.png")  # Save the image to send

    if channel == None :

        Channel = DiscordClient.DefaultChannel

    else :

        Channel = channel

    await DiscordClient.send_file(Channel,"Goodbye.png")    # Send the image in channel

    reload_Files()

#####################################################################################

@DiscordClient.event    # Bot event

async def on_ready () : # When bot starts

    Name = "the world"    # Description showed on Discord

    State = discord.Game(name = Name,type = 3)  # Create a state instance

    await DiscordClient.change_presence(game = State)   # Change the bot status on Discord

#####################################################################################

@DiscordClient.event    # Bot event

async def on_member_join (member) : # When a new member join the server

    try :   # Try to do the next line

        await send_Welcome_Image(member) # Send a welcome image on the default channel

        await send_Welcome(member)

    except :    # If try failed

        pass

#####################################################################################

@DiscordClient.event    # Bot event

async def on_member_remove (member) :   # When a member leaves the server

    try : # Try to do the next line

        await send_Goodbye_Image(member)

    except : # If try failed

        pass

#####################################################################################

Last_Users = []

async def on_reaction (server) :

    global Last_Users

    Emoji = emoji.emojize(":large_blue_diamond:")

    for reaction in DiscordClient.Msg_Watch.reactions :

        if reaction.emoji == Emoji :

            if Last_Users != [] :

                Users = await DiscordClient.get_reaction_users(reaction)

                if len(Last_Users) < len(Users) :

                    for user in Users :

                        if user not in Last_Users and user.id != DiscordClient.user.id :

                            Agree = discord.utils.get(server.roles, name = "Agree to terms") # Get the server role to add

                            Member = server.get_member(user.id)

                            await DiscordClient.add_roles(Member, Agree)    # Add the role to the member who reacts

                            Content = ":gem: Thank you for accepting the rules of Averuv !\n\nYou have now access to the server's content,\n:warning: ***However, you have undertaken to respect these rules so be careful and do not forget that any deviation may be sanctioned.***"

                            await DiscordClient.send_message(user,Content)

                    Last_Users = Users

                elif len(Last_Users) > len(Users) :

                    for user in Last_Users :

                        if user not in Users and user.id != DiscordClient.user.id :

                            Disagree = discord.utils.get(server.roles, name = "Agree to terms") # Get the server role to remove

                            Member = server.get_member(user.id)

                            await DiscordClient.remove_roles(Member, Disagree)    # Remove the role from the member

                            Content = ":warning: You no longer comply with the server's rules, so you no longer have access to its content !"

                            await DiscordClient.send_message(user,Content)

                    Last_Users = Users

            else : 

                Last_Users = await DiscordClient.get_reaction_users(reaction)

        break

    await asyncio.sleep(6)

    if DiscordClient.IsRunning != False :

        try :

            await on_reaction(server)

        except :

            await on_reaction(server)
            
#####################################################################################

@DiscordClient.event    # Bot event
    
async def on_message (message) :    # When a new message arrives

    if message.author == DiscordClient.user :   # If the author of the message is the bot

        return  # Exit the function

    if message.content.startswith(DiscordClient.CallCommand) :    # If the call command is detected on message

        Message = message.content[len(DiscordClient.CallCommand):]    # Get the area of interest on the message

        def if_Admin (author) :

            Roles = [Role.name for Role in author.roles]

            if DiscordClient.Admins in Roles or author == message.server.owner :

                return True

            else :

                return False

        async def erase_Msg(message) :
                
            await DiscordClient.delete_message(message)

        if Message == "help" :

            Check = if_Admin(message.author)

            if Check :

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Title = ">>> ***List of available commands :***"

            Embed = discord.Embed()

            Embed.add_field(name = ":beginner:latency",value = "\tGive the latency of the bot" , inline = False)

            Embed.add_field(name = ":beginner:welcome_img",value = "\tShow the welcome image" , inline = False)

            Embed.add_field(name = ":beginner:goodbye_image",value = "\tSet the image for member join" , inline = False)

            Embed.add_field(name = ":beginner:set_default_channel",value = "\tSet the channel to send welcome images" , inline = False)

            Embed.add_field(name = ":beginner:set_welcome_image",value = "\tSet the image for member join" , inline = False)

            Embed.add_field(name = ":beginner:watch_reactions",value = " \tSurvey a message and give a role when a member react to it" , inline = False)

            Embed.add_field(name = ":beginner:set_admins",value = "\tSet the admins" , inline = False)

            Embed.add_field(name = ":beginner:reload",value = " \tReload all files" , inline = False)

            Embed.set_thumbnail(url =DiscordClient.user.avatar_url)

            Embed.set_footer(text = "For more informations do {command} {help}")

            await DiscordClient.send_message(message.channel, Title, embed = Embed)

        elif Message == "latency" :   # If the command used was latency

            Check = if_Admin(message.author)

            if Check :

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Before = time.monotonic()

            Msg = await DiscordClient.send_message(message.channel,"Calculating ...")

            Latency = (time.monotonic() - Before)* 100

            Latency = ">>> Latency of : " + str(round(Latency,3)) + " ms"

            await DiscordClient.edit_message(Msg,Latency)

        #######################################################################################################

        elif Message.startswith("welcome_img") :  # If the command used was set_default_channel

            await send_Welcome_Image(message.author,message.channel)

        #######################################################################################################

        elif Message.startswith("goodbye_img") :  # If the command used was set_default_channel

            await send_Goodbye_Image(message.author,message.channel)

        #######################################################################################################

        elif Message.startswith("set_default_channel") :  # If the command used was set_default_channel

            Check = if_Admin(message.author)

            if Check :

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Channel = Message[20:]

            if Channel == "help" :

                await DiscordClient.send_message(message.channel,">>> Command format : \n```css\n[set_default_channel {#channel}```")

            else :

                await DiscordClient.send_message(message.channel, ">>> The zeppelin is treating the channel")
            
                Channel = DiscordClient.get_channel(Channel[2:-1])

                DiscordClient.DefaultChannel = Channel

                os.environ["DEFAULT CHANNEL"] = Channel.id

                Hello = await DiscordClient.send_message(Channel, ">>> This is now the default channel !")

                await asyncio.sleep(3)

                await DiscordClient.delete_message(Hello)

                await DiscordClient.send_message(message.channel,">>> The default channel of the zeppelin was set")

        #######################################################################################################

        elif Message.startswith("set_welcome_img") :  # If the command used was set_welcome_img

            Check = if_Admin(message.author)

            if Check :

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Params = Message[16:]

            if Params == "help" :

                await DiscordClient.send_message(message.channel,">>> Command format : \n```css\n[set_welcome_img {Avatar size} {Contour radius} {Contour{Text size} {Padding} {Message color}]\n```")

            else :  # 440 260 (239,210,66) 94 400 (255,255,255)

                await DiscordClient.send_message(message.channel, ">>> The zeppelin is treating the parameters")

                Params = Params.split(" ")

                DiscordClient.AvatarSize = int(Params[0])

                DiscordClient.ContourRadius = int(Params[1])

                DiscordClient.ContourColor = eval(Params[2])

                DiscordClient.TxtSize = int(Params[3])

                DiscordClient.Padding = int(Params[4])

                DiscordClient.MsgColor = eval(Params[5])

                create_Welcome_Image()

                await send_Welcome_Image(message.author)

        #######################################################################################################

        elif Message.startswith("watch_reactions") :  # If the command used was watch_reactions

            Check = if_Admin(message.author)

            if Check :

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Params = Message[16:]

            if Params == "help" :

                await DiscordClient.send_message(message.channel,">>> Command format : \n```css\n[watch_reactions {#channel} {message.id}]\n```")

            else :

                await DiscordClient.send_message(message.channel, ">>> The zeppelin is treating the message")

                Msg = Params.split(" ")

                Channel = DiscordClient.get_channel(Msg[0][2:-1])

                Msg = await DiscordClient.get_message(Channel, Msg[1])

                Emoji = emoji.emojize(":large_blue_diamond:")

                await asyncio.sleep(1)

                await DiscordClient.add_reaction(Msg, Emoji)

                async for msg in DiscordClient.logs_from(Channel) :

                    if msg.id == Msg.id :

                        print("Found :")

                        DiscordClient.Msg_Watch = msg

                        print(DiscordClient.Msg_Watch)

                        break

                os.environ["MSG"] = Params.split()

                DiscordClient.IsRunning = False

                await asyncio.sleep(6)

                DiscordClient.IsRunning = True

                await on_reaction(message.server)

                await DiscordClient.send_message(message.channel,">>> The zeppelin will now watch this message !")

        #######################################################################################################

        elif Message.startswith("set_admins") :

            Check = if_Admin(message.author)

            if Check :

                await DiscordClient.send_message(message.channel, ">>> The zeppelin is reloading")

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            Params = Message[11:]

            if Params == "help" :

                await DiscordClient.send_message(message.channel,">>> Command format : \n```css\n[set_admins {role1} {role2} ...]\n```")

            else :

                Params = Params.split(" ")

                DiscordClient.Admins = Params

                os.environ["ADMINS"] = Params

        #######################################################################################################

        elif Message.startswith("reload") :  # If the command used was set_default_channel

            Check = if_Admin(message.author)

            if Check :

                await DiscordClient.send_message(message.channel, ">>> The zeppelin is reloading")

                pass

            else :

                await erase_Msg(message)

                Warn = await DiscordClient.send_message(message.channel, ">>> Sorry but you don't have the right to speak with the captain of the zeppelin")

                await asyncio.sleep(6)

                await DiscordClient.delete_message(Warn)

                return

            reload_Files()

            await DiscordClient.send_message(message.channel, ">>> Reloading finished, the zeppelin is ready !")

        else :

            await DiscordClient.send_message(message.channel,">>> Unknow command !\nType :\n```css\n[help]```\nTo see all available commands")

##############################################################################################################################################################################

DiscordClient.run(TOKEN)    # Connection to the discord account with the token
