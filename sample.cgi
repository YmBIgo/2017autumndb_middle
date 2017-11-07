#!/usr/bin/perl
use CGI;
use DBI;

my $cgi = new CGI;
$cgi->charset('euc-jp');
print $cgi->header,
      $cgi->start_html(-title=>'PostgreSQL on CNS', -lang=>'ja-JP');

$conn = DBI->connect("dbi:Pg:dbname=s14343kk;host=webdb;port=5432", "s14343kk", "hogehoge");
if($conn->errstr != ""){
    $err = $conn->errstr;
}

if (length($cgi->param('keyword')) > 0) {
    $keyword = $conn->quote($cgi->param('keyword'));
    $sql = "SELECT media.mid, inner_product(media.r, media.g, media.b, keyword.r, keyword.g, keyword.b) AS score FROM media, keyword WHERE keyword.word = $keyword ORDER BY score DESC;";
} else {
    $sql = "SELECT media.mid, 0 AS score FROM media;";
}

my $sth = $conn->prepare($sql);
my $ref = $sth->execute;

print $cgi->h2('PostgreSQL on CNS'),
      $cgi->p($cgi->escapeHTML($sql));

while(my $arr_ref = $sth->fetchrow_arrayref){
    my ($id, $score) = @$arr_ref;
    my $url  = $cgi->escapeHTML($id);
    my $text = $cgi->escapeHTML(", $score");
    my $img  = $cgi->img({width=>100, src=>$url});
    print $cgi->a({href=>$url}, $img),
          $cgi->span($text),
          $cgi->br;
}

print $cgi->end_html;

$sth->finish;
$conn->disconnect;

exit;
