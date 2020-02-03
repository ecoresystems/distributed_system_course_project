#!/usr/bin/perl
BEGIN{
    push @INC,'./';
}
use Getopt::Std;
use Tool;
getopts("hd:q:n:m:");
if ($opt_h){
    print <<EOF;
usage: perl search.pl [-h] [-d db] [-q query] [-n n]
  -h : show this message
  -d : database
  -q : query
  -n : number of results, default n=10
EOF
    exit 0
}
my $db = $opt_d ? $opt_d : "sample";
my $q  = $opt_q ? $opt_q : "z";
my $n  = $opt_n ? $opt_n : 5;
my $m  = $opt_m ? $opt_m : 5;
&Tool::init($db);
my ($doc,$word) = &Tool::getdocword($q);
for(my $i=0;($i<$n)&&($i<@$doc);$i++){
    my ($doci,$wordi) = &Tool::getdocword("i:$doc->[$i]{name}");
    printf "%s\n",$doc->[$i]{name};
    for(my $j=0;($j<@$wordi)&&($j<$m);$j++){
	printf "  %2d %7.4f %s\n",$j+1,$wordi->[$j]{weight},$wordi->[$j]{name};
    };
}
