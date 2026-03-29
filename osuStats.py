from ossapi import *
import sys
import math
from pathlib import Path
import re


script_dir = Path(__file__).parent
icon_file = script_dir / "icon_ASCII.txt"
conf_file = script_dir / "OsuStats.config"

conf = open(conf_file, 'r+')
confread = conf.readlines()

conf_list = {}
for i in confread:
    option=i.split('=')[0]
    val=i.split('=')[1]
    conf_list[option]=val
askUser = conf_list["AskUser"]
User = conf_list["User"]
clientId_conf = conf_list["ClientId"]
clientSecret_conf = conf_list["ClientSecret"]

#change config option value
def writeconf(option, set_to):
    with open(conf_file, 'r') as file:
        content = file.read()
    content = content.replace(f"{option}=None", f"{option}={set_to}")
    with open(conf_file, 'w') as file:
        file.write(content)

#ask for client id
if clientId_conf.strip() == "None":
    client_id_input=input("What's your client id?\n")
    writeconf("ClientId", client_id_input)
    client_id = client_id_input.strip()
if clientId_conf.strip() != "None":
    client_id = clientId_conf.strip()

#ask for client secret
if clientSecret_conf.strip() == "None":
    client_secret_input=input("What's your client secret?\n")
    writeconf("ClientSecret", client_secret_input)
    client_secret = client_secret_input.strip()
if clientSecret_conf.strip() != "None":
    client_secret = clientSecret_conf.strip()

# Ask User config
if askUser.strip() == "None":
    AskUser_q = input("Ask for user each time? [y/n]:\n")
    if AskUser_q.strip() in ("YES","Yes","Y","yes","y"):
        with open(conf_file, 'r') as file:
            content = file.read()
        content = content.replace("AskUser=None","AskUser=True")
        with open(conf_file, 'w') as file:
            file.write(content)
        if __name__ == "__main__":
            if len(sys.argv) > 1:
                name=sys.argv[1]
            else:
                name_inp = input("what's your username?\n")
                name=name_inp.strip()
    if AskUser_q.strip() in ("NO","No","N","no","n"):
        with open(conf_file, 'r') as file:
            content = file.read()
        content = content.replace("AskUser=None","AskUser=False")
        with open(conf_file, 'w') as file:
            file.write(content)
        if User.strip() == "None":
            name=input("What's your username?\n")
            with open(conf_file, 'r') as file:
                content = file.read()
            content = content.replace("User=None", f"User={name}")
            with open(conf_file, 'w') as file:
                file.write(content)
    if User.strip() != "None":
        name =  User.strip()
#ask user each time / set constant user
if askUser.strip() == "True":
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            name=sys.argv[1]
        else:
            name_inp = input("what's your username?\n")
            name=name_inp.strip()
if askUser.strip() == "False":
    if User.strip() == "None":
        name=input("What's your username?\n")
        with open(conf_file, 'r') as file:
            content = file.read()
        content = content.replace("User=None", f"User={name}")
        with open(conf_file, 'w') as file:
            file.write(content)
    if User.strip() != "None":
        name =  User.strip()

RESET = "\033[0m"
MAIN_col = "\033[38;2;255;105;180m"
BG_col = "\033[38;2;255;255;255m"

icontxt = open(icon_file, "r")
iconReadlines = icontxt.readlines()

def ico(n):
    iconLine = str(iconReadlines[n].strip('\n'))
    colored_iconLine = iconLine.replace("░", MAIN_col+'░'+RESET).replace("▒", BG_col+'▒'+RESET)
    return colored_iconLine

api = Ossapi(client_id, client_secret)

user = api.user(name, key=UserLookupKey.USERNAME)
best_scores = api.user_scores(user.id, type="best", mode=GameMode.OSU, limit=1)

top_play = best_scores[0]

# top play stat list split for easy indexing
tp_stats = (str(top_play)).split(',')
def tp_stat_val(val):
    for item in tp_stats:
        if (f"{val}=") in item.strip():
            if item.count("=") > 1:
                return item.split('=')[2].strip()
            else:
                return item.split('=',1)[1].strip()
#user stats list split for easy indexing
stats = (str(user.statistics)).split(',')
stat_list = {}
for i in stats:
    key = i.split('=')[0].strip()
    value = i.split('=')[1].strip()
    stat_list[key] = value

# vars
global_rank = stat_list['global_rank']
country_rank = stat_list['country_rank']
total_pp = stat_list['pp']
play_time = stat_list['play_time']
tp_title = tp_stat_val('title').replace('"',"").replace("'","")
tp_artist = tp_stat_val('artist').replace('"',"").replace("'","")
tp_pp = tp_stat_val('pp')
tp_acc = tp_stat_val('accuracy')

def playtime(seconds):
    total_minutes = seconds // 60
    total_hours = total_minutes // 60
    days = total_hours // 24
    hours = total_hours - days*24
    minutes = total_minutes - total_hours*60
    return f"{days}d {hours}h {minutes}m"

def userclient():
    if 'CL' in str(top_play.mods):
        return "osu!(Stable)"
    if 'CL' not in str(top_play.mods):
        return "osu!(Lazer)"

matrix = [["Username", user.username],
         ["├",""],
         ["Statistics"," "],
         [" ├─Global rank", global_rank],
         [" ├─Country rank", country_rank],
         [" ├─Total PP", int(float(total_pp))],
         [" └─Playtime", playtime(int(play_time))],
         ["┌",""],
         ["Top Play"," "],
         [" ├─Map", tp_title+' - '+tp_artist],
         [" ├─PP", int(float(tp_pp))],
         [" └─Accuracy", f"{math.ceil((float(tp_acc)*100)*10)/10}%"],
         ["┌",""],
         ["Client", userclient()]]

# ├ ─ └
max_len = len(" ├─Map"+ tp_title+' - '+tp_artist)+4

#prints out all info (Depending on client)
if 'CL' not in str(top_play.mods):
    for i in range(0, len(matrix)):
            if matrix[0+i][1] == "":
                print(ico(i),f"    {matrix[0+i][0]+'─'*max_len}")
            else:
                if "├─" in matrix[0+i][0] or "└─" in matrix[0+i][0]:
                    print(ico(i),f"    {(matrix[0+i][0])[:3]}{MAIN_col}{(matrix[0+i][0])[3:]}\033[0m: {matrix[0+i][1]}")
                else: 
                    print(ico(i),f"    {MAIN_col}{matrix[0+i][0]}\033[0m: {matrix[0+i][1]}")
    for EmptyLines in range(14,17):
        print(ico(EmptyLines))

if 'CL' in str(top_play.mods):
    for i in range(0, len(matrix)):
            if matrix[0+i][1] == "":
                print(ico(i+18),f"    {matrix[0+i][0]+'─'*max_len}")
            else:
                if "├─" in matrix[0+i][0] or "└─" in matrix[0+i][0]:
                    print(ico(i+18),f"    {(matrix[0+i][0])[:3]}{MAIN_col}{(matrix[0+i][0])[3:]}\033[0m: {matrix[0+i][1]}")
                else: 
                    print(ico(i+18  ),f"    {MAIN_col}{matrix[0+i][0]}\033[0m: {matrix[0+i][1]}")
    for EmptyLines in range(32,36):
        print(ico(EmptyLines))