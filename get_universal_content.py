from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import psycopg2
def get_html(url):
	options = webdriver.FirefoxOptions()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	driver.get(url)
	try:
		element = WebDriverWait(driver, 60).until(
	      	EC.presence_of_element_located((By.CLASS_NAME, "conference-details"))
	      	)
	finally:
		try:
			link = driver.find_element_by_class_name('fa-globe')
			link.click()
			driver.switch_to.window(driver.window_handles[1])
			# driver.close()
			time.sleep(1)
			reqHtml = driver.page_source
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			driver.close()
			# driver.quit()
			return reqHtml
		except NoSuchElementException:
			driver.close()
			return 0
		except IndexError:
			driver.close()
			return 0
		else:
			return 0
def count_words(html,the_word):
    count = html.count(the_word)
    return count

def main():
	con = psycopg2.connect(
	host = "127.0.0.1",
	dbname = "postgres",
	user = "postgres",
	password = "postgres"
	)
	cursor = con.cursor()
	cursor.execute('SELECT * from conferences')
	conferences = cursor.fetchall()
	word = 'COVID-19'
	for conference in conferences:
		print('working on {}'.format(conference[0]))
		reqHtml = get_html(conference[4])
		if reqHtml!=0:
			count = count_words(reqHtml , word)
		else:
			count = 'no conference website';
		cursor.execute('INSERT into additional_information (id, number_of_word, word) values (%s,%s,%s)',(conference[0],count,word))
		con.commit()
	con.commit()
	cursor.close()
	con.close()
main()