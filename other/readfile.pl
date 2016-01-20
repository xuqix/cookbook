#!/usr/bin/perl
# 123x1323
#$d = readdir ".";
#print $d;
#exit;
open(file,"point_list") or die "open error";
open(OUT,">qq");
open(str,"ls |");
#while($l=<str>){
#    print $l;
#}
#exit;
while(<file>) {
    if (s/([-]?\d+)\s+([-]?\d+)/\t<key>$1<\/key>\n\t<string>$2<\/string>/){
        print OUT $_;
    }
    else {
        print OUT "\n"
    }
}
