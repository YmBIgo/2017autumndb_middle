#!usr/bin/perl
use CGI;
use DBI;

# -------------------------------------------------
# $cgi->param('')
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
	  $cgi->start_html(-title=>'Stock & News Database', -lang=>'ja-JP');

$conn = DBI->connect("dbi:Pg:dbname=s14343kk;host=webdb;port=5432", "s14343kk", "hogehoge");
if($conn->errstr != ""){
	$err = $conn->$errstr;
}
if (length($cgi->param('keyword')) > 0){
	$keyword = $conn->quote($cgi->param('keyword'));
	$sql = "";
	# "SELECT * FROM hoge WHERE fuga=$keyword"
}else{
	$sql = "";
}

my $sth = $conn->prepare($sql);
my $ref = $sth->execute;

print $cgi->h2('Result');

while(my $arr_ref = $sth_fetchrow_arrayref){
	my ($?, $? $?) 	= @$arr_ref;
	my $url 		= $cgi->escapeHTML($id);
	my $text		= $cgi->escapeHTML(", $score");
	my $img			= $cgi->img({width=>100, src=>$url});
	print $cgi->a({href=>$url}, $img),
		  $cgi->span($text),
		  $cgi->br;
}

print $cgi->end_html

$sth->finish;
$conn->disconnect;

exit;

