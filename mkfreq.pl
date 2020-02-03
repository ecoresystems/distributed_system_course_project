#!/usr/bin/perl

use Getopt::Std;

getopts("hf:u:i:");

if ($opt_h){
    print <<EOF;
usage: perl search.pl [-h] [-d db] [-q query] [-n n]
  -h : show this message
  -d : database
  -q : query
  -u : uuid
  -i : id
  -n : number of results, default n=10
EOF
    exit 0
}

my $file = $opt_f ? $opt_f : "blogs_0000001.json";
my $uuid = $opt_u ? $opt_u : "None";
my $id = $opt_i ? $opt_i : 1;
my $txt = "";
open(FF,$file) or die "$file not found";
while(my $line = <FF>){
    chomp $line;
    $line =~ s/[^a-z]+/ /ig;
    if ($line eq ""){
	my %tf;
	map{$tf{$_}++}split(/[\s]+/,$txt);
	printf "@%s\n",$uuid;
	print "1 z\n";
	printf "1 i:%d\n",$id;
	map {printf "%d %s\n",$tf{$_},$_}keys %tf;
	$id++;
	$txt = "";
    } else {
	$line = lc($line);
	$txt .= $line." ";
    }
}
close(FF);
