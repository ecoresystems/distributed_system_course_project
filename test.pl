#!/usr/bin/perl
use lib "../../mecab-perl-0.996/src/.libs";
use lib $ENV{PWD} . "/blib/lib";
use lib $ENV{PWD} . "/blib/arch";
use MeCab;
print $MeCab::VERSION, "\n";
my $sentence = "太郎はこの本を二郎を見た女性に渡した。";
my $model = new MeCab::Model(join " ", @ARGV);
my $c = $model->createTagger();
print $c->parse($sentence);
for (my $m = $c->parseToNode($sentence); $m; $m = $m->{next}) {
    printf("%s\t%s\n", $m->{surface}, $m->{feature});
}
