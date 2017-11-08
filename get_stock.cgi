#!/usr/bin/perl
use CGI;
use DBI;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'Stock and News Data', -lang=>'ja-JP'),
      '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.min.js"></script>';

$conn = DBI->connect("dbi:Pg:dbname=s14343kk;host=webdb;port=5432", "s14343kk", "hogehoge");
if($conn->errstr != ""){
    $err = $conn->errstr;
}

@corp = ('oracle', 'apple', 'accenture');

# $clength = length($cgi->param('company'));
# print $cgi->p($cgi->escapeHTML($clength));

print $cgi->h1("STOCK SEARCH RESULT");
$c_id = $conn->quote($cgi->param('company'));

# $clength = length($cgi->param('company'));
# print $cgi->p($cgi->escapeHTML($clength));

if (length($cgi->param('company')) > 0){
        # Create query only using c_id
        # $c_id = $conn->quote($cgi->param('company'));
        print $cgi->h3($corp[1]);
        $sql = "SELECT * FROM kawase_histories WHERE c_id=$c_id ORDER BY created_at ASC LIMIT 255;";
        if (length($cgi->param('start_date')) > 0){
        # Create query using c_id and date
                $start_date = $conn->quote($cgi->param('start_date'));
                $end_date = $conn->quote($cgi->param('end_date'));
                $sql = "SELECT * FROM kawase_histories WHERE c_id=$c_id  AND created_at BETWEEN $start_date AND $end_date ORDER BY created_at ASC LIMIT 255;";

                if (length($cgi->param('keyword')) > 0){
                # Create query using c_id and date and keyword
                        $keyword = $conn->quote($cgi->param('keyword'));
                        $sql = "SELECT * FROM kawase_histories WHERE c_id=$c_id AND created_at BETWEEN $start_date AND $end_date AND n_title LIKE ? ORDER BY created_at ASC LIMIT 255;";
                        # $sth->execute( $my_name . '%' );
                }

        }elsif (length($cgi->param('keyword')) > 0){
        # Create query using c_id and keyword
                $keyword = $conn->quote($cgi->param('keyword'));
                $sql = "SELECT * FROM kawase_histories WHERE c_id=$c_id AND n_title LIKE ? ORDER BY created_at ASC LIMIT 255;";
        }
}else{
        $sql = "SELECT * FROM kawase_histories WHERE id BETWEEN 1 AND 30 ORDER BY created_at ASC;";
}

if (length($cgi->param('company')) > 0){
        # Create query only using c_id
        # $c_id = $conn->quote($cgi->param('company'));
        $news_sql = "SELECT * FROM news WHERE c_id=$c_id LIMIT 10;";

        if (length($cgi->param('start_date')) > 0){
        # Create query using c_id and date
                # $start_date = $conn->quote($cgi->param('start_date'));
                # $end_date = $conn->quote($cgi->param('end_date'));
                $news_sql = "SELECT * FROM news WHERE c_id=$c_id  AND created_at BETWEEN $start_date AND $end_date LIMIT 10;";

                if (length($cgi->param('keyword')) > 0){
                # Create query using c_id and date and keyword
                        # $keyword = $conn->quote($cgi->param('keyword'));
                        $news_sql = "SELECT * FROM news WHERE c_id=$c_id AND created_at BETWEEN $start_date AND $end_date AND n_title LIKE ? LIMIT 10";
                }

        }elsif (length($cgi->param('keyword')) > 0){
        # Create query using c_id and keyword
                # $keyword = $conn->quote($cgi->param('keyword'));
                $news_sql = "SELECT * FROM news WHERE c_id=$c_id AND n_title LIKE ? LIMIT 10";
        }
}else{
        $news_sql = "SELECT * FROM news WHERE id BETWEEN 1 AND 10";
}

print $cgi->p($cgi->escapeHTML($news_sql));

# print $cgi->h1("STOCK SEARCH RESULT");
# print $cgi->hr;
print $cgi->p($cgi->escapeHTML($sql));

