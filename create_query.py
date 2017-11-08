import csv


# <CREATE TABLE QUERIES> 
# -------------------------------------------
# DROP TABLE IF EXISTS kawase_histories;
# DROP TABLE IF EXISTS companies;
# DROP TABLE IF EXISTS news;
# DROP TABLE IF EXISTS news_tabs;

# CREATE TABLE kawase_histories (
#         id SERIAL,
#         c_id integer,
#         open_price      integer default 0,
#         high_price      integer default 0,
#         low_price       integer default 0,
#         close_price     integer default 0,
#         created_at date default CURRENT_DATE
# );

# CREATE TABLE companies (
# 	id SERIAL,
# 	c_name varchar(64) default '',
# 	k_id varchar(32),
# 	capital integer default 10,
# 	operation_profit integer default 10,
# 	location varchar(256) default '',
# 	c_url varchar(512) default '',
# 	c_image varchar(512) default 'http://haginoryokkou.com/wp-content/uploads/2016/09/noimage.png',
# 	last_day_price integer default 0,
# 	created_at date default CURRENT_DATE,
# 	updated_at date default CURRENT_DATE
# );

# CREATE TABLE news (
# 	id SERIAL,
# 	c_id integer,
# 	n_image varchar(512),
# 	n_url varchar(512),
# 	day_price real default 0,
# 	created_at date default CURRENT_DATE
# );
# -------------------------------------------


# <QUERIES>
# -------------------------------------------
# Companies
# 
# [Oracle]
# INSERT INTO companies(cname, k_id, capital, operation_profit, location, c_url, c_image, last_price )
# VALUES('oracle', 'ORCL', 44648, 14684, 'California Redwood Shores', 'www.oracle.com', 'http://startupobserver.com/wp-content/uploads/2017/08/Oracle.jpg', 50.40);
# 
# [Apple]
# INSERT INTO companies(cname, k_id, capital, operation_profit, location, c_url, c_image, last_price)
# VALUES('apple', 'APPL', 128249, 60024, 'California Cupertino', 'www.apple.com', 'https://www.apple.com/ac/structured-data/images/open_graph_logo.png?201703170823', 174.25);
# 
# [Accenture]
# INSERT INTO companies(cname, k_id, capital, operation_profit, location, c_url, c_image, last_price)
# VALUES('accenture', 'ACN', .016, 4300, 'California Cupertino', 'www.accenture.com', 'https://www.accenture.com//www.accenture.com/t20170623T051930Z__w__/jp-ja/_acnmedia/Accenture/Conversion-Assets/Careers/Images/Global_50/Accenture-Job-Share-Thumbnail.jpg', 143.93);
# 
# --> I HARDCORD THESE CODE
# -------------------------------------------
# Kawase_histories
# 
# INSERT INTO kawase_histories(c_id, open_price, high_price, low_price, close_price, created_at)
# VALUES(1, 50.10, 50.55 ,50.02 ,50.40, "NOVEMBER 6 2017");
# 
# VALUES({}, {}, {} ,{} ,{}, {});
# -------------------------------------------
# news
# 
# INSERT INTO news(c_id, n_url, n_title, day_price, created_at)
# VALUES(1, 'https://www.oracle.com/corporate/pressrelease/oracle-leader-sales-force-automation-102517.html','Oracle Recognized as a Leader in Sales Force Automation Solutions by Gartner', 49.70, 'October 25, 2017');
# VALUES({}, {}, {}, {}, '{}')
# 
# 
# 
# 

kawase_query 	= "INSERT INTO kawase_histories(c_id, open_price, high_price, low_price, close_price, created_at) VALUES({}, {}, {} ,{} ,{}, '{}');"
news_query		= "INSERT INTO news(c_id, n_url, n_title, created_at) VALUES({}, '{}', '{}', '{}');"
stock_queries   = ""
news_queries	= ""

stock_data		= open("/Users/kuriharakazuya/SFC/database/news_database/company_stock_20171107_fixed.csv")
news_data 		= open("/Users/kuriharakazuya/SFC/database/news_database/company_news_20171107.csv")
stock_reader 	= csv.reader(stock_data)
news_reader		= csv.reader(news_data)

for row in stock_reader:
	# print row[0], row[1], row[2], row[3], row[4], row[5]
	c_id = 0
	if row[0] == 'oracle':
		c_id = 1
	elif row[0] == 'apple':
		c_id = 2
	elif row[0] == 'accenture':
		c_id = 3
	query = kawase_query.format(c_id, row[2], row[3], row[4], row[5], row[1])
	stock_queries += query + "\n"

stock_data.close()

# for row in news_reader:
# 	print row[0], row[1], row[2], row[3]
# 	c_id = 0
# 	if row[0] == 'oracle':
# 		c_id = 1
# 	elif row[0] == 'apple':
# 		c_id = 2
# 	elif row[0] == 'accenture':
# 		c_id = 3
# 	query = news_query.format(c_id, row[1], row[2], row[3])
# 	news_queries += query + "\n"

# news_data.close()

print news_queries
print stock_queries

sql_txt = open("create_queries_result_fixed.sql", 'w')
# sql_txt.write(news_queries)
sql_txt.write(stock_queries)
sql_txt.close()


