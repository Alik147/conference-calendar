from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from bs4 import BeautifulSoup
import time
q=input("Your query:")
HOST = 'https://conferences.ieee.org/conferences_events'
URL = 'https://conferences.ieee.org/conferences_events/conferences/search?q={}&subsequent_q=&date=all&from=&to=&region=all&country=all&pos={}&sortorder=desc&sponsor=&sponsor_type=all&state=all&field_of_interest=all&sortfield=relevance&searchmode=basic'.format(q,0)
def get_pages_count(url):
	soup = BeautifulSoup(get_html(url,False),'html.parser')
	pages=soup.find('ul',class_="ngx-pagination").find_all('li')
	if pages:
		return int(pages[-2].find_all('span')[1].get_text())
	else:
		return 1
def get_html(url,links_flag):
	options = webdriver.FirefoxOptions()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	driver.get(url)
	try:
		element = WebDriverWait(driver, 10).until(
	      	EC.presence_of_element_located((By.CLASS_NAME, "conference-item"))
	      	)
	finally:
		reqHtml = driver.page_source
		if links_flag:
			links=[]
			closeCookie = driver.find_element_by_class_name("cc-compliance")
			closeCookie.click()
			elements = driver.find_elements_by_class_name("fa-share-square")
			h = 0
			for element in elements:
				h+=165
				driver.execute_script("window.scrollTo(0, {})".format(h))
				element.click()
				nextelements = driver.find_elements_by_class_name("item-social")
				nextelements[4].click()
				newHtml = driver.page_source
				soup = BeautifulSoup(newHtml,'html.parser')
				links.append(soup.find('a',class_="btn-view").get('href'))
				close = driver.find_elements_by_class_name("close")
				close[0].click()
				time.sleep(0.5)
			driver.quit()
			return reqHtml,links
		driver.quit()

		return reqHtml

def parse_items_content(pages):
	conferences=[]
	counter=0
	for page in range(0,pages):
		print("working on {} page from {} pages".format(page+1,pages))
		url='https://conferences.ieee.org/conferences_events/conferences/search?q={}&subsequent_q=&date=all&from=&to=&region=all&country=all&pos={}&sortorder=desc&sponsor=&sponsor_type=all&state=all&field_of_interest=all&sortfield=relevance&searchmode=basic'.format(q,page)
		reqHtml,page_links=get_html(url,True)
		soup = BeautifulSoup(reqHtml,"html.parser")
		items = soup.find_all('div',class_='conference-item')
		for item in items :
			conferences.append({
				'title': item.find('div',class_="item-title").get_text(strip=True),
				'date':	item.find('div',class_="item-date").get_text(strip=True).split("|")[0],
				'location':item.find('div',class_="item-date").get_text(strip=True).split("|")[1],
				'link':HOST+page_links[counter-10*page]
				})
			counter+=1
	print("{} conferences processed".format(counter))
	return conferences

def parse():
	pages = get_pages_count(URL)
	conferences=parse_items_content(pages)
	print(conferences)
parse()