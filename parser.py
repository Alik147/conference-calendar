from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from bs4 import BeautifulSoup

URL = 'https://conferences.ieee.org/conferences_events/conferences/search?q=russia&subsequent_q=&date=all&from=&to=&region=all&country=all&pos=0&sortorder=desc&sponsor=&sponsor_type=all&state=all&field_of_interest=all&sortfield=relevance&searchmode=basic'

def get_pages_count(url):
	soup = BeautifulSoup(get_html(url),'html.parser')
	pages=soup.find('ul',class_="ngx-pagination").find_all('li')
	if pages:
		return int(pages[-2].find_all('span')[1].get_text())
	else:
		return 1
	

def get_html(url):
	options = webdriver.FirefoxOptions()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	driver.get(URL)
	element = WebDriverWait(driver, 10).until(
      	EC.presence_of_element_located((By.CLASS_NAME, "conference-item"))
      	)
	reqHtml = driver.page_source
	driver.quit()
	return reqHtml

def parse_items_content():
	pass

def parse():
	pages = get_pages_count(URL)
	print(pages)
	# for page in range(1,pages):
		
	# items = soup.find_all('div',class_='conference-item')
	# for item in items :
	# 	print(item.find('div',class_="item-title").get_text())


parse()