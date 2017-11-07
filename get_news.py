#!/usr/bin/python
# -*- coding: utf-8 -*-

import splinter
import selenium
import csv

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Using Fox News to get data
# -> but oracle has only 6 articles this year... so i just copy and paste the code.

# 
# # go to foxnews webpage and search news
# 
# apple_news_url 	= "http://www.foxnews.com/search-results/search?q=apple&ss=fn&sort=latest&section.path=fnc/archive,fnc/tech,fnc/science,fnc/world,fnc/transcript&min_date=2016-11-06&max_date=2017-11-06&start=0"
# http://www.foxnews.com/search-results/search?q=apple&ss=fn&sort=latest&start=100
# http://www.foxnews.com/search-results/search?q=apple&ss=fn&sort=latest&start=320
# 
# google_news_url = "http://www.foxnews.com/search-results/search?q=google&ss=fn&sort=latest&section.path=fnc/archive,fnc/tech,fnc/science,fnc/world,fnc/transcript&min_date=2016-11-06&max_date=2017-11-06&start=0"
# 
# oracle_news_url = "http://www.foxnews.com/search-results/search?q=oracle&ss=fn&sort=latest&section.path=fnc/archive,fnc/tech,fnc/science,fnc/world,fnc/transcript&min_date=2016-11-06&max_date=2017-11-06&start=0"
# 
# try:
# 	page_start_num = range(0, 310, 10)
# 	browser.visit(apple_news_url)
# 
# 	search_child_selector_num = range(4, 13)
# 	for child_num in search_child_selector_num:
# 		# CSS SELECTOR
# 		# div.search-directive:nth-child(4) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a
# 		# div.search-directive:nth-child(5) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)
# 		# ...
# 		# div.search-directive:nth-child(13) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)
# 		search_child_selector = "div.search-directive:nth-child({}) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1) > a:nth-child(1)".format(str(child_num))
# 		search_child_result = browser.find_by_css(search_child_selector)
# 		search_result.append(search_child_result['href'])
# 
# 	print search_result
# 
# except (splinter.exceptions.ElementDoesNotExist, splinter.exceptions.DriverNotFoundError, selenium.common.exceptions.InvalidElementStateException):
# 	browser.quit()
# 	print('Oops! Something wrong occurs.')
# 	pass
# 
# else:
# 	browser.quit()
# 	print('Finished')

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# So using each conpany's press release page to get some information

# <> Apple newsroom <>

# url
apple_press_release_url = "https://www.apple.com/newsroom/archive/?page={}"
# href
apple_press_release_href_xpath = "/html/body/main/section/div[2]/div/div[{}]/a[{}]"
# title
apple_press_release_title_xpath = "/html/body/main/section/div[2]/div/div[{}]/a[{}]/div[3]/h3"
# date
apple_press_release_date_xpath = "/html/body/main/section/div[2]/div/div[{}]/a[{}]/div[1]/span[1]"


# -------------------------------------------------------------------
# URL
# https://www.apple.com/newsroom/archive/
# https://www.apple.com/newsroom/archive/?page=3
# ...
# https://www.apple.com/newsroom/archive/?page=5
# -------------------------------------------------------------------
# X PATH
# /html/body/main/section/div[2]/div/div[1]/a[1]
# /html/body/main/section/div[2]/div/div[1]/a[2]
# /html/body/main/section/div[2]/div/div[2]/a[1]
# ...
# /html/body/main/section/div[2]/div/div[4]/a[3]
# -------------------------------------------------------------------
# DATA STRUCTURE
# <url>				https://www.apple.com/newsroom/2017/09/macos-high-sierra-now-available-as-a-free-update/
# <title>			macOS High Sierra now available as a free update
# <created_date>	September 25, 2017
# -------------------------------------------------------------------


# <> Oracle Press Release <>

# url
oracle_press_release_url = "https://www.oracle.com/search/press?No={}&Nr=101&Nrpp=10"
# href
oracle_press_release_href_xpath = "/html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[{}]/div/div/h4/a"
# title
# -> Can get text from href :)
# date
oracle_press_release_date_xpath = "/html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[{}]/div/div/div/div/div[1]"

