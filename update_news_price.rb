require "pg"

def connect_db()
	# dbname=s14343kk;host=webdb;port=5432", "s14343kk", ENV['SFC_DATABASE_PASS']
	connection = PG::connect(:host 		=> "webdb.sfc.keio.ac.jp",
							 :dbname	=> "s14343kk",
							 :user		=> "s14343kk",
							 :password  => ENV['SFC_DATABASE_PASS'],
							 :port 		=> "5432"
							 )
	begin
		update_news_queries = []
		get_kawase_query = "SELECT c_id, close_price, created_at FROM kawase_histories;"
		exec_query = connection.exec(get_kawase_query)
		exec_query.each do |tupple|
			c_id 		= tupple['c_id']
			price 		= tupple['close_price']
			created_at	= tupple['created_at']
			
			update_news_query = "UPDATE news SET day_price=#{price} WHERE day_price=0 AND c_id=#{c_id} AND created_at=#{created_at};"
			# print update_news_query
			update_news_queries.push(update_news_query)
		end
		puts update_news_queries
	ensure 
		connection.finish
	end
end

connect_db()