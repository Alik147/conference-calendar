import telebot
import psycopg2
import clear
import parse
bot = telebot.TeleBot('890467682:AAGcDbpPbIEAPUUYFFda7CVHG03VRGycUCw')
@bot.message_handler(content_types=['text'])
def echo(message):
	if message.text.lower()=='/start':
		bot.send_message(message.chat.id, 'Команды бота: ')
	elif message.text.lower().split(' ')[0] =='month':
		con = psycopg2.connect(
			host = "127.0.0.1",
			dbname = "postgres",
			user = "postgres",
			password = "postgres"
			)
		cursor = con.cursor()
		cursor.execute('SELECT * from conferences WHERE month = \'{}\' and year = \'{}\''.format(message.text.split(' ')[1],message.text.split(' ')[2]))
		conferences = cursor.fetchall()
		# output
		for conference in conferences:
			bot.send_message(message.chat.id, 'title: {}\n location: {}\n date: {}\n link:{}\n'.format(
				conference[3],
				conference[2],
				conference[1]+' '+conference[5]+' '+conference[6],
				conference[4]
				))
		# 
		con.commit()
		cursor.close()
		con.close()
	elif message.text.lower().split(' ')[0] =='refresh':
		clear.clear()
		parse.parse()
bot.polling()