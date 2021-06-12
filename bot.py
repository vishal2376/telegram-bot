"""
[emoji symbols]
orange box : 🔸
man with laptop : 👨‍💻
"""

import os
import telebot
from telebot import types
import random
import json

# TOKEN = open('.env').readline()
TOKEN = os.getenv('TOKEN')

cpp_data = json.load(open('cpp_resource.json'))

bot = telebot.TeleBot(TOKEN)

print("Bot is online")

hey_msg = ['Hi ','Hello ','Hey ']
bot_name = ['Developer','Coder','Mastermind','Cool','Resource']
user_name = ['Developer','Coder','Genius','Mastermind','Buddy','Programmer']

knownUsers = []
userStep = {}

#command_cpp keyboard [value=1]
cpp_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
cpp_select.add('Youtube videos','PDFs','Courses','Websites(Learning)','Websites(Practice)')


hideBoard = types.ReplyKeyboardRemove()  # if click on button then hide the keyboard

commands = {
	'start':'Restart bot',
    'cpp' : 'C++ resources',
    'all' : 'List all commands',
    'help': 'Help',
    'github' : 'still in development...',
    'codeforces' : 'still in development...',
}
 
@bot.message_handler(commands=['all'])
def command_all(m):
	text = " All available commands 👨‍💻 : \n\n"
	for key in commands:
		text += "🔸 /" + key + " : "
		text += commands[key] + "\n\n"
	bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['cpp'])
def command_cpp(m):
    cid = m.chat.id
    bot.send_message(cid, "What do you want ? ", reply_markup=cpp_select)
    userStep[cid] = 1

@bot.message_handler(commands=['codeforces'])
def command_codeforces(m):
	text = "Comming soon....."
	bot.reply_to(m, text)

@bot.message_handler(commands=['github'])
def command_github(m):
	text = "Comming soon....."
	bot.reply_to(m, text)

@bot.message_handler(commands=['help'])
def command_help(m):
	bot.send_chat_action(m.chat.id, 'typing')
	text = random.choice(hey_msg)
	if m.chat.type == "private":
		text += m.chat.first_name
	else:
		text += random.choice(user_name)	
	text += ' , I am a '+ random.choice(bot_name) + " Bot"
	text += '\n\nI can do following things :'
	text += '\n 🔸 Provide C++ Resources'
	text += '\n 🔸 Github Repository(comming soon)'
	text += '\n 🔸 Codeforces features(comming soon)'
	text += "\n\nSee all commands at  /all  :)"
	text += "\n\n\nContact Developer 👨‍💻: @vishal2376"
	bot.reply_to(m, text)

#get resource data
def cpp_resource(NAME):
	for cpp in cpp_data:
		if cpp['name'] == NAME:
			text = ''
			for i in cpp:
				if i!='name':
					text += '🔸 '
					text += i
					text += "\n"
					text += cpp[i]
					text += "\n\n"
			return text

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected")
        return 0


#console output
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " : " + m.text)

bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0
		command_help(m)
	else:
		command_help(m)
 
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_cpp_select(m):
	cid = m.chat.id
	userStep[cid] = 0
	bot.send_chat_action(cid, 'typing')
	if m.text == 'Youtube videos':
		text = cpp_resource('yt')
		bot.send_message(cid,text,disable_web_page_preview=True,reply_markup=hideBoard)
	elif m.text =='PDFs':
		text = cpp_resource('pdf')
		bot.send_message(cid,text,disable_web_page_preview=True,reply_markup=hideBoard)
	elif m.text =='Websites(Practice)':
		text = cpp_resource('practice_websites')
		bot.send_message(cid,text,disable_web_page_preview=True,reply_markup=hideBoard)
	elif m.text =='Websites(Learning)':
		text = cpp_resource('learning_websites')
		bot.send_message(cid,text,disable_web_page_preview=True,reply_markup=hideBoard)
	elif m.text =='Courses':
		text = cpp_resource('courses')
		bot.send_message(cid,text,disable_web_page_preview=True,reply_markup=hideBoard)
	else:
		bot.send_message(cid, "Invalid Commands")

# filter message
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):

	lower_text = m.text.lower()
	if lower_text == 'hello' or lower_text == 'hi':
		text = random.choice(hey_msg)
		if m.chat.type == 'private':
			text += m.chat.first_name
		else:
			text += random.choice(user_name)
		bot.reply_to(m, text)
 
bot.polling()
