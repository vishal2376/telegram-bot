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
from github_tools import *

#TOKEN = open('test-key.txt').readline()
TOKEN = os.getenv('TG_TOKEN')

cpp_data = json.load(open('cpp/cpp_resource.json'))

bot = telebot.TeleBot(TOKEN,parse_mode='HTML')

print("Bot is online")

hey_msg = ['Hi ','Hello ','Hey ']
bot_name = ['Developer','Coder','Mastermind','Cool','Resource']
user_name = ['Developer','Coder','Genius','Mastermind','Buddy','Programmer']

knownUsers = []
userStep = {}

#----------------Keyboard Layouts--------------------
#command_cpp keyboard [value=cpp]
cpp_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
cpp_select.add('Youtube videos','PDFs','Courses','Websites(Learning)','Websites(Practice)')

#command_github keyboard [value=github]
github_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
github_select.add('Search','Search(by user)')
github_select.add('Clone Repository')


hideBoard = types.ReplyKeyboardRemove()  # hide the keyboard

commands = {
	'start':'Restart bot',
    'cpp' : 'C++ resources',
    'all' : 'List all commands',
    'help': 'Help',
    'github' : 'Search and clone Repository',
    'codeforces' : 'still in development...',
    'stackoverflow' : 'still in development...'
}

#--------------------others functions----------------------
 
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

#------------------------All main commands--------------------------
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
    bot.send_message(cid, "What do you want ?", reply_markup=cpp_select)
    userStep[cid] = 'cpp'

@bot.message_handler(commands=['github'])
def command_github(m):
	cid = m.chat.id
	bot.send_message(cid, "What do you want ?", reply_markup=github_select)
	userStep[cid] = 'github'

@bot.message_handler(commands=['codeforces'])
def command_codeforces(m):
	text = "Comming soon....."
	bot.reply_to(m, text)

@bot.message_handler(commands=['stackoverflow'])
def command_stackoverflow(m):
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
	text += '\n 🔸 Stackoverflow QnA(comming soon)'
	text += "\n\nSee all commands at  /all  :)"
	text += "\n\n\nContact Developer 👨‍💻: @vishal2376"
	bot.reply_to(m, text)
 
@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0
	command_help(m)

#-------------------Custom keyboard functions-------------------
#---------------------------cpp-----------------------------
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'cpp')
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

#-------------------github all functions-------------------------
#[value=github]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'github')
def msg_github_select(m):
	cid = m.chat.id
	userStep[cid] = 0
	bot.send_chat_action(cid, 'typing')
	if m.text == 'Search':
		# text = 'Not available for some days'
		text = 'Enter your query '
		bot.send_message(m.chat.id,text,reply_markup=hideBoard)
		userStep[cid] = 'github_search' 
	elif m.text == 'Search(by user)':
		text = 'Enter username \nExample : vishal2376'
		bot.send_message(m.chat.id,text,reply_markup=hideBoard)
		userStep[cid] = 'github_search_user'
	elif m.text == 'Clone Repository':
		text = 'Enter username \nExample : vishal2376'
		bot.send_message(m.chat.id,text,reply_markup=hideBoard)
		userStep[cid] = 'github_clone_view'
	else:
		bot.send_message(cid, "Invalid Commands")

#[value=github_clone]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'github_clone')
def msg_github_clone(m):
	cid = m.chat.id
	userStep[cid] = 0
	user_name = ''
	with open('github/user_name.txt','r') as f:
		user_name = f.readline()
	repo_list = get_repo_list(user_name)
	try:
		for repo_name in repo_list:
			if m.text == '/stop':
				bot.send_message(cid,"Successfully stopped",reply_markup=hideBoard)
				break
			elif m.text == repo_name:
				full_repo = user_name +'/'+repo_name
				bot.send_chat_action(cid, 'typing')
				text = 'https://github.com/'+full_repo+'/archive/refs/heads/master.zip'
				msg = bot.send_message(cid,text,reply_markup=hideBoard)

	except Exception as e:
		bot.send_message(cid,'Something went Wrong',reply_markup=hideBoard)	
		print('Error : Failed to download or send files')

#[value=github_clone_view]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'github_clone_view')
def view_clone_repo(m):
	try:
		repo_list = get_repo_list(m.text)
		button = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		for repo_name in repo_list:
			button.add(repo_name)
		bot.send_message(m.chat.id,'Click button to clone Repository \n\nUse /stop to exit',reply_markup=button)
		userStep[m.chat.id] = 'github_clone'
	except Exception as e:
		bot.send_message(m.chat.id,'Something went wrong , Try again later',reply_markup=hideBoard)
		print("Error : Keyboard not created")

#[value=github_search_user]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'github_search_user')
def view_user_repo(m):
	try:
		userStep[m.chat.id]=0
		repo_list = search_user_repo(m.text)
		text = 'Github Repository List\n\n'
		for repo_name in repo_list:		
			name = repo_name.split('/')[1]
			stars = get_repo_stars(repo_name)
			issues = get_repo_issues(repo_name)
			text += '🔸 <b>'+ name + '</b>\n'
			text += 'Stars : '+str(stars)+'      |     Issues : '+ str(issues)
			text += '\n<a href = "https://github.com/'+ repo_name + '">Click here to visit</a>\n\n'  
		bot.send_message(m.chat.id,text,disable_web_page_preview=True)
	except Exception as e:
		bot.send_message(m.chat.id,'Github API search Limit exceed',reply_markup=hideBoard)
		print("Error : Github search Limit exceed")

#[value=github_search]
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 'github_search')		
def view_repo(m):
	try:
		userStep[m.chat.id]=0
		repo_list = search_repo(m.text)
		text = 'Top Search Results \n\n'
		for repo_name in repo_list:
			name = repo_name.split('/')[1]
			stars = get_repo_stars(repo_name)
			issues = get_repo_issues(repo_name)
			text += '🔸 '+ name + '\n'
			text += 'Stars : '+str(stars)+'      |     Issues : '+ str(issues)
			text += '\n<a href = "https://github.com/'+ repo_name + '">Click here to visit</a>\n\n'
		bot.send_message(m.chat.id,text,disable_web_page_preview=True)
	except Exception as e:
		bot.send_message(m.chat.id,'Github API search Limit exceed',reply_markup=hideBoard)
		print("Error : Search limit exceed")

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

