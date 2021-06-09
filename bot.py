import telebot

TOKEN = open('api-keys.txt').readline()

bot = telebot.TeleBot(TOKEN)

commands = {
    'help': 'Always ready for help',
    'all' : 'List all commands',
    'cpp' : 'Show best C++ Learning resources'
}

@bot.message_handler(commands=['start'])
def command_start(message):
	text = "Hello, " + message.chat.first_name
	bot.send_chat_action(message.chat.id, 'typing')
	bot.send_message(message.chat.id,text)
	command_help(message)


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_chat_action(message.chat.id, 'typing')
	text = "The following commands are available: \n"
	for key in commands:
		text += "/" + key + " : "
		text += commands[key] + "\n"
	bot.send_message(message.chat.id, text)

bot.polling()