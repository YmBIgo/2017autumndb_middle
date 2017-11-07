#!/usr/bin/python
# -*- coding: utf-8 -*-

import splinter
import selenium
import csv
import time

# Get Stock data from finance.yahoo.com/quoto/<COMPANY_NAME>/history?p=<COMPANY_NAME>
# 
# -------------------------------------------------------
# URL
# I chose ORCL(Oracle), AAPL(Apple), ACN(Accenture)
# ORCL 	: https://finance.yahoo.com/quoto/ORCL/history?p=ORCL
# AAPL	: https://finance.yahoo.com/quoto/AAPL/history?p=AAPL
# ACN 	: https://finance.yahoo.com/quoto/ACN/history?p=ACN
# -------------------------------------------------------
# XPATH
# date 	: /html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[{num}]/td[1]/span
# open 	: /html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[{num}]/td[2]/span
# high 	: /html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[{num}]/td[3]/span
# low	: /html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[{num}]/td[4]/span
# close	: /html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[{num}]/td[5]/span
# <num>	: 1-255
# -------------------------------------------------------
# DATA STRUCTURE
# <company>		: oracle
# <date>		: Nov 06, 2017
# <open>		: 50.10
# <high>		: 50.55
# <low>			: 50.02	
# <close>		: 50.40	
# -------------------------------------------------------

oracle_url 		= "https://finance.yahoo.com/quote/ORCL/history?p=ORCL"
apple_url  		= "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
accenture_url	= "https://finance.yahoo.com/quote/ACN/history?p=ACN"

button_xpath	= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/button"

date_xpath 		= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{}]/td[1]/span"
open_xpath 		= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{}]/td[2]/span"
high_xpath		= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{}]/td[3]/span"
low_xpath		= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{}]/td[4]/span"
close_xpath		= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[{}]/td[5]/span"

# search_company	= [oracle_url]
search_company	= {'oracle' : oracle_url, 'apple' : apple_url, 'accenture' : accenture_url}
search_xpath	= {'date':date_xpath, 'open':open_xpath, 'high':high_xpath, 'low':low_xpath, 'close':close_xpath}
search_range 	= range(1, 260)
search_result 	= {'oracle'		:{'date':[], 'open':[], 'high':[], 'low':[], 'close':[]},
				   'apple'		:{'date':[], 'open':[], 'high':[], 'low':[], 'close':[]},
				   'accenture'	:{'date':[], 'open':[], 'high':[], 'low':[], 'close':[]}}

class GetStock:

	# initialize browser
	def __init__(self, ):
		print('\nStarting Scraping...')
		self.browser = splinter.Browser('phantomjs', user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

	# visit url using browser
	def connect(self, url):
		print('\nConnecting {} ...'.format(url))
		self.browser.visit(url)

	def scroll_to_bottom(self):
		self.browser.execute_script("window.scrollTo(0, 10000);")
		print "Scrolling...<window.scrollTo(0, 10000);>"
		time.sleep(6)

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

	def click_xpath(self, xpath):
		result = self.browser.find_by_xpath(xpath).click()
		return result

	def return_xpath_result(self, results):
		xpath_results = ['']
		for r in results:
			xpath_results.insert(0, r)
		return xpath_results

	def get_results_from_xpath(self, xpath, xpath_num1, xpath_num2=''):
		page_xpath 			= self.format_str(xpath, str(xpath_num1), str(xpath_num2))
		page_xpath_results 	= self.select_xpath(page_xpath)
		page_xpath_result 	= self.return_xpath_result(page_xpath_results)
		return page_xpath_result

	def create_csv_file(self, filepath, results):
		try:
			f = open(filepath, 'w')
			writer = csv.writer(f, lineterminator='\n')
			# 
			for comp in results:
				for i  in search_range:
					num = i-1
					print comp, results[comp]['date'][num], results[comp]['open'][num], results[comp]['high'][num], results[comp]['low'][num], results[comp]['close'][num]
					writer.writerows([[comp, results[comp]['date'][num], results[comp]['open'][num], results[comp]['high'][num], results[comp]['low'][num], results[comp]['close'][num]]])
		except (UnicodeDecodeError, UnicodeEncodeError):
			pass
		# close CSV file
		f.close()

	def finish(self):
		self.browser.quit()

def fix_month(date_str):
	month_str = 		['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	month_fixed_str	=	['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
	short_month = date_str[:3]
	fixed_date_str = ''
	if 		short_month == month_str[0]:
		fixed_date_str = month_fixed_str[0] + date_str[3:]
	elif	short_month == month_str[1]:
		fixed_date_str = month_fixed_str[1] + date_str[3:]
	elif	short_month == month_str[2]:
		fixed_date_str = month_fixed_str[2] + date_str[3:]
	elif	short_month == month_str[3]:
		fixed_date_str = month_fixed_str[3] + date_str[3:]
	elif	short_month == month_str[4]:
		fixed_date_str = month_fixed_str[4] + date_str[3:]
	elif	short_month == month_str[5]:
		fixed_date_str = month_fixed_str[5] + date_str[3:]
	elif	short_month == month_str[6]:
		fixed_date_str = month_fixed_str[6] + date_str[3:]
	elif	short_month == month_str[7]:
		fixed_date_str = month_fixed_str[7] + date_str[3:]
	elif	short_month == month_str[8]:
		fixed_date_str = month_fixed_str[8] + date_str[3:]
	elif	short_month == month_str[9]:
		fixed_date_str = month_fixed_str[9] + date_str[3:]
	elif	short_month == month_str[10]:
		fixed_date_str = month_fixed_str[10] + date_str[3:]
	elif	short_month == month_str[11]:
		fixed_date_str = month_fixed_str[11] + date_str[3:]
	else:
		fixed_date_str = 'unknown'
	return fixed_date_str

get_stock = GetStock()

for c_url in search_company:
	get_stock.connect(search_company[c_url])
	get_stock.scroll_to_bottom()
	for c_xpath in search_xpath:
		for xpath_num in search_range:
			if xpath_num == 180 and c_xpath == 'date':
				get_stock.scroll_to_bottom()
			xpath_result = get_stock.get_results_from_xpath(search_xpath[c_xpath], xpath_num)
			xpath_result_content = xpath_result[0]
			if xpath_result[0] == '':
				xpath_result_content == 'Dividend'
			else:
				xpath_result_content = xpath_result[0].text
			if c_xpath == 'date':
				xpath_result_content = fix_month(xpath_result_content)
			print xpath_result_content
			search_result[c_url][c_xpath].append(xpath_result_content)

print search_result

filepath = '/Users/kuriharakazuya/SFC/database/news_database/company_stock_20171107_fixed.csv'
get_stock.create_csv_file(filepath, search_result)

get_stock.finish()