my $sth = $conn->prepare($sql);
my @open_prices     = ();
my @high_prices     = ();
my @low_prices      = ();
my @close_prices    = ();
my @created_dates   = ();
$open_price_str     = "";
$high_price_str     = "";
$low_price_str      = "";
$close_price_str    = "";
$created_date_str   = "";

#  add query if $keyword is existed. 
if (length($keyword) > 0){
        $sth->execute( $keyword . '%' );
}else{
        $sth->execute;
}

# print $corp[$c_id-1];

while(my $arr_ref = $sth->fetchrow_arrayref){
    my ($id, $c_id, $open_price, $high_price, $low_price, $close_price, $created_at) = @$arr_ref;
    # my $company   = $corp[$c_id-1];
    # my $title   = $cgi->escapeHTML($n_title);
    push(@open_prices, $open_price);
    push(@high_prices, $high_price);
    push(@low_prices, $low_price);
    push(@close_prices, $close_price);
    push(@created_dates, $created_at);
}

foreach my $o (@open_prices){
    $open_price_str = $open_price_str.$o.", ";
}
foreach my $h (@high_prices){
    $high_price_str = $high_price_str.$h.", ";
}
foreach my $l (@low_prices){
    $low_price_str = $low_price_str.$l.", ";
}
foreach my $c (@close_prices){
    $close_price_str = $close_price_str.$c.", ";
}
foreach my $cr (@created_dates){
    $created_date_str = $created_date_str."'".$cr."', ";
}

substr($open_price_str, -2, 2)  = "";
substr($high_price_str, -2, 2)  = "";
substr($low_price_str, -2, 2)   = "";
substr($close_price_str, -2, 2) = "";
substr($created_date_str, -2, 2) = "";

# print $open_price_str;

print "<canvas id='myChart'></canvas><script>var ctx = document.getElementById('myChart').getContext('2d');var myChart = new Chart(ctx, {type: 'line',data: {labels: [$created_date_str],";
print "datasets: [{label: 'high_price',data: [$high_price_str],backgroundColor: 'rgba(153,255,30,0.4)'},";
print "{label: 'open price',data: [$open_price_str] ,backgroundColor: 'rgba(153,255,102,0.4)'},";
print "{label: 'close price',data: [$close_price_str], backgroundColor: 'rgba(153,255,184,0.4)'},";
print "{label: 'low price',data: [$low_price_str], backgroundColor: 'rgba(153,255,255.4)'}] }});</script>";


my $sth_news = $conn->prepare($news_sql);
$sth_news->execute;

while(my $arr_news_ref = $sth_news->fetchrow_arrayref){
    my ($id, $c_id, $n_url, $n_title, $day_price, $created_at) = @$arr_news_ref;
    my $link    = $cgi->escapeHTML($n_url);
    my $title   = $cgi->escapeHTML($n_title);
    print $cgi->a({href=>$link}, $title),
          $cgi->span({style=>"font-size:75%;"}, " ($corp[$c_id-1], $c_id, $created_at)"),
          $cgi->br;
}

print   '<hr>';

print   '<h1>Search News</h1><form action="get_news.cgi" method="POST"><p>KEYWORD   : <input type="text" name="keyword" size="20"></p><p>COMPANY   : <select name="company"><option value="1" selected>oracle</option><option value="2">apple</option><option value="3">accenture</option></select></p><p>STARTDATE : <input type="text" name="start_date"></p><p>ENDDATE   : <input type="text" name="end_date"></p><p><input type="submit"></p></form><hr><h1>Search Stock Again</h1><form action="get_stock.cgi" method="POST"><p>COMPANY : <select name="company"><option value="1" selected>oracle</option><option value="2">apple</option><option value="3">accenture</option></select></p><p>STARTDATE : <input type="text" name="start_date"></p><p>ENDDATE : <input type="text" name="end_date"></p><p><input type="submit"></p></form>';


print $cgi->end_html;

$conn->disconnect;
exit;
