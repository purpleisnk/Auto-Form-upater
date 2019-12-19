import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

title  = input('\nEnter the title of the form\n')
thumbnail_link  = input('\nPlease provide a thumnail url\n')
desc  = input('\nEnter a little description\n')
generes  = input('\nAdd a few categories\n')
episode_link  = input('\nEnter the webiste to be  parsed \n')


def links():
	epi = episode_link

	# eppp = 'https://vidstreaming.io'
	eppp = ('anylink prefix')

	response = requests.get(epi)



	soup = BeautifulSoup(response.text, 'html.parser')

	video_container = soup.find('ul', attrs = {'class' : 'listing items lists'})

	vid_links = video_container.find_all('li')

	browseable_links = []

	for links in vid_links:
		## parsed the a tag to get the href value by split and indexing
		cleaned_link = str(links.find('a')).split()[1]
		browseable_links.append(eppp+cleaned_link[6:(len(cleaned_link)-2)])


	urls = browseable_links[::-1]

	link_list = []


	for url in urls:
		res = requests.get(url)	
		bigsoup = BeautifulSoup(res.text, 'html.parser')
		frame = bigsoup.find('iframe')
		src = str(frame).split()[6]
		cleaned_src = src[5:(len(src)-12)]
		link_list.append('https:' + cleaned_src)

	return link_list	

rings = links()
		
def log_update(name,image_url, desc, genres):

	

	path = 'driver/chromedriver'

	driver = webdriver.Chrome(executable_path = path)
	driver.get('login URL')
	
	
	## LOGIN
	user_ = driver.find_element_by_xpath('//*[@id="id_username"]')
	user_.send_keys('username')
	pswd = driver.find_element_by_xpath('//*[@id="id_password"]')
	pswd.send_keys('pswd', Keys.ENTER)
	
	#Open a new window to fill up new form
	driver.find_element_by_xpath('//*[@id="content-main"]/div[2]/table/tbody/tr[1]/td[1]/a').click()

	
	

	##TITLE OR ANYTHING ELSE
	title = driver.find_element_by_id('id_title')
	title.send_keys(name)

	image = driver.find_element_by_xpath('//*[@id="id_thumbnail_url"]')
	image.send_keys(image_url)	


	description = driver.find_element_by_xpath('//*[@id="id_description"]')
	description.send_keys(desc)	

	genre = driver.find_element_by_xpath('//*[@id="id_genre"]')
	genre.send_keys(genres)

	#!! Start looping over what you want to neccesarily update (For pop ups)
	
	main = driver.window_handles[0]
	main
	ep_no = 0

	for update in rings:
		ep_no = ep_no + 1
		try:
			driver.find_element_by_xpath('//*[@id="add_id_episodes"]').click()
			

			a = driver.window_handles[-1]
			driver.switch_to.window(a)

			ep_desc = driver.find_element_by_xpath('//*[@id="id_description"]')
		
			ep_desc.send_keys(f'{name} Epsiode {ep_no}')

			ep_nos = driver.find_element_by_xpath('//*[@id="id_episode_no"]')
			ep_nos.send_keys(f'{ep_no}')


			ep_link = driver.find_element_by_xpath('//*[@id="id_link"]')
			ep_link.send_keys(update)
			
			driver.find_element_by_class_name('default').click()


			
			driver.switch_to.window(main)


		except NoSuchElementException as e:
			print(e)
	try:		
		grand_save = driver.find_element_by_name('_save').click()
		time.sleep(10)

	except error as e:
		print(e)
log_update(title, desc, thumbnail_link, generes)