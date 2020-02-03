#!/usr/bin/perl
use lib "../../mecab-perl-0.996/src/.libs";
use lib $ENV{PWD} . "/blib/lib";
use lib $ENV{PWD} . "/blib/arch";
use MeCab;
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

my $uuid = $opt_u ? $opt_u : "None";
my $id = $opt_i ? $opt_i : 1;
my $txt = "";

my $model = new MeCab::Model(join " ", @ARGV);
my $c = $model->createTagger();

my $file = $opt_f ? $opt_f : "20190403.txt";
my $ln = 1;
my %tf;

open(FF,$file) or die "$file not found";
while(my $line = <FF>){
    chomp $line;
    for (my $m = $c->parseToNode($line); $m; $m = $m->{next}) {
        if ($m->{feature} =~ /名詞/){
            $tf{$m->{surface}}++;
        }
    }
    printf "@%s\n",$uuid;
    printf "1 i:%d\n",$ln;
    printf "1 z\n";
    map{printf "%d %s\n",$tf{$_},$_}keys %tf;
    $ln++;
    %tf = ();
}
close(FF);
