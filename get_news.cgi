#!/usr/bin/perl
use CGI;
use DBI;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'Stock and News Data', -lang=>'ja-JP');

$conn = DBI->connect("dbi:Pg:dbname=s14343kk;host=webdb;port=5432", "s14343kk", "hogehoge");
if($conn->errstr != ""){
    $err = $conn->errstr;
}

@corp = ('', 'oracle', 'apple', 'accenture');

# $clength = length($cgi->param('company'));
# print $cgi->p($cgi->escapeHTML($clength));

if (length($cgi->param('company')) > 0){
        # Create query only using c_id
        $c_id = $conn->quote($cgi->param('company'));
        $sql = "SELECT * FROM news WHERE c_id=$c_id LIMIT 10;";

        if (length($cgi->param('start_date')) > 0){
        # Create query using c_id and date
                $start_date = $conn->quote($cgi->param('start_date'));
                $end_date = $conn->quote($cgi->param('end_date'));
                $sql = "SELECT * FROM news WHERE c_id=$c_id  AND created_at BETWEEN $start_date AND $end_date LIMIT 10;";

                if (length($cgi->param('keyword')) > 0){
                # Create query using c_id and date and keyword
                        $keyword = $conn->quote($cgi->param('keyword'));
                        $sql = "SELECT * FROM news WHERE c_id=$c_id AND created_at BETWEEN $start_date AND $end_date AND n_title LIKE ? LIMIT 10;";
                        # $sth->execute( $my_name . '%' );
                }

        }elsif (length($cgi->param('keyword')) > 0){
        # Create query using c_id and keyword
                $keyword = $conn->quote($cgi->param('keyword'));
                $sql = "SELECT * FROM news WHERE c_id=$c_id AND n_title LIKE ? LIMIT 10;";
        }
}else{
        $sql = "SELECT * FROM news WHERE id BETWEEN 1 AND 10";
}

print $cgi->h1("NEWS SEARCH RESULT");
# print $cgi->hr;
print $cgi->p($cgi->escapeHTML($sql));

my $sth = $conn->prepare($sql);

#  add query if $keyword is existed. 
if (length($keyword) > 0){
        $sth->execute( $keyword . '%' );
}else{
        $sth->execute;
}

while(my $arr_ref = $sth->fetchrow_arrayref){
    my ($id, $c_id, $n_url, $n_title, $day_price, $created_at) = @$arr_ref;
    my $link    = $cgi->escapeHTML($n_url);
    my $title   = $cgi->escapeHTML($n_title);
    print $cgi->a({href=>$link}, $title),
          $cgi->span({style=>"font-size:75%;"}, " ($corp[$c_id-1], $c_id, $created_at)"),
          $cgi->br;
}

print   '<hr>';

print   '<h1>Search AGAIN News</h1><form action="get_news.cgi" method="POST"><p>KEYWORD   : <input type="text" name="keyword" size="20"></p><p>COMPANY   : <select name="company"><option value="1" selected>oracle</option><option value="2">apple</option><option value="3">accenture</option></select></p><p>STARTDATE : <input type="text" name="start_date"></p><p>ENDDATE   : <input type="text" name="end_date"></p><p><input type="submit"></p></form><hr><h1>Search Stock</h1><form action="get_stock.cgi" method="POST"><p>COMPANY : <select name="company"><option value="1" selected>oracle</option><option value="2">apple</option><option value="3">accenture</option></select></p><p>STARTDATE : <input type="text" name="start_date"></p><p>ENDDATE : <input type="text" name="end_date"></p><p><input type="submit"></p></form>';

print $cgi->end_html;

$conn->disconnect;
exit;
