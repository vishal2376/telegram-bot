import telebot
from telebot import types
import random

TOKEN = open('api-keys.txt').readline()

bot = telebot.TeleBot(TOKEN)

print("Bot is ready....")

hey_msg = ['Hi ','Hello ','Hey ']
bot_name = ['Developer','Coder','Resource','Dev']

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

#command_cpp keyboard [value=1]
cpp_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
cpp_select.add('Youtube videos','PDFs','websites','Courses')


hideBoard = types.ReplyKeyboardRemove()  # if click on button then hide the keyboard

commands = {
    'help': 'Always ready for help',
    'all' : 'List all commands',
    'cpp' : 'Show best C++ Learning resources',
    'codeforces' : 'still in development...'
}
 
@bot.message_handler(commands=['all'])
def command_all(m):
	text = "Available commands \n"
	for key in commands:
		text += "/" + key + " : "
		text += commands[key] + "\n"
	bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['all'])
def command_codeforces(m):
	text = "Still in development ....."
	bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['help'])
def command_help(m):
	bot.send_chat_action(m.chat.id, 'typing')
	text = random.choice(hey_msg)
	text += m.chat.first_name
	text += ', I am '+ random.choice(bot_name) + " Bot"
	text += '\nI can give you the best resources for programming (c++ available only , rest will add later)'
	text += "\n\nAll commands are available at  /all  :)"
	bot.send_message(m.chat.id, text)

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
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
	cid = m.chat.id
	if cid not in knownUsers:
		knownUsers.append(cid)
		userStep[cid] = 0
		command_help(m)
	else:
		text = random.choice(hey_msg)
		text += m.chat.first_name
		bot.send_message(cid, text)

@bot.message_handler(commands=['cpp'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "What do you want ? ", reply_markup=cpp_select)
    userStep[cid] = 1

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
	cid = m.chat.id
	userStep[cid] = 0
	bot.send_chat_action(cid, 'typing')
	if m.text == 'Youtube videos':
   		bot.send_message(cid,"yt links from file",reply_markup=hideBoard)
	elif m.text =='PDFs'  :
   		bot.send_message(cid,"pdfs link from file",reply_markup=hideBoard)
	elif m.text =='websites' :
   		bot.send_message(cid,"website text from file",reply_markup=hideBoard)
	elif m.text =='Courses' :
   		bot.send_message(cid,"coursed text from file",reply_markup=hideBoard)
	else:
		bot.send_message(cid, "Invalid Commands")

# filter message
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
	lower_text = m.text.lower()
	if m.text[0] == '/':
		text = "I don't understand command \" "
		text += m.text
		text += " \"\nI think you should try /help :) "
		bot.send_message(m.chat.id, text)
	elif lower_text == 'hi' or lower_text == 'hello':
		text = random.choice(hey_msg)
		text += m.chat.first_name
		text += ', I am '+ random.choice(bot_name) + " Bot"
		bot.send_message(m.chat.id, text)


bot.polling()