# -------------------------------------------------------------------
# URL
# https://www.oracle.com/search/press?No=10&Nr=101&Nrpp=10
# https://www.oracle.com/search/press?No=20&Nr=101&Nrpp=10
# ...
#  https://www.oracle.com/search/press?No=240&Nr=101&Nrpp=10
# -------------------------------------------------------------------
# X PATH
# /html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[1]/div/div/h4/a
# /html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/h4/a
# ...
# /html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[10]/div/div/h4/a
# -------------------------------------------------------------------
# DATA STRUCTURE
# <url>				https://www.oracle.com/corporate/pressrelease/nraef-oracle-hospitality-110217.html
# <title>			National Restaurant Association Educational Foundation and Oracle Hospitality Empower Students to Get Creative about Future of Hospitality
# <created_date>	Nov 2, 2017
# -------------------------------------------------------------------


# <> Google blog <>
# -> Cause www.blog.google has too much news so I chose accenture instead... 

# google_press_release_url = "https://www.blog.google/"
# -------------------------------------------------------------------
# URL
# https://www.blog.google/
# -------------------------------------------------------------------
# X PATH
# /html/body/main/article/section[2]/div/nav/a[1]
# ...
# /html/body/main/article/section[2]/div/nav/a[35]
# ... (until finding LAST YEAR )
# -------------------------------------------------------------------
# Button
# /html/body/main/article/section[2]/div/button
# -------------------------------------------------------------------
# DATA STRUCTURE
# <title>			Feed your need to know
# <created_date>	Jul 19, 2017
# -------------------------------------------------------------------


# <> Accenture newsroom <>

# url
accenture_press_release_url = "https://newsroom.accenture.com/?page={}"
# href
accenture_press_release_href_xpath = "/html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[{}]/div/h4/a"
# title
# -> Can get text from href :)
# date
accenture_press_release_date_xpath = "/html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[{}]/div/div[1]"


# -------------------------------------------------------------------
# URL
# https://newsroom.accenture.com/
# https://newsroom.accenture.com/?page=2
# ...
# https://newsroom.accenture.com/?page=42
# -------------------------------------------------------------------
# X PATH
# /html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[1]/div/h4/a
# /html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[2]/div/h4/a
# ...
# /html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[10]/div/h4/a
# -------------------------------------------------------------------
# DATA STRUCTURE
# <url>				https://newsroom.accenture.com/news/accenture-and-specular-theory-create-interactive-vcommerce-experience-behind-the-style.htm#search
# <title>			Accenture and Specular Theory Create Interactive Vcommerce Experience “Behind The Style”
# <created_date>	October 16, 2017
# -------------------------------------------------------------------


search_data = {}

# URL range
# apple : 5, oracle : 250, accnture : 43
apple_url_range 		= range(1, 5)
oracle_url_range 		= range(10, 250, 10)
accenture_url_range		= range(1, 43)

# XPATH range
# apple : 1-6, 1-13, oracle : 1-10, accenture : 1-10
apple_xpath_range 		= [range(1, 7), range(1, 14)]
oracle_xpath_range		= range(1, 11)
accenture_xpath_range 	= range(1, 11)


search_data["apple"] 		= {"URL"		: [apple_press_release_url, apple_url_range],
							   "HREF_XPATH"	: [apple_press_release_href_xpath, apple_xpath_range],
							   "TITLE_XPATH": [apple_press_release_title_xpath, apple_xpath_range],
							   "DATE_XPATH" : [apple_press_release_date_xpath, apple_xpath_range]}
search_data["oracle"]		= {"URL"		: [oracle_press_release_url, oracle_url_range],
							   "HREF_XPATH"	: [oracle_press_release_href_xpath, oracle_xpath_range],
							   "DATE_XPATH" : [oracle_press_release_date_xpath, oracle_xpath_range]}
search_data["accenture"]	= {"URL"		: [accenture_press_release_url, accenture_url_range],
							   "HREF_XPATH"	: [accenture_press_release_href_xpath, accenture_xpath_range],
							   "DATE_XPATH" : [accenture_press_release_date_xpath, accenture_xpath_range]}


