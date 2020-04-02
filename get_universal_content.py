from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import psycopg2
def count_word(html,word):
	pass
def get_html(url):
	options = webdriver.FirefoxOptions()
	options.add_argument('')
	driver = webdriver.Firefox(options=options)
	driver.get(url)
	try:
		element = WebDriverWait(driver, 60).until(
	      	EC.presence_of_element_located((By.CLASS_NAME, "conference-details"))
	      	)
	finally:
		link = driver.find_element_by_class_name('fa-globe')
		link.click()
		driver.switch_to.window(driver.window_handles[0])
		driver.close()
		time.sleep(5)
		reqHtml = driver.page_source
		# driver.quit()
		return reqHtml
def main():
	url = input()
	word = input()
	reqHtml = get_html(url)
	soup = BeautifulSoup(reqHtml,'html.parser')
	print(soup.find('div',class_ = 'carousel'))
main()