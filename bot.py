import telebot
import psycopg2
import clear
import parse
bot = telebot.TeleBot('')
titlewords = []
location = ''
@bot.message_handler(content_types=['text'])
def echo(message):
	if (message.text.lower()=='/start' or message.text.lower()=='y'):
		bot.send_message(message.chat.id, 'Bot can give you conferences by your preferences, if you dont want to use this filter input \%\%')
		question = bot.send_message(message.chat.id,'Input word(s) thats should be in title')
		bot.register_next_step_handler(question, by_title);
	elif message.text.lower().split(' ')[0] =='refresh':
		clear.clear()
		parse.parse()
def by_title(message):
	global titlewords
	titlewords = message.text.split(' ')
	question = bot.send_message(message.chat.id,'location')
	bot.register_next_step_handler(question, by_location);
def by_location(message):
	global location
	location = message.text;
	question = bot.send_message(message.chat.id,'month')
	bot.register_next_step_handler(question, by_month);
def by_month(message):
	month = message.text;
	con = psycopg2.connect(
		host = "127.0.0.1",
		dbname = "postgres",
		user = "postgres",
		password = "postgres"
		)
	cursor = con.cursor()
	global location
	global titlewords
	conferences = []
	for word in titlewords:
		cursor.execute('SELECT * from conferences WHERE LOWER(title) LIKE \'%{}%\' and LOWER(location) LIKE \'%{}%\' and LOWER(month) LIKE \'%{}%\''.format(word.lower(), location.lower() , month.lower()))
		if conferences:
			conferences = conferences.extend(cursor.fetchall())
		else:
			conferences = cursor.fetchall()
	for conference in conferences:
			bot.send_message(message.chat.id, 'title: {}\n location: {}\n date: {}\n link:{}\n'.format(
				conference[3],
				conference[2],
				conference[1]+' '+conference[5]+' '+conference[6],
				conference[4]
				))
	cursor.close()
	con.close()
	question = bot.send_message(message.chat.id,'Again? Y/N')
	bot.register_next_step_handler(question, echo);
bot.polling()