class GetNews:

	# initialize browser
	def __init__(self, ):
		print('\nStarting Scraping...')
		self.browser = splinter.Browser('phantomjs', user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

	# visit url using browser
	def connect(self, url):
		print('\nConnecting {} ...'.format(url))
		self.browser.visit(url)

	def format_str(self, str, append_str, optional_str=''):
		return str.format(append_str, optional_str)

	def select_xpath(self, xpath):
		print("Searching xpath @{}, {}".format(self.browser.url, xpath))
		try:
			select_xpath_result = self.browser.find_by_xpath(xpath)
			return select_xpath_result
		except (splinter.exceptions.ElementDoesNotExist, splinter.exceptions.DriverNotFoundError, selenium.common.exceptions.InvalidElementStateException):
			err_meaage = "Oops! Something wrong occurs.\n@{}, {}".format(self.browser.url, xpath)
			print(err_meaage)
			return [{'href':''}]

	def return_xpath_result(self, results):
		xpath_results = ['']
		for r in results:
			xpath_results.insert(0, r)
		return xpath_results

	def get_results_from_xpath(self, xpath, xpath_num1, xpath_num2=''):
		href_xpath 			= self.format_str(xpath, str(xpath_num1), str(xpath_num2))
		href_xpath_results 	= self.select_xpath(href_xpath)
		href_xpath_result 	= self.return_xpath_result(href_xpath_results)
		return href_xpath_result

	def create_csv_file(self, filepath, results):
		try:
			f = open(filepath, 'w')
			writer = csv.writer(f, lineterminator='\n')
			# 
			for comp in results:
				for result in results[comp]:
					writer.writerows([[comp, result[0], result[1], result[2]]])
		except (UnicodeDecodeError, UnicodeEncodeError):
			pass
		# close CSV file
		f.close()

	def finish(self):
		self.browser.quit()

search_result = {'apple':[], 'oracle':[], 'accenture':[]}

get_news = GetNews()

# -------------------------------------------------------------------
# < USAGE EXAMPLE >
# get_news.connect("https://newsroom.accenture.com/")
# xpaths = get_news.select_xpath('/html/body/div[2]/div[6]/div[1]/div[2]/section/div[1]/div[2]/div/div/div[1]/div/h4/a')
# print get_news.return_xpath_result(xpaths)
# -------------------------------------------------------------------

for company in search_data:
	url_data 				= search_data[company]["URL"]
	xpath_href_data 		= search_data[company]["HREF_XPATH"]
	xpath_date_data			= search_data[company]["DATE_XPATH"]
	for url_num in url_data[1]:
		company_url = get_news.format_str(url_data[0], str(url_num))
		get_news.connect(company_url)
		if company == "oracle" or company == "accenture":
			for xpath_num in xpath_href_data[1]:
				href_xpath_result  = get_news.get_results_from_xpath(xpath_href_data[0], str(xpath_num))[0]
				if href_xpath_result == '':
					break
				href_xpath_result = href_xpath_result['href']
				title_xpath_result = get_news.get_results_from_xpath(xpath_href_data[0], str(xpath_num))[0].text
				date_xpath_result  = get_news.get_results_from_xpath(xpath_date_data[0], str(xpath_num))[0].text
				xpath_content_results = [href_xpath_result.encode('utf-8'), title_xpath_result.encode('utf-8'), date_xpath_result.encode('utf-8')]
				print href_xpath_result
				search_result[company].append(xpath_content_results)

		elif company == "apple":
			xpath_title_data		= search_data[company]["TITLE_XPATH"]
			for xpath_num1 in xpath_href_data[1][0]:
				for xpath_num2 in xpath_href_data[1][1]:
					href_xpath_result  = get_news.get_results_from_xpath(xpath_href_data[0], str(xpath_num1), str(xpath_num2))[0]
					if href_xpath_result == '':
						break
					href_xpath_result = href_xpath_result['href']
					title_xpath_result = get_news.get_results_from_xpath(xpath_title_data[0], str(xpath_num1), str(xpath_num2))[0]
					print title_xpath_result
					if title_xpath_result == '':
						break
					title_xpath_result = title_xpath_result.text
					date_xpath_result  = get_news.get_results_from_xpath(xpath_date_data[0], str(xpath_num1), str(xpath_num2))[0].text
					xpath_content_results = [href_xpath_result.encode('utf-8'), title_xpath_result.encode('utf-8'), date_xpath_result.encode('utf-8')]
					print xpath_content_results
					search_result[company].append(xpath_content_results)

print search_result

get_news.create_csv_file('company_news.csv', search_result)

get_news.finish()

